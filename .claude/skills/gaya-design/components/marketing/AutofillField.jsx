import React from "react";

function markSrc() {
  if (typeof document === "undefined") return "assets/logo/gaya-isotype-color.svg";
  const s = Array.from(document.scripts).find((el) => /_ds_bundle\.js(\?|$)/.test(el.src));
  return s ? new URL("assets/logo/gaya-isotype-color.svg", s.src).href : "assets/logo/gaya-isotype-color.svg";
}

/** A form field shown as "filled by Gaya": orange-tinted value + isotype marker. The signature product motif. */
export function AutofillField({ label, value, filled = true, full = false, style = {}, ...rest }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 5, gridColumn: full ? "1 / -1" : undefined, minWidth: 0, ...style }} {...rest}>
      <div style={{ font: "600 10px/1.1 var(--font-accent)", letterSpacing: "0.08em", textTransform: "uppercase", color: "var(--neutral-500)" }}>{label}</div>
      <div style={{
        display: "flex", alignItems: "center", justifyContent: "space-between", gap: 8,
        height: 32, padding: "0 10px", borderRadius: 6,
        background: filled ? "var(--orange-50)" : "var(--neutral-0)",
        border: `1px solid ${filled ? "var(--orange-100)" : "var(--neutral-200)"}`,
        font: "500 13px/1 var(--font-mono)", color: filled ? "var(--neutral-900)" : "var(--neutral-400)",
        whiteSpace: "nowrap", overflow: "hidden",
      }}>
        <span style={{ overflow: "hidden", textOverflow: "ellipsis" }}>{value}</span>
        {filled && <img src={markSrc()} alt="" style={{ height: 16, width: "auto", flex: "none" }} />}
      </div>
    </div>
  );
}
