import React from "react";

/** Proof stat: big number + small caps label. Use in a row separated by hairlines. */
export function Stat({ value, label, tone = "ink", size = 48, style = {}, ...rest }) {
  const color = { ink: "var(--neutral-900)", orange: "var(--brand)", purple: "var(--purple-500)", white: "var(--white)" }[tone];
  const labelColor = tone === "white" ? "var(--neutral-300)" : "var(--neutral-600)";
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 6, ...style }} {...rest}>
      <div style={{ font: `800 ${size}px/1 var(--font-display)`, letterSpacing: "-0.02em", color }}>{value}</div>
      <div style={{ font: `600 ${Math.max(11, Math.round(size * 0.26))}px/1.2 var(--font-accent)`, letterSpacing: "0.1em", textTransform: "uppercase", color: labelColor }}>{label}</div>
    </div>
  );
}

/** Row of Stats separated by hairline dividers. */
export function StatRow({ children, dark = false, style = {}, ...rest }) {
  const items = React.Children.toArray(children);
  return (
    <div style={{ display: "flex", alignItems: "stretch", gap: 0, ...style }} {...rest}>
      {items.map((c, i) => (
        <div key={i} style={{ flex: 1, padding: "4px 28px", paddingLeft: i === 0 ? 0 : 28, borderLeft: i === 0 ? "none" : `1px solid ${dark ? "rgba(255,255,255,0.18)" : "var(--neutral-200)"}` }}>{c}</div>
      ))}
    </div>
  );
}
