import React from "react";

/** GAYA avatar — image or initials fallback. */
export function Avatar({
  size = "md",      // sm | md | lg
  src = "",
  name = "",
  className = "",
  ...rest
}) {
  const initials = name
    .split(" ")
    .map((w) => w[0])
    .filter(Boolean)
    .slice(0, 2)
    .join("")
    .toUpperCase();
  const cls = ["gaya-avatar", `gaya-avatar--${size}`, className]
    .filter(Boolean).join(" ");
  return (
    <span className={cls} aria-label={name || undefined} {...rest}>
      {src ? <img src={src} alt={name} /> : initials}
    </span>
  );
}
