import React from "react";

/**
 * Square icon-only button (toolbar actions, close buttons, etc.).
 * Always pass an accessible `aria-label`.
 */
export function IconButton({
  size = "md",     // sm | md | lg
  className = "",
  children,
  ...rest
}) {
  const cls = ["gaya-iconbtn", `gaya-iconbtn--${size}`, className]
    .filter(Boolean)
    .join(" ");
  return (
    <button type="button" className={cls} {...rest}>
      {children}
    </button>
  );
}
