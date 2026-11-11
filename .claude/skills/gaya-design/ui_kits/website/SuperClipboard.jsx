/* ====================================================================
   GAYA UI Kit — interactive "Super Clipboard" product panel.
   The signature flow: Super Copy captures fields from a carrier portal,
   then Super Paste autofills the next one. This mirrors the real product
   surface (Chrome side panel) using the GAYA design-system primitives.
   ==================================================================== */
const { Badge: SCBadge, Button: SCButton, Logo: SCLogo } = window.GAYADesignSystem_f55ce3;

const CAPTURED = [
  { k: "Insured name", v: "Maria Delgado", icon: "user" },
  { k: "Property address", v: "1487 Larkspur Ave, Austin TX", icon: "map-pin" },
  { k: "Year built", v: "2014", icon: "calendar" },
  { k: "Coverage A", v: "$420,000", icon: "shield" },
  { k: "Prior carrier", v: "Progressive", icon: "building-2" },
  { k: "Effective date", v: "2026-07-01", icon: "clock" },
];

function SuperClipboard() {
  // phases: idle -> copying -> captured -> pasting -> done
  const [phase, setPhase] = React.useState("idle");
  const [visible, setVisible] = React.useState(0);

  React.useEffect(() => {
    let t;
    if (phase === "copying") {
      setVisible(0);
      const tick = (i) => {
        setVisible(i);
        if (i < CAPTURED.length) t = setTimeout(() => tick(i + 1), 230);
        else t = setTimeout(() => setPhase("captured"), 260);
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

  const reset = () => { setPhase("idle"); setVisible(0); };

  return (
    <div className="sc">
      <header className="sc__bar">
        <div className="sc__bar-left">
          <SCLogo variant="mark" size={26} />
          <span className="sc__title">Super Clipboard</span>
        </div>
        <div className="sc__bar-right">
          <SCBadge color="green" dot>Connected</SCBadge>
          <i data-lucide="more-horizontal" className="sc__more"></i>
        </div>
      </header>

      <div className="sc__context">
        <i data-lucide="globe"></i>
        <span>portal.progressive-agent.com</span>
        <span className="sc__tag">Source</span>
      </div>

      <div className="sc__body">
        {phase === "idle" && (
          <div className="sc__empty">
            <div className="sc__empty-ico"><i data-lucide="clipboard-list"></i></div>
            <p className="sc__empty-title">Clipboard is empty</p>
            <p className="sc__empty-sub">Run Super Copy on a carrier portal, dec page or ACORD form to capture every field at once.</p>
          </div>
        )}

        {phase !== "idle" && (
          <ul className="sc__fields">
            {CAPTURED.map((f, i) => {
              const shown = phase === "copying" ? i < visible : true;
              return (
                <li key={f.k} className={"sc__field" + (shown ? " is-in" : "")}>
                  <span className="sc__field-ico"><i data-lucide={f.icon}></i></span>
                  <span className="sc__field-text">
                    <span className="sc__field-k">{f.k}</span>
                    <span className="sc__field-v">{f.v}</span>
                  </span>
                  {(phase === "captured" || phase === "pasting" || phase === "done") && (
                    <i data-lucide={phase === "done" ? "check-check" : "check"} className="sc__field-check"></i>
                  )}
                </li>
              );
            })}
          </ul>
        )}
      </div>

      {(phase === "captured" || phase === "pasting" || phase === "done") && (
        <div className="sc__dest">
          <i data-lucide="globe"></i>
          <span>app.ezlynx.com/rating</span>
          <span className="sc__tag sc__tag--dest">Target</span>
        </div>
      )}

      <footer className="sc__foot">
        {phase === "idle" && (
          <SCButton variant="primary" block leadingIcon={<i data-lucide="copy"></i>} onClick={() => setPhase("copying")}>
            Super Copy
          </SCButton>
        )}
        {phase === "copying" && (
          <SCButton variant="primary" block disabled leadingIcon={<i data-lucide="loader"></i>}>
            Capturing {visible}/{CAPTURED.length}…
          </SCButton>
        )}
        {phase === "captured" && (
          <div className="sc__foot-row">
            <SCButton variant="secondary" leadingIcon={<i data-lucide="rotate-ccw"></i>} onClick={reset}>Clear</SCButton>
            <SCButton variant="primary" block leadingIcon={<i data-lucide="clipboard-paste"></i>} onClick={() => setPhase("pasting")}>
              Super Paste
            </SCButton>
          </div>
        )}
        {phase === "pasting" && (
          <SCButton variant="primary" block disabled leadingIcon={<i data-lucide="loader"></i>}>
            Filling EZLynx…
          </SCButton>
        )}
        {phase === "done" && (
          <div className="sc__done">
            <div className="sc__done-msg"><i data-lucide="circle-check-big"></i> 6 fields placed · 0 errors</div>
            <SCButton variant="brandtint" block leadingIcon={<i data-lucide="rotate-ccw"></i>} onClick={reset}>Start another quote</SCButton>
          </div>
        )}
      </footer>
    </div>
  );
}

window.SuperClipboard = SuperClipboard;
