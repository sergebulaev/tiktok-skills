# Pre-Film Audit Checklist with thresholds

The detection-only checklist behind `tt-humanizer --mode audit`. Thresholds are
explicit so the audit is repeatable. Blockers fail the draft; warnings flag it.

## Blockers (any one = FAIL)

| # | Check | Threshold |
|---|---|---|
| B1 | Em / en / double dash | any in caption or on-screen text |
| B2 | Intro before payoff | greeting, logo, or zoom in the first second |
| B3 | Written-not-spoken hook | "In this video I will.." style opener |
| B4 | Hook == on-screen text | identical words in both layers |
| B5 | Unshown promise | hook promises a result the video never shows |
| B6 | Caption length | > 2,200 chars (hashtags included) |
| B7 | AI vocabulary | any blacklist word (see scrub-rules Tier 2) |
| B8 | Commercial disclosure | commercialContent true, both brand flags false |
| B9 | Dead closer | ends on "thanks for watching" / "subscribe" |

## Warnings (flag with a fix, do not fail)

| # | Check | Threshold |
|---|---|---|
| W1 | No number in hook | zero specific numbers where one would fit |
| W2 | Hashtag count | 6 or more, or any mid-sentence |
| W3 | No loop-close | last frame does not restart the video |
| W4 | Teleprompter rhythm | all lines within ~15% of the same length |
| W5 | Empty tricolon | rule-of-three with no concrete items |
| W6 | Two-breath line | any line that cannot be said in one breath |
| W7 | CTA stack | 3 or more calls to action |
| W8 | viewerSetting | unset, or public claimed on an unaudited app |
| W9 | No primary goal | chases completion + saves + comments + shares at once |

## Info (neutral notes, always include)

- **Length read:** the shortest length that fully delivers the one idea.
- **Caption plan:** are on-screen captions / auto-captions planned (lifts
  completion and accessibility).
- **Sound:** if a trending sound is used, is it still early (hand to
  `tt-trend-mapper`).

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
- W1 no number in the hook: add the real figure ("3 takes", "47 minutes")
- W3 no loop-close: end on the line that recontextualizes the open

Info:
- length: 18-24s fully delivers this one idea
- captions: plan on-screen text for the muted-first viewers
- goal: this reads as a saves play (T9); make the "save this" ask explicit
```
