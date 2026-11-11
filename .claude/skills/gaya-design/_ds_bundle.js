/* @ds-bundle: {"format":4,"namespace":"GAYADesignSystem_f55ce3","components":[{"name":"Logo","sourcePath":"components/brand/Logo.jsx"},{"name":"Button","sourcePath":"components/core/Button.jsx"},{"name":"IconButton","sourcePath":"components/core/IconButton.jsx"},{"name":"Avatar","sourcePath":"components/display/Avatar.jsx"},{"name":"Badge","sourcePath":"components/display/Badge.jsx"},{"name":"Card","sourcePath":"components/display/Card.jsx"},{"name":"Input","sourcePath":"components/forms/Input.jsx"},{"name":"Switch","sourcePath":"components/forms/Switch.jsx"},{"name":"AutofillField","sourcePath":"components/marketing/AutofillField.jsx"},{"name":"Stat","sourcePath":"components/marketing/Stat.jsx"},{"name":"StatRow","sourcePath":"components/marketing/Stat.jsx"},{"name":"StepCard","sourcePath":"components/marketing/StepCard.jsx"}],"sourceHashes":{"components/brand/Logo.jsx":"9b3474f7bc4d","components/core/Button.jsx":"5268588a37cc","components/core/IconButton.jsx":"bc2279021991","components/display/Avatar.jsx":"b3d836e2440c","components/display/Badge.jsx":"ece9c12e7f65","components/display/Card.jsx":"330c363d158f","components/forms/Input.jsx":"528d8985a2f8","components/forms/Switch.jsx":"a2f65a1704d0","components/marketing/AutofillField.jsx":"d7a38200b5b8","components/marketing/Stat.jsx":"bfbff658f515","components/marketing/StepCard.jsx":"aec287a49d5d","ui_kits/website/SuperClipboard.jsx":"2c1ffb667573","ui_kits/website/sections.jsx":"d5e51efe0447"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.GAYADesignSystem_f55ce3 = window.GAYADesignSystem_f55ce3 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/brand/Logo.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/*
 * GAYA logo — renders the official artwork from assets/logo/.
 * Asset URLs resolve relative to the loaded _ds_bundle.js, so the
 * logo works at any page depth (and in consuming projects that ship
 * assets/ next to the bundle).
 */
function logoBase() {
  if (typeof document === "undefined") return "assets/logo/";
  const s = Array.from(document.scripts).find(el => /_ds_bundle\.js(\?|$)/.test(el.src));
  return s ? new URL("assets/logo/", s.src).href : "assets/logo/";
}
const FILES = {
  lockup: {
    color: "gaya-lockup-color.svg",
    reversed: "gaya-lockup-reversed.svg",
    white: "gaya-lockup-white.svg",
    black: "gaya-lockup-black.svg"
  },
  vertical: {
    color: "gaya-lockup-vertical-color.svg",
    reversed: "gaya-lockup-vertical-color.svg",
    white: "gaya-lockup-vertical-white.svg",
    black: "gaya-lockup-vertical-black.svg"
  },
  mark: {
    color: "gaya-isotype-color.svg",
    reversed: "gaya-isotype-color.svg",
    white: "gaya-isotype-white.svg",
    black: "gaya-isotype-black.svg"
  },
  wordmark: {
    color: "gaya-wordmark-black.svg",
    orange: "gaya-wordmark-orange.svg",
    reversed: "gaya-wordmark-white.svg",
    white: "gaya-wordmark-white.svg",
    black: "gaya-wordmark-black.svg"
  }
};
function Logo({
  variant = "lockup",
  // "lockup" | "vertical" | "mark" | "wordmark"
  tone = "color",
  // "color" | "reversed" | "white" | "black" | "orange" (wordmark only)
  size = 40,
  // rendered height in px
  className = "",
  style = {},
  ...rest
}) {
  const set = FILES[variant] || FILES.lockup;
  const file = set[tone] || set.color;
  return /*#__PURE__*/React.createElement("img", _extends({
    src: logoBase() + file,
    alt: "GAYA",
    className: className,
    style: {
      height: `${size}px`,
      width: "auto",
      display: "inline-block",
      verticalAlign: "middle",
      flex: "none",
      ...style
    },
    draggable: false
  }, rest));
}
Object.assign(__ds_scope, { Logo });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/brand/Logo.jsx", error: String((e && e.message) || e) }); }

// components/core/Button.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * GAYA primary action control. Wraps a native <button>.
 */
function Button({
  variant = "primary",
  // primary | secondary | ghost | brandtint | danger
  size = "md",
  // sm | md | lg
  block = false,
  leadingIcon = null,
  trailingIcon = null,
  type = "button",
  className = "",
  children,
  ...rest
}) {
  const cls = ["gaya-btn", `gaya-btn--${variant}`, `gaya-btn--${size}`, block ? "gaya-btn--block" : "", className].filter(Boolean).join(" ");
  return /*#__PURE__*/React.createElement("button", _extends({
    type: type,
    className: cls
  }, rest), leadingIcon && /*#__PURE__*/React.createElement("span", {
    className: "gaya-btn__icon"
  }, leadingIcon), children && /*#__PURE__*/React.createElement("span", null, children), trailingIcon && /*#__PURE__*/React.createElement("span", {
    className: "gaya-btn__icon"
  }, trailingIcon));
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Button.jsx", error: String((e && e.message) || e) }); }

// components/core/IconButton.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Square icon-only button (toolbar actions, close buttons, etc.).
 * Always pass an accessible `aria-label`.
 */
function IconButton({
  size = "md",
  // sm | md | lg
  className = "",
  children,
  ...rest
}) {
  const cls = ["gaya-iconbtn", `gaya-iconbtn--${size}`, className].filter(Boolean).join(" ");
  return /*#__PURE__*/React.createElement("button", _extends({
    type: "button",
    className: cls
  }, rest), children);
}
Object.assign(__ds_scope, { IconButton });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/IconButton.jsx", error: String((e && e.message) || e) }); }

// components/display/Avatar.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/** GAYA avatar — image or initials fallback. */
function Avatar({
  size = "md",
  // sm | md | lg
  src = "",
  name = "",
  className = "",
  ...rest
}) {
  const initials = name.split(" ").map(w => w[0]).filter(Boolean).slice(0, 2).join("").toUpperCase();
  const cls = ["gaya-avatar", `gaya-avatar--${size}`, className].filter(Boolean).join(" ");
  return /*#__PURE__*/React.createElement("span", _extends({
    className: cls,
    "aria-label": name || undefined
  }, rest), src ? /*#__PURE__*/React.createElement("img", {
    src: src,
    alt: name
  }) : initials);
}
Object.assign(__ds_scope, { Avatar });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/display/Avatar.jsx", error: String((e && e.message) || e) }); }

// components/display/Badge.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/** GAYA badge / tag / status pill. */
function Badge({
  color = "neutral",
  // solid | neutral | orange | green | yellow | purple | outline
  dot = false,
  className = "",
  children,
  ...rest
}) {
  const cls = ["gaya-badge", `gaya-badge--${color}`, className].filter(Boolean).join(" ");
  return /*#__PURE__*/React.createElement("span", _extends({
    className: cls
  }, rest), dot && /*#__PURE__*/React.createElement("span", {
    className: "gaya-badge__dot"
  }), children);
}
Object.assign(__ds_scope, { Badge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/display/Badge.jsx", error: String((e && e.message) || e) }); }

// components/display/Card.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/** GAYA surface container. */
function Card({
  elevation = "outline",
  // outline | flat | raised
  padding = "md",
  // none | sm | md | lg
  interactive = false,
  as: Tag = "div",
  className = "",
  children,
  ...rest
}) {
  const cls = ["gaya-card", elevation === "flat" ? "gaya-card--flat" : "", elevation === "raised" ? "gaya-card--raised" : "", padding !== "none" ? `gaya-card--pad-${padding}` : "", interactive ? "gaya-card--interactive" : "", className].filter(Boolean).join(" ");
  return /*#__PURE__*/React.createElement(Tag, _extends({
    className: cls
  }, rest), children);
}
Object.assign(__ds_scope, { Card });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/display/Card.jsx", error: String((e && e.message) || e) }); }

// components/forms/Input.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
let _id = 0;

/**
 * GAYA text field with label, hint/error, and optional lead/trail affixes.
 */
function Input({
  label,
  hint,
  error,
  required = false,
  leadingAffix = null,
  trailingAffix = null,
  className = "",
  id,
  ...rest
}) {
  const fieldId = id || React.useMemo(() => `gaya-input-${++_id}`, [id]);
  const invalid = Boolean(error);
  const inputCls = ["gaya-input", leadingAffix ? "gaya-input--has-lead" : "", trailingAffix ? "gaya-input--has-trail" : "", invalid ? "gaya-input--invalid" : ""].filter(Boolean).join(" ");
  return /*#__PURE__*/React.createElement("div", {
    className: ["gaya-field", className].filter(Boolean).join(" ")
  }, label && /*#__PURE__*/React.createElement("label", {
    className: "gaya-label",
    htmlFor: fieldId
  }, label, required && /*#__PURE__*/React.createElement("span", {
    className: "gaya-label__req"
  }, "*")), /*#__PURE__*/React.createElement("div", {
    className: "gaya-input-wrap"
  }, leadingAffix && /*#__PURE__*/React.createElement("span", {
    className: "gaya-input__affix gaya-input__affix--lead"
  }, leadingAffix), /*#__PURE__*/React.createElement("input", _extends({
    id: fieldId,
    className: inputCls,
    "aria-invalid": invalid || undefined
  }, rest)), trailingAffix && /*#__PURE__*/React.createElement("span", {
    className: "gaya-input__affix gaya-input__affix--trail"
  }, trailingAffix)), (error || hint) && /*#__PURE__*/React.createElement("span", {
    className: ["gaya-hint", invalid ? "gaya-hint--error" : ""].filter(Boolean).join(" ")
  }, error || hint));
}
Object.assign(__ds_scope, { Input });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Input.jsx", error: String((e && e.message) || e) }); }

// components/forms/Switch.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/** GAYA on/off switch. Controlled or uncontrolled native checkbox. */
function Switch({
  label,
  className = "",
  ...rest
}) {
  return /*#__PURE__*/React.createElement("label", {
    className: ["gaya-switch", className].filter(Boolean).join(" ")
  }, /*#__PURE__*/React.createElement("input", _extends({
    type: "checkbox",
    role: "switch"
  }, rest)), /*#__PURE__*/React.createElement("span", {
    className: "gaya-switch__track"
  }, /*#__PURE__*/React.createElement("span", {
    className: "gaya-switch__thumb"
  })), label && /*#__PURE__*/React.createElement("span", {
    className: "gaya-switch__label"
  }, label));
}
Object.assign(__ds_scope, { Switch });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Switch.jsx", error: String((e && e.message) || e) }); }

// components/marketing/AutofillField.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function markSrc() {
  if (typeof document === "undefined") return "assets/logo/gaya-isotype-color.svg";
  const s = Array.from(document.scripts).find(el => /_ds_bundle\.js(\?|$)/.test(el.src));
  return s ? new URL("assets/logo/gaya-isotype-color.svg", s.src).href : "assets/logo/gaya-isotype-color.svg";
}

/** A form field shown as "filled by Gaya": orange-tinted value + isotype marker. The signature product motif. */
function AutofillField({
  label,
  value,
  filled = true,
  full = false,
  style = {},
  ...rest
}) {
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      display: "flex",
      flexDirection: "column",
      gap: 5,
      gridColumn: full ? "1 / -1" : undefined,
      minWidth: 0,
      ...style
    }
  }, rest), /*#__PURE__*/React.createElement("div", {
    style: {
      font: "600 10px/1.1 var(--font-accent)",
      letterSpacing: "0.08em",
      textTransform: "uppercase",
      color: "var(--neutral-500)"
    }
  }, label), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      gap: 8,
      height: 32,
      padding: "0 10px",
      borderRadius: 6,
      background: filled ? "var(--orange-50)" : "var(--neutral-0)",
      border: `1px solid ${filled ? "var(--orange-100)" : "var(--neutral-200)"}`,
      font: "500 13px/1 var(--font-mono)",
      color: filled ? "var(--neutral-900)" : "var(--neutral-400)",
      whiteSpace: "nowrap",
      overflow: "hidden"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      overflow: "hidden",
      textOverflow: "ellipsis"
    }
  }, value), filled && /*#__PURE__*/React.createElement("img", {
    src: markSrc(),
    alt: "",
    style: {
      height: 16,
      width: "auto",
      flex: "none"
    }
  })));
}
Object.assign(__ds_scope, { AutofillField });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/marketing/AutofillField.jsx", error: String((e && e.message) || e) }); }

// components/marketing/Stat.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/** Proof stat: big number + small caps label. Use in a row separated by hairlines. */
function Stat({
  value,
  label,
  tone = "ink",
  size = 48,
  style = {},
  ...rest
}) {
  const color = {
    ink: "var(--neutral-900)",
    orange: "var(--brand)",
    purple: "var(--purple-500)",
    white: "var(--white)"
  }[tone];
  const labelColor = tone === "white" ? "var(--neutral-300)" : "var(--neutral-600)";
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      display: "flex",
      flexDirection: "column",
      gap: 6,
      ...style
    }
  }, rest), /*#__PURE__*/React.createElement("div", {
    style: {
      font: `800 ${size}px/1 var(--font-display)`,
      letterSpacing: "-0.02em",
      color
    }
  }, value), /*#__PURE__*/React.createElement("div", {
    style: {
      font: `600 ${Math.max(11, Math.round(size * 0.26))}px/1.2 var(--font-accent)`,
      letterSpacing: "0.1em",
      textTransform: "uppercase",
      color: labelColor
    }
  }, label));
}

/** Row of Stats separated by hairline dividers. */
function StatRow({
  children,
  dark = false,
  style = {},
  ...rest
}) {
  const items = React.Children.toArray(children);
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      display: "flex",
      alignItems: "stretch",
      gap: 0,
      ...style
    }
  }, rest), items.map((c, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    style: {
      flex: 1,
      padding: "4px 28px",
      paddingLeft: i === 0 ? 0 : 28,
      borderLeft: i === 0 ? "none" : `1px solid ${dark ? "rgba(255,255,255,0.18)" : "var(--neutral-200)"}`
    }
  }, c)));
}
Object.assign(__ds_scope, { Stat, StatRow });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/marketing/Stat.jsx", error: String((e && e.message) || e) }); }

// components/marketing/StepCard.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/** Numbered flow step (Super Copy → Super Clipboard → Super Paste). `active` = the purple highlighted final step. */
function StepCard({
  n,
  title,
  children,
  active = false,
  style = {},
  ...rest
}) {
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      flex: 1,
      minWidth: 0,
      display: "flex",
      flexDirection: "column",
      gap: 8,
      padding: "18px 20px",
      borderRadius: "var(--radius-lg)",
      background: active ? "var(--purple-500)" : "var(--neutral-0)",
      border: active ? "1px solid var(--purple-500)" : "1px solid var(--neutral-200)",
      color: active ? "var(--white)" : "var(--neutral-900)",
      ...style
    }
  }, rest), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: 10
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 24,
      height: 24,
      borderRadius: "50%",
      display: "grid",
      placeItems: "center",
      flex: "none",
      background: active ? "var(--white)" : "var(--purple-500)",
      color: active ? "var(--purple-500)" : "var(--white)",
      font: "700 13px/1 var(--font-accent)"
    }
  }, n), /*#__PURE__*/React.createElement("span", {
    style: {
      font: "700 18px/1.2 var(--font-display)",
      letterSpacing: "-0.01em"
    }
  }, title)), /*#__PURE__*/React.createElement("div", {
    style: {
      font: "400 14px/1.45 var(--font-body)",
      color: active ? "var(--purple-50)" : "var(--neutral-600)"
    }
  }, children));
}
Object.assign(__ds_scope, { StepCard });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/marketing/StepCard.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/SuperClipboard.jsx
try { (() => {
/* ====================================================================
   GAYA UI Kit — interactive "Super Clipboard" product panel.
   The signature flow: Super Copy captures fields from a carrier portal,
   then Super Paste autofills the next one. This mirrors the real product
   surface (Chrome side panel) using the GAYA design-system primitives.
   ==================================================================== */
const {
  Badge: SCBadge,
  Button: SCButton,
  Logo: SCLogo
} = window.GAYADesignSystem_f55ce3;
const CAPTURED = [{
  k: "Insured name",
  v: "Maria Delgado",
  icon: "user"
}, {
  k: "Property address",
  v: "1487 Larkspur Ave, Austin TX",
  icon: "map-pin"
}, {
  k: "Year built",
  v: "2014",
  icon: "calendar"
}, {
  k: "Coverage A",
  v: "$420,000",
  icon: "shield"
}, {
  k: "Prior carrier",
  v: "Progressive",
  icon: "building-2"
}, {
  k: "Effective date",
  v: "2026-07-01",
  icon: "clock"
}];
function SuperClipboard() {
  // phases: idle -> copying -> captured -> pasting -> done
  const [phase, setPhase] = React.useState("idle");
  const [visible, setVisible] = React.useState(0);
  React.useEffect(() => {
    let t;
    if (phase === "copying") {
      setVisible(0);
      const tick = i => {
        setVisible(i);
        if (i < CAPTURED.length) t = setTimeout(() => tick(i + 1), 230);else t = setTimeout(() => setPhase("captured"), 260);
      };
      tick(1);
    } else if (phase === "pasting") {
      t = setTimeout(() => setPhase("done"), 1500);
    }
    return () => clearTimeout(t);
  }, [phase]);
  React.useEffect(() => {
    if (window.lucide) window.lucide.createIcons();
  });
  const reset = () => {
    setPhase("idle");
    setVisible(0);
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "sc"
  }, /*#__PURE__*/React.createElement("header", {
    className: "sc__bar"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sc__bar-left"
  }, /*#__PURE__*/React.createElement(SCLogo, {
    variant: "mark",
    size: 26
  }), /*#__PURE__*/React.createElement("span", {
    className: "sc__title"
  }, "Super Clipboard")), /*#__PURE__*/React.createElement("div", {
    className: "sc__bar-right"
  }, /*#__PURE__*/React.createElement(SCBadge, {
    color: "green",
    dot: true
  }, "Connected"), /*#__PURE__*/React.createElement("i", {
    "data-lucide": "more-horizontal",
    className: "sc__more"
  }))), /*#__PURE__*/React.createElement("div", {
    className: "sc__context"
  }, /*#__PURE__*/React.createElement("i", {
    "data-lucide": "globe"
  }), /*#__PURE__*/React.createElement("span", null, "portal.progressive-agent.com"), /*#__PURE__*/React.createElement("span", {
    className: "sc__tag"
  }, "Source")), /*#__PURE__*/React.createElement("div", {
    className: "sc__body"
  }, phase === "idle" && /*#__PURE__*/React.createElement("div", {
    className: "sc__empty"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sc__empty-ico"
  }, /*#__PURE__*/React.createElement("i", {
    "data-lucide": "clipboard-list"
  })), /*#__PURE__*/React.createElement("p", {
    className: "sc__empty-title"
  }, "Clipboard is empty"), /*#__PURE__*/React.createElement("p", {
    className: "sc__empty-sub"
  }, "Run Super Copy on a carrier portal, dec page or ACORD form to capture every field at once.")), phase !== "idle" && /*#__PURE__*/React.createElement("ul", {
    className: "sc__fields"
  }, CAPTURED.map((f, i) => {
    const shown = phase === "copying" ? i < visible : true;
    return /*#__PURE__*/React.createElement("li", {
      key: f.k,
      className: "sc__field" + (shown ? " is-in" : "")
    }, /*#__PURE__*/React.createElement("span", {
      className: "sc__field-ico"
    }, /*#__PURE__*/React.createElement("i", {
      "data-lucide": f.icon
    })), /*#__PURE__*/React.createElement("span", {
      className: "sc__field-text"
    }, /*#__PURE__*/React.createElement("span", {
      className: "sc__field-k"
    }, f.k), /*#__PURE__*/React.createElement("span", {
      className: "sc__field-v"
    }, f.v)), (phase === "captured" || phase === "pasting" || phase === "done") && /*#__PURE__*/React.createElement("i", {
      "data-lucide": phase === "done" ? "check-check" : "check",
      className: "sc__field-check"
    }));
  }))), (phase === "captured" || phase === "pasting" || phase === "done") && /*#__PURE__*/React.createElement("div", {
    className: "sc__dest"
  }, /*#__PURE__*/React.createElement("i", {
    "data-lucide": "globe"
  }), /*#__PURE__*/React.createElement("span", null, "app.ezlynx.com/rating"), /*#__PURE__*/React.createElement("span", {
    className: "sc__tag sc__tag--dest"
  }, "Target")), /*#__PURE__*/React.createElement("footer", {
    className: "sc__foot"
  }, phase === "idle" && /*#__PURE__*/React.createElement(SCButton, {
    variant: "primary",
    block: true,
    leadingIcon: /*#__PURE__*/React.createElement("i", {
      "data-lucide": "copy"
    }),
    onClick: () => setPhase("copying")
  }, "Super Copy"), phase === "copying" && /*#__PURE__*/React.createElement(SCButton, {
    variant: "primary",
    block: true,
    disabled: true,
    leadingIcon: /*#__PURE__*/React.createElement("i", {
      "data-lucide": "loader"
    })
  }, "Capturing ", visible, "/", CAPTURED.length, "\u2026"), phase === "captured" && /*#__PURE__*/React.createElement("div", {
    className: "sc__foot-row"
  }, /*#__PURE__*/React.createElement(SCButton, {
    variant: "secondary",
    leadingIcon: /*#__PURE__*/React.createElement("i", {
      "data-lucide": "rotate-ccw"
    }),
    onClick: reset
  }, "Clear"), /*#__PURE__*/React.createElement(SCButton, {
    variant: "primary",
    block: true,
    leadingIcon: /*#__PURE__*/React.createElement("i", {
      "data-lucide": "clipboard-paste"
    }),
    onClick: () => setPhase("pasting")
  }, "Super Paste")), phase === "pasting" && /*#__PURE__*/React.createElement(SCButton, {
    variant: "primary",
    block: true,
    disabled: true,
    leadingIcon: /*#__PURE__*/React.createElement("i", {
      "data-lucide": "loader"
    })
  }, "Filling EZLynx\u2026"), phase === "done" && /*#__PURE__*/React.createElement("div", {
    className: "sc__done"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sc__done-msg"
  }, /*#__PURE__*/React.createElement("i", {
    "data-lucide": "circle-check-big"
  }), " 6 fields placed \xB7 0 errors"), /*#__PURE__*/React.createElement(SCButton, {
    variant: "brandtint",
    block: true,
    leadingIcon: /*#__PURE__*/React.createElement("i", {
      "data-lucide": "rotate-ccw"
    }),
    onClick: reset
  }, "Start another quote"))));
}
window.SuperClipboard = SuperClipboard;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/SuperClipboard.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/sections.jsx
try { (() => {
/* GAYA website UI kit — marketing page sections. */
const {
  Button,
  Badge,
  Avatar,
  Logo
} = window.GAYADesignSystem_f55ce3;
const ClipboardPanel = window.SuperClipboard;
function Nav() {
  return /*#__PURE__*/React.createElement("nav", {
    className: "nav"
  }, /*#__PURE__*/React.createElement("div", {
    className: "kit-wrap nav__row"
  }, /*#__PURE__*/React.createElement(Logo, {
    size: 38
  }), /*#__PURE__*/React.createElement("div", {
    className: "nav__links"
  }, /*#__PURE__*/React.createElement("span", {
    className: "nav__link"
  }, "Product"), /*#__PURE__*/React.createElement("span", {
    className: "nav__link"
  }, "Carriers"), /*#__PURE__*/React.createElement("span", {
    className: "nav__link"
  }, "Pricing"), /*#__PURE__*/React.createElement("span", {
    className: "nav__link"
  }, "Resources"), /*#__PURE__*/React.createElement("span", {
    className: "nav__link"
  }, "Security")), /*#__PURE__*/React.createElement("div", {
    className: "nav__actions"
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "ghost",
    size: "sm"
  }, "Sign in"), /*#__PURE__*/React.createElement(Button, {
    variant: "primary",
    size: "sm",
    leadingIcon: /*#__PURE__*/React.createElement("i", {
      "data-lucide": "chrome"
    })
  }, "Add to Chrome"))));
}
function Hero() {
  return /*#__PURE__*/React.createElement("header", {
    className: "hero"
  }, /*#__PURE__*/React.createElement("div", {
    className: "kit-wrap hero__grid"
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("span", {
    className: "gaya-eyebrow"
  }, "AI Copilot for Insurance"), /*#__PURE__*/React.createElement("h1", null, "Quote ", /*#__PURE__*/React.createElement("em", null, "10\xD7 faster"), " \u2014 no more retyping."), /*#__PURE__*/React.createElement("p", {
    className: "hero__sub"
  }, "Super Copy captures every field once. Super Paste autofills it across 500+ carrier portals, raters and AMS platforms \u2014 in a single click."), /*#__PURE__*/React.createElement("div", {
    className: "hero__cta"
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "primary",
    size: "lg",
    leadingIcon: /*#__PURE__*/React.createElement("i", {
      "data-lucide": "chrome"
    })
  }, "Add to Chrome \u2014 free"), /*#__PURE__*/React.createElement(Button, {
    variant: "secondary",
    size: "lg",
    leadingIcon: /*#__PURE__*/React.createElement("i", {
      "data-lucide": "play"
    })
  }, "Watch demo")), /*#__PURE__*/React.createElement("div", {
    className: "hero__trust"
  }, /*#__PURE__*/React.createElement("span", null, /*#__PURE__*/React.createElement("i", {
    "data-lucide": "shield-check"
  }), " SOC 2 Type II"), /*#__PURE__*/React.createElement("span", null, /*#__PURE__*/React.createElement("i", {
    "data-lucide": "lock"
  }), " Bank-grade encryption"), /*#__PURE__*/React.createElement("span", null, /*#__PURE__*/React.createElement("i", {
    "data-lucide": "users"
  }), " Trusted by 1,000s of agents"))), /*#__PURE__*/React.createElement("div", {
    className: "hero__visual"
  }, /*#__PURE__*/React.createElement(ClipboardPanel, null))));
}
function Stats() {
  const data = [{
    n: "10×",
    l: "Faster quoting"
  }, {
    n: "500+",
    l: "Carrier portals & raters"
  }, {
    n: "80%",
    l: "Less data-entry time"
  }, {
    n: "0",
    l: "Copy-paste errors"
  }];
  return /*#__PURE__*/React.createElement("section", {
    className: "stats"
  }, /*#__PURE__*/React.createElement("div", {
    className: "kit-wrap stats__row"
  }, data.map(s => /*#__PURE__*/React.createElement("div", {
    className: "stat",
    key: s.l
  }, /*#__PURE__*/React.createElement("div", {
    className: "stat__n"
  }, s.n), /*#__PURE__*/React.createElement("div", {
    className: "stat__l"
  }, s.l)))));
}
function HowItWorks() {
  const steps = [{
    num: "01",
    ico: "copy",
    tint: "var(--orange-50)",
    fg: "var(--brand)",
    t: "Super Copy",
    d: "Capture every field from a carrier portal, dec page or ACORD form in one click — no selecting, no retyping."
  }, {
    num: "02",
    ico: "sparkles",
    tint: "var(--purple-50)",
    fg: "var(--accent-purple)",
    t: "Gaya understands it",
    d: "Our LLMs normalize names, dates, dropdowns and checkboxes, adapting automatically when carrier interfaces change."
  }, {
    num: "03",
    ico: "clipboard-paste",
    tint: "var(--green-50)",
    fg: "var(--accent-green)",
    t: "Super Paste",
    d: "Autofill the next portal, rater or AMS instantly and accurately — every field placed in the right spot."
  }];
  return /*#__PURE__*/React.createElement("section", {
    className: "section"
  }, /*#__PURE__*/React.createElement("div", {
    className: "kit-wrap"
  }, /*#__PURE__*/React.createElement("div", {
    className: "section__head"
  }, /*#__PURE__*/React.createElement("span", {
    className: "gaya-eyebrow"
  }, "How it works"), /*#__PURE__*/React.createElement("h2", null, "Copy once. Paste everywhere."), /*#__PURE__*/React.createElement("p", null, "Gaya works inside the tools you already use \u2014 your browser, your carrier portals, your AMS.")), /*#__PURE__*/React.createElement("div", {
    className: "steps"
  }, steps.map(s => /*#__PURE__*/React.createElement("div", {
    className: "step",
    key: s.num
  }, /*#__PURE__*/React.createElement("div", {
    className: "step__ico",
    style: {
      background: s.tint,
      color: s.fg
    }
  }, /*#__PURE__*/React.createElement("i", {
    "data-lucide": s.ico
  })), /*#__PURE__*/React.createElement("span", {
    className: "step__num"
  }, s.num), /*#__PURE__*/React.createElement("h3", null, s.t), /*#__PURE__*/React.createElement("p", null, s.d))))));
}
function Testimonial() {
  return /*#__PURE__*/React.createElement("section", {
    className: "quote gaya-purple-stage gaya-purple-stage--glow"
  }, /*#__PURE__*/React.createElement("div", {
    className: "quote__inner"
  }, /*#__PURE__*/React.createElement("i", {
    "data-lucide": "quote",
    className: "quote__mark"
  }), /*#__PURE__*/React.createElement("blockquote", null, "A home-and-auto quote used to take me ", /*#__PURE__*/React.createElement("em", null, "17 minutes"), ". With Gaya it's down to ", /*#__PURE__*/React.createElement("em", null, "8"), ". That makes my life so much easier."), /*#__PURE__*/React.createElement("div", {
    className: "quote__who"
  }, /*#__PURE__*/React.createElement(Avatar, {
    name: "Independent Agent",
    size: "md"
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      textAlign: "left"
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "quote__who-name"
  }, "Independent Agent"), /*#__PURE__*/React.createElement("div", {
    className: "quote__who-role"
  }, "Personal Lines \xB7 Texas")))));
}
function CTA() {
  return /*#__PURE__*/React.createElement("section", {
    className: "cta"
  }, /*#__PURE__*/React.createElement("div", {
    className: "kit-wrap"
  }, /*#__PURE__*/React.createElement("div", {
    className: "cta__card"
  }, /*#__PURE__*/React.createElement("h2", null, "Get your time back."), /*#__PURE__*/React.createElement("p", null, "Join thousands of insurance professionals quoting faster with Gaya. Free to install \u2014 no setup, no friction."), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: "var(--space-3)",
      justifyContent: "center"
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "secondary",
    size: "lg",
    leadingIcon: /*#__PURE__*/React.createElement("i", {
      "data-lucide": "chrome"
    })
  }, "Add to Chrome"), /*#__PURE__*/React.createElement(Button, {
    variant: "ghost",
    size: "lg",
    style: {
      color: "#fff"
    },
    trailingIcon: /*#__PURE__*/React.createElement("i", {
      "data-lucide": "arrow-right"
    })
  }, "Book a demo")))));
}
function Footer() {
  const cols = [{
    h: "Product",
    links: ["Super Copy", "Super Paste", "Integrations", "Security", "Pricing"]
  }, {
    h: "Company",
    links: ["About", "Careers", "Blog", "Contact"]
  }, {
    h: "Resources",
    links: ["Guides", "Help center", "API docs", "Status"]
  }];
  return /*#__PURE__*/React.createElement("footer", {
    className: "footer"
  }, /*#__PURE__*/React.createElement("div", {
    className: "kit-wrap"
  }, /*#__PURE__*/React.createElement("div", {
    className: "footer__row"
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(Logo, {
    size: 38
  }), /*#__PURE__*/React.createElement("p", {
    className: "footer__about"
  }, "The AI copilot for insurance agents. Bringing the power of large language models to quoting and servicing.")), cols.map(c => /*#__PURE__*/React.createElement("div", {
    className: "footer__col",
    key: c.h
  }, /*#__PURE__*/React.createElement("h4", null, c.h), c.links.map(l => /*#__PURE__*/React.createElement("a", {
    key: l
  }, l))))), /*#__PURE__*/React.createElement("div", {
    className: "footer__base"
  }, /*#__PURE__*/React.createElement("span", null, "\xA9 2026 Gaya Technologies Inc. All rights reserved."), /*#__PURE__*/React.createElement("span", {
    style: {
      display: "flex",
      gap: "var(--space-4)"
    }
  }, /*#__PURE__*/React.createElement("a", {
    href: "#"
  }, "Privacy"), /*#__PURE__*/React.createElement("a", {
    href: "#"
  }, "Terms"), /*#__PURE__*/React.createElement("a", {
    href: "#"
  }, "SOC 2")))));
}
window.GayaSite = {
  Nav,
  Hero,
  Stats,
  HowItWorks,
  Testimonial,
  CTA,
  Footer
};
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/sections.jsx", error: String((e && e.message) || e) }); }

__ds_ns.Logo = __ds_scope.Logo;

__ds_ns.Button = __ds_scope.Button;

__ds_ns.IconButton = __ds_scope.IconButton;

__ds_ns.Avatar = __ds_scope.Avatar;

__ds_ns.Badge = __ds_scope.Badge;

__ds_ns.Card = __ds_scope.Card;

__ds_ns.Input = __ds_scope.Input;

__ds_ns.Switch = __ds_scope.Switch;

__ds_ns.AutofillField = __ds_scope.AutofillField;

__ds_ns.Stat = __ds_scope.Stat;

__ds_ns.StatRow = __ds_scope.StatRow;

__ds_ns.StepCard = __ds_scope.StepCard;

})();
