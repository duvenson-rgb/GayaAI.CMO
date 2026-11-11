import * as React from "react";

export interface AutofillFieldProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Small caps field label, e.g. "Driver 1 · License #". */
  label: React.ReactNode;
  /** Field value (rendered in mono). */
  value: React.ReactNode;
  /** Show the Gaya-filled treatment (orange tint + isotype). Default true. */
  filled?: boolean;
  /** Span all columns when inside a grid. */
  full?: boolean;
}

/** Form field shown as autofilled by Gaya. */
export function AutofillField(props: AutofillFieldProps): JSX.Element;
