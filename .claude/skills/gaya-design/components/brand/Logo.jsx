import React from "react";

/*
 * GAYA logo — renders the official artwork from assets/logo/.
 * Asset URLs resolve relative to the loaded _ds_bundle.js, so the
 * logo works at any page depth (and in consuming projects that ship
 * assets/ next to the bundle).
 */
function logoBase() {
  if (typeof document === "undefined") return "assets/logo/";
  const s = Array.from(document.scripts).find((el) => /_ds_bundle\.js(\?|$)/.test(el.src));
  return s ? new URL("assets/logo/", s.src).href : "assets/logo/";
}

const FILES = {
  lockup:   { color: "gaya-lockup-color.svg", reversed: "gaya-lockup-reversed.svg", white: "gaya-lockup-white.svg", black: "gaya-lockup-black.svg" },
  vertical: { color: "gaya-lockup-vertical-color.svg", reversed: "gaya-lockup-vertical-color.svg", white: "gaya-lockup-vertical-white.svg", black: "gaya-lockup-vertical-black.svg" },
  mark:     { color: "gaya-isotype-color.svg", reversed: "gaya-isotype-color.svg", white: "gaya-isotype-white.svg", black: "gaya-isotype-black.svg" },
  wordmark: { color: "gaya-wordmark-black.svg", orange: "gaya-wordmark-orange.svg", reversed: "gaya-wordmark-white.svg", white: "gaya-wordmark-white.svg", black: "gaya-wordmark-black.svg" },
};

export function Logo({
  variant = "lockup",   // "lockup" | "vertical" | "mark" | "wordmark"
  tone = "color",       // "color" | "reversed" | "white" | "black" | "orange" (wordmark only)
  size = 40,            // rendered height in px
  className = "",
  style = {},
  ...rest
}) {
  const set = FILES[variant] || FILES.lockup;
  const file = set[tone] || set.color;
  return (
    <img
      src={logoBase() + file}
      alt="GAYA"
      className={className}
      style={{ height: `${size}px`, width: "auto", display: "inline-block", verticalAlign: "middle", flex: "none", ...style }}
      draggable={false}
      {...rest}
    />
  );
}
