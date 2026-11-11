Display primitives — containers and labels for GAYA surfaces.

```jsx
<Card padding="lg" interactive>…</Card>
<Card elevation="raised">…</Card>
<Badge color="green" dot>Synced</Badge>
<Badge color="orange">Beta</Badge>
<Avatar name="Carl Ziadé" />
<Avatar src="/me.jpg" name="Carl Ziadé" size="lg" />
```

`Card` elevations: `outline` (default, hairline border), `flat`, `raised` (soft shadow). `Badge` colors map to the brand quartet plus `neutral`/`solid`/`outline`; add `dot` for live-status pills. `Avatar` shows the image or auto initials.
