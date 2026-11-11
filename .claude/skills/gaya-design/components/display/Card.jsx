import React from "react";

/** GAYA surface container. */
export function Card({
  elevation = "outline",  // outline | flat | raised
  padding = "md",          // none | sm | md | lg
  interactive = false,
  as: Tag = "div",
  className = "",
  children,
  ...rest
}) {
  const cls = [
    "gaya-card",
    elevation === "flat" ? "gaya-card--flat" : "",
    elevation === "raised" ? "gaya-card--raised" : "",
    padding !== "none" ? `gaya-card--pad-${padding}` : "",
    interactive ? "gaya-card--interactive" : "",
    className,
  ].filter(Boolean).join(" ");
  return (
    <Tag className={cls} {...rest}>
      {children}
    </Tag>
  );
}
