# Style: podcast-bold (default for podcast clips)

Derived from devinjatho (bold talking-head), adapted to multi-speaker podcast footage and to a data-driven engine so several clips can be produced per episode without hand-coding graphics. Engine: `assets/engine_podcast.html`. Engine samples: `assets/refs/podcast-bold_sheet.jpg` (video layouts), `assets/refs/podcast-audio_sheet.jpg` (audio-only). Registered Sept 2026 as the podcast-clipper default.

## Look
- Video: speaker crops 9:16 with the face ~1/3 from the top; `bold` grade (lowered exposure, contrast up, slightly desaturated, cool shadows / warm highlights) + vignette; soft black gradient over the bottom ~45 % and top ~25 % so white text reads.
- Split: 400 px black header band + two stacked 1080×760 panels (host top, guest bottom), per-panel vignette.
- Audio-only: near-black radial gradient, guest photo or initials in a circle with an accent ring that pulses with the voice, 34-bar mirrored waveform in the accent color.

## Typography
- Captions: Montserrat 900, ALL CAPS (uppercased by `tocaps`), 110 px, line-height 0.96, letter-spacing −1 px, white with drop shadow; 1–4 words per cue, max 2 balanced lines, shrink-to-fit 970 px. Pop-in scale 0.78→1 ease-out-back 0.16 s, never a blank frame between cues.
- Caption position: chest (y 1215, lowered with zoom) on single shots; on the seam between panels in split; y 1330 in wide/audio.
- Hook headline: dark glass box, Montserrat 900 caps 62 px, show name as a small letterspaced overline with a red "live" dot. Top (y ≈ 300) on single shots, inside the header band on split. Default visible 0–~3.5 s; `t1:null` keeps it as a persistent title.
- Name tags: glass pill with an accent bar, name 38 px 800 + role 26 px; first time each person speaks.

## Color & highlights
- One accent per episode (`CLIP.accent`, default #46ff5e green; use the show's brand color if it has one — 123Viral orange #EF7B00). `*word*` → accent glow.
- Semantic overrides as in devinjatho: red (fear, loss, "not", mistakes), green (success, the fix), blue (mind, ideas), gold serif (names, prestige). One highlighted word or phrase per cue at most, and not on every cue — roughly one cue in three.

## Graphic vocabulary (data-driven, `CLIP.graphics`)
stat (count-up number), list (items tick in on cue), quote (pull quote), compare (two bars), badge (pill above the caption: "RULE #1", "THE FIX"), slam (full-screen pattern break). 1–4 graphics per 60 s clip — podcasts carry on the speaker's face; graphics mark the numbers, lists and the one line worth screenshotting.

## Motion & pacing
- Cuts follow the speaker at sentence boundaries; split for fast exchanges and reactions; punch-in 1.12–1.2 on the punchline; segments ≥ 1.5 s.
- Micro-edits tighten pauses to ~0.25 s (cut in `keep` ranges, never with jump-zooms hiding meaning changes).
- No end fade by default (clips loop better with a hard end on the landing line).

## Audio
Voice dominant, −14 LUFS, true peak ≤ −1 dB. Light SFX: whoosh on the hook and on layout changes, pop on cards, ding when a stat lands, short impact on the punchline. No music unless supplied.

## Adapting to our content
- Creole clips: hook, cards and name tag roles in Creole; captions from the approved Creole SRT.
- Mock data in cards (numbers the speaker did not say) is not allowed — cards only visualize what is said.
