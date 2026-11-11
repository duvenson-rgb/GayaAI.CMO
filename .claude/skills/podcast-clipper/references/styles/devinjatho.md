# Style: devinjatho (bold talking-head)

Source: devinjatho_DbS2vcfyQxx.mp4 — 47.6 s, 720×1280, 30 fps, English. Registered on project "Pale devan kamera" (Haitian Creole, 60 s). Contact sheet: `assets/refs/devinjatho_sheet.jpg`.

## Look
- Talking head, medium shot, dark cinematic grade: lowered exposure, raised contrast, slightly desaturated, cool shadows / warm highlights, heavy vignette, extra black gradient over the bottom ~45%.
- For bright footage, the grade that worked: `eq=brightness=-0.05:contrast=1.12:saturation=0.85:gamma=0.94,colorbalance=rs=-0.05:bs=0.06:rh=0.04:bh=-0.03,vignette=PI/3.3`.
- Landscape source → 9:16 crop around the speaker (keep lead room on the side they look/gesture toward).

## Typography
- Captions: Montserrat 900, ALL CAPS, 114 px, line-height 0.96, letter-spacing −1 px, white, soft drop shadow. 1–4 words per caption, max 2 lines, balanced split, each line shrink-to-fit to 970 px.
- Position: centered on the chest just under the chin: y ≈ 1215 px on the wide shot, lowered with zoom (`y = 1215 + (zoom−1)·820`).
- Entrance: pop from scale 0.78 → 1 with ease-out-back over 0.16 s; whole caption at once (no word-by-word).
- Gold serif accent for "prestige" words: Cinzel 800, mixed case, gold gradient (#fff8d0 → #ffd75a → #c98a12) + gold glow.

## Color & highlights
One keyword per beat gets a neon glow: red #ff2b43 (fear, negation, loss, "not true"), green #46ff5e (success, overcoming, focus), blue #49b4ff (the mind, comments), gold serif (names, "popular", the topic phrase). Everything else white.

## Graphic vocabulary (all in `assets/engine_bold.html`)
- Glass cards under the caption (left 120, width 840, top ≈ 1395–1475, radius 34, rgba(18,19,24,.78), blur): ranking bars, level/progress bar with counter, profile card with verified badge + climbing follower count, poll with animated result bars, comments list, two-bar comparison.
- Floating icons near the head: mic badge, eyes that blink then close, thought bubble with avatar. Head-relative positions go through `mapPt()` so they follow zooms.
- Camera REC viewfinder: corner brackets, blinking red dot, running timecode, battery.
- Camera AF focus reticle locking onto the face.
- Full-screen black insert (~1 s) with a big Michroma timer/counter — the reference's "72:00:00" pattern-break moment.
- Pill badge ("RÈG #1") above the caption.

## Motion & pacing
- Hard cuts at sentence boundaries with alternating punch-in zooms (1.0 / 1.06–1.18 / 1.25–1.3 for punchlines); cut frames shared by the video pass and the overlay engine (`edl.json`).
- Graphics enter with slide-up + scale (0.35 s ease-out-back), exit with fade + drop.
- Never put a card on a tight punch-in (≥1.1): the caption drops low and collides.

## Audio
- SFX on every graphic: whooshes on card entries, pops on icons, dings on completions, sub impacts on punchlines, buzzer on "not true", beeps for camera UI, ticks under timers. Voice stays dominant.
- Master −14 LUFS. No music unless supplied.

## Adapting to our content
- Map abstract statements to a concrete UI metaphor (fear ranking, poll, comments, timer).
- Use real names the user gives (e.g. Cristiano Ronaldo) in captions and cards; avoid real photos — use initials avatars (CR7).
- Mock data (usernames, counts) must be flagged to the user in the storyboard.
