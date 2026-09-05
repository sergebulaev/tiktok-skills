# Pre-Film Audit Checklist with thresholds (V3, 2026-09)

The detection-only checklist behind `tt-humanizer --mode audit`. Thresholds are
explicit so the audit is repeatable. Blockers fail the draft; warnings flag it.
V3: AI tells are scored by density per script beat; em dashes are capped in
the caption and on cards, and are only breath marks in the spoken script;
forced rhythm is a tell.

## Blockers (any one = FAIL)

| # | Check | Threshold |
|---|---|---|
| B1 | Em dash density | caption above ~1 per 100 words (1-2 per caption), or more than one on an on-screen card; en / double dash between clauses. A single em dash is not a blocker; a dash in the spoken script is a breath mark, not a tell |
| B2 | Intro before payoff | greeting, logo, or zoom in the first second |
| B3 | Written-not-spoken hook | "In this video I will.." style opener |
| B4 | Hook == on-screen text | identical words in both layers |
| B5 | Unshown promise | hook promises a result the video never shows |
| B6 | Caption length | > 2,200 chars (hashtags included) |
| B7 | AI vocabulary cluster | any script beat or caption paragraph with 3+ markers (see scrub-rules Tier 2); one marker is a slip, not a fail |
| B7a | Reveal bridge / negative parallelism | "The result?", "Here's what nobody tells you", "Stop X, start Y", "It's not X, it's Y" (single hit) |
| B7b | Sincerity opener | "not gonna lie", "let me be honest", "real talk", "storytime" with no story in frame one, "unpopular opinion:" on a popular take |
| B8 | Commercial disclosure | commercialContent true, both brand flags false |
| B9 | Dead closer | ends on "thanks for watching" / "subscribe" / "let that sink in" |

## Warnings (flag with a fix, do not fail)

| # | Check | Threshold |
|---|---|---|
| W1 | No referenced number in hook | zero odd-precision numbers with a referent where one would fit (a bare number does not clear this) |
| W2 | Hashtag count | 6 or more, or any mid-sentence |
| W3 | No loop-close | last frame does not restart the video |
| W4 | Teleprompter-flat run | 4+ consecutive lines the same length AND none carrying a real clause. Flag that run only; never suggest inserting a punch line or varying length as a tactic |
| W4a | Staged rhythm (patterns not already a B7a blocker) | "No X. No Y. Just Z.", one-word lines for drama, an inserted punch line between long ones, a long/short/long/short seesaw; more than 2 standalone fragments in the caption |
| W5 | Stacked or hollow tricolon | rule-of-three with interchangeable or no concrete items, or a second triad in the script (one natural triad passes) |
| W6 | Two-breath line | any line that cannot be said in one breath |
| W6a | Framed confession or inserted hedge | a sincerity sentence wrapped around a fact; "I think maybe", "I might be wrong but" the speaker did not write |
| W6b | Over-scrubbed (only when the original is in hand to compare against; never on a fresh draft) | uniformly flat tone, the speaker's slang gone, no reaction anywhere, the one natural triad gone |
| W7 | CTA stack | 3 or more calls to action |
| W8 | viewerSetting | unset, or public claimed on an unaudited app |
| W9 | No primary goal | chases completion + saves + comments + shares at once |

## Info (neutral notes, always include)

- **Length read:** the shortest length that fully delivers the one idea.
- **Caption plan:** are on-screen captions / auto-captions planned (lifts
  completion and accessibility).
- **Sound:** if a trending sound is used, is it still early (hand to
  `tt-trend-mapper`).
- **Tell density:** markers per beat, em dashes per 100 caption words, triad
  count. No detector score: on script-length text those are noise, nobody runs
  one on a video, and this skill does not promise to beat them.

## Scoring

- **Any blocker present:** FAIL. Return the blockers first, offer an auto-rewrite
  via `tt-humanizer`.
- **No blockers, warnings present:** PASS WITH WARNINGS. List the warnings with
  fixes, ordered by impact on completion.
- **No blockers, no warnings:** PASS. Add the info notes and a length/loop note.

## Output shape

```
PASS WITH WARNINGS

Blockers: none

Warnings:
- W1 no referenced number in the hook: add the real figure with its referent ("3 takes", "47 minutes on the third take")
- W3 no loop-close: end on the line that recontextualizes the open

Info:
- length: 18-24s fully delivers this one idea
- captions: plan on-screen text for the muted-first viewers
- goal: this reads as a saves play (T9); make the "save this" ask explicit
- tell density: hook 0, value 1 ("robust", left), loop-close 0; caption 0 em dashes
```
