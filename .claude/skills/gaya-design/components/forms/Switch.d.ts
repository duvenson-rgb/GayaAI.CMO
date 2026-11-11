import * as React from "react";

export interface SwitchProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, "type"> {
  /** Text label rendered beside the switch. */
  label?: React.ReactNode;
}

/** GAYA toggle switch. */
export function Switch(props: SwitchProps): JSX.Element;
