Form controls — labelled inputs and toggles for GAYA's data-entry surfaces.

```jsx
<Input label="Policy number" placeholder="e.g. HO-4821" required />
<Input label="Premium" leadingAffix="$" defaultValue="1,240" />
<Input label="Email" error="Enter a valid email" defaultValue="bad@" />
<Switch label="Auto-fill carrier portals" defaultChecked />
```

`Input` supports `hint`, `error` (flips to invalid + red ring), `leadingAffix` / `trailingAffix` for icons or symbols. `Switch` is a native checkbox with `role="switch"`; pass `checked`/`onChange` for controlled use. Both inherit brand focus rings automatically.
