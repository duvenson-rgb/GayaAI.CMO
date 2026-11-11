import React from "react";

/** Numbered flow step (Super Copy → Super Clipboard → Super Paste). `active` = the purple highlighted final step. */
export function StepCard({ n, title, children, active = false, style = {}, ...rest }) {
  return (
    <div style={{
      flex: 1, minWidth: 0, display: "flex", flexDirection: "column", gap: 8, padding: "18px 20px",
      borderRadius: "var(--radius-lg)",
      background: active ? "var(--purple-500)" : "var(--neutral-0)",
      border: active ? "1px solid var(--purple-500)" : "1px solid var(--neutral-200)",
      color: active ? "var(--white)" : "var(--neutral-900)", ...style,
    }} {...rest}>
      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
        <span style={{ width: 24, height: 24, borderRadius: "50%", display: "grid", placeItems: "center", flex: "none",
          background: active ? "var(--white)" : "var(--purple-500)", color: active ? "var(--purple-500)" : "var(--white)",
          font: "700 13px/1 var(--font-accent)" }}>{n}</span>
        <span style={{ font: "700 18px/1.2 var(--font-display)", letterSpacing: "-0.01em" }}>{title}</span>
      </div>
      <div style={{ font: "400 14px/1.45 var(--font-body)", color: active ? "var(--purple-50)" : "var(--neutral-600)" }}>{children}</div>
    </div>
  );
}
