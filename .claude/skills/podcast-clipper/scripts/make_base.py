#!/usr/bin/env python3
"""Build the 1080x1920 base video for one clip from a layout plan, and the EDL the overlay engine needs.
  make_base.py CLIP.mp4 LAYOUT.json OUT.mp4 EDL.js [--still T1,T2,...]   (--still: only write JPEG stills at those times)

LAYOUT.json:
 {"grade": "bold" | "clean" | "none" | "<raw ffmpeg filter chain>",
  "boxes": {"A": {"x":..,"y":..,"w":..,"h":..}, "B": {...}},     # 9:16 crop boxes in CLIP pixels, face ~1/3 from the top
  "split": {"top": "A", "bottom": "B", "band": 400},            # stacked layout: header band + two 1080x760 panels
  "segments": [{"t0":0, "t1":4.2, "mode":"A", "z":1.0},          # mode: a box name | "split" | "wide"
               {"t0":4.2, "t1":9.8, "mode":"B", "z":1.15}, ...]} # z = punch-in (1.0-1.3), face stays at the same height
Segments must tile the clip (t1 of one = t0 of the next; last t1 = clip duration; t1 may be omitted on the last one)."""
import sys, json, subprocess, argparse

GRADES = {
    "bold": "eq=brightness=-0.05:contrast=1.12:saturation=0.85:gamma=0.94,colorbalance=rs=-0.05:bs=0.06:rh=0.04:bh=-0.03",
    "clean": "eq=contrast=1.05:saturation=1.05",
    "none": "null",
}
ap = argparse.ArgumentParser(); ap.add_argument("clip"); ap.add_argument("layout"); ap.add_argument("out"); ap.add_argument("edl")
ap.add_argument("--still", default=None)
a = ap.parse_args(); L = json.load(open(a.layout))

pr = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height:format=duration",
                     "-of", "json", a.clip], capture_output=True, text=True).stdout
pj = json.loads(pr); W, H = pj["streams"][0]["width"], pj["streams"][0]["height"]; D = float(pj["format"]["duration"])
segs = L["segments"]; segs[-1]["t1"] = segs[-1].get("t1") or D
grade = GRADES.get(L.get("grade", "bold"), L.get("grade"))
ev = lambda x: int(round(x / 2) * 2)

def box_crop(name, z=1.0, aspect=9 / 16, widen=1.0):
    b = L["boxes"][name]; fy = b["y"] + b["h"] * 0.33; cx = b["x"] + b["w"] / 2
    if aspect == 9 / 16:
        h = b["h"] / z; w = h * 9 / 16; y = fy - 0.33 * h
    else:  # panel: wider than the 9:16 box, face at ~42% of panel height
        w = b["w"] * widen / z; h = w / aspect; y = fy - 0.42 * h
    w, h = min(w, W), min(h, H)
    x = min(max(0, cx - w / 2), W - w); y = min(max(0, y), H - h)
    return f"crop={ev(w)}:{ev(h)}:{ev(x)}:{ev(y)}"

fg = []
for i, s in enumerate(segs):
    tr = f"[0:v]trim=start={s['t0']:.4f}:end={s['t1']:.4f},setpts=PTS-STARTPTS"
    m, z = s["mode"], s.get("z", 1.0)
    if m == "split":
        sp = L["split"]; band = sp.get("band", 400); ph = (1920 - band) // 2
        fg.append(f"{tr},split[t{i}][b{i}]")
        fg.append(f"[t{i}]{box_crop(sp['top'], z, 1080/ph, 1.1)},scale=1080:{ph}:flags=lanczos,vignette=PI/4.5[tp{i}]")
        fg.append(f"[b{i}]{box_crop(sp['bottom'], z, 1080/ph, 1.1)},scale=1080:{ph}:flags=lanczos,vignette=PI/4.5[bp{i}]")
        fg.append(f"color=c=0x07080a:s=1080x{band}:r=30,trim=duration={s['t1']-s['t0']:.4f}[band{i}]")
        fg.append(f"[band{i}][tp{i}][bp{i}]vstack=inputs=3,setsar=1[s{i}]")
    elif m == "wide":
        fg.append(f"{tr},split[w{i}][g{i}]")
        fg.append(f"[g{i}]scale=-2:1920,crop=1080:1920,boxblur=30:2,eq=brightness=-0.25[bg{i}]")
        fg.append(f"[w{i}]scale=1080:-2:flags=lanczos[fgw{i}]")
        fg.append(f"[bg{i}][fgw{i}]overlay=0:(H-h)/2*0.8,setsar=1[s{i}]")
    else:
        fg.append(f"{tr},{box_crop(m, z)},scale=1080:1920:flags=lanczos,vignette=PI/3.3,setsar=1[s{i}]")
fg.append("".join(f"[s{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=0,{grade},format=yuv420p[v]")

edl = {"cuts": [s["t0"] for s in segs], "z": [s.get("z", 1.0) for s in segs], "mode": [s["mode"] for s in segs],
       "band": L.get("split", {}).get("band", 400)}
open(a.edl, "w").write("window.EDL=" + json.dumps(edl) + ";\n")

if a.still:
    for t in a.still.split(","):
        fn = a.out.replace(".mp4", f"_{float(t):05.2f}.jpg")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.clip, "-filter_complex", ";".join(fg), "-map", "[v]",
                        "-ss", t, "-frames:v", "1", "-q:v", "3", fn], check=True); print(fn)
else:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.clip, "-filter_complex", ";".join(fg), "-map", "[v]", "-an",
                    "-r", "30", "-c:v", "libx264", "-preset", "veryfast", "-crf", "15", a.out], check=True)
    print(a.out, f"{D:.2f}s", len(segs), "segments")
