#!/usr/bin/env python3
"""Turn an HTML page that uses the GAYA design system into ONE self-contained file.

Why: published pages, email previews and most hosts can't follow relative links to
styles.css, the logo SVGs or local images, and many block unpkg.com. This script:

  * replaces <link rel="stylesheet" href=".../styles.css"> (or any local .css) with an
    inline <style> holding the flattened CSS (@imports resolved, url()s inlined)
  * replaces a literal <!-- gaya:styles --> comment with the same flattened CSS
  * inlines local <img src>, <image-slot src>, <source srcset> and CSS url() files as data: URIs
  * inlines local <script src> files (including text/babel)
  * resolves src="gaya:logo/<file>.svg" (or any gaya:<path> under assets/) to the skill's files,
    so a page written anywhere can use the official logos
  * rewrites unpkg.com script URLs to cdn.jsdelivr.net/npm (same package@version/path)
    and drops their integrity attributes

Usage:
  python3 make_standalone.py page.html out.html
  python3 make_standalone.py --css-only out.css      # just the flattened design-system CSS

Paths are resolved relative to the input file. Remote URLs (http/https/data) are left alone.
"""
import base64, mimetypes, re, sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
mimetypes.add_type("image/avif", ".avif")
mimetypes.add_type("image/webp", ".webp")
mimetypes.add_type("image/svg+xml", ".svg")
mimetypes.add_type("font/woff2", ".woff2")

def is_remote(u):
    return u.startswith(("http://", "https://", "data:", "//", "#", "mailto:"))

def data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()

def flatten_css(path: Path, seen=None) -> str:
    seen = seen or set()
    path = path.resolve()
    if path in seen or not path.exists():
        return ""
    seen.add(path)
    css = path.read_text(encoding="utf-8")

    def imp(m):
        target = m.group(2)
        if is_remote(target):
            return m.group(0)
        return flatten_css(path.parent / target, seen)
    css = re.sub(r"""@import\s+(url\()?["']?([^"')]+)["']?\)?\s*;""", imp, css)

    def url(m):
        target = m.group(2)
        if is_remote(target):
            return m.group(0)
        p = (path.parent / target).resolve()
        return f'url("{data_uri(p)}")' if p.exists() else m.group(0)
    css = re.sub(r"""url\((["']?)([^"')]+)\1\)""", url, css)
    return css

def patch_bundle(js: str) -> str:
    """The component bundle resolves logo files relative to its own <script src>. Once it
    is inlined that lookup fails, so swap the two resolver functions for data-URI lookups."""
    logos = {f.name: data_uri(f) for f in (SKILL_ROOT / "assets/logo").glob("*.svg")}
    import json
    prelude = "var __GAYA_LOGOS=" + json.dumps(logos) + ";\n"
    js = js.replace('return s ? new URL("assets/logo/", s.src).href : "assets/logo/";',
                    'return "__GAYA_LOGO__/";')
    js = js.replace('src: logoBase() + file,', 'src: __GAYA_LOGOS[file] || (logoBase() + file),')
    js = js.replace('return s ? new URL("assets/logo/gaya-isotype-color.svg", s.src).href : "assets/logo/gaya-isotype-color.svg";',
                    'return __GAYA_LOGOS["gaya-isotype-color.svg"];')
    return prelude + js

def rewrite_unpkg(tag: str) -> str:
    tag = re.sub(r"https://unpkg\.com/", "https://cdn.jsdelivr.net/npm/", tag)
    tag = re.sub(r'\s+integrity="[^"]*"', "", tag)
    return tag

def build(src: Path) -> str:
    html = src.read_text(encoding="utf-8")
    base = src.parent
    ds_css = None

    def link(m):
        nonlocal ds_css
        href = m.group(1)
        if is_remote(href):
            return m.group(0)
        p = (base / href).resolve()
        if not p.exists():
            print(f"  ! missing stylesheet {href}", file=sys.stderr)
            return m.group(0)
        return "<style>\n" + flatten_css(p) + "\n</style>"
    html = re.sub(r'<link[^>]*rel="stylesheet"[^>]*href="([^"]+)"[^>]*/?>', link, html)
    html = re.sub(r'<link[^>]*href="([^"]+\.css)"[^>]*rel="stylesheet"[^>]*/?>', link, html)

    if "<!-- gaya:styles -->" in html:
        ds_css = flatten_css(SKILL_ROOT / "styles.css")
        html = html.replace("<!-- gaya:styles -->", "<style>\n" + ds_css + "\n</style>")

    def script(m):
        attrs, src_ = m.group(1), m.group(2)
        if src_.startswith("https://unpkg.com/"):
            return rewrite_unpkg(m.group(0))
        if is_remote(src_):
            return m.group(0)
        p = (base / src_).resolve()
        if not p.exists():
            print(f"  ! missing script {src_}", file=sys.stderr)
            return m.group(0)
        attrs = re.sub(r'\s*src="[^"]*"', "", attrs)
        body = p.read_text(encoding="utf-8")
        if p.name == "_ds_bundle.js":
            body = patch_bundle(body)
        body = body.replace("</script", "<\\/script")
        return f"<script{attrs}>\n{body}\n</script>"
    html = re.sub(r'<script([^>]*?\bsrc="([^"]+)"[^>]*)>\s*</script>', script, html)

    def asset(m):
        attr, target = m.group(1), m.group(2)
        if target.startswith("gaya:"):          # gaya:logo/x.svg -> skill assets/logo/x.svg
            p = SKILL_ROOT / "assets" / target[5:]
            if p.exists():
                return f'{attr}="{data_uri(p)}"'
            print(f"  ! unknown gaya asset {target}", file=sys.stderr)
            return m.group(0)
        if is_remote(target):
            return m.group(0)
        p = (base / target).resolve()
        if not p.exists():
            print(f"  ! missing asset {target}", file=sys.stderr)
            return m.group(0)
        return f'{attr}="{data_uri(p)}"'
    html = re.sub(r'\b(src|srcset|poster)="([^"]+)"', asset, html)

    def inline_url(m):
        target = m.group(2)
        if is_remote(target):
            return m.group(0)
        p = (base / target).resolve()
        return f'url("{data_uri(p)}")' if p.exists() else m.group(0)
    html = re.sub(r"""url\((["']?)([^"')]+\.(?:png|jpe?g|svg|webp|avif|gif|woff2?))\1\)""", inline_url, html)
    return html

def main():
    args = sys.argv[1:]
    if len(args) == 2 and args[0] == "--css-only":
        Path(args[1]).write_text(flatten_css(SKILL_ROOT / "styles.css"), encoding="utf-8")
        print(f"wrote {args[1]}")
        return
    if len(args) != 2:
        print(__doc__)
        sys.exit(1)
    src, out = Path(args[0]), Path(args[1])
    result = build(src)
    out.write_text(result, encoding="utf-8")
    kb = len(result.encode()) / 1024
    print(f"wrote {out} ({kb:,.0f} KB)")
    left = re.findall(r'(?:src|href)="(?!https?:|data:|#|mailto:)([^"]+)"', result)
    if left:
        print("  note: still-relative references:", sorted(set(left))[:10])

if __name__ == "__main__":
    main()
