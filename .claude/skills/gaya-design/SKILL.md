---
name: gaya-design
description: GAYA's design system and brand kit (the AI copilot for insurance agents, Super Copy / Super Paste). Colors, Montserrat type, spacing, official logo SVGs, React components, finished templates (sales deck, flyer, LinkedIn testimonial, article cover, event and webinar posts, landing page) and the real product-UI rules. Use this skill whenever the user wants anything that should look like Gaya — a flyer, social post, slide or deck, banner, landing page, email header, one-pager, mockup, ad, video super or end card, or any HTML/React UI for Gaya — even if they just say "make it on-brand", "in our style", or name a format without mentioning the brand. Also use it before depicting the Gaya Chrome extension or portal in any visual.
---

# GAYA design

Everything needed to make on-brand GAYA work. The full brand guide is `readme.md` — read it at the start
of any design task (voice, surfaces, layouts, logo rules). This file tells you how to work with the kit.

## What's in here

| Path | What it is | When to open it |
|---|---|---|
| `readme.md` | Brand guide: voice, proof points, surfaces, layouts, color/type/motion rules, logo rules | Always, first |
| `styles.css` → `tokens/*.css`, `components/components.css` | The tokens (CSS variables) and component classes | Reference token names from here; never hard-code a hex that has a token |
| `assets/gaya.css` | `styles.css` flattened into one file (fonts via Google Fonts) | Paste into production code or a tool that can't follow `@import` |
| `assets/logo/*.svg` | Official logos: lockup, vertical, isotype, wordmark × color/reversed/white/black | Every piece that signs off with the brand |
| `templates/<name>/*.dc.html` + `templates/_previews/*.jpg` | GAYA's finished pieces | Look at the preview, then read the markup, before inventing a layout |
| `ui_kits/website/` | Marketing landing page composed from the components | Web pages and component usage |
| `components/**/*.prompt.md`, `*.d.ts` | Component usage and props | When using the React components |
| `guidelines/*.card.html` | Specimen cards for each foundation | Visual reference for a token group |
| `references/product-ui.md` | What the shipped extension and portal really look like | **Any time the product UI appears** (see below) |
| `uploads/GAYA_Brand_Manual.pdf` | The corporate identity manual (authoritative) | Logo/color disputes |
| `scripts/make_standalone.py`, `scripts/render_preview.py` | Build one self-contained file; screenshot it | Every HTML deliverable |

## Workflow for a visual piece

1. **Read `readme.md`**, then pick the closest template. Open its preview in
   `templates/_previews/` (sales-deck, flyer, linkedin-testimonial, article-cover, event-social,
   webinar-visuals, website-ui-kit) and read the matching `.dc.html` for exact sizes, spacing and copy
   patterns. Reuse its structure; don't invent a new layout when a template fits.
2. **Show 2–3 options side by side** for any new piece (this is how GAYA's own projects were built).
   Start from `assets/starter-options.html`: badges 1A/1B/1C (next round 2A…, newest round on top), each
   with a one-line label naming the real axis it differs on — surface/color, layout, or headline angle.
   All options on-brand. Once the user picks, build the rest in that style. Skip options for small edits
   or when the user asked for one specific thing.
3. **Write plain HTML** (not the `.dc.html` runtime format — that only runs inside Claude Design). Put
   `<!-- gaya:styles -->` in `<head>` and reference logos as `src="gaya:logo/gaya-lockup-color.svg"`;
   use token variables (`var(--orange-500)`, `var(--font-display)`, `var(--space-6)`…) everywhere.
   Set each artboard to its real format size (see the formats list in `readme.md`).
4. **Make it self-contained:** `python3 scripts/make_standalone.py page.html out.html`. It inlines the
   CSS, fonts' stylesheet, logos, local images and local scripts, and moves unpkg scripts to jsDelivr —
   so the file works when published, emailed or opened offline.
5. **Look at it before handing it over:** `python3 scripts/render_preview.py out.html shot.png --width W
   --height H [--full]`, then view the PNG. Check logo clear space, one accent per surface, headline wrap,
   nothing clipped.
6. Deliver the way the environment expects (publish the HTML as an artifact, or save and present the
   file). For a PowerPoint / Word / PDF request, use that format's skill and carry these tokens, fonts and
   logo files into it.

Using the React components: load React UMD, then `_ds_bundle.js`, then read components from
`window.GAYADesignSystem_f55ce3` (Logo, Button, IconButton, Input, Switch, Card, Badge, Avatar,
AutofillField, Stat, StatRow, StepCard). `ui_kits/website/index.html` shows the pattern, and
`make_standalone.py` inlines the bundle with working logos. For static pieces, plain HTML with the
component classes is simpler.

Icons: Lucide (`<i data-lucide="name">` + `lucide.createIcons()`), loaded from
`https://cdn.jsdelivr.net/npm/lucide@0.460.0/dist/umd/lucide.min.js`. Lucide is a stand-in; the brand has
no icon set of its own yet.

## Rules that matter most

- **Montserrat** for everything (400 body → 600 labels → 700/800 headlines); **JetBrains Mono** only for
  data values (policy numbers, VINs, dates). No other fonts in marketing pieces.
- **Orange `#EF5A24` leads.** Plus at most **one** supporting accent per surface (purple *or* green *or*
  yellow). Warm-grey neutrals. Flat backgrounds; the only gradients are the orange CTA band and the warm
  testimonial gradient.
- Recurring move: UPPERCASE wide-tracked orange eyebrow → 700–800 tight headline with **one phrase in
  orange** → one line of support.
- Logo is artwork, never live text. Flat (no shadow/glow/outline), never recolored or stretched, clear
  space ≈ height of the "A", ≥100px wide on screen. `color` tone on light, `reversed` on dark/purple.
- Voice: confident, plain, benefit-first, speaks to **you**. Sentence case. Super Copy, Super Paste,
  Super Clipboard are proper nouns. No emoji. No exclamation spam.
- **Proof points — use only these:** 3–10× faster quotes · 15–20 minutes saved per quote · 500+ carriers,
  raters & AMS · **450+ agencies** (never 250+ or 300+) · SOC 2 Type II · Personal and Commercial Lines.
  Some templates and the UI kit carry older or unverified numbers (flyer V1–V3 say "3–4×"; the UI kit
  shows "80%", "0 copy-paste errors", "Trusted by 1,000s of agents"). Replace them with the list above
  unless the user supplies a newer figure.
- Third-party logos (carriers, AMS, agencies, partners) in the templates are the owners' marks. Reuse them
  only in the same kind of context GAYA already used them (integration/customer walls, partner lockups).

## When the product itself is shown

The design system was built without the product code; `references/product-ui.md` records what the real
extension and portal look like. Read it whenever a design shows or recreates the product (panel bar,
side panel, field highlights, paste indicator, portal screens) or overlays copy on product footage
(videos, GIFs, screenshot callouts). There, product truth wins:

- Prefer real screenshots/recordings to drawn UI; label any drawn mock as illustrative.
- In product UI, **Super Copy is purple and Super Paste is green**; the extension uses Manrope, the portal
  Lexend. Don't restyle product UI into Montserrat/orange.
- Don't show features or feedback the product doesn't have (success toasts after copy/paste, fields
  filling all at once, copying from a PDF, flying-data animations, dark mode).
- `AutofillField`, `StepCard` and the UI-kit Super Clipboard panel are marketing illustrations, not the
  product. Fine on flyers and decks; not in anything presented as the real UI.

Open question (ask the user if it matters for the piece): the product colors copy purple / paste green,
while the marketing templates mark the Super Paste step in purple and use orange for Super Copy buttons.
Until the team decides, follow the templates for marketing layouts and the product rule for anything
paired with product footage.
