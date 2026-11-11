import * as React from "react";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  /** Field label rendered above the control. */
  label?: React.ReactNode;
  /** Helper text below the field. */
  hint?: React.ReactNode;
  /** Error message — also flips the field into the invalid state. */
  error?: React.ReactNode;
  /** Show a required asterisk on the label. */
  required?: boolean;
  /** Node pinned inside the left edge (icon, currency symbol). */
  leadingAffix?: React.ReactNode;
  /** Node pinned inside the right edge. */
  trailingAffix?: React.ReactNode;
}

/**
 * GAYA text input field.
 * @startingPoint section="Forms" subtitle="Labelled text field with hint / error / affixes" viewport="700x170"
 */
export function Input(props: InputProps): JSX.Element;
