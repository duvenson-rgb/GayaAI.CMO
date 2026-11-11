# Finding clips

The job is not "cut the video into pieces". It is finding the moments that work for a stranger who has never heard of the show, scrolling with the sound on for one second before deciding. Everything below serves that one test.

## The standalone test

A clip passes only if someone with zero context:

1. **understands what it is about within ~3 seconds** (from the first line, or the first line + the on-screen hook text),
2. **gets a complete idea** (setup → development → landing) without needing anything said before or after,
3. **gets something worth keeping** — they would save it, share it, comment, or feel something.

Read each candidate as if it were the whole episode. If you catch yourself thinking "well, earlier he explained that…", it fails or needs its opening moved.

### Dangling-reference check (do it word by word on the first 2 sentences)

Openings that break standalone: "So yeah…", "And that's why…", "Like I said", "Going back to…", "Exactly", "Right, and…", a pronoun with no referent ("he", "she", "they", "that", "it", "this thing"), a name not introduced, an answer to a question the viewer didn't hear.

Fixes, in order of preference:
- **Start later**, at the first sentence that stands on its own.
- **Keep the host's question** if it is short and strong — questions are often the best hooks ("What's the biggest mistake new founders make?").
- **Let the on-screen hook supply the context** ("Why he turned down $10M") so a mild reference in line one still lands.
- **Cold open**: put a 2–6 s punchline first, then play from the beginning. Always flag it.

Internal references ("as I said a minute ago") can often be cut out with a micro-edit.

## What makes a clip valuable

Give each candidate a type; it guides the hook, the graphics, and the post caption.

| Type | Signal in the transcript | Why people engage |
|---|---|---|
| insight / lesson | "The thing most people miss…", a reframe, a principle | save |
| tactical / how-to / list | numbered steps, "here's what I do", tools, numbers | save |
| story | a specific moment, place, time, stakes, a turn | watch to the end, share |
| contrarian / hot take | "Unpopular opinion", "Everyone says X, but…" | comment, share |
| stat / proof | a surprising number, a before/after | share |
| emotional / vulnerable | admission, failure, fear, gratitude | share, comment |
| funny | laughter on the tape, a quick exchange | share |
| quotable line | one sentence that could be a poster | save, share |

Strong clips usually combine two (a story that lands on a lesson; a stat that sets up a contrarian take).

## Scoring rubric (1–5 each, /25)

- **Hook** — does the first line create curiosity, tension or a bold claim? 5 = you have to keep watching. 1 = throat-clearing.
- **Standalone** — passes the test above with no fixes (5), with a small fix (3–4), needs heavy surgery (1–2).
- **Value** — how much a viewer gets: a clear takeaway, a feeling, a laugh. Specific beats generic.
- **Payoff** — does it end on a landing (punchline, conclusion, a line that closes the loop)? Ending mid-thought or trailing into the next topic = low.
- **Delivery** — energy, conviction, pace, audio quality, and (for video) whether the speaker is on camera and expressive. Proxies from the transcript: few fillers and false starts, a pace of ~2.3–3.3 words/s, no long hesitations. Check the frames at the hook for video clips.

**Tier A ≥ 20** (produce), **Tier B 15–19** (usable, recommend if the user wants volume), **< 15 drop** — but list notable drops so the user can overrule.

## How many clips

No quota. Quality decides. A dense 10-minute conversation typically yields 3–6; a rambling one may yield 1–2; an hour-long episode often 8–15. Never pad the list with weak clips to hit a number, and never merge two ideas into one clip to make it longer. If the user asked for a number, give the best N and say how many more passed.

## Length

- Sweet spot **25–60 s**. Allowed 15–90 s.
- Up to ~2–3 min only for an exceptional story that holds (Reels maximum is 3 min).
- Shorter is better when the idea is complete. The tightest version that still has setup and payoff wins.

## Boundaries and micro-edits

- Start ~0.1 s before the first word, end ~0.25 s after the last (`clip_tools.py snap` does this from word timestamps).
- Tighten inside the clip: remove false starts, repeated words, "um/uh/you know" clusters, long pauses (> 0.6 s → cut to ~0.25 s), tangents that the payoff does not need. Each removal is a new keep range.
- Cut only at word gaps. Check that the joins sound natural (listen for breaths cut in half, pitch jumps).
- **Integrity rule:** micro-edits may shorten, never change meaning. Never splice words into a sentence the speaker did not say, never remove a "not", a qualifier ("sometimes", "for me") or a condition that changes the claim, never move a line so it answers a different question. Cold opens repeat a line the speaker really said in that context — flag every one in the clip map.
- Clips may overlap only if they are genuinely different ideas; otherwise pick the better version.

## Working method

1. Skim the readable transcript (`transcript.txt`) once end to end and note topic changes with timestamps.
2. Mark candidate moments: questions followed by committed answers, stories, lists, numbers, laughter, strong one-liners, changes in energy.
3. For each candidate, find the tightest start and end, run the dangling-reference check, write the hook, score it.
4. Print each candidate's exact words with `clip_tools.py text` and read them as a stranger would. Rescore honestly.
5. Build `clips.json` (schema in `scripts/clip_tools.py`), including `why` (one sentence: why it stands alone and why someone would care), `type`, `hook`, `post` (a draft post caption), and `flags`.
6. Build the clip map page and present it (Gate 1).

## Writing the on-screen hook

- 3–9 words, a claim or a curiosity gap, not a summary ("The mistake that kills 90% of startups", not "Talking about startup mistakes").
- Must be true to what the clip says. No clickbait the clip doesn't pay off.
- One highlighted word with `*word*` (the tension word: a number, "not", "never", the surprising noun).
- Same language as the clip. For Creole clips, write it in Creole.

## Post caption (delivered with each clip)

One or two lines that restate the takeaway in a new way + a question or save prompt. Optional 3–5 relevant hashtags. Keep the user's voice (short, direct).
