# Pipeline commands

Skill at `$S` (e.g. `/mnt/skills/user/podcast-clipper`), work dir `/home/claude/job`. Each clip gets its own folder `job/clip_NN/`.

## Setup (once per session, foreground)

```bash
pip install faster-whisper --break-system-packages -q
S=/mnt/skills/user/podcast-clipper; mkdir -p /home/claude/job && cd /home/claude/job
```

## Time budget (1 CPU)

| Step | Speed | 10-min episode | 60-min episode |
|---|---|---|---|
| Transcribe, `small` | ~4 s per 15 s of audio (≈4× realtime) | ~3 min (1–2 calls) | ~15 min (4–5 calls) |
| Transcribe, `medium` | ≈1.7× realtime | ~6 min | too slow — use `small`, then `medium` on clips only |
| Base video per clip (1080p source) | ~2.5 s per s of clip | 60 s clip ≈ 2.5 min | same |
| Overlay frames (with reuse) | ~0.1 s per frame | 60 s clip ≈ 3 min | same |

Every command must finish in one tool call (< ~280 s). Everything here is resumable or per-clip, so re-run and continue.

## 1. Intake

```bash
ffprobe -v error -show_entries format=duration:stream=codec_type,codec_name,width,height,r_frame_rate,channels -of compact EP.mp4
# overview sheet: one frame every N s so it fits one 8x6 sheet  (N = duration/48)
ffmpeg -v error -y -i EP.mp4 -vf "fps=1/N,scale=320:-1,drawtext=text='%{pts\:hms}':x=6:y=6:fontsize=16:fontcolor=yellow,tile=8x6" -frames:v 1 overview.jpg
# full-res frames to place speaker boxes
ffmpeg -v error -y -ss T -i EP.mp4 -frames:v 1 frame_T.jpg
```

From the overview, note: camera setup (one wide shot / two-shot / separate angles already switched / screen recording), where each person sits, burned-in text, logo bugs, black frames.

**Speaker boxes** (for the single-speaker crop): for each person, a 9:16 box in source pixels with the face about 1/3 from the top of the box and the shoulders inside. Draw them on a frame to check:

```bash
ffmpeg -v error -y -i frame_T.jpg -vf "drawbox=x=259:y=40:w=562:h=1000:c=orange:t=6,drawbox=x=1099:y=40:w=562:h=1000:c=cyan:t=6" boxes_check.jpg
```

Audio-only input (WAV/MP3): no boxes; layout is `audio`.

## 2. Full transcription (long, chunked)

```bash
ffmpeg -v error -y -i EP.mp4 -ac 1 -ar 16000 a16.wav
python3 $S/scripts/transcribe_long.py split a16.wav tl --chunk 120
python3 $S/scripts/transcribe_long.py run tl --lang en --model small     # repeat until it prints ALL DONE
python3 $S/scripts/transcribe_long.py merge tl tr.json transcript.txt
```

`--lang ht` for Haitian Creole (expect phonetic French-ish spelling; timing is fine, words are not — see the Creole notes in SKILL.md). Episode ≤ ~15 min in English: `--model medium` is affordable and saves the re-transcription later.

## 3. Clip discovery → clips.json → clip map (Gate 1)

Method and rubric: `references/clip_selection.md`. Then:

```bash
python3 $S/scripts/clip_tools.py snap tr.json clips.json        # tighten every keep range to word boundaries
python3 $S/scripts/clip_tools.py text tr.json clips.json        # read each clip as a stranger would
# thumbnails (video): a frame at each clip's first keep range start + 1 s
ffmpeg -v error -y -ss T -i EP.mp4 -frames:v 1 -vf "crop=ih*9/16:ih,scale=360:-1" thumbs/clip_01.jpg
python3 $S/scripts/build_clipmap.py clips.json tr.json clipmap.html --thumbs thumbs --episode "Title" --dropped dropped.json
```

Publish `clipmap.html` with the Artifact tool. After the user picks, remove unpicked clips from clips.json (keep a copy) or pass `--ids`.

## 4. Cut + per-clip SRT (Gate 2)

```bash
python3 $S/scripts/clip_tools.py cut clips.json clips --ids 1,3,4          # clips/clip_01.mp4 (or .wav)
python3 $S/scripts/clip_tools.py words tr.json clips.json clips --ids 1,3,4 # clips/clip_01_tr.json, clip-local time
```

If discovery used `small`, re-transcribe each cut clip with medium for caption accuracy (60 s clip ≈ 35 s):

```bash
ffmpeg -v error -y -i clips/clip_01.mp4 -ac 1 -ar 16000 clips/c01_16k.wav
python3 $S/scripts/transcribe.py clips/c01_16k.wav clips/clip_01_tr.json --lang en --model medium --prompt "names/terms from the episode"
```

Then per clip:

```bash
python3 $S/scripts/srt_tools.py draft clips/clip_01_tr.json clip_01/draft.srt --max-words 4   # hand-correct the text
python3 $S/scripts/srt_tools.py show clip_01/clip_01.srt                                         # paste in the reply
```

Highlight markup (optional, also allowed in the approved SRT): `*word*` → accent color, `*two words*|red` → forced color (red, green, blue, gold).

## 5. Base video per clip (footage layouts)

`clip_01/layout.json`:

```json
{"grade": "bold",
 "boxes": {"A": {"x":259,"y":40,"w":562,"h":1000}, "B": {"x":1099,"y":40,"w":562,"h":1000}},
 "split": {"top": "A", "bottom": "B", "band": 400},
 "segments": [{"t0":0,"t1":4.6,"mode":"A"}, {"t0":4.6,"t1":16.4,"mode":"B"},
              {"t0":16.4,"t1":20.0,"mode":"split"}, {"t0":20.0,"mode":"B","z":1.18}]}
```

Modes: a box name (single-speaker 9:16 crop), `split` (header band + two stacked panels), `wide` (whole frame on a blurred fill — for moments where both people react, or screen shares). `z` = punch-in 1.0–1.3 (face stays at the same height). Grades: `bold` (dark cinematic), `clean` (light touch), `none`, or a raw ffmpeg filter chain.

Segment rules: cut to whoever is speaking at sentence boundaries; host question → host box (or split); use split for fast back-and-forth and for reactions; punch in on punchlines; keep each segment ≥ ~1.5 s.

```bash
cd clip_01
python3 $S/scripts/make_base.py ../clips/clip_01.mp4 layout.json base.mp4 edl.js --still 1.2,6.5,17.5   # storyboard stills only (fast)
python3 $S/scripts/make_base.py ../clips/clip_01.mp4 layout.json base.mp4 edl.js                        # full base video
```

## 6. Overlay engine per clip

```bash
cp $S/assets/engine_podcast.html engine.html && ln -sfn $S/assets/fonts fonts
python3 $S/scripts/srt_tools.py tocaps clip_01.srt caps.js                # approved SRT -> caption data
python3 $S/scripts/clip_tools.py env ../clips/clip_01.wav env.js          # audio layout only (waveform)
# write clip.js (schema at the top of engine_podcast.html): hook, names, graphics, accent, dur
cat caps.js edl.js clip.js > data.js                                      # audio: cat caps.js env.js clip.js
python3 $S/scripts/srt_tools.py diff clip_01.srt caps.js                  # must print OK
```

Stills for the storyboard (video layouts composite overlay on the base still):

```bash
python3 $S/scripts/render_frames.py --html engine.html --out ov --alpha list 1.2,6.5,17.5
ffmpeg -v error -y -i base_01.20.jpg -i ov/s01.20.png -filter_complex overlay -q:v 3 st_01.20.jpg
# audio layout: frames are opaque, render straight to JPEG
python3 $S/scripts/render_frames.py --html engine.html --out st --jpeg list 0.6,6.0,13.5
```

Graphic placement is automatic: on a normal single shot a card sits above the bottom safe zone and the caption rides up above it; on `split`, on punch-ins ≥ 1.1, or with `insert:true` the frame dims and the card centers with the caption below it; `slam` is a full-screen pattern break; in the audio layout cards replace the waveform. Name tags hide while a card is up.

Full frames (resumable; static frames are hard-linked via `stateKey`, typically 50–65 % reuse):

```bash
python3 $S/scripts/render_frames.py --html engine.html --out frames --alpha range 0 N     # video layouts
python3 $S/scripts/render_frames.py --html engine.html --out frames range 0 N             # audio layout (opaque)
```

N = ceil(duration × 30). If a call might exceed ~280 s, split the range (0 900, then 900 N).

Custom "hero" clip with bespoke graphics beyond the data vocabulary: start from `assets/engine_bold.html` (devinjatho) or `assets/engine_minimal.html` (thedankoe) as in the short-form-video-edit skill.

## 7. Audio

```bash
python3 $S/scripts/sfx.py sfx.json sfx.wav DUR     # [[t,"name",dB],...] from the storyboard sound column
ffmpeg -v error -y -i ../clips/clip_01.mp4 -i sfx.wav -filter_complex "[0:a]aresample=48000,highpass=f=70,\
acompressor=threshold=-20dB:ratio=2.5:attack=5:release=80,apad=whole_dur=DUR[v];[v][1:a]amix=inputs=2:normalize=0:duration=longest,atrim=0:DUR[m]" \
-map "[m]" -ar 48000 pre.wav
ffmpeg -hide_banner -i pre.wav -af ebur128 -f null - 2>&1 | grep -A3 Summary | grep " I:"     # gain = -14 - I
ffmpeg -v error -y -i pre.wav -af "volume=GAINdB,alimiter=limit=0.85:attack=3:release=50:level=disabled" mix.wav
```

Podcast audio is usually already compressed; if it sounds squashed, drop the acompressor. Noisy rooms: add `afftdn=nf=-25` before the compressor.

## 8. Final encode

Video layouts:
```bash
ffmpeg -v error -y -i base.mp4 -framerate 30 -i frames/%05d.png -i mix.wav \
 -filter_complex "[0:v][1:v]overlay=format=auto:shortest=1,setsar=1,format=yuv420p[v]" -map "[v]" -map 2:a \
 -c:v libx264 -preset faster -crf 18 -profile:v high -c:a aac -b:a 192k -ar 48000 -movflags +faststart -shortest ../out/clip_01.mp4
```

Audio layout:
```bash
ffmpeg -v error -y -framerate 30 -i frames/%05d.png -i mix.wav -vf "setsar=1,format=yuv420p" \
 -c:v libx264 -preset faster -crf 18 -tune animation -profile:v high -c:a aac -b:a 192k -ar 48000 -movflags +faststart -shortest ../out/clip_01.mp4
```

## QA helpers

```bash
ffmpeg -v error -y -i OUT.mp4 -vf "fps=1,scale=180:-1,tile=10x6" -frames:v 1 qa_sheet.jpg
ffmpeg -v error -y -i OUT.mp4 -vf "select='between(n,A,A+5)+between(n,B,B+5)',scale=240:-1,tile=12x1" -vsync 0 -frames:v 1 qa_cuts.jpg
ffprobe -v error -select_streams v -show_entries stream=width,height,sample_aspect_ratio,display_aspect_ratio -of compact OUT.mp4
ffmpeg -hide_banner -i OUT.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -A12 Summary
```

## Instagram Reels spec (verified Sept 2026)

1080×1920, 9:16, MP4, H.264, AAC ≥128 kbps, 30 fps, ≤ 3 min in-app. Safe zone: avoid top ~250 px and bottom ~250 px, keep clear of the right-edge buttons. Feed preview crops to 4:5, profile grid to 3:4 or 1:1 — keep key content centered. Instagram normalizes to about −14 LUFS.
