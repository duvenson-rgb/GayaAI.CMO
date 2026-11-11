#!/usr/bin/env python3
"""Research + download reusable B-roll / images, with license and credit tracking.
  broll_search.py search "query" --kind image|video [--n 6] [--out assets] [--allow-sa]
  broll_search.py fetch URL --title "..." --source "OpenAI newsroom (press kit)" --license "press use" [--out assets]
  broll_search.py sheet [--out assets]        numbered contact sheet of all candidates -> assets/candidates.jpg
  broll_search.py credits [--out assets]      credits.md for the post caption (only assets marked used)
Sources: Openverse (CC images), Wikimedia Commons (images + video), Pexels / Pixabay if PEXELS_API_KEY / PIXABAY_API_KEY are set.
Only licenses that allow commercial use AND modification are kept: CC0, public domain, CC BY (and CC BY-SA with --allow-sa),
Pexels / Pixabay licenses. NC and ND are always excluded. Everything is logged in assets/candidates.json."""
import sys, os, json, re, argparse, subprocess, urllib.request, urllib.parse, hashlib
UA={"User-Agent":"short-form-video-edit/1.0 (content research; contact via 123Viral)"}
def get(url,headers=None,raw=False,tries=3):
    import time
    for k in range(tries):
        try:
            r=urllib.request.urlopen(urllib.request.Request(url,headers={**UA,**(headers or {})}),timeout=40); b=r.read()
            return b if raw else json.loads(b)
        except urllib.error.HTTPError as e:
            if e.code in (429,500,502,503) and k<tries-1: time.sleep(2+3*k); continue
            raise
def ok_license(s,allow_sa):
    s=(s or "").lower().replace("-"," ")
    if any(k in s for k in ("nc","nd","noncommercial","no deriv")) and "cc0" not in s: return False
    if "sa" in s.split() or "share alike" in s or "sharealike" in s: return allow_sa
    return any(k in s for k in ("cc0","public domain","pdm","cc by","pexels","pixabay","by "))
def openverse(q,n,allow_sa):
    d=get("https://api.openverse.org/v1/images/?"+urllib.parse.urlencode({"q":q,"page_size":n*2,"license_type":"commercial,modification","mature":"false"}))
    out=[]
    for r in d.get("results",[]):
        lic=f'{r.get("license","")} {r.get("license_version","")}'.strip()
        if r.get("license")=="by-sa" and not allow_sa: continue
        out.append({"kind":"image","title":r.get("title") or q,"creator":r.get("creator") or "unknown","source":f'Openverse / {r.get("source")}',
          "page":r.get("foreign_landing_url"),"url":r.get("url"),"license":"CC "+lic.upper() if r.get("license") not in ("cc0","pdm") else r.get("license").upper(),
          "license_url":r.get("license_url"),"w":r.get("width"),"h":r.get("height")})
    return out[:n]
def commons(q,kind,n,allow_sa):
    ft="filetype:video" if kind=="video" else "filetype:bitmap"
    d=get("https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode({"action":"query","format":"json","generator":"search","gsrsearch":f"{q} {ft}",
        "gsrnamespace":6,"gsrlimit":n*3,"prop":"imageinfo","iiprop":"url|extmetadata|mime|size","iiurlwidth":1280}))
    out=[]
    for p in (d.get("query",{}).get("pages",{}) or {}).values():
        ii=(p.get("imageinfo") or [{}])[0]; m=ii.get("extmetadata",{}); lic=m.get("LicenseShortName",{}).get("value","")
        if not ok_license(lic,allow_sa): continue
        creator=re.sub("<[^>]+>","",m.get("Artist",{}).get("value","unknown")).strip()[:80]
        url=ii.get("url") if kind=="video" else (ii.get("thumburl") or ii.get("url"))
        out.append({"kind":kind,"title":p["title"].replace("File:",""),"creator":creator,"source":"Wikimedia Commons","page":ii.get("descriptionurl"),
          "url":url,"license":lic,"license_url":m.get("LicenseUrl",{}).get("value",""),"w":ii.get("width"),"h":ii.get("height"),"duration":ii.get("duration")})
    return out[:n]
def pexels(q,kind,n):
    k=os.environ.get("PEXELS_API_KEY"); 
    if not k: return []
    if kind=="video":
        d=get("https://api.pexels.com/videos/search?"+urllib.parse.urlencode({"query":q,"per_page":n,"orientation":"landscape"}),{"Authorization":k})
        return [{"kind":"video","title":q,"creator":v["user"]["name"],"source":"Pexels","page":v["url"],"license":"Pexels License","license_url":"https://www.pexels.com/license/",
          "url":sorted([f for f in v["video_files"] if (f.get("width") or 0)<=1920],key=lambda f:-(f.get("width") or 0))[0]["link"],"w":v["width"],"h":v["height"],"duration":v["duration"]} for v in d.get("videos",[])]
    d=get("https://api.pexels.com/v1/search?"+urllib.parse.urlencode({"query":q,"per_page":n}),{"Authorization":k})
    return [{"kind":"image","title":p.get("alt") or q,"creator":p["photographer"],"source":"Pexels","page":p["url"],"license":"Pexels License",
      "license_url":"https://www.pexels.com/license/","url":p["src"]["large2x"],"w":p["width"],"h":p["height"]} for p in d.get("photos",[])]
def pixabay(q,kind,n):
    k=os.environ.get("PIXABAY_API_KEY")
    if not k: return []
    base="https://pixabay.com/api/videos/" if kind=="video" else "https://pixabay.com/api/"
    d=get(base+"?"+urllib.parse.urlencode({"key":k,"q":q,"per_page":max(3,n),"safesearch":"true"}))
    out=[]
    for h in d.get("hits",[]):
        url=(h["videos"].get("large") or h["videos"]["medium"])["url"] if kind=="video" else h.get("largeImageURL")
        out.append({"kind":kind,"title":h.get("tags") or q,"creator":h.get("user"),"source":"Pixabay","page":h.get("pageURL"),"license":"Pixabay Content License",
          "license_url":"https://pixabay.com/service/license-summary/","url":url,"w":h.get("imageWidth") or h.get("videos",{}).get("large",{}).get("width"),"duration":h.get("duration")})
    return out[:n]
def db_load(out):
    p=os.path.join(out,"candidates.json"); return json.load(open(p)) if os.path.exists(p) else []
def db_save(out,db): json.dump(db,open(os.path.join(out,"candidates.json"),"w"),indent=1,ensure_ascii=False)
def download(c,out):
    ext=os.path.splitext(urllib.parse.urlparse(c["url"]).path)[1].lower() or (".mp4" if c["kind"]=="video" else ".jpg")
    if c["kind"]=="video":  # stream only the first 20 s straight from the URL (some sources are hour-long); mp4, <=1920 wide, no audio
        fn=os.path.join(out,f'{c["id"]}.mp4')
        subprocess.run(["ffmpeg","-v","error","-y","-user_agent",UA["User-Agent"],"-t","20","-i",c["url"],"-t","20","-an","-vf","scale='min(1920,iw)':-2,fps=30",
                        "-c:v","libx264","-preset","veryfast","-crf","18",fn],check=True,timeout=180)
    else:
        fn=os.path.join(out,f'{c["id"]}{ext}'); open(fn,"wb").write(get(c["url"],raw=True))
    c["file"]=fn; return c
ap=argparse.ArgumentParser(); ap.add_argument("cmd"); ap.add_argument("arg",nargs="?"); ap.add_argument("--kind",default="image")
ap.add_argument("--n",type=int,default=6); ap.add_argument("--out",default="assets"); ap.add_argument("--allow-sa",action="store_true")
ap.add_argument("--title"); ap.add_argument("--source"); ap.add_argument("--license"); A=ap.parse_args()
os.makedirs(A.out,exist_ok=True); db=db_load(A.out)
if A.cmd=="search":
    found=[]
    for fn in (lambda: pexels(A.arg,A.kind,A.n), lambda: pixabay(A.arg,A.kind,A.n),
               lambda: openverse(A.arg,A.n,A.allow_sa) if A.kind=="image" else [], lambda: commons(A.arg,A.kind,A.n,A.allow_sa)):
        try: found+=fn()
        except Exception as e: print("source failed:",str(e)[:120])
    added=0
    for c in found:
        if not c.get("url") or any(x["url"]==c["url"] for x in db): continue
        c["id"]=f'a{len(db)+1:03d}'; c["query"]=A.arg; c["used"]=False
        try: download(c,A.out); db.append(c); added+=1; print(f'{c["id"]}  {c["kind"]:5} {c["source"]:28} {c["license"]:18} {c["title"][:60]}')
        except Exception as e: print("download failed:",c["url"][:80],str(e)[:80])
        if added>=A.n: break
    db_save(A.out,db); print(added,"added")
elif A.cmd=="fetch":
    kind="video" if re.search(r"\.(mp4|mov|webm|m4v)(\?|$)",A.arg,re.I) else "image"
    c={"id":f'a{len(db)+1:03d}',"kind":kind,"title":A.title or A.arg,"creator":"","source":A.source or "user-supplied","page":A.arg,"url":A.arg,
       "license":A.license or "user-supplied — user confirms rights","used":False}
    download(c,A.out); db.append(c); db_save(A.out,db); print(c["id"],c["file"])
elif A.cmd=="sheet":
    from PIL import Image, ImageDraw
    th=[]
    for c in db:
        f=c["file"]; im_path=f
        if c["kind"]=="video": im_path=f+".jpg"; subprocess.run(["ffmpeg","-v","error","-y","-ss","1","-i",f,"-frames:v","1",im_path])
        im=Image.open(im_path).convert("RGB"); im.thumbnail((320,320)); cv=Image.new("RGB",(320,360),"#111"); cv.paste(im,((320-im.width)//2,(320-im.height)//2))
        d=ImageDraw.Draw(cv); d.text((8,326),f'{c["id"]} {c["kind"]} · {c["license"][:18]}',fill="#fff"); th.append(cv)
    cols=5; rows=(len(th)+cols-1)//cols; S=Image.new("RGB",(cols*320,rows*360),"#000")
    for i,t in enumerate(th): S.paste(t,((i%cols)*320,(i//cols)*360))
    S.save(os.path.join(A.out,"candidates.jpg"),quality=85); print("sheet:",len(th))
elif A.cmd=="credits":
    L=["Credits (B-roll & images):"]+[f'- {c["title"][:70]} — {c.get("creator") or "unknown"} / {c["source"]} — {c["license"]} {c.get("page","")}' for c in db if c.get("used")]
    open(os.path.join(A.out,"credits.md"),"w").write("\n".join(L)+"\n"); print("\n".join(L))
