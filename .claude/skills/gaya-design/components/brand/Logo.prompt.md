The official GAYA logo — use wherever the brand signs a surface (nav bars, footers, slide corners, loading states, favicons).

```jsx
<Logo />                              {/* full-color horizontal lockup, 40px tall */}
<Logo tone="reversed" size={48} />    {/* on dark: color isotype + white wordmark */}
<Logo variant="mark" size={32} />     {/* isotype only — app icon, favicon, avatar */}
<Logo variant="vertical" size={160} /> {/* stacked, all-orange — posters, splash, square formats */}
<Logo variant="wordmark" size={24} /> {/* wordmark only; tone="orange" for the orange version */}
<Logo tone="white" />                 {/* on photos or orange */}
```

`size` is the rendered height in px. Tones: `color` on white/light (preferred — the manual says the ideal background is white), `reversed` on dark neutrals, `white` on photos/brand orange, `black` for B&W print. Never recolor, stretch, rotate, outline or add shadows. Keep clear space ≈ the height of the wordmark's "A"; minimum 100px wide on screen. Vector SVG masters live in `assets/logo/`.
