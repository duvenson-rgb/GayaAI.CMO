# Pipeline commands

All paths assume the skill is at `$S` (e.g. `/mnt/skills/user/short-form-video-edit`) and the work dir is `/home/claude/job`.

## Setup (once per session)

```bash
pip install faster-whisper --break-system-packages -q   # foreground; background installs get killed
mkdir -p /home/claude/job/fonts && cp $S/assets/fonts/* /home/claude/job/fonts/
CHROME=$(ls -d /opt/pw-browsers/chromium-*/chrome-linux/chrome | head -1)
```

## Intake

```bash
ffprobe -v error -show_entries format=duration:stream=codec_type,codec_name,width,height,r_frame_rate -of compact IN.mp4
ffmpeg -v error -y -i IN.mp4 -vf "fps=1/3,scale=320:-1,tile=6x5" -frames:v 1 sheet.jpg
```

Burned-in captions: find the text band on the contact sheet, then read it over time:

```bash
ffmpeg -v error -y -i IN.mp4 -vf "fps=4,crop=W:H:X:Y,scale=380:-1,drawtext=text='%{pts\:flt}':x=4:y=4:fontsize=13:fontcolor=yellow,tile=4x11" -frames:v 1 caps.jpg
```

## Transcription

```bash
ffmpeg -v error -y -i IN.mp4 -ac 1 -ar 16000 a16.wav
python3 $S/scripts/transcribe.py a16.wav tr.json --lang ht            # medium, word timestamps
python3 $S/scripts/srt_tools.py draft tr.json draft.srt --max-words 4 # then hand-correct the text
```

Whisper Creole output is phonetic French-ish spelling; timing is good, spelling is not. Useful reads seen so far: "sampli"→"sanble", "surmonte"→"surmonter", "kounmwante"→"kòmantè", "lo oumoun"→"lòt moun", "pè kè si anoun nal do"→"Cristiano Ronaldo". A priming `--prompt` with correct Creole helps spelling slightly; do not prime with guessed content.

Approved SRT → caption data for the engine:

```bash
python3 $S/scripts/srt_tools.py tojs approved.srt captions.js   # window.CUES=[[t0,t1,"text"],...]
```

Highlight markup in the SRT is optional: `*word*` → style keyword chosen in the storyboard; `*word*|red` forces a color.

## Base video (footage styles)

Crop 16:9 → 9:16 around the speaker, zoom per segment with zoompan, grade. `zexpr` is a nested `if(lt(in,FRAME),Z,…)` built from the EDL (cut frames + zoom per segment); save the EDL as `edl.json` for the overlay engine too.

```bash
ffmpeg -v error -y -i IN.mp4 -an -filter_complex "[0:v]crop=608:1080:X0:0,scale=1216:2160:flags=lanczos,\
zoompan=z='$ZEXPR':x='max(0,min(iw-iw/zoom,iw*0.47-iw/zoom/2))':y='max(0,min(ih-ih/zoom,ih*0.36-ih/zoom/2))':d=1:s=1080x1920:fps=30,\
eq=brightness=-0.05:contrast=1.12:saturation=0.85:gamma=0.94,colorbalance=rs=-0.05:bs=0.06:rh=0.04:bh=-0.03,vignette=PI/3.3,format=yuv420p[v]" \
-map "[v]" -c:v libx264 -preset veryfast -crf 15 base.mp4
```

60 s of 1080p HEVC → ~4 min on 1 CPU. For 4K sources add `scale=1920:-2` first.

## Overlay / animation frames

```bash
python3 $S/scripts/render_frames.py --html engine.html --out frames range 0 900      # resumable, ≤280 s per call
python3 $S/scripts/render_frames.py --html engine.html --out stills --jpeg list 1.2,2.2,5.0
```

- Transparent overlay (bold style): PNG with `--alpha`. Opaque graphics (minimal style): PNG without alpha.
- Frame reuse is opt-in: if an engine defines `window.stateKey(t)` (a string that is identical whenever the frame is identical), repeated frames are hard-linked instead of re-rendered. Neither bundled engine defines it yet — add it when a style has long static holds.

## Face safety (split screen instead of covering the face)

```bash
python3 $S/scripts/face_track.py base.mp4 faces.js            # padded head box per 0.2 s
python3 $S/scripts/plan_layout.py --html engine.html plan.json # which windows split / which captions moved
python3 $S/scripts/split_composite.py base.mp4 frames plan.json mix.wav OUT.mp4
```

Only `engine_brand.html` implements `planLayout()` so far; port `faceAt`/`rectOf`/`planLayout` and the `#panel`/`#ov`/`#capL` layers to another engine to give it the same rule.

## B-roll research and news composition

```bash
export PEXELS_API_KEY=...  PIXABAY_API_KEY=...        # optional, free; much better stock video
python3 $S/scripts/broll_search.py search "electric car factory" --kind video --n 4 --out assets
python3 $S/scripts/broll_search.py search "smartphone app screen" --kind image --n 4 --out assets
python3 $S/scripts/broll_search.py fetch https://example.com/press/launch.mp4 --source "Company newsroom" --license "press use" --out assets
python3 $S/scripts/broll_search.py sheet --out assets      # numbered candidates.jpg for curation + storyboard
python3 $S/scripts/news_compose.py BEATS.json base.mp4     # split / card / full / host / white per beat
python3 $S/scripts/broll_search.py credits --out assets    # after marking "used": true
```

Commons full-text search is noisy (a "server room" video query returned White House events) — always curate visually. Videos are streamed (first 20 s only), so hour-long files are fine.

## Audio

```bash
ffmpeg -v error -y -i IN.mp4 -i sfx.wav -filter_complex "[0:a]aresample=48000,highpass=f=70,\
acompressor=threshold=-20dB:ratio=2.5:attack=5:release=80,apad=whole_dur=DUR[v];[v][1:a]amix=inputs=2:normalize=0:duration=longest,atrim=0:DUR[m]" \
-map "[m]" -ar 48000 pre.wav
ffmpeg -hide_banner -i pre.wav -af ebur128 -f null - 2>&1 | grep -A3 Summary | grep " I:"   # read I, compute gain = -14 - I
ffmpeg -v error -y -i pre.wav -af "volume=GAINdB,alimiter=limit=0.85:attack=3:release=50:level=disabled" mix.wav
```

## Final encode

Overlay on footage:
```bash
ffmpeg -v error -y -i base.mp4 -framerate 30 -i frames/%05d.png -i mix.wav \
 -filter_complex "[0:v][1:v]overlay=format=auto:shortest=1,setsar=1,format=yuv420p[v]" -map "[v]" -map 2:a \
 -c:v libx264 -preset faster -crf 18 -profile:v high -c:a aac -b:a 192k -ar 48000 -movflags +faststart -shortest OUT.mp4
```

Pure graphics:
```bash
ffmpeg -v error -y -framerate 30 -i frames/%05d.png -i mix.wav -vf "setsar=1,format=yuv420p" \
 -c:v libx264 -preset slow -crf 16 -tune animation -profile:v high -c:a aac -b:a 192k -ar 48000 -movflags +faststart -shortest OUT.mp4
```

## QA helpers

```bash
ffmpeg -v error -y -i OUT.mp4 -vf "fps=1,scale=180:-1,tile=10x6" -frames:v 1 qa_sheet.jpg
ffmpeg -v error -y -i OUT.mp4 -vf "select='between(n,A,A+5)+between(n,B,B+5)',scale=240:-1,tile=12x1" -vsync 0 -frames:v 1 qa_cuts.jpg
ffprobe -v error -select_streams v -show_entries stream=width,height,sample_aspect_ratio,display_aspect_ratio -of compact OUT.mp4
```

## Instagram Reels spec (verified Sept 2026)

1080×1920, 9:16, MP4, H.264, AAC ≥128 kbps, 30 fps, ≤ 3 min in-app. Safe zone: avoid top ~250 px and bottom ~250 px, keep clear of the right-edge buttons. Feed preview crops to 4:5, profile grid to 3:4 or 1:1 — keep key content centered. Instagram normalizes to about −14 LUFS.
