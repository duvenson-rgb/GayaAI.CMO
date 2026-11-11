import React from "react";

let _id = 0;

/**
 * GAYA text field with label, hint/error, and optional lead/trail affixes.
 */
export function Input({
  label,
  hint,
  error,
  required = false,
  leadingAffix = null,
  trailingAffix = null,
  className = "",
  id,
  ...rest
}) {
  const fieldId = id || React.useMemo(() => `gaya-input-${++_id}`, [id]);
  const invalid = Boolean(error);

  const inputCls = [
    "gaya-input",
    leadingAffix ? "gaya-input--has-lead" : "",
    trailingAffix ? "gaya-input--has-trail" : "",
    invalid ? "gaya-input--invalid" : "",
  ].filter(Boolean).join(" ");

  return (
    <div className={["gaya-field", className].filter(Boolean).join(" ")}>
      {label && (
        <label className="gaya-label" htmlFor={fieldId}>
          {label}
          {required && <span className="gaya-label__req">*</span>}
        </label>
      )}
      <div className="gaya-input-wrap">
        {leadingAffix && (
          <span className="gaya-input__affix gaya-input__affix--lead">{leadingAffix}</span>
        )}
        <input
          id={fieldId}
          className={inputCls}
          aria-invalid={invalid || undefined}
          {...rest}
        />
        {trailingAffix && (
          <span className="gaya-input__affix gaya-input__affix--trail">{trailingAffix}</span>
        )}
      </div>
      {(error || hint) && (
        <span className={["gaya-hint", invalid ? "gaya-hint--error" : ""].filter(Boolean).join(" ")}>
          {error || hint}
        </span>
      )}
    </div>
  );
}
