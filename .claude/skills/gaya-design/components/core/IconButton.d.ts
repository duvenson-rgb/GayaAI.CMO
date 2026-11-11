import * as React from "react";

export interface IconButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  /** Control size. Default "md". */
  size?: "sm" | "md" | "lg";
  /** Required for accessibility. */
  "aria-label": string;
}

/** Square icon-only button. */
export function IconButton(props: IconButtonProps): JSX.Element;
