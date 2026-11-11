---
name: ishikawa-method
description: Root-cause analysis using the Ishikawa (fishbone / cause-and-effect / diagramme d'Ishikawa / arêtes de poisson) method combined with the 5 Whys. Use this skill whenever the user wants to attack a problem, find out why something is happening or keeps going wrong, diagnose a drop in a metric (conversion, churn, activation, revenue, response rate, quality), run a postmortem or retro, or asks for a fishbone, Ishikawa, 6M, 5 Whys or root cause — even if they only say "why is X happening?", "help me figure out what's wrong with Y", "attack this problem" or "Ishikawa this". Produces a precise problem statement, a fishbone diagram, scored root causes, and an action plan.
---

# Ishikawa Method

A structured way to attack a problem: define it precisely, map every plausible cause by family, drill each cause down to its root with the 5 Whys, score what matters, and turn the top root causes into an action plan.

The point of the method is to stop the team from jumping to the first obvious explanation. Treat every cause as a hypothesis until evidence supports it.

## Choose the mode

**Workshop mode** (default when the problem is vague, high-stakes, or the user wants to think it through): go step by step with the user. Ask one question at a time, propose drafts they can react to, and move on once they confirm. Use tappable-choice tools when they exist.

**Fast mode** (when the user gives rich context or says "just run it"): run all 7 steps in one pass. Label every assumption clearly, and end with the facts that would confirm or kill the top causes.

Whichever mode, Step 2 is a gate: if the problem statement is too vague to analyze, sharpen it before anything else. Propose a precise version and confirm it rather than asking the user to write it from scratch.

## The 7 steps

### 1. Assemble the team (Créer l'équipe de travail)

Identify who touches the problem: the people doing the work, the people affected, the people who own the levers. Ask the user who's involved, and flag missing perspectives ("Nobody from support is in this — they see the complaints first"). In a solo session, Claude plays devil's advocate for the missing roles.

### 2. Define the problem precisely (Définir le problème avec précision)

A good problem statement is specific, measurable and contains no cause. Use this template:

> **[What]** is **[current state]** instead of **[expected/baseline]**, in **[where/scope]**, since **[when]**, costing **[impact]**.

- Bad: "Sales are bad." / "Onboarding doesn't work because the CSM is overloaded." (the second hides a cause)
- Good: "Demo-to-close rate fell from 30% to 18% for small-business accounts since August, costing ~$40k MRR in Q3."

If numbers are unknown, write the statement with placeholders and list what data to pull. Separate the problem from its symptoms: symptoms often become causes on the diagram.

### 3. Inventory possible causes (Dresser un inventaire des causes possibles)

Brainstorm broadly before judging. Aim for at least 2–3 causes per family, and push into families the user hasn't mentioned — the overlooked family is often where the answer hides. Mark each cause as **fact** (observed, with evidence) or **hypothesis** (plausible, unverified).

### 4. Classify causes into families (Classifier les causes par familles)

Pick the family set that fits the domain. The classic is **6M**: Method (Méthode), Materials (Matière), Manpower (Main-d'œuvre), Machines (Matériel), Environment (Milieu), Measurement (Mesure). Many infographics drop Measurement — keep it; it's where "we didn't notice" problems live.

For non-manufacturing problems, read `references/cause-families.md` and pick or adapt a set (SaaS/GTM, customer success, marketing 8P, service 4S, software incidents, personal productivity). Use 4–7 families. If a cause fits two families, put it where the fix would be made.

### 5. Apply the 5 Whys (Appliquer la méthode des "5 pourquoi ?")

For each cause worth pursuing, ask "why?" repeatedly until you reach a cause that is **actionable and within the team's control**. Five is a guide, not a rule — stop at 3 if you've hit the root, go to 6 if you haven't.

Rules for a sound chain:
- Each "because" must actually cause the line above it. Read the chain backwards with "therefore" to check.
- When a "why" has two genuine answers, branch rather than picking one.
- "Human error", "lack of time" and "bad luck" are never root causes. Ask why the system let the error happen, or why the time went elsewhere.
- Stop going deeper when the next answer is outside anyone's control ("the economy") — the root is the last controllable link above it.
- Prefer evidence over plausible stories; note where a link is assumed.

### 6. Evaluate the most relevant causes (Évaluer les causes les plus pertinentes)

Score each root cause 1–5 on three axes:
- **Impact** — how much of the problem it explains if true
- **Evidence** — how strongly facts support it (1 = pure guess, 5 = confirmed by data)
- **Control** — how much the team can act on it

**Priority score = Impact × Evidence × Control ÷ 25**, giving a 0–5 scale (matches the star ratings on classic Ishikawa infographics). Round to the nearest 0.5.

Special case: **high Impact + low Evidence = "investigate first"**, not "ignore". Give it a validation test (what data or experiment would confirm it in days, not months) before spending on a fix.

### 7. Build the action plan (Établir le plan d'actions)

For the top 2–3 root causes, define actions with:
- **Type** — Contain (stop the bleeding now), Fix (remove the root cause), or Prevent (stop it recurring: process, guardrail, metric)
- **Owner**, **deadline**, and a **success metric** tied back to the problem statement
- How you'll know the fix worked (re-measure the metric from Step 2)

Don't fix everything. A focused plan on the highest-scored roots beats a long list nobody owns.

## Deliverable

At the end of the analysis (or at each step, in workshop mode), present:

1. **Problem statement** — the confirmed version from Step 2
2. **Fishbone diagram** — render it visually (see below)
3. **Cause table** — Family · Cause · Why-chain (condensed) · Root cause · I / E / C · Score
4. **Top root causes** — 2–3, each with its validation test
5. **Action plan table** — Action · Root cause addressed · Type · Owner · Due · Success metric
6. **Open questions & assumptions** — what's unverified and how to check it

Write in the user's language. If the user works in French, use the French family and step names.

### Rendering the fishbone

Use the bundled renderer for a clean, consistent diagram. Write a JSON spec, then run:

```bash
python scripts/render_fishbone.py spec.json fishbone.svg
```

Spec format:

```json
{
  "title": "Optional title",
  "problem": "Demo-to-close rate fell from 30% to 18% since August",
  "highlight_top": 2,
  "families": [
    {"name": "Method", "causes": [
      {"cause": "Same demo for every customer segment", "root": "No demo playbook by segment", "score": 4.5}
    ]}
  ]
}
```

`score` is optional; `highlight_top` colors the N highest-scored causes red as priorities. Keep cause and root text short (under ~60 characters) so the diagram stays readable — the full detail lives in the cause table. For a French diagram, add `"labels": {"root": "Cause racine", "legend": "Score = Impact × Preuves × Contrôle ÷ 25 (0–5) · Rouge = causes prioritaires"}`. Present the SVG to the user as a file, or show it inline if a tool for inline visuals is available. If no code execution is available, draw the fishbone as an indented text tree instead.

## Worked example (condensed)

**Problem:** 28% of online orders shipped late in October, against a target under 5%, generating a spike in refund requests.

- **Method** → Orders packed in arrival order, not by ship deadline → why? no prioritization rule → why? process never updated when same-day shipping launched → **root: picking process not redesigned for the same-day promise** (I5 E4 C5 → 4.0)
- **Measurement** → Late orders noticed only through complaints → why? on-time dispatch isn't tracked daily → **root: no leading indicator of delays** (I4 E5 C5 → 4.0)
- **Manpower** → Afternoon shift understaffed → why? schedule built on last year's volume → **root: staffing not linked to order forecast** (I4 E2 C4 → 1.5, investigate: high impact, weak evidence)
- **Machines** → Label printer jams daily → why? never serviced → **root: no maintenance schedule** (I2 E4 C5 → 1.5)
- **Environment** → Courier pickup moved one hour earlier → **root: carrier contract change not communicated to the warehouse** (I3 E3 C3 → 1.0)

**Actions:** sort the pick queue by ship deadline (Fix); add a daily on-time-dispatch dashboard with an alert below 95% (Prevent); compare staffing vs order volume by hour for the last 4 weeks before hiring (validation test).

## Pitfalls to watch for

- Starting with a solution in disguise ("the problem is we don't have a CRM")
- Stopping at symptoms — if the "root" is something nobody can change, you went one why too far; if it just restates the problem, one too few
- Blaming individuals instead of the system that let the failure happen
- Scoring by gut feel — tie Evidence scores to actual facts
- Treating the diagram as proof: it generates hypotheses; data confirms them
