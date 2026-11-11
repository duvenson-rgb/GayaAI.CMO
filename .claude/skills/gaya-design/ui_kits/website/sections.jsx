/* GAYA website UI kit — marketing page sections. */
const { Button, Badge, Avatar, Logo } = window.GAYADesignSystem_f55ce3;
const ClipboardPanel = window.SuperClipboard;

function Nav() {
  return (
    <nav className="nav">
      <div className="kit-wrap nav__row">
        <Logo size={38} />
        <div className="nav__links">
          <span className="nav__link">Product</span>
          <span className="nav__link">Carriers</span>
          <span className="nav__link">Pricing</span>
          <span className="nav__link">Resources</span>
          <span className="nav__link">Security</span>
        </div>
        <div className="nav__actions">
          <Button variant="ghost" size="sm">Sign in</Button>
          <Button variant="primary" size="sm" leadingIcon={<i data-lucide="chrome"></i>}>Add to Chrome</Button>
        </div>
      </div>
    </nav>
  );
}

function Hero() {
  return (
    <header className="hero">
      <div className="kit-wrap hero__grid">
        <div>
          <span className="gaya-eyebrow">AI Copilot for Insurance</span>
          <h1>Quote <em>10× faster</em> — no more retyping.</h1>
          <p className="hero__sub">
            Super Copy captures every field once. Super Paste autofills it across 500+ carrier
            portals, raters and AMS platforms — in a single click.
          </p>
          <div className="hero__cta">
            <Button variant="primary" size="lg" leadingIcon={<i data-lucide="chrome"></i>}>Add to Chrome — free</Button>
            <Button variant="secondary" size="lg" leadingIcon={<i data-lucide="play"></i>}>Watch demo</Button>
          </div>
          <div className="hero__trust">
            <span><i data-lucide="shield-check"></i> SOC 2 Type II</span>
            <span><i data-lucide="lock"></i> Bank-grade encryption</span>
            <span><i data-lucide="users"></i> Trusted by 1,000s of agents</span>
          </div>
        </div>
        <div className="hero__visual">
          <ClipboardPanel />
        </div>
      </div>
    </header>
  );
}

function Stats() {
  const data = [
    { n: "10×", l: "Faster quoting" },
    { n: "500+", l: "Carrier portals & raters" },
    { n: "80%", l: "Less data-entry time" },
    { n: "0", l: "Copy-paste errors" },
  ];
  return (
    <section className="stats">
      <div className="kit-wrap stats__row">
        {data.map((s) => (
          <div className="stat" key={s.l}>
            <div className="stat__n">{s.n}</div>
            <div className="stat__l">{s.l}</div>
          </div>
        ))}
      </div>
    </section>
  );
}

function HowItWorks() {
  const steps = [
    { num: "01", ico: "copy", tint: "var(--orange-50)", fg: "var(--brand)", t: "Super Copy", d: "Capture every field from a carrier portal, dec page or ACORD form in one click — no selecting, no retyping." },
    { num: "02", ico: "sparkles", tint: "var(--purple-50)", fg: "var(--accent-purple)", t: "Gaya understands it", d: "Our LLMs normalize names, dates, dropdowns and checkboxes, adapting automatically when carrier interfaces change." },
    { num: "03", ico: "clipboard-paste", tint: "var(--green-50)", fg: "var(--accent-green)", t: "Super Paste", d: "Autofill the next portal, rater or AMS instantly and accurately — every field placed in the right spot." },
  ];
  return (
    <section className="section">
      <div className="kit-wrap">
        <div className="section__head">
          <span className="gaya-eyebrow">How it works</span>
          <h2>Copy once. Paste everywhere.</h2>
          <p>Gaya works inside the tools you already use — your browser, your carrier portals, your AMS.</p>
        </div>
        <div className="steps">
          {steps.map((s) => (
            <div className="step" key={s.num}>
              <div className="step__ico" style={{ background: s.tint, color: s.fg }}>
                <i data-lucide={s.ico}></i>
              </div>
              <span className="step__num">{s.num}</span>
              <h3>{s.t}</h3>
              <p>{s.d}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function Testimonial() {
  return (
    <section className="quote gaya-purple-stage gaya-purple-stage--glow">
      <div className="quote__inner">
        <i data-lucide="quote" className="quote__mark"></i>
        <blockquote>
          A home-and-auto quote used to take me <em>17 minutes</em>. With Gaya it's down to <em>8</em>.
          That makes my life so much easier.
        </blockquote>
        <div className="quote__who">
          <Avatar name="Independent Agent" size="md" />
          <div style={{ textAlign: "left" }}>
            <div className="quote__who-name">Independent Agent</div>
            <div className="quote__who-role">Personal Lines · Texas</div>
          </div>
        </div>
      </div>
    </section>
  );
}

function CTA() {
  return (
    <section className="cta">
      <div className="kit-wrap">
        <div className="cta__card">
          <h2>Get your time back.</h2>
          <p>Join thousands of insurance professionals quoting faster with Gaya. Free to install — no setup, no friction.</p>
          <div style={{ display: "flex", gap: "var(--space-3)", justifyContent: "center" }}>
            <Button variant="secondary" size="lg" leadingIcon={<i data-lucide="chrome"></i>}>Add to Chrome</Button>
            <Button variant="ghost" size="lg" style={{ color: "#fff" }} trailingIcon={<i data-lucide="arrow-right"></i>}>Book a demo</Button>
          </div>
        </div>
      </div>
    </section>
  );
}

function Footer() {
  const cols = [
    { h: "Product", links: ["Super Copy", "Super Paste", "Integrations", "Security", "Pricing"] },
    { h: "Company", links: ["About", "Careers", "Blog", "Contact"] },
    { h: "Resources", links: ["Guides", "Help center", "API docs", "Status"] },
  ];
  return (
    <footer className="footer">
      <div className="kit-wrap">
        <div className="footer__row">
          <div>
            <Logo size={38} />
            <p className="footer__about">The AI copilot for insurance agents. Bringing the power of large language models to quoting and servicing.</p>
          </div>
          {cols.map((c) => (
            <div className="footer__col" key={c.h}>
              <h4>{c.h}</h4>
              {c.links.map((l) => <a key={l}>{l}</a>)}
            </div>
          ))}
        </div>
        <div className="footer__base">
          <span>© 2026 Gaya Technologies Inc. All rights reserved.</span>
          <span style={{ display: "flex", gap: "var(--space-4)" }}>
            <a href="#">Privacy</a><a href="#">Terms</a><a href="#">SOC 2</a>
          </span>
        </div>
      </div>
    </footer>
  );
}

window.GayaSite = { Nav, Hero, Stats, HowItWorks, Testimonial, CTA, Footer };
