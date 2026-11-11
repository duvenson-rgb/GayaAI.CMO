#!/usr/bin/env python3
"""SRT helpers.
  draft TR.json OUT.srt [--max-words 4]   whisper words -> draft cues (text still needs correcting)
  tojs  IN.srt OUT.js                     approved SRT -> window.CUES=[[t0,t1,"text"],...]
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
    cues=[]
    for s in d:
        ws=s["words"]
        for i in range(0,len(ws),mw):
            g=ws[i:i+mw]; cues.append([g[0]["s"],g[-1]["e"]," ".join(w["w"].strip() for w in g)])
    for a,b in zip(cues,cues[1:]):
        if b[0]-a[1]<0.3: a[1]=b[0]
    write(cues,sys.argv[3]); print(open(sys.argv[3]).read())
elif cmd=="tojs":
    cues=read(sys.argv[2]); open(sys.argv[3],"w").write("window.CUES="+json.dumps(cues,ensure_ascii=False)+";\n"); print(len(cues),"cues")
elif cmd=="show": print(open(sys.argv[2],encoding="utf-8").read())
elif cmd=="diff":
    srt=[re.sub(r"[*]|\|\w+","",c[2]).lower() for c in read(sys.argv[2])]
    js=json.loads(open(sys.argv[3]).read().split("=",1)[1].rstrip().rstrip(";"))
    eng=[(c[2] if isinstance(c,list) else " ".join(p["t"] for p in c["parts"])).lower() for c in js]
    bad=[(i+1,a,b) for i,(a,b) in enumerate(zip(srt,eng)) if re.sub(r"\W","",a)!=re.sub(r"\W","",b)]
    print("OK" if not bad and len(srt)==len(eng) else f"MISMATCH {bad} count {len(srt)} vs {len(eng)}")
