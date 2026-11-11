import React from "react";

/**
 * GAYA primary action control. Wraps a native <button>.
 */
export function Button({
  variant = "primary",   // primary | secondary | ghost | brandtint | danger
  size = "md",            // sm | md | lg
  block = false,
  leadingIcon = null,
  trailingIcon = null,
  type = "button",
  className = "",
  children,
  ...rest
}) {
  const cls = [
    "gaya-btn",
    `gaya-btn--${variant}`,
    `gaya-btn--${size}`,
    block ? "gaya-btn--block" : "",
    className,
  ].filter(Boolean).join(" ");

  return (
    <button type={type} className={cls} {...rest}>
      {leadingIcon && <span className="gaya-btn__icon">{leadingIcon}</span>}
      {children && <span>{children}</span>}
      {trailingIcon && <span className="gaya-btn__icon">{trailingIcon}</span>}
    </button>
  );
}
