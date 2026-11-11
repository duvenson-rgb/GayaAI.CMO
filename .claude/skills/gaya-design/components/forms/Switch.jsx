import React from "react";

/** GAYA on/off switch. Controlled or uncontrolled native checkbox. */
export function Switch({ label, className = "", ...rest }) {
  return (
    <label className={["gaya-switch", className].filter(Boolean).join(" ")}>
      <input type="checkbox" role="switch" {...rest} />
      <span className="gaya-switch__track">
        <span className="gaya-switch__thumb" />
      </span>
      {label && <span className="gaya-switch__label">{label}</span>}
    </label>
  );
}
