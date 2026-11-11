#!/usr/bin/env python3
"""Transcribe with faster-whisper (medium, int8, word timestamps). Run in the foreground.
usage: transcribe.py AUDIO16K.wav OUT.json [--lang ht] [--model medium] [--prompt "..."] [--beam 1]"""
import argparse, json, wave, time, numpy as np
from faster_whisper import WhisperModel
ap=argparse.ArgumentParser(); ap.add_argument("wav"); ap.add_argument("out")
ap.add_argument("--lang",default="ht"); ap.add_argument("--model",default="medium")
ap.add_argument("--prompt",default=None); ap.add_argument("--beam",type=int,default=1)
a=ap.parse_args()
m=WhisperModel(a.model,device="cpu",compute_type="int8",cpu_threads=1)
wf=wave.open(a.wav); aud=np.frombuffer(wf.readframes(wf.getnframes()),dtype=np.int16).astype(np.float32)/32768.0  # avoids PyAV
t=time.time(); res=[]
segs,_=m.transcribe(aud,language=a.lang,beam_size=a.beam,word_timestamps=True,vad_filter=False,initial_prompt=a.prompt)
for s in segs:
    print(f"[{s.start:.2f}-{s.end:.2f}] {s.text}",flush=True)
    res.append({"start":s.start,"end":s.end,"text":s.text,"words":[{"w":w.word,"s":w.start,"e":w.end,"p":round(w.probability,2)} for w in s.words]})
json.dump(res,open(a.out,"w"),ensure_ascii=False,indent=1); print(f"done in {time.time()-t:.0f}s")
