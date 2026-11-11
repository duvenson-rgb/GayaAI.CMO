# GAYA Design System

The design system for **GAYA** — the AI copilot for insurance agents. GAYA brings large
language models to insurance quoting and servicing: its signature **Super Copy → Super Paste**
flow captures every field from a carrier portal, dec page or ACORD form once, then autofills it
across 500+ carrier portals, raters and AMS platforms in a single click.

This project is a self-contained design system. Consuming projects link the single root
`styles.css`, use the compiled component bundle, and follow the guidance below.

---

## Sources

- **Earlier Claude Design projects** (read-only references): ad1e522a… (event/article/webinar), ff5b7647… (demo storyboards), d5117d89… (sales deck), dd69d473… (flyer), 9b611b69… (AMS/carrier animations), 84b73a05… (dec-page animation), 44777eb9… (LinkedIn testimonials).

- **`uploads/gaya_logo-Box7pLgT.webp`, `uploads/Gaya Logo (3).avif`** — early raster logo files.
- **`uploads/Gaya Logo V1.svg` / `V2.svg`** (+ PNG/JPG) — vector logo masters (horizontal / vertical). Source of every file in `assets/logo/`.
- **`uploads/GAYA_Brand_Manual.pdf`** — the GAYA Corporate Identity Manual (20 pages). The
  authoritative source for colors, typography and logo rules. Color values, font names and
  logo/usage rules in this system are taken directly from it. (The manual's logo and color
  pages are vector-drawn; they could not be rasterized in-tool, and the logo contains no
  embedded bitmap to extract — see CAVEATS.)
- **Product context** — gathered from public sources (gaya.ai, Chrome Web Store, press). Used
  to ground copy and the UI kit in the real product. GAYA was founded in 2023; the product is a
  browser extension ("AI-powered clipboard") plus web app for insurance brokers in the U.S.

> No product codebase, Figma file, or product screenshots were provided. The UI kit is a
> **brand application** of this design system to GAYA's documented product surfaces (a marketing
> site with an interactive Super Clipboard panel), not a pixel-copy of the live product.

---

## Learned from GAYA's own work

Merged from seven earlier Claude Design projects (sales deck, one-page flyer, LinkedIn
testimonials, article/partner covers, Applied Net 2026 event posts, webinar visuals, demo
storyboards, AMS / carrier logo animations, dec-page volume animation). The finished pieces
live in `templates/` — start from them.

**Recurring layouts**
- **Eyebrow → headline → one line of support.** Every surface opens with an UPPERCASE
  Montserrat eyebrow (600–700, +0.16–0.24em, orange; `--orange-300` on dark), then a 700–800
  headline with tight tracking where **one phrase is set in orange** ("3-10× faster quotes.
  **Zero manual entry.**", "Type it once. **Super Paste** everywhere").
- **Problem → Feature → Outcome.** Demo slides and flyer sections use this 3-beat structure,
  labelled with caps eyebrows ("THE PROBLEM", "THE FIX") and mono section tags (`DEMO / 01`
  followed by a hairline rule).
- **Three-step flow:** Super Copy → Super Clipboard → Super Paste, numbered, with the payoff
  step in **solid purple** (`StepCard active`).
- **Stat row:** big 700–800 numbers + small caps labels, separated by hairlines (`StatRow`).
- **Autofilled field motif:** form fields with an orange-50 value box + the isotype on the right
  = "Gaya filled this" (`AutofillField`). Shown inside a quiet browser-window card.
- **Logo walls:** "INTEGRATES WITH YOUR AMS" (Applied, HawkSoft, AMS360, EZLynx, Salesforce,
  Vertafore, Momentum…) and "TRUSTED BY 450+ AGENCIES" (USI, Acrisure, NFP, Heffernan,
  Leavitt, TWFG). Logos in one even row, equal optical size, on white.
- **Partner lockup:** `Partner logo × GAYA logo`, the × in a light neutral.
- **Isotype watermark:** a giant isotype at ~6% opacity, cropped off a corner.
- **Footer band:** orange-600/700 band with a white-circle isotype, "Simple. Yet Powerful.",
  URL + email, and "SCAN THE QR TO BOOK YOUR DEMO ↑".

**Surfaces**
- **Paper** `--surface-paper` #FBF8F5 is the default canvas for covers, posts and slides.
- **Ink** `--surface-ink` #141210 for title, quote and "why" slides (white logo, `--orange-300` eyebrow).
- **Solid orange** for section dividers ("Let me show you.").
- **Purple stage** for bold social/announcements (see Visual foundations).
- **Warm gradient** `--gradient-warm` (white → peach) for testimonial posts only.
- Always one accent per surface: orange, plus purple *or* green, never all.

**Formats used**
- Slides 1920×1080 · LinkedIn portrait 1080×1350 · LinkedIn square 1200×1200 · Article cover
  1600×840 · Letter flyer 816×1056 · Banner 800×200 / 1920×280.

**Testimonial posts:** big faint orange quote mark, the quote in **purple** 700 with the key
phrase in orange, name in orange + role in grey, initial-avatar circle (green/purple/orange),
"Gaya.ai" in orange at the bottom.

**Event posts:** "We're heading to Applied Net 2026" / "Badge on. Demo ready." with a hanging
conference-badge mockup, and a footer with MEET US ON THE GROUND · Booth · Dates · City.

**Motion (animations projects):** logo walls reveal one by one along a line from the isotype;
counters tick up ("Captured in one Super Copy: 5 pages · 68 drivers · 67 vehicles"); whole
words slam in large ("Quote", "Fast") before resolving to the headline.

## Working with this system: always show options

When generating designs with GAYA, **always present 2–3 side-by-side options** rather than a
single answer — the way the original testimonial, article-cover and event projects were built:
- Lay options out next to each other on one canvas page (start from `assets/starter-options.html`; inside Claude Design, `<meta name="design_doc_mode" content="canvas">` makes it pannable).
- Label each with a visible badge and stable id: **1A, 1B, 1C** (next round 2A, 2B…); newest round on top.
- Give each a one-line name that says how it differs (e.g. "1A · Warm gradient — house style",
  "1B · Inverse — quiet and confident", "1C · Purple stage").
- Options must differ on a real axis (surface/color, layout, or headline angle), all on-brand.
- Once one is picked, build the remaining pieces in that style.

## Content fundamentals

How GAYA writes and sounds.

- **Voice:** confident, plain-spoken, benefit-first. Speaks to busy independent agents who
  value time. Outcomes over features ("Quote 10× faster", "Get your time back").
- **Person:** addresses the reader as **you**; the company is **Gaya** / **we**. Product
  actions are branded proper nouns: **Super Copy**, **Super Paste**, **Super Clipboard**.
- **Casing:** Sentence case for headlines and UI. The wordmark is **GAYA** (all caps).
  Eyebrows/kickers are UPPERCASE with wide tracking (e.g. `AI COPILOT FOR INSURANCE`).
- **Numbers as proof:** concrete, verifiable stats carry the message — `10×`, `500+`,
  `80%`, `17 minutes → 8`. Avoid vague superlatives.
- **Tone:** trustworthy first (it's insurance + sensitive data → "SOC 2 Type II",
  "bank-grade encryption"), energetic second. Calm, never hype-y. No exclamation spam.
- **Emoji:** none. Not part of the brand. Use the icon system instead.
- **Sentence length:** short. One idea per line. Generous whitespace.

Proof points in use (keep consistent; latest wins):
- **3–10× faster quotes** · **15–20 minutes saved per quote** · **500+ carriers, raters & AMS**
  · **450+ agencies** (current — never 250+ / 300+) · **SOC 2 Type II** · Personal *and* Commercial Lines
  · Chrome/Edge "AI autofill browser extension".

Punctuation: short declaratives with periods ("Simple. Yet Powerful.", "Badge on. Demo
ready."); middots to join facts ("Direct API · No retyping · Setup in 5 minutes"); colons over
dashes in body copy.

Examples (real product copy):
- "Quote 10× faster — no more retyping."
- "Copy once. Paste everywhere."
- "Gaya takes care of laborious data entry so you get back the time to build trust with clients."
- "Type it once. Super Paste everywhere."
- "I refuse to copy & paste."
- "By the end of the next 30 minutes, you'll see exactly how your team gets 15–20 minutes back on every quote."

---

## Visual foundations

- **Color:** A warm, optimistic four-color brand palette — **Orange `#EF5A24`** (the primary
  identifier / isotype color), plus **Green `#036303`**, **Yellow `#F9AE3B`** and
  **Purple `#521184`** as supporting accents. Orange leads almost everything; use **one**
  supporting accent per surface, never all four at once. Neutrals are **warm-leaning greys**
  (a hint of the orange temperature) so the system stays cohesive. Full ramps + semantic
  aliases live in `tokens/colors.css`.
- **Type:** **Montserrat is the GAYA typeface** — headlines, UI, body and eyebrows all use it.
  Hierarchy comes from weight (400 body → 600 labels → 700/800 headlines) and size. Headlines
  are tight-tracked; eyebrows are UPPERCASE with +0.18em tracking. **JetBrains Mono** is used
  only for data values (policy numbers, dates, codes). The manual's Arkhip is the logotype face —
  the logo ships as artwork, so it's never set as live text. See `tokens/typography.css`.
- **Spacing:** 4px base grid. Generous, architectural rhythm. `tokens/spacing.css`.
- **Backgrounds:** clean and flat. White / warm off-white (`--surface-page`) is the default,
  exactly as the manual prescribes ("the ideal background is white"). Dark sections use the
  near-black `--surface-inverse`. The single permitted gradient is the **orange CTA band**
  (`orange-500 → orange-600`); no bluish-purple gradients, no busy textures, no photo washes by
  default. Imagery, when used, should be warm and bright to match the palette.
- **Purple stage (alternate background):** GAYA sometimes runs whole surfaces on flat brand
  **Purple `#521184`** — social banners, announcements, hero/testimonial bands. Recipe: flat
  purple, **white bold Montserrat** headline (short, first-person, punchy — "I refuse to copy &
  paste."), the **full-color isotype** (orange reads beautifully on purple), **orange** accent
  text for the URL/CTA (`Gaya.ai` + Lucide `mouse-pointer-click`), and optionally a soft,
  **grainy lavender/rose/orange glow** bleeding in from one edge. Use class
  `gaya-purple-stage` (+ `gaya-purple-stage--glow`) and tokens `--surface-purple`,
  `--on-purple`, `--on-purple-accent`. Use the `reversed` logo tone here. Reference:
  `assets/imagery/purple-banner-reference.jpg`. Keep orange text large/bold on purple (≈3.6:1).
- **Corner radii:** moderate, not pill-everything. Cards `--radius-lg` (14px), controls
  `--radius-md` (10px). Pills (`--radius-full`) are reserved for badges and switches.
- **Cards:** white surface, hairline `--border-subtle` border, soft `--shadow-sm`. Interactive
  cards lift 2px on hover. Avoid the "rounded box + colored left-border accent" cliché.
- **Borders:** hairline neutral borders do most of the structural work (the brand reads clean
  and precise). 1.5px brand border on primary/focused controls.
- **Shadows:** soft, low-contrast, **warm-tinted** (the shadow color carries the brand
  temperature). Five-step elevation in `tokens/effects.css`. Restrained — never glossy. NB: the
  **logo itself is strictly flat** — no drop shadow, glow, or stroke, per the manual.
- **Motion:** calm and confident. Standard easing `cubic-bezier(0.2,0,0,1)`, durations
  120/200/320ms. Fades and small slides; **no bounce**, no infinite decorative loops.
- **Hover:** shift to the next-darker brand step (`--brand-hover`); primary buttons also gain a
  soft brand glow. **Press:** next step darker + `transform: scale(0.98)`. **Focus:** 3px
  `--focus-ring` halo (translucent orange).
- **Transparency / blur:** used sparingly — the sticky nav uses a translucent surface +
  `--blur-md` backdrop. Overlays use the `--scrim` dim.

---

## Iconography

- **System:** [**Lucide**](https://lucide.dev) — clean, geometric, consistent 2px-stroke
  outline icons. This is a **substitution**: the brand manual specifies no icon library, and no
  product icon set was provided. Lucide's geometric, even-stroke style pairs naturally with
  geometric Montserrat and the flat, precise brand. **Flag:** swap for GAYA's
  own icon set if/when one exists.
- **Delivery:** loaded from CDN (`cdn.jsdelivr.net/npm/lucide@0.460.0`; the templates still reference unpkg, which `scripts/make_standalone.py` rewrites) and rendered via `<i data-lucide="name">`
  + `lucide.createIcons()`. No icon font, no committed SVG sprite. Cards and the UI kit use it
  directly.
- **Sizing:** 16px in buttons/inline, 18–24px for feature/step icons, with `currentColor` so
  icons inherit text color. Feature icons sit on a soft tinted tile (`--orange-50` / accent-50).
- **Emoji:** never used as iconography. **Unicode glyphs:** not used as icons (the `×` mark
  and arrows come from Lucide).
- The **GAYA isotype** is a brand mark, not an icon — see the Logo section.

---

## Logo

The logo is a **bird-of-paradise "G"**: an orange G whose cut-out top sprouts leaves in orange, purple, yellow and green — the whole brand quartet in one mark — paired with a custom geometric **GAYA** wordmark (angled A crossbars).

Files (`assets/logo/`, vector SVG):
- gaya-lockup-color.svg — primary horizontal lockup (color isotype + black wordmark), on white/light
- gaya-lockup-reversed.svg — color isotype + white wordmark, on dark
- gaya-lockup-white.svg / gaya-lockup-black.svg — one-color
- gaya-lockup-vertical-color.svg — stacked, all-orange (posters, splash, square formats)
- gaya-lockup-vertical-white.svg / -black.svg — one-color stacked
- gaya-isotype-color|white|black.svg — mark only (app icon, favicon, avatar)
- gaya-wordmark-black|orange|white.svg — wordmark only

Use the `Logo` component (`variant` lockup|vertical|mark|wordmark, `tone` color|reversed|white|black, `size` = height px). Rules from the manual: white is the ideal background; clear space ≈ height of the "A"; min 100px wide on screen / 20mm in print; never stretch, rotate, recolor, outline or add shadows/glows.

---

## Index / manifest

**Root**
- `styles.css` — the single entry point consumers link. `@import`s only.
- `readme.md` — this guide.
- `SKILL.md` — Agent-Skill front-matter wrapper.

**`tokens/`** — `fonts.css`, `colors.css`, `typography.css`, `spacing.css`, `effects.css`,
`base.css` (element defaults). All reached from `styles.css`.

**`components/`** — React primitives (compiled into the bundle, exported on
`window.GAYADesignSystem_f55ce3`):
- `brand/Logo` — official logo artwork (variants lockup / mark / wordmark; tones color / reversed / white / black).
- `core/Button`, `core/IconButton` — actions.
- `forms/Input`, `forms/Switch` — data-entry controls.
- `display/Card`, `display/Badge`, `display/Avatar` — surfaces, status, identity.
- `marketing/AutofillField`, `marketing/Stat` + `StatRow`, `marketing/StepCard` — proof motifs from GAYA's marketing.
- `components/components.css` — class-based styling for the above (driven by tokens).

**`guidelines/`** — foundation specimen cards (Colors, Type, Spacing, Brand) shown in the
Design System tab.

**`ui_kits/website/`** — GAYA marketing landing page (`index.html`) with an interactive
**Super Clipboard** product panel, stats, how-it-works, testimonial, CTA and footer. Also a
Starting Point.

**`assets/logo/`** — official vector logo SVGs (see Logo section).

**`assets/imagery/`** — `purple-banner-reference.jpg` (purple-stage reference).

**`thumbnail.html`** — project tile.

**`templates/`** — finished GAYA pieces to start from (fonts normalized to Montserrat):
- `sales-deck/` — 1920×1080 sales deck
- `flyer/` — Letter one-page flyer
- `linkedin-testimonial/` — 1080×1350 quote posts
- `article-cover/` — 1600×840 partner/integration cover
- `event-social/` — conference LinkedIn posts
- `webinar-visuals/` — webinar promo set

**`uploads/`** — the original brand manual PDF and logo files.

**Added when packaging as a Claude skill**
- `SKILL.md` — how to work with the kit (workflow, rules, product-UI precedence).
- `references/product-ui.md` — what the shipped extension and portal actually look like (from a code audit).
- `assets/gaya.css` — `styles.css` flattened into one file.
- `assets/starter-options.html` — side-by-side options canvas (1A / 1B / 1C).
- `templates/_previews/*.jpg` — rendered previews of every template and the UI kit.
- `scripts/make_standalone.py` — inlines CSS, logos, images and scripts into one self-contained HTML file.
- `scripts/render_preview.py` — screenshots an HTML file for review.

---

## CAVEATS

- **The UI kit is a brand application,** not a recreation of the live product (no codebase /
  Figma / screenshots were available). The product's real fonts, colors and UI are now documented in
  `references/product-ui.md`; use that whenever the product itself is shown.
- **Templates use the Claude Design runtime** (`.dc.html`, `support.js`). They render when served over
  HTTP (`scripts/render_preview.py` does this) but aren't meant to be shipped as-is: rebuild the chosen
  layout as plain HTML.
