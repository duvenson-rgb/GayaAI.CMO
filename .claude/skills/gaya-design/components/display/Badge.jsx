import React from "react";

/** GAYA badge / tag / status pill. */
export function Badge({
  color = "neutral",  // solid | neutral | orange | green | yellow | purple | outline
  dot = false,
  className = "",
  children,
  ...rest
}) {
  const cls = ["gaya-badge", `gaya-badge--${color}`, className]
    .filter(Boolean).join(" ");
  return (
    <span className={cls} {...rest}>
      {dot && <span className="gaya-badge__dot" />}
      {children}
    </span>
  );
}
