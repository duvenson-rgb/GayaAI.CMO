#!/usr/bin/env python3
"""Phone-frame preview page for a vertical video (the chat player letterboxes vertical video in a wide box).
  build_phone_preview.py VIDEO.mp4 OUT.html "Title"   -> publish OUT.html with the Artifact tool (video must be < ~12 MB)"""
import sys, base64
v,out,title=sys.argv[1],sys.argv[2],sys.argv[3]
b=base64.b64encode(open(v,"rb").read()).decode()
open(out,"w").write(f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title><style>:root{{--bg:#e9e7e3;--fg:#111;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#1a1a1c;--fg:#f2f2f2}}}}:root[data-theme="dark"]{{--bg:#1a1a1c;--fg:#f2f2f2}}:root[data-theme="light"]{{--bg:#e9e7e3;--fg:#111}}
html,body{{height:100%}}body{{margin:0;background:var(--bg);color:var(--fg);font-family:-apple-system,Helvetica,Arial,sans-serif;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;padding:20px}}
.phone{{height:min(82vh,860px);aspect-ratio:9/16;max-width:92vw;border-radius:36px;border:10px solid #0b0b0c;background:#000;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.35)}}
video{{width:100%;height:100%;object-fit:cover;display:block;max-width:100%}}p{{margin:0;font-size:14px;opacity:.6}}</style></head><body>
<div class="phone"><video src="data:video/mp4;base64,{b}" controls playsinline loop></video></div><p>1080 × 1920 · 9:16 · as it plays on Reels</p></body></html>''')
print("ok")
