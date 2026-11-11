import * as React from "react";

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  /** Color treatment. Default "neutral". */
  color?: "solid" | "neutral" | "orange" | "green" | "yellow" | "purple" | "outline";
  /** Render a leading status dot. */
  dot?: boolean;
}

/** GAYA badge / status pill. */
export function Badge(props: BadgeProps): JSX.Element;
