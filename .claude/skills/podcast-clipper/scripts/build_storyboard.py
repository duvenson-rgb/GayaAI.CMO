#!/usr/bin/env python3
"""Build a reviewable storyboard page (publish it with the Artifact tool).
  build_storyboard.py BEATS.json OUT.html
BEATS.json = {"title": "...", "intro": "...",
  "spec": [["Format","1080×1920, 30fps"], ...],
  "beats": [{"tc":"0.00–1.38","still":"stills/s01.20.jpeg","caption":"...","anim":"...","sound":"...","note":"optional flag"}],
  "footer": "optional", "theme": "dark"|"light"}
Multi-clip (podcast-clipper): replace "spec"/"beats" with
  "clips": [{"title": "Clip 1 · ...", "spec": [[k,v],...], "beats": [...]}, ...]  -> one section per clip, beats numbered 1.1, 1.2 ...
Stills are embedded as data URIs so the page is self-contained."""
import sys, json, base64, subprocess, html as H
d=json.load(open(sys.argv[1])); dark=d.get("theme","dark")=="dark"
def img(p):
    tmp="/tmp/_sb.jpg"; subprocess.run(["ffmpeg","-v","error","-y","-i",p,"-vf","scale=432:-1","-q:v","4",tmp],check=True)
    return base64.b64encode(open(tmp,"rb").read()).decode()
def beats_html(beats,prefix=""):
    rows=[]
    for i,b in enumerate(beats,1):
        note=f'<p class="note">{H.escape(b["note"])}</p>' if b.get("note") else ""
        rows.append(f'''<article class="beat"><figure><img src="data:image/jpeg;base64,{img(b["still"])}" alt="Beat {prefix}{i}"></figure>
<div><div class="meta"><span class="n">Beat {prefix}{i}</span><span>{H.escape(b["tc"])}s</span></div>
<p class="cap">{H.escape(b["caption"])}</p><p class="anim">{H.escape(b["anim"])}</p>
<p class="snd"><span>Sound</span>{H.escape(b.get("sound","—"))}</p>{note}</div></article>''')
    return "".join(rows)
def spec_html(sp): return "".join(f'<div><b>{H.escape(k)}</b>{H.escape(v)}</div>' for k,v in sp)
if "clips" in d:
    body="".join(f'<section class="clipsec" id="c{j}"><h2>{H.escape(c["title"])}</h2><div class="spec">{spec_html(c.get("spec",[]))}</div>{beats_html(c["beats"],f"{j}.")}</section>' for j,c in enumerate(d["clips"],1))
    nav='<nav>'+"".join(f'<a href="#c{j}">{H.escape(c["title"])}</a>' for j,c in enumerate(d["clips"],1))+'</nav>'
else:
    body=beats_html(d["beats"]); nav=""
spec=spec_html(d.get("spec",[]))
D=("#050505","#f2f2f2","rgba(242,242,242,.55)","rgba(242,242,242,.14)"); L=("#f4f3f1","#111","rgba(17,17,17,.55)","rgba(17,17,17,.14)")
P,Q=(D,L) if dark else (L,D)
v=lambda c:f"--bg:{c[0]};--fg:{c[1]};--mute:{c[2]};--line:{c[3]}"
page=f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><title>Storyboard · {H.escape(d["title"])}</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500&display=swap" rel="stylesheet">
<style>:root{{{v(P)};box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}
@media (prefers-color-scheme:{"light" if dark else "dark"}){{:root:not([data-theme="{"dark" if dark else "light"}"]){{{v(Q)}}}}}
:root[data-theme="light"]{{{v(L)}}}:root[data-theme="dark"]{{{v(D)}}}
html{{scroll-padding-top:env(safe-area-inset-top,0px)}}*,*::before,*::after{{box-sizing:inherit}}
body{{margin:0;background:var(--bg);color:var(--fg);font-family:Poppins,"Helvetica Neue",Arial,sans-serif;font-weight:300;line-height:1.55}}
main{{max-width:880px;margin:0 auto;padding:56px 22px 90px}}header{{padding-bottom:36px;border-bottom:1px solid var(--line)}}
h1{{font-weight:400;font-size:clamp(28px,5vw,42px);margin:0 0 10px}}.lede{{color:var(--mute);max-width:62ch;margin:0}}
.spec{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:18px 28px;margin-top:28px}}
.spec div{{font-size:14px;color:var(--mute)}}.spec b{{display:block;font-weight:400;color:var(--fg);font-size:15px}}
.beat{{display:grid;grid-template-columns:minmax(150px,216px) 1fr;gap:30px;padding:34px 0;border-bottom:1px solid var(--line);align-items:start}}
figure{{margin:0;border-radius:18px;overflow:hidden;border:1px solid var(--line);background:#000;aspect-ratio:9/16}}
figure img{{display:block;width:100%;max-width:100%;height:100%;object-fit:cover}}
.meta{{display:flex;gap:14px;font-size:14px;color:var(--mute)}}.n{{color:var(--fg);font-weight:500}}
.cap{{font-size:clamp(20px,3.2vw,26px);font-weight:400;margin:10px 0 12px}}.anim{{margin:0 0 12px;max-width:60ch}}
.snd,.note{{margin:0;color:var(--mute);font-size:15px}}.snd span{{display:inline-block;min-width:62px;color:var(--fg);font-weight:400}}
.note{{margin-top:10px;border-left:2px solid var(--fg);padding-left:12px}}footer{{padding-top:34px;color:var(--mute);max-width:62ch}}
.clipsec{{padding-top:40px}}.clipsec h2{{font-weight:500;font-size:clamp(22px,4vw,30px);margin:0 0 6px}}
nav{{display:flex;flex-wrap:wrap;gap:8px;margin-top:24px}}nav a{{color:var(--fg);border:1px solid var(--line);border-radius:20px;padding:4px 14px;font-size:14px;text-decoration:none}}
@media (max-width:560px){{.beat{{grid-template-columns:120px 1fr;gap:18px}}}}</style></head><body><main>
<header><h1>{H.escape(d["title"])}</h1><p class="lede">{H.escape(d.get("intro","Storyboard for approval. Every still is a real frame from the animation engine. Reply with changes by beat number."))}</p>
<div class="spec">{spec}</div>{nav}</header>{body}<footer><p>{H.escape(d.get("footer",""))}</p></footer></main></body></html>'''
open(sys.argv[2],"w").write(page); print(len(page)//1024,"KB")
