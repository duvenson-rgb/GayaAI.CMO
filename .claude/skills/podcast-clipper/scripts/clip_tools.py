#!/usr/bin/env python3
"""Clip tools. CLIPS.json schema (see references/clip_selection.md):
  {"source": "/abs/episode.mp4", "lang": "en", "clips": [
    {"id": 1, "title": "...", "hook": "on-screen hook text", "keep": [[t0, t1], ...], "tier": "A",
     "score": {"hook":5,"standalone":4,"value":5,"payoff":4,"delivery":4}, "type": "insight",
     "why": "...", "post": "post caption", "flags": ["..."]}]}
"keep" ranges are in SOURCE time and play in the order listed (list a later range first = cold open).

  clip_tools.py snap  TR.json CLIPS.json            snap every keep range to word boundaries (rewrites CLIPS.json)
  clip_tools.py text  TR.json CLIPS.json [--ids 1,3] print each clip's words (standalone check / paste in chat)
  clip_tools.py cut   CLIPS.json OUTDIR [--ids 1,3] [--maxw 1920]   -> OUTDIR/clip_01.mp4 (or .wav for audio sources)
  clip_tools.py words TR.json CLIPS.json OUTDIR [--ids 1,3]        -> OUTDIR/clip_01_tr.json in clip-local time
  clip_tools.py env   CLIP.(mp4|wav) OUT.js [--fps 30]              -> window.ENV=[per-frame loudness 0..1]"""
import sys, os, json, subprocess, argparse, wave, numpy as np

def words_of(tr): return [w for s in tr for w in s["words"]]
def sel(clips, ids): return [c for c in clips if not ids or c["id"] in ids]
def dur(c): return sum(b - a for a, b in c["keep"])

def snap(a):
    W = words_of(json.load(open(a.tr))); d = json.load(open(a.clips))
    for c in d["clips"]:
        new = []
        for t0, t1 in c["keep"]:
            inside = [i for i, w in enumerate(W) if t0 <= (w["s"] + w["e"]) / 2 <= t1]
            if not inside: new.append([t0, t1]); continue
            i, j = inside[0], inside[-1]
            s = W[i]["s"] - 0.12; e = W[j]["e"] + 0.25
            if i > 0: s = max(s, (W[i - 1]["e"] + W[i]["s"]) / 2)
            if j + 1 < len(W): e = min(e, (W[j]["e"] + W[j + 1]["s"]) / 2)
            new.append([round(max(0, s), 2), round(e, 2)])
        if new != c["keep"]: print(f"clip {c['id']}: {c['keep']} -> {new}")
        c["keep"] = new
    json.dump(d, open(a.clips, "w"), ensure_ascii=False, indent=1); print("snapped")

def text(a):
    W = words_of(json.load(open(a.tr))); d = json.load(open(a.clips))
    for c in sel(d["clips"], a.ids):
        parts = []
        for t0, t1 in c["keep"]:
            parts.append("".join(w["w"] for w in W if t0 <= (w["s"] + w["e"]) / 2 <= t1).strip())
        print(f"--- clip {c['id']} ({dur(c):.1f}s) {c.get('title','')}\n" + "\n[CUT]\n".join(parts) + "\n")

def probe_video(src):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width",
                          "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip()
    return int(out.splitlines()[0]) if out else 0

def cut(a):
    d = json.load(open(a.clips)); src = d["source"]; os.makedirs(a.out, exist_ok=True)
    width = probe_video(src); has_v = width > 0
    for c in sel(d["clips"], a.ids):
        fn = f"{a.out}/clip_{c['id']:02d}." + ("mp4" if has_v else "wav")
        cmd = ["ffmpeg", "-v", "error", "-y"]
        for t0, t1 in c["keep"]:
            cmd += ["-ss", f"{t0:.3f}", "-t", f"{t1 - t0:.3f}", "-i", src]
        n = len(c["keep"]); fg = []
        for i, (t0, t1) in enumerate(c["keep"]):
            L = t1 - t0
            fg.append(f"[{i}:a]aresample=48000,afade=t=in:d=0.015,afade=t=out:st={max(0, L - 0.015):.3f}:d=0.015[a{i}]")
            if has_v:
                sc = f",scale={a.maxw}:-2" if width > a.maxw else ""
                fg.append(f"[{i}:v]fps=30,setpts=PTS-STARTPTS{sc},format=yuv420p[v{i}]")
        if has_v:
            fg.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v][a]")
            cmd += ["-filter_complex", ";".join(fg), "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-c:a", "aac", "-b:a", "320k", fn]
        else:
            fg.append("".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[a]")
            cmd += ["-filter_complex", ";".join(fg), "-map", "[a]", "-c:a", "pcm_s16le", fn]
        subprocess.run(cmd, check=True); print(f"{fn}  {dur(c):.2f}s  ({n} range{'s' if n > 1 else ''})", flush=True)

def words(a):
    W = words_of(json.load(open(a.tr))); d = json.load(open(a.clips)); os.makedirs(a.out, exist_ok=True)
    for c in sel(d["clips"], a.ids):
        off = 0.0; segs = []
        for t0, t1 in c["keep"]:
            ws = [{"w": w["w"], "s": round(max(0, w["s"] - t0) + off, 3), "e": round(min(t1 - t0, w["e"] - t0) + off, 3),
                   "p": w.get("p", 1)} for w in W if t0 <= (w["s"] + w["e"]) / 2 <= t1]
            # one pseudo-segment per sentence-ish run so srt_tools draft works unchanged
            cur = []
            for w in ws:
                cur.append(w)
                if w["w"].strip()[-1:] in ".?!":
                    segs.append(cur); cur = []
            if cur: segs.append(cur)
            off += t1 - t0
        out = [{"start": s[0]["s"], "end": s[-1]["e"], "text": "".join(w["w"] for w in s), "words": s} for s in segs]
        fn = f"{a.out}/clip_{c['id']:02d}_tr.json"; json.dump(out, open(fn, "w"), ensure_ascii=False, indent=1)
        print(fn, sum(len(s) for s in segs), "words")

def env(a):
    tmp = "/tmp/_env.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.media, "-ac", "1", "-ar", "16000", tmp], check=True)
    w = wave.open(tmp); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    hop = int(16000 / a.fps); n = len(x) // hop
    r = np.sqrt(np.mean(x[: n * hop].reshape(n, hop) ** 2, axis=1) + 1e-9)
    db = 20 * np.log10(r); v = np.clip((db + 50) / 38, 0, 1)            # -50 dBFS -> 0, -12 dBFS -> 1
    sm = np.copy(v)
    for i in range(1, n): sm[i] = max(v[i], sm[i - 1] * 0.82)            # fast attack, smooth release
    open(a.out, "w").write("window.ENV=" + json.dumps([round(float(s), 3) for s in sm]) + ";\n"); print(n, "frames")

ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="cmd", required=True)
ids = lambda s: [int(x) for x in s.split(",")]
p = sp.add_parser("snap"); p.add_argument("tr"); p.add_argument("clips")
p = sp.add_parser("text"); p.add_argument("tr"); p.add_argument("clips"); p.add_argument("--ids", type=ids)
p = sp.add_parser("cut"); p.add_argument("clips"); p.add_argument("out"); p.add_argument("--ids", type=ids); p.add_argument("--maxw", type=int, default=1920)
p = sp.add_parser("words"); p.add_argument("tr"); p.add_argument("clips"); p.add_argument("out"); p.add_argument("--ids", type=ids)
p = sp.add_parser("env"); p.add_argument("media"); p.add_argument("out"); p.add_argument("--fps", type=float, default=30)
a = ap.parse_args(); {"snap": snap, "text": text, "cut": cut, "words": words, "env": env}[a.cmd](a)
