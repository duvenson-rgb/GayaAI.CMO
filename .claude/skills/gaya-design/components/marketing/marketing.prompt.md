Marketing building blocks distilled from GAYA's flyer, sales deck and social work — use them to prove the product visually.

```jsx
<div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:10}}>
  <AutofillField label="Vehicle 1 · Year / Make / Model" value="2021 Toyota RAV4 XLE" full />
  <AutofillField label="Collision ded." value="$500" />
</div>

<StatRow>
  <Stat value="3–10×" label="Faster quoting" tone="purple" />
  <Stat value="500+" label="Carriers, raters & AMS" tone="purple" />
  <Stat value="SOC 2" label="Type II certified" tone="purple" />
</StatRow>

<div style={{display:'flex',gap:12}}>
  <StepCard n={1} title="Super Copy">From dec pages, ACORDs, PDFs, screenshots or your AMS.</StepCard>
  <StepCard n={2} title="Super Clipboard">One clean client record, ready for any portal.</StepCard>
  <StepCard n={3} title="Super Paste" active>One click autofills every field.</StepCard>
</div>
```

`AutofillField` is the signature motif: orange-50 value box + isotype = "Gaya filled this". `Stat` tones: ink / orange / purple / white. `StepCard active` marks the payoff step in solid purple.
