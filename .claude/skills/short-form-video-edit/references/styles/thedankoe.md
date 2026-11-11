# Style: thedankoe (minimal line diagrams)

Source: thedankoe_Dd6gGIJKgI1.mp4 — 28.5 s, 720×1280, 24 fps, English. Registered on project "Pri w peye pou disiplin" (Haitian Creole, 10 s). Contact sheet: `assets/refs/thedankoe_sheet.jpg`.

## Look
- Pure black background, **no footage** — voice-over only.
- Thin white vector diagrams (3 px strokes, round caps), one glowing white dot as the "protagonist" (13 px radius, radial glow ~5× radius).
- Diagram centered around y ≈ 1000 px; lots of empty space.

## Typography
- Captions: Poppins 400, **lowercase**, 50 px, white, centered at y ≈ 520 px (top third). One short phrase per caption.
- Entrance: fade + blur 6→0 px + 14 px rise over ~0.16–0.3 s. Exit: 0.1 s fade. Consecutive captions must not overlap (fade out before the next blurs in).
- Small labels: grey word + value in a dark rounded box with a faint border (e.g. `jou [02]`, timer `[05:00]`).

## Color & highlights
Monochrome only. Emphasis via brightness, glow intensity, dashed vs. solid strokes, and dim (0.1–0.35 alpha) ghost elements. No colored words.

## Graphic vocabulary (all in `assets/engine_minimal.html`)
- Dot + straight line to a vertical tick marker (a goal / direction).
- Loop circle with the dot orbiting and a counter flipping each lap (routine, repetition).
- Dashed wandering path that sags and falls short of the marker (lack of direction).
- Concentric ghost rings stacking (repetition piling up).
- Ripples from the dot (listening / hearing).
- Progress ring + fast-forward timer (time passing, reflection).
- Branching curve to a higher point with a dotted halo + underline marker (a better position / "it's real").
- Clusters of small circles around a central one (the crowd vs. you).

## Motion & pacing
- Continuous, eased morphs from one diagram to the next; no hard cuts. One idea per caption.
- Easing: cubic in-out for drawing, cubic out for reveals. Lines draw on; circles draw clockwise from 12 o'clock.
- Hold silences — a lone breathing dot carries a pause. End with a short hold (~0.8 s) and fade to black.

## Audio
Voice at −14 LUFS; very soft SFX (clicks on dot appearance, quiet ticks per orbit lap, low tone for failure, soft swell, soft chime at the end). No music unless supplied.

## Adapting to our content
- Build mirrored visuals for mirrored sentences (discipline: straight line + small loop of days; no discipline: wandering path + big loop of years).
- If the raw clip has burned-in captions, going pure graphics avoids showing two caption sets.
