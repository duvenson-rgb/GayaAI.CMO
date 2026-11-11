import * as React from "react";

export interface StepCardProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Step number. */
  n: React.ReactNode;
  /** Step title, e.g. "Super Copy". */
  title: React.ReactNode;
  /** Highlight as the payoff step (solid purple). */
  active?: boolean;
  children?: React.ReactNode;
}

/** Numbered flow step card. */
export function StepCard(props: StepCardProps): JSX.Element;
