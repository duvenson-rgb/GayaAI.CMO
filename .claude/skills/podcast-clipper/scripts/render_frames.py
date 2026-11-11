#!/usr/bin/env python3
"""Render frames from an HTML engine exposing window.render(t) (and optionally window.stateKey(t)).
  render_frames.py --html engine.html --out DIR [--alpha] [--jpeg] [--fps 30] range N0 N1
  render_frames.py --html engine.html --out DIR --jpeg list 1.2,2.2,5.0
Resumable (skips existing files). Keep each call under ~280 s (~1000-1400 frames).
Fonts are preloaded before the first render: lazy-loaded fonts measure too narrow."""
import argparse, os, asyncio, glob
from playwright.async_api import async_playwright
ap=argparse.ArgumentParser(); ap.add_argument("--html",required=True); ap.add_argument("--out",required=True)
ap.add_argument("--alpha",action="store_true"); ap.add_argument("--jpeg",action="store_true"); ap.add_argument("--fps",type=float,default=30)
ap.add_argument("--fonts",default="400 50px Poppins,500 38px Poppins,900 50px M,700 50px M,800 50px C,50px T")
ap.add_argument("mode"); ap.add_argument("a"); ap.add_argument("b",nargs="?")
A=ap.parse_args()
CHROME=sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome"))[-1]
ext="jpeg" if A.jpeg else "png"
if A.mode=="range": jobs=[(f"{i:05d}",i/A.fps) for i in range(int(A.a),int(A.b))]
else: jobs=[(f"s{float(x):05.2f}",float(x)) for x in A.a.split(",")]
async def main():
    os.makedirs(A.out,exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path=CHROME,args=["--allow-file-access-from-files"])
        pg=await b.new_page(viewport={"width":1080,"height":1920})
        await pg.goto("file://"+os.path.abspath(A.html))
        fl=",".join(f"document.fonts.load('{f}').catch(()=>0)" for f in A.fonts.split(","))
        await pg.evaluate(f"Promise.all([{fl}])"); await pg.wait_for_timeout(200)
        has_key=await pg.evaluate("typeof window.stateKey==='function'")
        prev_key=prev_file=None; made=linked=0
        for name,t in jobs:
            fn=f"{A.out}/{name}.{ext}"
            if os.path.exists(fn): prev_key=None; continue
            key=await pg.evaluate(f"stateKey({t})") if has_key else None
            if key is not None and key==prev_key and prev_file:
                os.link(prev_file,fn); linked+=1; continue
            await pg.evaluate(f"render({t})")
            kw={"type":ext}
            if A.jpeg: kw["quality"]=95
            if A.alpha: kw["omit_background"]=True
            await pg.screenshot(path=fn,**kw); made+=1; prev_key=key; prev_file=fn
        await b.close(); print(f"rendered {made}, reused {linked}")
asyncio.run(main())
