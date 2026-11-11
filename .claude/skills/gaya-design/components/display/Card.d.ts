import * as React from "react";

export interface CardProps extends React.HTMLAttributes<HTMLElement> {
  /** Shadow / border treatment. Default "outline". */
  elevation?: "outline" | "flat" | "raised";
  /** Inner padding. Default "md". */
  padding?: "none" | "sm" | "md" | "lg";
  /** Adds hover lift + pointer cursor. */
  interactive?: boolean;
  /** Element to render as. Default "div". */
  as?: React.ElementType;
}

/**
 * GAYA surface card.
 * @startingPoint section="Display" subtitle="Surface container — outline / flat / raised" viewport="700x220"
 */
export function Card(props: CardProps): JSX.Element;
