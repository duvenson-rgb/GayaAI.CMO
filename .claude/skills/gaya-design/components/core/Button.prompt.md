One-sentence: GAYA's button — the primary way to trigger an action; defaults to the orange brand fill.

```jsx
<Button>Super Copy</Button>
<Button variant="secondary" size="lg">Cancel</Button>
<Button variant="ghost" leadingIcon={<PlusIcon/>}>Add field</Button>
<Button variant="danger">Delete</Button>
<IconButton aria-label="Settings"><GearIcon/></IconButton>
```

Variants: `primary` (orange, for the single most important action), `secondary` (outlined neutral), `ghost` (text only), `brandtint` (soft orange wash), `danger`. Sizes `sm | md | lg`. Use `block` to fill width. Hover darkens one brand step + soft glow; press scales to 0.98. Use `IconButton` for icon-only toolbar actions.
