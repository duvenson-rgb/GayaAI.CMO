---
name: "podcast-clipper"
description: Turns one long-form recording — a podcast, interview, livestream, webinar, talk, or a long WAV/MP3 — into several standalone short-form vertical clips (Reels, TikTok, Shorts), each edited with captions, hook text and motion graphics. Finds the moments that make sense with zero context, proposes a scored clip map, then runs a gated review (clip map → SRTs → storyboard → final render). Use this skill whenever the user uploads or links a long video or audio file and wants clips, highlights, shorts or "content" out of it, says "clip this", "podcast clipper", "cut this into shorts", "find the best moments", or mentions repurposing long-form content — even if they don't name the skill. For editing a single short raw clip, use short-form-video-edit instead.
---

# Podcast clipper

Takes a long recording and produces N standalone vertical clips (1080×1920), each one a complete idea a stranger can understand, save or share with no context from the rest of the episode. N is decided by quality, not quota.

It reuses the editing system of the short-form-video-edit skill (caption look, grades, SFX, storyboard, −14 LUFS, QA) and adds: long-file transcription, clip discovery, podcast layouts, and a data-driven overlay engine so every clip is configured with a small data file instead of hand-written HTML.

## The process

```
1. Intake                      → probe, overview sheet, speakers, style
2. Full transcript             → chunked, resumable
3. Clip map          [GATE 1: user picks which clips to produce]
4. SRT per clip      [GATE 2: user validates the text]
5. Storyboard        [GATE 3: user approves the visuals]
6. Render all approved clips + QA
7. Delivery                    → clips + post captions
```

Never skip a gate. Never render a final before its storyboard is approved. If the user says "go"/"continue" at a gate, that approves the current version; state the assumptions you proceed with. The gates exist because choosing the wrong moment, a wrong word in a caption (especially in Creole), and a graphic the user dislikes are all cheap to fix before rendering and expensive after.

Long jobs span many tool calls. Keep the user oriented with one short progress line when a step takes several calls (e.g. "Transcribing: 18 of 31 min done").

All commands are in `references/pipeline.md`. Read it before starting.

### Step 1 — Intake

1. `ffprobe` the upload. Note duration, video/audio-only, resolution, fps, channels.
2. Make an overview contact sheet (48 frames across the whole file, with timecodes). Identify: camera setup (wide two-shot, separate angles already switched, single guest, screen share), where each person sits and who is the host, burned-in text, logos.
3. For video, define a 9:16 **speaker box** per person (face ~1/3 from the top) and draw them on a frame to check. Audio-only input → `audio` layout (waveform + guest photo/initials).
4. Style: default `podcast-bold`. If the user attached a new reference video, register it first (see below). If they name a registered style, use it.
5. Ask nothing unless something blocks the work. Useful to know but assume if absent: speaker names and roles (use what the conversation reveals; otherwise "Host"/"Guest" and flag it), show name, brand accent color (123Viral → #EF7B00).

### Step 2 — Full transcript

Chunked with `scripts/transcribe_long.py` (split at quiet points, resumable, stops before the tool-call limit — rerun until ALL DONE, then merge). Model: `small` for discovery on long episodes, `medium` if ≤ ~15 min English. Produces `tr.json` (word timestamps) and `transcript.txt` (readable, timestamped).

### Step 3 — Clip map (Gate 1)

Read `references/clip_selection.md` and follow it: the standalone test, the dangling-reference check, clip types, the 5-part rubric (/25), tiers, length rules, micro-edits and the integrity rule.

1. Build `clips.json` with every clip that scores ≥ 15, best first. Each clip: keep ranges, title, on-screen hook, type, score, one-line "why it stands alone", draft post caption, flags (cold opens, heavy trims, uncertain words).
2. `clip_tools.py snap` then `clip_tools.py text` — reread every clip's exact words as a stranger. Rescore honestly.
3. Build the clip map page (`scripts/build_clipmap.py`, with thumbnails for video) and publish it as an artifact. Include notable dropped moments so the user can overrule.
4. In the reply, a compact list too (one line per clip: number, tier, duration, title, source time) so the user can answer without opening the page. Recommend which to produce (all Tier A by default).
5. Stop and wait. The user answers with clip numbers and any changes ("3: start at the question", "drop 5").

### Step 4 — SRT per clip (Gate 2)

1. Cut the approved clips (`clip_tools.py cut`) and retime their words (`clip_tools.py words`). If discovery used `small`, re-transcribe each cut clip with `medium` (prime it with names and terms from the episode).
2. Correct the text using, in order of trust: burned-in captions > user-supplied script > your language knowledge (Creole notes below) > raw ASR. Keep the speaker's actual words — fix spelling, not phrasing.
3. Draft cues with `srt_tools.py draft` (breaks at punctuation, 1–4 words per cue for podcast-bold). You may add `*highlight*` markup here or in the storyboard.
4. Deliver **both, for every clip**: the `.srt` files via `present_files`, AND the full SRT text of each clip pasted in the reply in code blocks, headed by clip number and title. Flag uncertain cues by clip and cue number ("2 · cue 11").
5. Tell the user they can reply in any form ("2 · cue 11: …", or paste an SRT back). If they change only words, keep the timestamps.
6. After edits: apply, paste the updated SRT(s) again in full, confirm they are now the source of truth. Captions must never deviate from the approved SRT.

With more than ~5 clips, run Gates 2–3 in waves of 3–4 clips so each message stays readable; say so.

### Step 5 — Storyboard (Gate 3)

One storyboard artifact for all clips in the wave, stills rendered from the real engine and real base video, so what is approved is exactly what renders.

1. Per clip, write `layout.json` (speaker segments: who is on screen when, split for exchanges/reactions, punch-ins on punchlines) and `clip.js` (hook, name tags, graphics, accent). Graphics only visualize what is actually said — no invented numbers.
2. Render base stills with `make_base.py --still` and overlay stills with `render_frames.py list`, composite them. 4–7 beats per clip: hook frame, each layout change, each graphic, the landing line.
3. `build_storyboard.py` with the multi-clip `clips` format → publish as artifact (republish the same artifact on revisions by passing its url).
4. In the reply: a short text summary per clip (beats, graphics, layout choices, SFX, hook text) and ask for feedback **by clip and beat number** ("1.3: …").
5. Once approved, start the full base-video renders for approved clips right away (they don't depend on further caption edits).

### Step 6 — Render + QA

Per clip: full base video → full overlay frames (resumable, static frames reused) → SFX → mix to −14 LUFS → encode. Run the QA checklist on each clip before delivering. Deliver clips as they finish if the batch is long, and say which are still rendering.

### Step 7 — Delivery

Present all final MP4s with `present_files`, plus a `posting.md` with, per clip: title, on-screen hook, post caption, suggested hashtags, source timestamps. Add one line: *"The chat preview shows every video in a wide box — on a phone / in Instagram it fills the screen vertically."* Offer the phone-frame preview (`scripts/build_phone_preview.py`) if useful.

## QA checklist (every clip, before delivery)

- Clip is still standalone after editing: watch the first 3 s as a stranger (first frames + first caption cues).
- Joins inside the clip: no half-words, no cut breaths, no pitch jumps (listen/look at each keep-range boundary).
- Captions match the approved SRT word for word (`srt_tools.py diff` prints OK).
- Caption transitions checked in motion at several cue boundaries (consecutive frames): no blank frame, no overlap, no flicker.
- Layout switches land on the cut frame; caption position follows (chest / seam / low).
- Nothing collides: captions vs cards vs name tags vs hook; nothing in the top ~250 px or bottom ~250 px except the header band hook; nothing under the right-edge buttons.
- Faces are inside the crop through the whole clip (people lean — check the 1 fps sheet).
- Loudness −14 LUFS ±0.5, true peak ≤ −1 dB, no clipping.
- File: 1080×1920, SAR 1:1, DAR 9:16, H.264 High + AAC 48 kHz, MP4, 30 fps.

## Haitian Creole content

Common for this user. ASR (Whisper `ht`) gets timing right and words wrong (phonetic French-ish spelling). Correct from context; flag every cue you are unsure of rather than guessing silently; ask for the script if a whole passage is unclear. Known reads: "sampli"→"sanble", "surmonte"→"surmonter", "kounmwante"→"kòmantè", "lo oumoun"→"lòt moun". Hooks, name-tag roles and card text in Creole too. Clip selection works the same; the standalone test is applied to the corrected Creole text, never to raw ASR.

## Registering a reference

When the user shares a reference clip (a clipped podcast they like, or any short-form edit), register it here so the skill improves:

1. Analyze: ffprobe; 1 fps contact sheet; 4–6 full-res frames; layout (single/split/other), caption font/size/position/case, highlight rules, hook/title treatment, name tags, graphics, cut rhythm, zooms, music/SFX, loudness (ebur128).
2. Write `references/styles/<name>.md` from `references/styles/_TEMPLATE.md`, mapping everything to what `engine_podcast.html` and `make_base.py` can do; note what would need engine changes.
3. Save a small contact sheet as `assets/refs/<name>_sheet.jpg`; add a row to the table below.
4. If the style needs engine changes, make them in `engine_podcast.html` (keep the data format backward compatible) and test with stills.
5. Repackage the skill (skill-creator's `package_skill.py`) and present the `.skill` file so the user can save the update. One line to the user that the reference was registered.

## Registered styles

| Style | File | Summary |
|---|---|---|
| podcast-bold (default) | `references/styles/podcast-bold.md` | Bold captions on the chest with one glowing keyword, glass hook headline, name tags, speaker-follow crops + stacked split, stat/list/quote/compare cards, dark cinematic grade. Audio-only variant with waveform. Engine: `assets/engine_podcast.html` |
| devinjatho | `references/styles/devinjatho.md` | Bold talking-head with bespoke UI-metaphor graphics — for a hero clip worth custom work. Engine: `assets/engine_bold.html` |
| thedankoe | `references/styles/thedankoe.md` | Minimal pure-black line diagrams, voice-over — good for audio-only philosophical clips. Engine: `assets/engine_minimal.html` |

## Environment notes

1 CPU, ~4 GB RAM. faster-whisper `small` int8 ≈ 4× realtime, `medium` ≈ 1.7×; `large-v3` runs out of memory — never use it. Background processes die between tool calls: run everything in the foreground, chunked and resumable, each call under ~280 s. Playwright Chromium at `/opt/pw-browsers/chromium-*/chrome-linux/chrome`. Sources wider than 1920 px are downscaled at cut time. See `references/pipeline.md` for timings.

## User context

The user (Duvenson, runs 123Viral) communicates briefly and expects full pipeline ownership. Content is often in Haitian Creole. He always wants to see and edit the caption text and the storyboard before the final render, and wants the full SRT text pasted in the chat as well as the file.
