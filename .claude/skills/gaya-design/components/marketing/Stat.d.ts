import * as React from "react";

export interface StatProps extends React.HTMLAttributes<HTMLDivElement> {
  /** The number, e.g. "3–10×", "500+", "SOC 2". */
  value: React.ReactNode;
  /** Caps label, e.g. "Faster quoting". */
  label: React.ReactNode;
  /** Number color. Default "ink". */
  tone?: "ink" | "orange" | "purple" | "white";
  /** Number size in px. Default 48. */
  size?: number;
}

export interface StatRowProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Use light dividers for dark backgrounds. */
  dark?: boolean;
  children?: React.ReactNode;
}

/** Proof stat. */
export function Stat(props: StatProps): JSX.Element;
/** Hairline-divided row of stats. */
export function StatRow(props: StatRowProps): JSX.Element;
