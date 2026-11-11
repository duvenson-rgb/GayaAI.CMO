#!/usr/bin/env python3
"""Screenshot an HTML file so you can look at your own design before handing it over.

Usage:
  python3 render_preview.py page.html out.png [--width 1920 --height 1080] [--full]

Serves the file's directory over a local HTTP server (so relative assets and the
templates' runtime work), waits for fonts/network, then saves a PNG. Needs playwright
(`pip install playwright --break-system-packages && playwright install chromium` if missing).
"""
import argparse, asyncio, functools, http.server, socketserver, threading
from pathlib import Path

def serve(root: Path):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root))
    handler.log_message = lambda *a, **k: None
    httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd

async def shoot(url, out, w, h, full):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": w, "height": h})
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)[:200]))
        await pg.goto(url, wait_until="networkidle", timeout=60000)
        await pg.evaluate("document.fonts && document.fonts.ready")
        await pg.wait_for_timeout(1500)
        await pg.screenshot(path=out, full_page=full)
        await b.close()
        for e in errors:
            print("  page error:", e)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html"); ap.add_argument("out")
    ap.add_argument("--width", type=int, default=1440)
    ap.add_argument("--height", type=int, default=900)
    ap.add_argument("--full", action="store_true", help="capture the full scroll height")
    ap.add_argument("--root", help="directory to serve (default: the skill root if the file is inside it, else the file's folder)")
    a = ap.parse_args()
    f = Path(a.html).resolve()
    skill_root = Path(__file__).resolve().parent.parent
    root = Path(a.root).resolve() if a.root else (skill_root if skill_root in f.parents else f.parent)
    httpd = serve(root)
    url = f"http://127.0.0.1:{httpd.server_address[1]}/{f.relative_to(root).as_posix()}"
    asyncio.run(shoot(url, a.out, a.width, a.height, a.full))
    httpd.shutdown()
    print(f"wrote {a.out}")

if __name__ == "__main__":
    main()
