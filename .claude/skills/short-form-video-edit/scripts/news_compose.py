#!/usr/bin/env python3
"""Compose the picture track for the news/B-roll style from a beat list (host voice runs over everything).
  news_compose.py BEATS.json OUT_base.mp4
BEATS.json = {"host":"host_9x16.mp4", "faces":"faces.js" (optional, for split framing), "fps":30,
  "beats":[{"t0":0,"t1":2.1,"layout":"split|card|full|host|white","media":"assets/a007.jpg","ss":0,"kb":"in|out|none"}]}
layouts: split = media top half + host (reframed on the head) bottom half; card = media in a rounded 16:9 card over a blurred,
darkened copy of itself; full = media fills the frame; host = host footage; white = plain white (engine draws on it).
Images get a slow Ken Burns move. Each beat renders to a segment, then segments are concatenated."""
import sys, json, os, subprocess, tempfile
from PIL import Image, ImageDraw
B=json.load(open(sys.argv[1])); OUT=sys.argv[2]; FPS=B.get("fps",30); tmp=tempfile.mkdtemp(prefix="nc_")
def run(a): subprocess.run(["ffmpeg","-v","error","-y",*a],check=True)
heads=None
if B.get("faces"):
    F=json.loads(open(B["faces"]).read().split("=",1)[1].rstrip().rstrip(";")); heads=(F["fps"],[b[1] for b in F["boxes"]])
def y0_for(t0,t1):
    if not heads: return 480
    f,tops=heads; seg=sorted(tops[int(t0*f):max(int(t0*f)+1,int(t1*f))]); return max(0,min(960,seg[len(seg)//2]-60))
def mask(w,h,r=40):
    p=os.path.join(tmp,f"m{w}x{h}.png")
    if not os.path.exists(p):
        m=Image.new("L",(w,h),0); ImageDraw.Draw(m).rounded_rectangle([0,0,w-1,h-1],r,fill=255); m.save(p)
    return p
def media_in(b,dur):
    m=b["media"]
    if m.lower().endswith((".jpg",".jpeg",".png",".webp")):
        n=int(dur*FPS)+1; z={"in":f"1+0.08*on/{n}","out":f"1.08-0.08*on/{n}"}.get(b.get("kb","in"),"1")
        # upscale first so the Ken Burns move is smooth; output a 1920x1080-ish working frame keeping aspect
        return ["-loop","1","-framerate",str(FPS),"-t",f"{dur:.3f}","-i",m], f"scale=3840:-2,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps={FPS}"
    return ["-ss",str(b.get("ss",0)),"-t",f"{dur:.3f}","-i",m], f"fps={FPS}"
cover=lambda w,h:f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}"
segs=[]
for i,b in enumerate(B["beats"]):
    dur=b["t1"]-b["t0"]; o=os.path.join(tmp,f"s{i:03d}.mp4"); L=b["layout"]; enc=["-t",f"{dur:.3f}","-r",str(FPS),"-c:v","libx264","-preset","veryfast","-crf","17","-pix_fmt","yuv420p","-an",o]
    host=["-ss",f'{b["t0"]:.3f}',"-t",f"{dur:.3f}","-i",B["host"]]
    if L=="host": run(host+["-vf",f"{cover(1080,1920)},setsar=1"]+enc)
    elif L=="white": run(["-f","lavfi","-t",f"{dur:.3f}","-i",f"color=white:s=1080x1920:r={FPS}"]+enc)
    else:
        mi,mf=media_in(b,dur)
        if L=="full": run(mi+["-vf",f"{mf},{cover(1080,1920)},setsar=1"]+enc)
        elif L=="split":
            y0=y0_for(b["t0"],b["t1"])
            run(mi+host+["-filter_complex",f"[0:v]{mf},{cover(1080,960)}[t];[1:v]{cover(1080,1920)},crop=1080:960:0:{y0}[h];[t][h]vstack,setsar=1[v]","-map","[v]"]+enc)
        elif L=="card":
            w,h=1000,562
            run(mi+["-i",mask(w,h),"-filter_complex",f"[0:v]{mf},split[a][b];[a]{cover(1080,1920)},boxblur=40:2,eq=brightness=-0.28:saturation=0.8[bg];"
                f"[b]{cover(w,h)}[fg0];[fg0][1:v]alphamerge[fg];[bg][fg]overlay=40:{(1920-h)//2-120}:shortest=1,setsar=1[v]","-map","[v]"]+enc)
    segs.append(o); print(f"beat {i+1}: {L} {dur:.2f}s")
lst=os.path.join(tmp,"list.txt"); open(lst,"w").write("".join(f"file '{s}'\n" for s in segs))
run(["-f","concat","-safe","0","-i",lst,"-c","copy",OUT]); print("ok",OUT)
