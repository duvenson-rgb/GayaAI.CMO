#!/usr/bin/env python3
"""SRT helpers.
  draft TR.json OUT.srt [--max-words 4]   whisper words -> draft cues (text still needs correcting)
  tojs  IN.srt OUT.js                     approved SRT -> window.CUES=[[t0,t1,"text"],...]   (engine_minimal)
  tocaps IN.srt OUT.js [--case keep]      approved SRT -> window.CAPS=[{t0,t1,parts:[{t,s}]}] (engine_podcast / engine_bold)
                                          markup: *word* -> accent color, *two words*|red -> forced color; text uppercased by default
  show  IN.srt                            print SRT (paste it in the reply)
  diff  IN.srt CAPTIONS.js                check engine captions == approved SRT text"""
import sys, json, re
def ts(t): h=int(t//3600); m=int(t%3600//60); s=t%60; return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s%1)*1000)):03d}".replace(",1000",",999")
def pt(s): h,m,r=s.split(":"); sec,ms=r.split(","); return int(h)*3600+int(m)*60+int(sec)+int(ms)/1000
def read(path):
    out=[]
    for b in re.split(r"\n\s*\n",open(path,encoding="utf-8").read().strip()):
        L=b.strip().splitlines()
        if len(L)>=3 and "-->" in L[1]:
            a,b2=[x.strip() for x in L[1].split("-->")]; out.append([pt(a),pt(b2)," ".join(L[2:]).strip()])
    return out
def write(cues,path):
    open(path,"w",encoding="utf-8").write("\n".join(f"{i}\n{ts(a)} --> {ts(b)}\n{t}\n" for i,(a,b,t) in enumerate(cues,1)))
cmd=sys.argv[1]
if cmd=="draft":
    d=json.load(open(sys.argv[2])); mw=int(sys.argv[sys.argv.index("--max-words")+1]) if "--max-words" in sys.argv else 4
    ws=[w for s in d for w in s["words"]]; cues=[]; cur=[]
    # break at sentence ends, then commas (>=2 words), else at max words; a sentence-final word may make it max+1
    for k,w in enumerate(ws):
        cur.append(w); e=w["w"].strip()[-1:]; nxt=ws[k+1]["w"].strip() if k+1<len(ws) else ""
        gap=(ws[k+1]["s"]-w["e"]) if k+1<len(ws) else 9
        if e in ".?!" or (e in ",;:" and len(cur)>=2) or gap>0.6 or \
           (len(cur)>=mw and not (len(cur)==mw and nxt[-1:] in ".?!,")) or len(cur)>mw:
            cues.append([cur[0]["s"],cur[-1]["e"],"".join(x["w"] for x in cur).strip()]); cur=[]
    if cur: cues.append([cur[0]["s"],cur[-1]["e"],"".join(x["w"] for x in cur).strip()])
    for a,b in zip(cues,cues[1:]):
        if b[0]-a[1]<0.3: a[1]=b[0]
    write(cues,sys.argv[3]); print(open(sys.argv[3]).read())
elif cmd=="tojs":
    cues=read(sys.argv[2]); open(sys.argv[3],"w").write("window.CUES="+json.dumps(cues,ensure_ascii=False)+";\n"); print(len(cues),"cues")
elif cmd=="tocaps":
    up="--case" not in sys.argv or sys.argv[sys.argv.index("--case")+1]!="keep"; out=[]
    for a,b,t in read(sys.argv[2]):
        parts=[]; pos=0
        for m in re.finditer(r"\*([^*]+)\*(?:\|(\w+))?",t):
            if m.start()>pos: parts.append({"t":t[pos:m.start()].strip(),"s":"w"})
            parts.append({"t":m.group(1).strip(),"s":m.group(2) or "hi"}); pos=m.end()
        if pos<len(t): parts.append({"t":t[pos:].strip(),"s":"w"})
        parts=[dict(p,t=p["t"].upper() if up and p["s"]!="gold" else p["t"]) for p in parts if p["t"]]
        out.append({"t0":round(a,3),"t1":round(b,3),"parts":parts})
    open(sys.argv[3],"w").write("window.CAPS="+json.dumps(out,ensure_ascii=False)+";\n"); print(len(out),"caps")
elif cmd=="show": print(open(sys.argv[2],encoding="utf-8").read())
elif cmd=="diff":
    srt=[re.sub(r"[*]|\|\w+","",c[2]).lower() for c in read(sys.argv[2])]
    js=json.loads(open(sys.argv[3]).read().split("=",1)[1].rstrip().rstrip(";"))
    eng=[(c[2] if isinstance(c,list) else " ".join(p["t"] for p in c["parts"])).lower() for c in js]
    bad=[(i+1,a,b) for i,(a,b) in enumerate(zip(srt,eng)) if re.sub(r"\W","",a)!=re.sub(r"\W","",b)]
    print("OK" if not bad and len(srt)==len(eng) else f"MISMATCH {bad} count {len(srt)} vs {len(eng)}")
