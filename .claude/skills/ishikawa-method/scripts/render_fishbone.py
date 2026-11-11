#!/usr/bin/env python3
"""Render an Ishikawa (fishbone) diagram as a standalone SVG from a JSON spec.

Usage:
    python render_fishbone.py spec.json out.svg

Spec:
{
  "title": "optional title shown above the fish",
  "problem": "the effect / problem statement (fish head)",
  "highlight_top": 2,            # optional: highlight the N highest-scored causes
  "labels": {"root": "Cause racine", "legend": "..."},  # optional: translate labels
  "families": [
    {"name": "Method", "causes": [
        {"cause": "short cause", "root": "short root cause", "score": 4.5}
    ]}
  ]
}
Only "problem" and "families[].name" are required.
"""
import json
import math
import sys
from xml.sax.saxutils import escape

PALETTE = ["#E0962B", "#B5523B", "#C94A55", "#6FA53A", "#3F93A3", "#5E6FD0", "#8E5CC0", "#2F8F69"]
SPINE = "#2F4A7A"
HEAD = "#4F7FC9"
PRIORITY = "#D7372A"
FONT = "Helvetica, Arial, sans-serif"


def wrap(text, width, max_lines):
    words = str(text or "").split()
    lines, cur = [], ""
    for w in words:
        if not cur:
            cur = w
        elif len(cur) + 1 + len(w) <= width:
            cur += " " + w
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        lines[-1] = (last[: width - 1].rstrip() + "…") if len(last) >= width else last + "…"
    return lines


def text_block(x, y, lines, size, color, weight="normal", anchor="start", line_h=None):
    line_h = line_h or size * 1.25
    out = []
    for i, ln in enumerate(lines):
        out.append(
            f'<text x="{x:.1f}" y="{y + i * line_h:.1f}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{escape(ln)}</text>'
        )
    return out


def render(spec):
    fams = spec.get("families") or []
    if not fams:
        raise ValueError("spec needs at least one family")
    problem = spec.get("problem", "Problem")
    title = spec.get("title")
    top_n = int(spec.get("highlight_top", 0) or 0)
    labels = spec.get("labels") or {}
    root_label = labels.get("root", "Root")

    # Pick priority causes
    scored = []
    for fi, f in enumerate(fams):
        for ci, c in enumerate(f.get("causes") or []):
            if isinstance(c.get("score"), (int, float)):
                scored.append((c["score"], fi, ci))
    scored.sort(reverse=True)
    priority = {(fi, ci) for _, fi, ci in scored[:top_n]}

    n = len(fams)
    cols = math.ceil(n / 2)
    max_causes = max([len(f.get("causes") or []) for f in fams] + [1])

    ROW = 74
    col_w = 330
    rib_len = 205
    bone_h = max(190, ROW * max_causes + 70)
    slant = bone_h * 0.35
    title_h = 60 if title else 20
    left = 40
    tail_w = 70
    head_w = 280
    spine_start = left + tail_w
    spine_end = spine_start + col_w * cols + 60
    W = spine_end + head_w + 30
    spine_y = title_h + 50 + bone_h
    H = spine_y + bone_h + 90

    s = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}">',
        f'<rect width="100%" height="100%" fill="#FFFFFF"/>',
    ]
    if title:
        s += text_block(W / 2, 42, [title], 26, "#1D2433", "bold", "middle")

    # Tail
    s.append(
        f'<path d="M{spine_start:.1f},{spine_y:.1f} L{left:.1f},{spine_y - 55:.1f} '
        f'Q{left + 22:.1f},{spine_y:.1f} {left:.1f},{spine_y + 55:.1f} Z" fill="{HEAD}" opacity="0.85"/>'
    )
    # Spine
    s.append(
        f'<line x1="{spine_start:.1f}" y1="{spine_y:.1f}" x2="{spine_end:.1f}" y2="{spine_y:.1f}" '
        f'stroke="{SPINE}" stroke-width="6" stroke-linecap="round"/>'
    )

    # Head with problem text
    p_lines = wrap(problem, 26, 7)
    hh = max(70, len(p_lines) * 10 + 40)
    hx = spine_end
    s.append(
        f'<path d="M{hx:.1f},{spine_y - hh:.1f} C{hx + head_w * 0.75:.1f},{spine_y - hh:.1f} '
        f'{hx + head_w:.1f},{spine_y - hh * 0.35:.1f} {hx + head_w:.1f},{spine_y:.1f} '
        f'C{hx + head_w:.1f},{spine_y + hh * 0.35:.1f} {hx + head_w * 0.75:.1f},{spine_y + hh:.1f} '
        f'{hx:.1f},{spine_y + hh:.1f} Z" fill="{HEAD}"/>'
    )
    lh = 19
    ty = spine_y - (len(p_lines) - 1) * lh / 2 + 5
    s += text_block(hx + head_w * 0.47, ty, p_lines, 15, "#FFFFFF", "bold", "middle", lh)

    # Bones
    for idx, fam in enumerate(fams):
        col = idx // 2
        top = idx % 2 == 0
        color = fam.get("color") or PALETTE[idx % len(PALETTE)]
        ax = spine_start + col_w * (col + 1) + 20
        sign = -1 if top else 1
        ex, ey = ax - slant, spine_y + sign * bone_h
        s.append(
            f'<line x1="{ex:.1f}" y1="{ey:.1f}" x2="{ax:.1f}" y2="{spine_y:.1f}" '
            f'stroke="{color}" stroke-width="4" stroke-linecap="round"/>'
        )
        label_y = ey - 16 if top else ey + 30
        s += text_block(ex, label_y, [fam.get("name", "")], 19, color, "bold", "middle")

        causes = fam.get("causes") or []
        k = len(causes)
        for ci, c in enumerate(causes):
            t = (ci + 0.75) / (k + 0.5)
            px = ex + t * (ax - ex)
            py = ey + t * (spine_y - ey)
            is_pri = (idx, ci) in priority
            rc = PRIORITY if is_pri else color
            sw = 3 if is_pri else 1.8
            x0 = px - rib_len
            s.append(
                f'<line x1="{x0:.1f}" y1="{py:.1f}" x2="{px:.1f}" y2="{py:.1f}" '
                f'stroke="{rc}" stroke-width="{sw}"/>'
            )
            c_lines = wrap(c.get("cause", ""), 30, 2)
            s += text_block(
                x0 + 4, py - 6 - (len(c_lines) - 1) * 15, c_lines, 12.5,
                "#1D2433", "bold" if is_pri else "normal", "start", 15
            )
            if c.get("root"):
                r_lines = wrap(f"{root_label}: " + str(c["root"]), 36, 2)
                s += text_block(x0 + 4, py + 14, r_lines, 10.5, rc, "bold", "start", 13)
            if isinstance(c.get("score"), (int, float)):
                bx = x0 - 17
                s.append(
                    f'<circle cx="{bx:.1f}" cy="{py:.1f}" r="14" fill="{PRIORITY if is_pri else "#FFFFFF"}" '
                    f'stroke="{rc}" stroke-width="2"/>'
                )
                sc = c["score"]
                sc_txt = f"{sc:g}"
                s += text_block(bx, py + 4, [sc_txt], 11, "#FFFFFF" if is_pri else rc, "bold", "middle")

    legend = labels.get("legend")
    if legend is None:
        legend = "Score = Impact × Evidence × Control ÷ 25 (0–5)"
        if priority:
            legend += "  ·  Red = priority root causes"
    s += text_block(left, H - 24, [legend], 12, "#5A6275")
    s.append("</svg>")
    return "\n".join(s)


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        spec = json.load(f)
    svg = render(spec)
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {sys.argv[2]}")


if __name__ == "__main__":
    main()
