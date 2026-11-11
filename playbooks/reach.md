# Reach playbook

Read this before any Reach task. CLAUDE.md still wins where the two disagree.

## Goal

Phase 1: get Gaya seen by more insurance professionals, and send them to gaya.ai.

Weekly numbers (from the sources in CLAUDE.md section 2):
- Organic impressions across the 8 Buffer accounts
- Website sessions from Organic Social, and from all organic channels
- Untracked share of website sessions (Direct + Unassigned), which should fall as UTMs spread

A post that gets impressions but no visits is half a win. Every post should give people a reason
to click through to a specific gaya.ai page.

## The accounts

| Account | Voice | Leans toward |
|---|---|---|
| Gaya · LinkedIn page | The company | Product in action, proof, launches, events, webinars |
| Carl Ziadé · LinkedIn | Co-founder, close to agencies | Agency workflow pain, lessons from customers, industry views |
| Jean-Pierre Vertil · LinkedIn | Co-founder, product and tech | How the product works, AI in insurance, what's shipping |
| Dana Zahreddine · LinkedIn | Team member | Behind the scenes, customer moments, events |
| getgaya · Instagram | The company | Short videos, carousels, team and event moments |
| Gaya Technologies · Facebook | The company | Re-cut of LinkedIn and Instagram posts; agency groups |
| trygaya · TikTok | The company | Short videos only: before/after, quick demos, trends adapted |
| getgaya · X | The company | Short takes, launch news, links to longer posts |

Posts for a person's own profile are drafts in their voice. They always need approval, and you
never publish as a person (CLAUDE.md section 8).

## Starting cadence

A starting point for Duvenson to adjust once there is data:

| Account | Posts per week |
|---|---|
| Gaya · LinkedIn page | 5 |
| Carl Ziadé · LinkedIn | 3 |
| Jean-Pierre Vertil · LinkedIn | 2 |
| Dana Zahreddine · LinkedIn | 2 |
| Instagram | 3 |
| TikTok | 3 |
| Facebook | 3 (mostly re-cuts) |
| X | 5 (short, mostly links) |

Never let an account go a full week without a draft in its queue.

## Content pillars

Rotate through these. No pillar takes more than 2 of an account's posts in a row.

1. **The rekeying tax.** Real agency workflow pain: typing the same client into 10 to 20 portals,
   renewal season, supplementals, schedules. Make the cost concrete in time.
2. **Product in action.** The Submission OS doing the work: a dec page becoming a client profile,
   a portal filling itself, Kee working the portals while the agent reviews. Only show what is
   live (CLAUDE.md, top of file).
3. **Proof.** Customer results and quotes from Fireflies calls. A customer's name, quote or logo
   needs that customer's approval first.
4. **Lines of business.** One angle per niche the website covers: high net worth, coastal homes,
   E&S, small business, middle market, trucking. Link to that niche's page.
5. **Founder point of view.** Carl and JP on where agencies and AI are going. Opinions, not hype.
6. **Moments.** Webinars, events, launches and podcast episodes, each with its own landing page.

## Where ideas come from

- **Fireflies:** the week's calls. Pull real phrases agents use, and the problems they describe.
- **Product updates and the roadmap hub:** what just shipped and what is coming.
- **The website:** each niche page and feature page is a post waiting to be written.
- **`references/`:** posts Duvenson likes. Copy the format, structure and hook style. Never copy
  their words.
- **What worked:** the top posts from the last Monday scorecard, and `learnings.md`.

## Quality bar

A draft goes to Buffer only if all of these are true:

- **The first line earns the second.** A specific claim, number, question or scene. Not
  "Excited to announce."
- **One idea per post.**
- **It sounds like an agency person wrote it.** Producers, AMs, CSRs, carriers, submissions,
  renewals. Plain language and short sentences (CLAUDE.md section 12).
- **One clear next step**, with a UTM-tagged link to the most relevant gaya.ai page.
- **Every claim is true today.** No invented numbers. A customer result needs its source call
  linked on the board task.
- **Visuals follow the gaya-design skill.** Gaya orange #EF5A24, Montserrat, flat 2D.
- **It fits the network.** LinkedIn: about 900 to 1,300 characters, line breaks, link in the post
  or first comment. Instagram and TikTok: the hook in the first 2 seconds and captions on screen.
  X: under 280 characters.

## UTM links

Every link to gaya.ai or the booking page in anything you draft (posts, ads, emails, bios, event
pages) carries UTM tags. No exceptions: untracked traffic is a Phase 1 number.

```
utm_source   = linkedin | instagram | facebook | tiktok | x | meta_ads | linkedin_ads | email | podcast | event
utm_medium   = organic_social | paid_social | email | referral | event
utm_campaign = <yyyy-mm>-<theme>          e.g. 2026-11-kee-launch, 2026-11-rekeying-tax
utm_content  = <account>-<post-slug>      e.g. carl-portal-fatigue, gaya-trucking-carousel
```

Lowercase, hyphens, no spaces. Write the full tagged link in the draft, and put the campaign name
on the board task so results can be traced back.

Example:
`https://gaya.ai/commercial-lines?utm_source=linkedin&utm_medium=organic_social&utm_campaign=2026-11-trucking&utm_content=gaya-trucking-carousel`

## Weekly loop

1. **Monday (with the scorecard):** propose the week's posts per account on the board: pillar,
   hook, target page and campaign name.
2. **During the week:** once the plan is approved, draft posts in Buffer as drafts, a few per run.
   Never schedule or publish. Link each draft on its board task.
3. **After 7 days:** read each post's results with Buffer `list_posts` (includeMetrics true) and
   the matching sessions in Google Analytics, by campaign.
4. **Learn:** write the top and bottom 3 into the next scorecard. When a test ends, add one rule to
   `learnings.md`.

## Experiments

- Change one thing at a time: the hook, the format, the posting time or the pillar.
- Run a test for at least 2 weeks or 6 posts before calling it.
- Log each experiment as a board task with Type = Experiment, a hypothesis and a success metric
  (impressions, engagement rate or website sessions).

## Paid creative

For Meta and LinkedIn ads, draft variations only: 3 hooks × 2 formats, each with UTM links
(`utm_medium=paid_social`). Never create, edit, launch or change budgets in an ad account. Ad
results come from the Percuity reads in CLAUDE.md section 2.
