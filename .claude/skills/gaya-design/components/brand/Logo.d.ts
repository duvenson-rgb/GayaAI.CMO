import * as React from "react";

export interface LogoProps extends React.ImgHTMLAttributes<HTMLImageElement> {
  /** Horizontal lockup, vertical (stacked, all-orange) lockup, isotype only, or wordmark only. Default "lockup". */
  variant?: "lockup" | "vertical" | "mark" | "wordmark";
  /**
   * Color treatment per the brand manual:
   * "color" (full color on light), "reversed" (full-color isotype + white wordmark, on dark),
   * "white" (all white, on photos / brand color), "black" (all black, B&W print), "orange" (wordmark only). Default "color".
   */
  tone?: "color" | "reversed" | "white" | "black" | "orange";
  /** Rendered height in px. Default 40. */
  size?: number;
}

/**
 * Official GAYA logo (bird-of-paradise "G" isotype + GAYA wordmark).
 * @startingPoint section="Brand" subtitle="Official GAYA logo — lockup, isotype, wordmark" viewport="700x180"
 */
export function Logo(props: LogoProps): JSX.Element;
