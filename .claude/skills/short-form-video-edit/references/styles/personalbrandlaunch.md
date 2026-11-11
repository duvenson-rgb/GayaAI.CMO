# Style: personalbrandlaunch (brand explainer, recolored to #0abbc2)

Source: personalbrandlaunch_Dd14dQbupYL.mp4 — 30.3 s, 720×1280, 30 fps, English, −14.1 LUFS. Registered Sept 30 2026. Contact sheet: `assets/refs/personalbrandlaunch_sheet.jpg`.
**User rules:**
1. Replace the reference's neon lime (#c8fa00) with the brand color #0abbc2 and its palette below. Never use the lime.
2. **Animations never cover the user's face.** If a graphic would, the screen splits: animation in the top half, the head in the bottom half (see "Face safety").

## Look
- Talking head in natural, bright, ungraded footage (no dark grade, no vignette). Full-frame, no punch-in zooms needed.
- Alternates with **full-screen brand-color inserts** (≈3–7 s each) that explain the idea with documents, screenshots and poster grids. Reference cuts: 8.4, 11.3, 16.1, 23.0 s (talking head → insert → talking head…).

## Palette (tokens in `assets/engine_brand.html` :root)
| Token | Hex | Use |
|---|---|---|
| brand | #0abbc2 | big keywords, insert backgrounds, comment-card border, primary timeline segment |
| brand-light | #7fe4e8 | glows, avatar gradients, subtle fills |
| brand-deep | #067e83 | borders, gradient ends, pressed states |
| ink | #04191a | all text on brand backgrounds (8.9:1 contrast; white on #0abbc2 is only 2.4:1 — never use white text on the brand color) |
| accent | #ff6b5b | complementary coral: send button, alert, first ("Hook") segment |
| amber | #ffb347 | split-complement: warm segment |
| violet / blue | #8b7bff / #3d7bff | extra timeline segments |

## Typography (Montserrat, 1080×1920)
- **Sandwich caption** (signature): small white lead-in (600, 50 px, left-aligned at x≈120), huge keyword (900, 180 px, letter-spacing −3, brand color, soft dark shadow, shrink-to-fit 940 px), small white trailing words (600, 50 px, right-aligned). Keyword centered at y ≈ 1150–1270 (chest). One keyword per sentence.
- **Normal caption**: white 500, 54 px, keyword in 800 via `**bold**`; y ≈ 1150–1200.
- **On inserts**: headers ink 900, 66 px, uppercase; subline ink 500, 30 px; captions become **white pills** with ink 800 46 px text at y ≈ 1340–1420.
- Entrances: keyword pops (scale .7→1, ease-out-back .22 s); side words slide up 16 px, staggered .08 s.

## Graphic vocabulary (engine event types)
- `doc` — white paper card, text types on (the script being written). Place it where the head is not.
- `timeline` — segmented bar with colored ticks + legend with colored dots (structure of a video). `active` dims all segments except one.
- `label` — white pill with a hand-drawn white arrow pointing to part of a graphic ("HOOK").
- `insert` — full-screen brand background opening with a circular wipe; header + subline + white cards that rise in, staggered.
- `pill` — caption pill on inserts.
- `comment` — Instagram-style comment card: brand border, gradient avatar, username, typed keyword, coral send button (the CTA "comment KEYWORD").
- Reference also uses movie-poster grids and app screenshots inside inserts — use real screenshots the user supplies; never fake third-party posters.

## Motion & pacing
Fast: a caption change every ~0.4–0.8 s, a graphic change every 2–4 s, an insert every ~5–8 s. Hard cuts between footage and inserts; the circular wipe is the only transition.

## Audio
Voice at −14 LUFS. Light SFX: soft pop on keyword, keyboard ticks under typing, whoosh on insert wipes, notification pop on the comment card. Reference music not confirmed — ask.

## Adapting to our content
- Built for educational/how-to scripts (frameworks, steps, templates) — a natural fit for 123Viral content.
- Keyword choice: the verb or noun that carries the sentence (EKRI, ESTRIKTI, HOOK). Creole words are longer; the keyword auto-shrinks, but prefer ≤ 9 letters.
- Check the teal against each video's footage: on bright or cyan-ish backgrounds, increase the keyword shadow.

## Face safety (mandatory for this style)
1. Render/prepare the footage exactly as it will sit under the overlays, then `python3 $S/scripts/face_track.py base.mp4 faces.js` (YuNet, handles 3/4 profiles; padded head box incl. headwear + chin).
2. Put `faces.js` next to the engine. At load the engine runs `planLayout()`:
   - captions/pills touching the face move down below the chin (never below y=1650);
   - any other graphic touching the face — or a caption that cannot move far enough — turns its whole event window into a **split**: top half = dark panel (#0e2224→#04191a, 6 px teal seam) with the graphics fitted inside and captions near its bottom (y≈820); bottom half = footage reframed on the head (1080×960 crop at the head).
   - adjacent split windows < 0.6 s apart merge (no flicker); full-screen inserts are cutaways and stay as they are.
3. `python3 $S/scripts/plan_layout.py --html engine.html plan.json` — list which beats split and which captions moved; **show this in the storyboard** (mark split beats, render their stills through `split_composite.py`).
4. Final: `python3 $S/scripts/split_composite.py base.mp4 frames plan.json mix.wav OUT.mp4`.
5. QA: sample a frame inside every split and every moved-caption beat; the whole head must be visible and untouched.

## Engine
`assets/engine_brand.html` — data-driven: write `events.js` with `window.EVENTS=[...]` (see the header comment). The built-in DEMO timeline is a working Creole example.
