---
name: "gaya-linkedin-weekly"
description: Gaya's weekly call-to-LinkedIn pipeline. Pulls the week's Fireflies calls, extracts content-worthy moments with deep links, and drafts 2 LinkedIn posts per idea (Story + Framework, 3 hooks each) for the Gaya company page, founders and team. Use when asked to run the weekly content extraction, find content-worthy moments in calls, turn calls into LinkedIn posts, or draft Gaya LinkedIn content from customer conversations. Also used by the Friday 9 PM ET scheduled run.
---

# Gaya weekly calls → LinkedIn pipeline

Four stages, always in this order: **Extract → Review packet → Draft → Push to Buffer**. The output is one
weekly report plus Buffer idea cards.
Read `references/gaya-guardrails.md` before drafting anything, and `references/linkedin-playbook.md`
before writing hooks or bodies. Voices are in `references/voices.md`.

## Stage 1: Extract

**Window.** The 7 days ending at the run time (Friday 9:00 PM US Eastern → previous Friday 9:00 PM ET).
Rolling windows mean nothing falls between two runs. Convert to UTC for Fireflies filters (ET is UTC−4
in daylight time, UTC−5 in standard time).

**Pull.** `fireflies_get_transcripts` with `fromDate`/`toDate`, limit 50, paginate with `skip` until
empty. For every meeting, decide its coverage status before reading:
- `Silent Meeting: true` or no sentences → try `fireflies_fetch` once (it sometimes returns sentences
  when `get_transcript` doesn't). Still nothing → status **No transcript**.
- Personal/non-work entries (calendar placeholders, school events) → **Skipped: not a work call**.
- Hiring/compensation, pricing/contract negotiation, performance reviews, health, personal chat →
  **Excluded: sensitive**. Don't mine them, don't quote them.
- Everything else → read the full transcript (**Read**).

**What counts as a content-worthy moment** (look for these, in this order of value):
1. A customer describing a workaround or workflow they invented with Gaya.
2. A switching story (what they dropped, why, what changed).
3. A live reaction to the product (surprise, delight, "that's so cool").
4. A before/after that's visual (handwritten notes → filled carrier form).
5. A clear answer to a common objection or confusion (e.g. "does it log into carriers for me?").
6. A market observation a founder can comment on (how agencies/brokers actually work).
7. A product truth that builds trust (validation catches bad data, badges show what was touched).
8. Partner/integration news (gated until the partner approves).
9. Team and culture moments (where people work from, what onboarding looks like).

Skip: moments where the product failed during a demo (log them under "Product feedback" instead),
off-topic banter, anything that only makes sense with confidential context.

**Every idea must carry evidence**: call title + date, speaker (name and company), timestamp, deep
link `https://app.fireflies.ai/view/{transcriptId}?t={seconds}`, and a short excerpt in the
speaker's words (under 25 words). No excerpt, no idea. Never attribute a line to someone who didn't
say it: Fireflies speaker labels are sometimes wrong (e.g. one person labelled for two). If the label
looks wrong, say so in the idea's flags.

Aim for quality, not a quota. A quiet week with 4 strong ideas beats 12 weak ones.

## Stage 2: Review packet (this is how the user checks Stage 1)

For each idea record:
- **Title** (one line) and the **moment** in 2–3 sentences.
- **Evidence**: link(s) + excerpt + speaker.
- **Suggested author**: Gaya company page, a founder, or a named team member (see voices.md).
- **Funnel**: Know / Like / Trust (playbook §1).
- **Readiness**: Ready · Needs customer permission · Needs partner approval · Needs fact check · Internal only.
- **Flags**: anything touching guardrails (unapproved numbers, product claims to verify, names).

Plus, at the top of the report:
- **Coverage log**: a table of every meeting in the window: date, title, status (Read / No transcript
  / Skipped / Excluded), and ideas found. This is the proof nothing was missed.
- **Product feedback** (short list, internal): bugs, confusion, feature requests heard on calls, with links.

## Stage 3: Draft

For **every** idea that isn't "Internal only": write **2 drafts**.
- **Draft A: Story** (narrative, one moment, one lesson). Playbook §3.
- **Draft B: Framework** (steps, list, or questions the reader can use). Playbook §4.
- Each draft gets **3 hook options** (different hook templates, not rewordings) and **one body** that
  works under any of the three. So N ideas → 2N drafts → 6N hooks.
- Under each draft: suggested author, CTA or "no CTA" (TOF posts get none), and which guardrail
  checks it passed.
- **Visual decision (required):** pick the media for each draft with `references/visual-decision.md`
  (video, photo, screenshot, design or text only, in that order of preference) and record type, why,
  source/brief, who acts, consent and fallback. Only build a designed graphic when the decision lands
  on Design. When it lands on Video or a call frame, cut it from the Fireflies recording during the run.

Then run the **pre-ship checklist** (guardrails §6) on every draft and fix before output.

## Output

One report titled `Gaya LinkedIn — week of {Monday date}`:
1. Summary line (calls in window, read, ideas, drafts).
2. Coverage log.
3. Ideas (review packet), numbered.
4. Drafts, grouped by idea number (Idea 3 → 3A Story, 3B Framework), each with its visual decision.
   Put a one-table summary of all visual decisions (draft, media type, who acts, consent) at the top
   of this section so the week's asks to authors are clear.
5. Product feedback.

## Stage 4: Push to Buffer

Buffer workspace: **Gaya Content** (organizationId `6ab495a780316960c7ff55f0`). Column: **Unassigned**
(the board's default column for ideas with no group). Create every card there, even though its title
already names the suggested author from the Gaya team: humans assign the author and move cards through
Assigned, Drafting, Under Review, Validated and Published.

- One card per draft (2 per idea). Create them with `execute_mutation` → `createIdea` and **omit
  `group`** (no `groupId`) so the card lands in Unassigned, batching several aliases in one mutation.
- `services: ["linkedin"]`. Title: `{n}{A|B} · {Story|Framework} · {author} · {short idea name}`.
- Text layout, plain text, no markdown:
  `HOOK OPTIONS (keep one, delete the others)` → 3 numbered hooks → `POST` → body →
  a line of em dashes → `NOTES (delete before posting)` with suggested author, funnel, CTA, readiness,
  `Account:` the real customer/prospect names and companies behind the draft (the post itself stays
  anonymized; names live only in the notes so the team can use them once permission is given),
  Fireflies links, and the visual decision (type, who acts, consent, fallback).
- Skip ideas marked "Internal only".
- Images: attach only if you have a permanent public URL. Canva export links expire the same
  day and Buffer stores the link, not the file, so don't attach them. Instead, list the visuals
  and requests in the card notes; the team attaches images themselves.
- The connector can create cards but can't edit or delete them. Never create test cards; if a card
  is wrong, create the corrected one and flag the old title for manual deletion in the report.
- Don't create posts or schedule anything. Ideas only.

## Delivery

If Claude Docs tools are available, create it as a Claude Doc; otherwise write
`/mnt/user-data/outputs/gaya-linkedin-week-of-{YYYY-MM-DD}.md` and present it. On unattended runs,
don't ask questions: note open questions at the top of the report instead.
