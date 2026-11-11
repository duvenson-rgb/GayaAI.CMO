#!/usr/bin/env python3
"""Final composite with face-safe split screens.
  split_composite.py BASE.mp4 FRAMES_DIR PLAN.json AUDIO.wav OUT.mp4 [--fps 30]
During each split window the footage is reframed: a 1080x960 crop starting at y0 (the head) is placed in the bottom half;
the engine's opaque panel covers the top half. Overlay frames go on top as usual."""
import sys, json, subprocess, argparse
ap=argparse.ArgumentParser(); ap.add_argument("base"); ap.add_argument("frames"); ap.add_argument("plan"); ap.add_argument("audio"); ap.add_argument("out")
ap.add_argument("--fps",type=int,default=30); A=ap.parse_args()
sp=json.load(open(A.plan))["splits"]; n=len(sp)
fc=f"[0:v]split={n+1}" + "".join(f"[s{i}]" for i in range(n+1)) + ";" if n else "[0:v]null[s0];"
cur="s0"
for i,s in enumerate(sp,1):
    fc+=f"[s{i}]crop=1080:960:0:{s['y0']}[c{i}];[{cur}][c{i}]overlay=0:960:enable='between(t,{s['t0']},{s['t1']-0.001})'[m{i}];"; cur=f"m{i}"
fc+=f"[{cur}][1:v]overlay=format=auto:shortest=1,setsar=1,format=yuv420p[v]"
cmd=["ffmpeg","-v","error","-y","-i",A.base,"-framerate",str(A.fps),"-i",f"{A.frames}/%05d.png","-i",A.audio,"-filter_complex",fc,
     "-map","[v]","-map","2:a","-c:v","libx264","-preset","faster","-crf","18","-profile:v","high","-c:a","aac","-b:a","192k","-ar","48000",
     "-movflags","+faststart","-shortest",A.out]
subprocess.run(cmd,check=True); print("ok", n, "split windows")
