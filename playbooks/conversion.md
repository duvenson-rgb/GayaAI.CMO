# Conversion playbook

Goal: turn qualified contacts into demos that happen. Autonomy: see the table in CLAUDE.md section 8.

> Starter version written from CLAUDE.md. Duvenson owns this playbook. Tighten it as results come in.

## Metrics
- Quantity: demos booked from marketing sources
- Quality: show rate; % that sales marks qualified after the demo

## Workflows

### Website conversion audit
1. Walk the path from a landing page to a booked demo, on desktop and mobile.
2. Check for broken links, slow pages, form friction, a clear CTA, and that the booking flow works.
3. Write up the problems with screenshots and propose A/B tests. Each test gets a hypothesis, one
   variable, a success metric and the sample it needs.
4. Vercel is read only. Never deploy or change the site.

### Lifecycle and nurture email tests
- Test one thing at a time: subject, hook or CTA.
- Compare against the email's current benchmark. Drafts only.
- Don't start a new test on an email while one is still running (CLAUDE.md section 5).

### Handoff quality
- Every marketing lead that reaches sales in Attio has a source, rubric score, premium estimate
  and one line of context (what they engaged with).
- Flag gaps in an Attio note. Never edit sales-owned fields.

## Quality bar (check before you deliver)
- [ ] Every finding has evidence (screenshot, link or number with its source).
- [ ] Every test proposal has a hypothesis and a success metric.
- [ ] Claims and ROI numbers on pages or emails are flagged for approval.
- [ ] Nothing was deployed or sent.
