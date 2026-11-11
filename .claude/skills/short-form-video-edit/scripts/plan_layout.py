#!/usr/bin/env python3
"""Print/save the face-safety plan computed by an engine (window.PLAN) — which windows split, which captions moved.
  plan_layout.py --html engine.html OUT_plan.json"""
import sys, json, glob, os, asyncio, argparse
from playwright.async_api import async_playwright
ap=argparse.ArgumentParser(); ap.add_argument("--html",required=True); ap.add_argument("out"); A=ap.parse_args()
CHROME=sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome"))[-1]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path=CHROME,args=["--allow-file-access-from-files"])
        pg=await b.new_page(viewport={"width":1080,"height":1920}); await pg.goto("file://"+os.path.abspath(A.html))
        await pg.evaluate("Promise.all(['900 50px M','800 50px M','600 50px M','500 50px M'].map(f=>document.fonts.load(f)))")
        await pg.evaluate("planLayout()")  # re-plan with fonts loaded (text widths change)
        plan=await pg.evaluate("({splits:window.PLAN.splits,moved:EVENTS.filter(e=>e.dy).map(e=>({type:e.type,t0:e.t0,dy:Math.round(e.dy)})),split_events:EVENTS.filter(e=>e.split).map(e=>({type:e.type,t0:e.t0,t1:e.t1}))})")
        await b.close()
    json.dump(plan,open(A.out,"w"),indent=1); print(json.dumps(plan,indent=1))
asyncio.run(main())
