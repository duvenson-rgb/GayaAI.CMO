# Real product UI (what the shipped Gaya product actually looks like)

The design system in this skill was built from the brand manual and GAYA's marketing work, **without
access to the product code**. A later code audit of `gaya-fi/chrome-extension@develop` (`e4f855f9`,
v4.1.26) and `gaya-fi/portal-gaya@staging` (`48ab222`) found that the product itself uses different
fonts, a different copy/paste color rule, and specific UI patterns. Everything below comes from that
audit (full detail with file/line references: `claude/video-treatment.md` and
`claude/video-18s-cut-kit.md` in the gaya-marketing project).

**When to read this file:** any time a design shows, recreates, mocks up or animates the product
(Chrome extension panel, side panel, in-page highlights, portal screens), or pairs marketing copy with
product footage (videos, demo GIFs, screenshot callouts). For pure marketing layouts that don't depict
the product, the main design system wins.

## Precedence

1. Real screen recordings / screenshots beat any drawn version. Don't redraw product UI when footage
   can be used; if a mock is unavoidable, label it as illustrative.
2. When depicting the product, use the values here, not the marketing tokens.
3. Never show a feature, label, animation or state that isn't listed here (or confirmed in code).

## Color meaning in the product

- **Super Copy = purple `#521184`. Super Paste = green `#036302` / `#036303`** on every surface: panel
  buttons, field highlights, side-panel buttons, notifications, portal buttons ("Open in Extension"
  purple, "Paste to PDF & CSV" green).
- **Orange `#EF5A24`** is brand + utility: logo, loaders, "See Clipboard" ring, pasted-field badge ring,
  hover tints, "Portal" pill.
- Portal's shadcn `--primary` is `#FF6900` (Tailwind orange-500) — not brand. Always use `#EF5A24`.
- Extension ramps (Mantine): primary `#EEE7F2 … #521184 (6) … #280642`; green `#E6F4E6 … #036302 (6)`;
  orange `#FFE9E0 … #EF5A24 (6) …`; red `#C31F00`; near-black `#09090B`.
- Neutrals: panel/app bg `#F7F7F7`; extension text `#585858`; field label `rgb(75,75,75)`; tooltip
  `#21252b`; portal label `#565656` 13px / value `#495057` 14px 500; portal card border `#E5E8EB`;
  newly augmented value `#AF69EF` italic.
- Light mode only (the extension forces `color-scheme: light`).

## Type in the product

| Surface | Font |
|---|---|
| Extension (side panel, popup, in-page iframes) | **Manrope** (action buttons 800/16px) |
| Panel count badge | Inter Bold 22px |
| In-page paste indicator & notifications | Roboto / system |
| Portal | **Lexend** |

Marketing supers laid over product footage used **Manrope 800** so they match the extension buttons.
This conflicts with the design system's "Montserrat for everything" rule — see the open question in
SKILL.md.

## Radii, spacing, shadows (product)

Mantine radius sm/md/lg 8/12/16px; panel bar left corners 28px; panel buttons 48px circles; field
highlight 8px; indicator pill 32px; toggle 32×17. Portal `--radius` 0.65rem, cards `rounded-xl`.
Panel bar 60px tall; side panel content 500px wide; buttons sm/md/lg 36/42/50px.
Shadows: panel bar `0 4px 10px rgba(0,0,0,.15)`; indicator `0 0 18px 3px rgba(0,0,0,.2)`.

## Real UI and labels

- **In-page panel bar:** `#F7F7F7` pill docked to the right edge, vertically centered. Primary circle is
  purple (copy) on the source tab; it flips to green (paste) once the clipboard has records and you're on
  a different tab. Resting state shows a white count "N+" badge. Tooltips: "Super Copy", "Super Paste",
  "See Clipboard", "Exit Mode", "See Defaults", "Capture data", "Expand panel". **No entrance animation.**
- **Hover preview:** hovering the button outlines every field the action will touch with a breathing
  frame (purple copy / green paste), 8px radius, 1.1s pulse.
- **After Super Copy:** a purple toggle (32×17) appears at the inside end of each captured field. No
  toast or banner. On the source tab the count usually doesn't change.
- **Super Paste:** white top-center pill: orange spinner, "Analyzing page..." → "Super Pasting...", red
  ⓧ to stop. Fields fill **one at a time**; each gets a Gaya G badge in a white circle with a 1px orange
  ring. No success banner.
- **Side panel (ClipboardScreen):** header with orange GAYA wordmark, "Personal Line" / "Commercial
  Line"; customer card "Unsaved" + green "Save to Portal"; entity cards ("Customer", "Driver 1",
  "Vehicle 1" = Year Make Model); footer "+" (Add More Data), **Super Copy** (purple), **Super Paste**
  (green), each with a count. Menu: "Super Paste to PDF", "Super Paste to CSV".
- **Portal:** nav "Home", "Client Records › Personal / Commercial"; record page with "Look up an item",
  "Paste to PDF & CSV" (green), "Open in Extension" (purple); sidebar "Summary / Notes". Data reaches the
  portal only via "Save to Portal" (not automatic).
- Keyboard: Alt+Shift+G copy, Alt+G paste.

## Things the product does NOT do (don't show them)

- Super Copy on a PDF/document (documents go through a separate upload/extraction feature).
- Super Copy/Paste on any website — only mapped platforms.
- Data "flowing", particles, or a "structuring" animation.
- A success toast/counter after copy or paste.
- All fields filling simultaneously.
- Automatic sync from extension to portal.
- Dark mode.

## Where the design system's own mockups differ from the product

- `ui_kits/website/` Super Clipboard panel: orange Super Copy button, "Connected" badge, "SOURCE" URL
  row. It's a brand illustration, not the real side panel.
- `AutofillField` (orange-50 box + isotype inside the field) is a marketing motif. The real pasted-field
  marker is a G badge in a white circle with an orange ring **beside** the field.
- `StepCard active` puts Super Paste in solid purple; in the product, paste is green.
