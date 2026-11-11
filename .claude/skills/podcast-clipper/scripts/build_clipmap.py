#!/usr/bin/env python3
"""Clip map page for Gate 1 (publish with the Artifact tool).
  build_clipmap.py CLIPS.json TR.json OUT.html [--thumbs DIR] [--episode "Title"] [--dropped DROPPED.json]
Thumbnails (optional): DIR/clip_01.jpg ... (a frame at the hook). DROPPED.json (optional): [{"range":"12:40-13:30","why":"..."}]
so the user can see what was considered and rejected."""
import sys, json, os, re, base64, subprocess, argparse, html as H
ap = argparse.ArgumentParser(); ap.add_argument("clips"); ap.add_argument("tr"); ap.add_argument("out")
ap.add_argument("--thumbs"); ap.add_argument("--episode", default="Episode"); ap.add_argument("--dropped")
a = ap.parse_args(); d = json.load(open(a.clips)); W = [w for s in json.load(open(a.tr)) for w in s["words"]]
mm = lambda t: f"{int(t//60)}:{t%60:04.1f}"
def thumb(i):
    if not a.thumbs: return ""
    p = f"{a.thumbs}/clip_{i:02d}.jpg"
    if not os.path.exists(p): return ""
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p, "-vf", "scale=360:-1", "-q:v", "4", "/tmp/_cm.jpg"], check=True)
    return f'<figure><img src="data:image/jpeg;base64,{base64.b64encode(open("/tmp/_cm.jpg","rb").read()).decode()}" alt="Clip {i}"></figure>'
KEYS = [("hook", "Hook"), ("standalone", "Standalone"), ("value", "Value"), ("payoff", "Payoff"), ("delivery", "Delivery")]
cards = []
for c in d["clips"]:
    sc = c.get("score", {}); tot = sum(sc.get(k, 0) for k, _ in KEYS); dur = sum(t1 - t0 for t0, t1 in c["keep"])
    txt = " <em>[cut]</em> ".join(H.escape("".join(w["w"] for w in W if t0 <= (w["s"] + w["e"]) / 2 <= t1).strip()) for t0, t1 in c["keep"])
    bars = "".join(f'<div class="sc"><span>{n}</span><i><b style="width:{sc.get(k,0)*20}%"></b></i><em>{sc.get(k,"–")}</em></div>' for k, n in KEYS)
    flags = "".join(f'<p class="flag">{H.escape(f)}</p>' for f in c.get("flags", []))
    rng = " + ".join(f"{mm(t0)}–{mm(t1)}" for t0, t1 in c["keep"])
    cards.append(f'''<article class="clip">{thumb(c["id"])}<div class="body">
<div class="meta"><span class="n">Clip {c["id"]}</span><span class="tier t{c.get("tier","B")}">Tier {c.get("tier","B")}</span><span>{dur:.0f}s</span><span>{H.escape(c.get("type",""))}</span><span>{tot}/25</span></div>
<h2>{H.escape(c.get("title",""))}</h2><p class="hook"><span>On-screen hook</span>{re.sub(r"\*([^*]+)\*", r"<mark>\1</mark>", H.escape(c.get("hook","")))}</p>
<p class="why">{H.escape(c.get("why",""))}</p><div class="scores">{bars}</div>{flags}
<p class="rng">Source: {rng}</p><details><summary>Full clip text</summary><p class="tx">{txt}</p></details></div></article>''')
drop = ""
if a.dropped and os.path.exists(a.dropped):
    rows = "".join(f'<li><b>{H.escape(x["range"])}</b> {H.escape(x["why"])}</li>' for x in json.load(open(a.dropped)))
    drop = f'<section class="drop"><h3>Considered and dropped</h3><ul>{rows}</ul></section>'
V = lambda bg, fg, mu, li, ca: f"--bg:{bg};--fg:{fg};--mute:{mu};--line:{li};--card:{ca}"
Lt = V("#f4f3f1", "#111", "rgba(17,17,17,.58)", "rgba(17,17,17,.13)", "#fff"); Dk = V("#08090b", "#f2f2f2", "rgba(242,242,242,.56)", "rgba(242,242,242,.13)", "#121317")
total = sum(sum(t1 - t0 for t0, t1 in c["keep"]) for c in d["clips"])
page = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Clip map · {H.escape(a.episode)}</title><link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>:root{{{Lt};box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{{Dk}}}}}:root[data-theme="dark"]{{{Dk}}}:root[data-theme="light"]{{{Lt}}}
html{{scroll-padding-top:env(safe-area-inset-top,0px)}}*,*::before,*::after{{box-sizing:inherit}}
body{{margin:0;background:var(--bg);color:var(--fg);font-family:Poppins,"Helvetica Neue",Arial,sans-serif;font-weight:300;line-height:1.55}}
main{{max-width:900px;margin:0 auto;padding:52px 20px 90px}}h1{{font-weight:500;font-size:clamp(28px,5vw,40px);margin:0 0 8px}}
.lede{{color:var(--mute);margin:0 0 30px;max-width:64ch}}.clip{{display:grid;grid-template-columns:150px 1fr;gap:26px;background:var(--card);border:1px solid var(--line);border-radius:22px;padding:22px;margin:18px 0}}
.clip:not(:has(figure)){{grid-template-columns:1fr}}figure{{margin:0;border-radius:14px;overflow:hidden;aspect-ratio:9/16;background:#000}}figure img{{width:100%;height:100%;object-fit:cover;display:block;max-width:100%}}
.meta{{display:flex;flex-wrap:wrap;gap:8px 14px;font-size:14px;color:var(--mute);align-items:center}}.n{{color:var(--fg);font-weight:600}}
.tier{{padding:2px 10px;border-radius:20px;font-weight:500;font-size:13px}}.tA{{background:#1f9d4a;color:#fff}}.tB{{background:var(--line);color:var(--fg)}}
h2{{font-weight:500;font-size:clamp(20px,3vw,25px);margin:8px 0 10px;line-height:1.3}}.hook{{margin:0 0 10px;font-weight:500}}.hook span,.rng{{color:var(--mute);font-weight:300}}
mark{{background:#ef7b00;color:#fff;padding:0 4px;border-radius:4px}}.hook span{{display:block;font-size:13px;text-transform:uppercase;letter-spacing:.08em}}.why{{margin:0 0 14px}}
.scores{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:6px 18px;margin-bottom:12px}}.sc{{display:flex;align-items:center;gap:8px;font-size:13px;color:var(--mute)}}
.sc span{{width:78px}}.sc i{{flex:1;height:6px;border-radius:3px;background:var(--line);overflow:hidden}}.sc b{{display:block;height:100%;background:var(--fg)}}.sc em{{font-style:normal;color:var(--fg);width:12px}}
.flag{{margin:6px 0;border-left:2px solid #e08a00;padding-left:10px;font-size:14px}}.rng{{font-size:14px;margin:8px 0}}
details summary{{cursor:pointer;font-size:14px;font-weight:500}}.tx{{font-size:15px;color:var(--mute)}}.tx em{{color:#e08a00;font-style:normal}}
.drop{{margin-top:36px;color:var(--mute)}}.drop h3{{color:var(--fg);font-weight:500}}.drop li{{margin:6px 0}}.drop b{{color:var(--fg);font-weight:500}}
@media (max-width:560px){{.clip{{grid-template-columns:96px 1fr;gap:16px;padding:16px}}}}</style></head><body><main>
<h1>{H.escape(a.episode)}</h1><p class="lede">{len(d["clips"])} proposed clips · {total:.0f}s total. Reply with the clip numbers to produce (e.g. "1, 3, 4"), and any range or hook changes by clip number.</p>
{"".join(cards)}{drop}</main></body></html>'''
open(a.out, "w").write(page); print(len(page) // 1024, "KB")
