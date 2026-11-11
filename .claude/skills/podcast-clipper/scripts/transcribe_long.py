#!/usr/bin/env python3
"""Long-form transcription that survives the ~280 s tool-call limit.
Splits a 16 kHz mono WAV at quiet points, transcribes chunk by chunk, skips chunks already done,
stops cleanly before the time budget runs out. Call it again until it prints ALL DONE, then merge.

  transcribe_long.py split  A16.wav WORKDIR [--chunk 120]
  transcribe_long.py run    WORKDIR [--lang en] [--model small] [--budget 230] [--beam 1]
  transcribe_long.py merge  WORKDIR OUT.json OUT.txt
  transcribe_long.py status WORKDIR

OUT.json = [{start,end,text,words:[{w,s,e,p}]}] in source time (same format as transcribe.py),
OUT.txt  = readable "[mm:ss] text" lines for clip finding.
Each chunk is primed with the tail of the previous chunk's text (continuity of names/spelling)."""
import sys, os, json, wave, time, argparse, numpy as np

def load(path):
    w = wave.open(path); assert w.getframerate() == 16000 and w.getnchannels() == 1, "need 16 kHz mono"
    return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0

def split(a):
    x = load(a.wav); sr = 16000; n = len(x); hop = int(0.05 * sr)
    rms = np.sqrt(np.convolve(x ** 2, np.ones(hop) / hop, mode="same")[::hop] + 1e-12)  # 50 ms frames
    cuts = [0.0]; target = a.chunk
    while cuts[-1] + target < n / sr - min(20, target * 0.5):
        w = min(15, target * 0.25); lo, hi = cuts[-1] + target - w, cuts[-1] + target + w
        i0, i1 = int(lo / 0.05), min(int(hi / 0.05), len(rms) - 6)
        win = np.convolve(rms[i0:i1 + 6], np.ones(6) / 6, mode="valid")[: i1 - i0]  # quietest 300 ms
        cuts.append(round((i0 + int(np.argmin(win)) + 3) * 0.05, 2))
    cuts.append(n / sr)
    os.makedirs(a.work, exist_ok=True)
    chunks = [{"i": i, "t0": cuts[i], "t1": cuts[i + 1]} for i in range(len(cuts) - 1)]
    json.dump({"wav": os.path.abspath(a.wav), "dur": n / sr, "chunks": chunks}, open(f"{a.work}/plan.json", "w"), indent=1)
    print(f"{len(chunks)} chunks, {n/sr/60:.1f} min")

def run(a):
    t_start = time.time()
    plan = json.load(open(f"{a.work}/plan.json"))
    todo = [c for c in plan["chunks"] if not os.path.exists(f"{a.work}/c{c['i']:03d}.json")]
    if not todo: print("ALL DONE"); return
    from faster_whisper import WhisperModel
    m = WhisperModel(a.model, device="cpu", compute_type="int8", cpu_threads=1)
    x = load(plan["wav"]); sr = 16000; per_chunk = None
    for c in todo:
        el = time.time() - t_start
        if per_chunk and el + per_chunk * 1.15 > a.budget:
            break
        prev = f"{a.work}/c{c['i']-1:03d}.json"
        prompt = a.prompt
        if os.path.exists(prev):
            tail = " ".join(s["text"].strip() for s in json.load(open(prev)))[-200:]
            prompt = ((a.prompt + " ") if a.prompt else "") + tail
        t0 = time.time(); seg = x[int(c["t0"] * sr): int(c["t1"] * sr)]
        segs, _ = m.transcribe(seg, language=a.lang, beam_size=a.beam, word_timestamps=True,
                               vad_filter=False, initial_prompt=prompt or None)
        out = []
        for s in segs:
            out.append({"start": s.start + c["t0"], "end": s.end + c["t0"], "text": s.text,
                        "words": [{"w": w.word, "s": round(w.start + c["t0"], 3), "e": round(w.end + c["t0"], 3),
                                   "p": round(w.probability, 2)} for w in (s.words or [])]})
        json.dump(out, open(f"{a.work}/c{c['i']:03d}.json", "w"), ensure_ascii=False)
        dt = time.time() - t0; per_chunk = dt if per_chunk is None else max(per_chunk, dt)
        print(f"chunk {c['i']+1}/{len(plan['chunks'])} ({c['t1']-c['t0']:.0f}s audio) in {dt:.0f}s", flush=True)
    status(a)

def status(a):
    plan = json.load(open(f"{a.work}/plan.json"))
    done = sum(os.path.exists(f"{a.work}/c{c['i']:03d}.json") for c in plan["chunks"])
    print("ALL DONE" if done == len(plan["chunks"]) else f"{done}/{len(plan['chunks'])} chunks done - run again")

def merge(a):
    plan = json.load(open(f"{a.work}/plan.json")); res = []
    for c in plan["chunks"]:
        res += json.load(open(f"{a.work}/c{c['i']:03d}.json"))
    json.dump(res, open(a.out_json, "w"), ensure_ascii=False, indent=1)
    with open(a.out_txt, "w", encoding="utf-8") as f:
        for s in res:
            f.write(f"[{int(s['start']//60):02d}:{s['start']%60:05.2f}] {s['text'].strip()}\n")
    print(f"{len(res)} segments, {sum(len(s['words']) for s in res)} words -> {a.out_json}, {a.out_txt}")

ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="cmd", required=True)
p = sp.add_parser("split"); p.add_argument("wav"); p.add_argument("work"); p.add_argument("--chunk", type=float, default=120)
p = sp.add_parser("run"); p.add_argument("work"); p.add_argument("--lang", default="en"); p.add_argument("--model", default="small")
p.add_argument("--budget", type=float, default=230); p.add_argument("--beam", type=int, default=1); p.add_argument("--prompt", default="")
p = sp.add_parser("merge"); p.add_argument("work"); p.add_argument("out_json"); p.add_argument("out_txt")
p = sp.add_parser("status"); p.add_argument("work")
a = ap.parse_args(); {"split": split, "run": run, "merge": merge, "status": status}[a.cmd](a)
