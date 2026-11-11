import * as React from "react";

export interface AvatarProps extends React.HTMLAttributes<HTMLSpanElement> {
  /** Avatar size. Default "md". */
  size?: "sm" | "md" | "lg";
  /** Image URL. Falls back to initials when absent. */
  src?: string;
  /** Full name — drives initials + accessible label. */
  name?: string;
}

/** GAYA avatar. */
export function Avatar(props: AvatarProps): JSX.Element;
