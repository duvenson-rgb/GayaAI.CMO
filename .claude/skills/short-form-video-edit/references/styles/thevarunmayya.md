# Style: thevarunmayya (news / B-roll explainer)

Source: thevarunmayya_Dd4YFpdziV4.mp4 — 60.7 s, 720×1280, 29.97 fps, English, −14.2 LUFS, ~32 cuts (one every 1–2 s). Registered Sept 30 2026. Contact sheet: `assets/refs/thevarunmayya_sheet.jpg`.
**This style needs asset research** — see "Asset research" in SKILL.md and the rules below.

## Look
The host's voice runs over everything; the picture is mostly B-roll. Layouts (`scripts/news_compose.py`):
- `split` — B-roll top half, host bottom half (reframed on the head via faces.js). Used for the opening hook and returns to the host.
- `card` — landscape clip in a rounded 1000×562 card (radius 40) slightly above center, over a blurred (boxblur 40), darkened (−0.28) copy of itself. The signature look for launch footage.
- `full` — media fills the frame (vertical clips, strong photos); images get a slow Ken Burns zoom.
- `host` — host full screen (reactions, "I'm genuinely excited").
- `white` — plain white with a big black word or product graphic ("ALWAYS ON AGENTS").

## Typography (Montserrat)
- Caption pill: white 800, 46 px, on near-black #0b0b0c pill (radius 16, padding 10/24). 1–4 words per cue, a new cue every ~0.5–1 s. At the seam (y=960) on split beats, y=1400 elsewhere.
- Big word: 900, 150 px, letter-spacing −3; white with shadow over footage, black on white. Replaces the pill while shown.
- Headline card: white card, source initial badge + source name + date, 50 px 800 headline.
- Tag: red #e8202a "BREAKING" pill with pulsing dot, slides in from the left.

## Pacing
Cut every 1–2 s; never hold one B-roll longer than ~3 s. Open with a split + "Breaking news!" in the first second. Alternate B-roll types (clip, UI screenshot, product image, host) so no two neighbours look alike.

## Asset rules (mandatory)
- Only reusable sources: Pexels, Pixabay (free API keys → env PEXELS_API_KEY / PIXABAY_API_KEY), Openverse and Wikimedia Commons (CC0 / public domain / CC BY; CC BY-SA only with --allow-sa; never NC or ND), and links the user supplies (official press kits / newsrooms / his own screen recordings — mark the license he states).
- Never download news-agency photos (AP, Reuters, Getty), TV/broadcast clips, YouTube/TikTok/Instagram videos, or screenshots of articles.
- Headline cards carry **our own paraphrase** of the news plus source name and date — never copied article text. Direct quotes ≤ 15 words, attributed.
- Every used asset is marked `"used": true` in assets/candidates.json; deliver `credits.md` with the final video for the post caption. CC BY assets also get an on-screen `credit` event while visible.
- Real people: only licensed photos (e.g. Commons CC portraits); no invented quotes.

## Audio
Host voice at −14 LUFS; light whooshes on layout changes, a riser under the opening tag, pops on headline cards. No music unless supplied.

## Engine
`assets/engine_news.html` (captions.js from the SRT, beats.js from BEATS.json, events.js for big/tag/headline/credit) over `news_compose.py` output.
