---
name: "short-form-video-edit"
description: End-to-end editing of short-form vertical videos (Instagram Reels, TikTok, YouTube Shorts) from a raw clip and a style reference, using a gated review process — SRT caption review, visual storyboard approval, then final render. Use this skill whenever the user uploads a raw video to be edited, asks to edit a video "in the style of" another video, sends a reference/example video, asks for captions or an SRT for a video, mentions Reels/TikTok/Shorts editing, motion graphics, or Haitian Creole (Kreyòl) video content — even if they don't say "skill" or name the process. Also use it whenever the user shares a new reference video, to register it as a style preset.
---

# Short-form video edit

Edits a raw talking video into a platform-ready vertical video (1080×1920, 9:16) in the style of a reference, through five steps with two approval gates. The gates exist because accuracy problems (especially Creole captions) and taste problems (graphics) are cheap to fix before rendering and expensive after.

## The process

```
1. Raw file (+ optional reference)          → Claude: probe, register reference if new
2. SRT for review          [GATE 1: user validates the text]
3. Storyboard for feedback [GATE 2: user approves the visuals]
4. Final edit              (only after approval)
5. Delivery + QA notes
```

Never skip a gate. Never render the final before the storyboard is approved. If the user says "continue" or "go" at a gate, treat that as approval of the current version and state which assumptions you are proceeding with.

### Step 1 — Intake (same turn as step 2)

1. `ffprobe` every upload (duration, resolution, fps, rotation, codec).
2. Identify the style:
   - New reference video attached → **register it** (see "Registering a reference" below) before doing anything else with it.
   - No reference → ask which registered style to use, or default to the last one used. List registered styles from `references/styles/`.
3. Make a contact sheet of the raw clip. **Look for burned-in captions** — if the raw clip already has text on screen, read it (crop the caption band, sample at 3–4 fps, see `references/pipeline.md`). Burned-in text is ground truth and beats ASR, especially for Creole.

### Step 2 — SRT for review (Gate 1)

1. Transcribe with `scripts/transcribe.py` (faster-whisper **medium**, int8, word timestamps). Do not try large-v3: it runs out of memory on this machine. For Haitian Creole use `--lang ht`.
2. Correct the text using, in order of trust: burned-in captions > user-supplied script > your Creole knowledge > raw ASR.
3. Split into cues with `scripts/srt_tools.py draft`. **One cue = one on-screen caption**, sized for the chosen style (bold style: 1–4 words; minimal style: one short phrase). Timings come from word timestamps.
4. Deliver it in two forms, always both:
   - the `.srt` file via `present_files`, AND
   - **the full SRT text pasted in the reply in a code block**, so the user can read and edit it without opening anything.
5. Flag uncertain lines explicitly by cue number (e.g. "cue 8 is my best guess — the audio is unclear").
6. Tell the user how to give changes: any form works — "cue 8: …", or paste the whole SRT back. If they change only words, keep the timestamps.
7. Ask at most one decision question here (e.g. footage vs. pure graphics). Then stop and wait.

After the user edits: apply the changes, **paste the updated SRT again in full**, and confirm it is now the source of truth. Captions must never deviate from the approved SRT.

### Step 2b — Asset research (styles that need B-roll, e.g. thevarunmayya)

After the SRT is approved, before the storyboard:
1. For each beat, decide what the viewer should see (product, place, person, concept) and write 1–3 search queries. For current news, first confirm the facts with web search so the visuals match what actually happened.
2. Ask the user once for official links (press kit, launch video file, newsroom images) — they are the best B-roll for news. Fetch them with `broll_search.py fetch`.
3. Search reusable libraries with `scripts/broll_search.py search` (Pexels/Pixabay if keys are set, Openverse, Wikimedia Commons). Look at every candidate (`broll_search.py sheet`) and keep only relevant, good-looking ones — relevance is judged by looking, not by the search ranking.
4. Assign assets to beats in BEATS.json. Put the numbered candidate sheet and each asset's source + license in the storyboard, so the user can swap by ID ("beat 3: use a012").
5. Follow the style's asset rules (licenses, no news-agency or broadcast footage, paraphrased headlines, credits).

### Step 3 — Storyboard (Gate 2)

Build the real animation engine first (from the style's template in `assets/`), then render stills from it. Stills from the actual engine mean the approved storyboard is exactly what the final looks like.

1. Render the base video in the same turn if the style uses footage (crop/grade/zooms do not depend on caption text) — saves time at step 4.
2. Plan beats: for each beat — number, timecode, caption, what animates, which words are highlighted, zoom level (if footage), sound effect.
3. Render one still per beat with `scripts/render_frames.py list …`. For styles with a face-safety rule, run `face_track.py` + `plan_layout.py` first and mark split-screen beats in the storyboard.
4. Build the storyboard page with `scripts/build_storyboard.py` and **publish it as an artifact** (HTML, stills embedded as data URIs).
5. In the reply, also give a short text summary of the beats (so feedback is possible even if the page does not render), state the global choices (length, audio, music, format), and ask for feedback **by beat number**.
6. Apply feedback, republish the same artifact (pass its url), repeat until approved.

### Step 4 — Final edit

1. Render all frames (`scripts/render_frames.py range 0 N`), in chunks that finish in under ~280 s per tool call — background processes are killed between calls, so everything runs in the foreground and must be resumable (the script skips existing frames).
2. Build SFX with `scripts/sfx.py` from the storyboard's sound column.
3. Mix: voice (highpass 70 Hz, light compression) + SFX → gain + limiter to **−14 LUFS**, true peak ≤ −1 dB. Measure with `ebur128`.
4. Composite/encode: H.264 High, yuv420p, 30 fps, AAC 192 kbps 48 kHz, `setsar=1`, `+faststart`.
5. Run the QA checklist below before presenting.
6. B-roll styles: mark used assets in candidates.json and deliver `credits.md` (`broll_search.py credits`) with the video, for the post caption.

### Step 5 — Delivery

Present the file. Always add one line: *"The chat preview shows every video in a wide box — on a phone / in Instagram it fills the screen vertically."* (A black-background video pillarboxed in the chat player looks horizontal; this confused the user once.) If needed, offer the phone-frame preview page (`scripts/build_phone_preview.py`).

## QA checklist (run before every final delivery)

- Captions match the approved SRT word-for-word (diff them).
- Caption transitions checked **in motion** (sample consecutive frames at cue boundaries): no two captions overlapping, no flicker.
- Caption position changes land on the exact cut frame when zoom changes (known failure point).
- No caption line runs off-screen: fonts are preloaded before measuring (lazy-loaded fonts measure too narrow), lines use `white-space:nowrap` + shrink-to-fit measured with `offsetWidth` (not `getBoundingClientRect`, which includes pop-in transforms).
- Cards/graphics never collide with captions on punched-in shots.
- Face safety (personalbrandlaunch style, and any style where the user asks): no animation overlaps the face box from `face_track.py`; every split window shows the full head in the bottom half.
- Safe zones for Reels: keep text out of the top ~250 px and bottom ~250 px (more at the bottom on bold styles), and away from the right-edge buttons.
- Loudness −14 LUFS ±0.5, no clipping.
- File: 1080×1920, SAR 1:1, DAR 9:16, H.264 + AAC, MP4.

## Registering a reference

Whenever the user shares a reference video — even mid-project — register it so the skill improves over time:

1. Analyze it: ffprobe; 1 fps contact sheet; 2 fps sheets of sections; 4–6 full-res frames of typical moments; scene-cut times; loudness (ebur128); presence of music.
2. Write `references/styles/<creator-or-name>.md` using `references/styles/_TEMPLATE.md`: look, typography (font, size in px at 1080×1920, case, position), color and highlight rules, graphic vocabulary, motion and transitions, pacing, audio, footage usage, and how it was adapted to Creole content.
3. Save a small contact sheet as `assets/refs/<name>_sheet.jpg`. Apply any user overrides (e.g. brand colors) in the style file and engine, and state them as rules at the top of the style file.
4. Add the style to the table below.
5. Repackage the skill (`python -m scripts.package_skill` from the skill-creator) and present the new `.skill` file so the user can save the update. Tell the user in one line that the reference was registered.

## Registered styles

| Style | File | Summary |
|---|---|---|
| devinjatho | `references/styles/devinjatho.md` | Bold talking-head: dark moody grade, heavy all-caps captions on the chest with glowing keywords, stat/UI cards, punch-in zooms, full-screen black inserts, busy SFX. Engine: `assets/engine_bold.html` |
| thedankoe | `references/styles/thedankoe.md` | Minimal: pure black, no footage, voice-over, thin white line diagrams with one glowing dot, small lowercase captions in the top third, soft SFX. Engine: `assets/engine_minimal.html` |
| personalbrandlaunch | `references/styles/personalbrandlaunch.md` | Brand explainer in the user's teal #0abbc2 (never the reference lime): natural footage, "sandwich" captions (small white words + huge teal keyword), full-screen teal inserts with white doc cards and pills, typing doc, color-coded structure timeline, comment-card CTA. Engine: `assets/engine_brand.html` (data-driven EVENTS) |
| thevarunmayya | `references/styles/thevarunmayya.md` | News / B-roll explainer: host voice over researched B-roll cut every 1–2 s; split (B-roll top, host bottom), rounded card over blurred copy, full-bleed images, white big-word screens; black caption pills; BREAKING tag and headline cards. Needs asset research. Composer: `scripts/news_compose.py`, engine: `assets/engine_news.html` |

## Environment notes

1 CPU, ~4 GB RAM. faster-whisper medium int8 ≈ 1.7× realtime; large-v3 OOMs. Background processes die between tool calls — run in the foreground, chunk long jobs, make them resumable. Playwright Chromium lives at `/opt/pw-browsers/chromium-*/chrome-linux/chrome`. Overlay frames render at ~0.17–0.25 s each. See `references/pipeline.md` for all commands.

## User context

The user (Duvenson, runs 123Viral) communicates briefly and expects full pipeline ownership. Content is often in Haitian Creole. He wants to always see and edit the caption text and the storyboard before the final render.
