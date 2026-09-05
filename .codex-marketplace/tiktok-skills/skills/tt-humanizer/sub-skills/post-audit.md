# TikTok Pre-Film Audit

Run a spoken script (and caption) through the 2026 TikTok checklist before you
film. Catches AI tells, a weak hook, completion-killing structure, and caption /
settings problems while they are still cheap to fix. This is the `tt-humanizer
--mode audit` workflow: detection only, no rewrite.

## When to use

- Before filming a hand-written or AI-drafted script
- When `tt-hook-scripter` or `tt-caption-writer` finishes a draft (auto-invoked)
- When a recent video underperformed and the user wants a post-mortem

## Input

- A spoken script (hook + body), optionally the caption and the chosen settings
- Optional: niche/audience, the primary goal (completion / saves / comments /
  shares / follows)

## Output

- **Pass / Fail** header
- **Blockers** (must fix before filming): em dashes over the caption/card cap,
  beats at 3+ AI markers, reveal bridges, sincerity openers, written-not-spoken
  hooks, dead filler, dead closers
- **Warnings** (ship-risky): staged rhythm, stacked triads, framed confessions,
  missing referenced numbers, two-breath lines
- **Suggested fixes** for each issue
- **Completion read:** where in the script attention is likely to drop
- **Per-beat tell density** (markers, em dashes per 100 caption words, triads).
  No detector score: on script-length text those are noise and nobody runs one
  on a video

## Checks

### Blockers (auto-fail)

1. Em dash density over the cap: more than about 1 per 100 words in the caption
   (1-2 per caption), or more than one on an on-screen card; en dash or double
   dash between clauses. A single em dash is not a blocker; a dash in the
   spoken script is a breath mark, not a tell.
2. The first 1-3 seconds open on a greeting, a logo, or a slow zoom (no payoff or
   tension in frame one).
3. The spoken hook is written-not-spoken ("In this video I will demonstrate..").
4. The spoken hook and the on-screen text are the identical words.
5. The hook promises a result the script never shows on screen.
6. Caption over 2,200 chars (API limit, hashtags included).
7. Any script beat or caption paragraph with 3+ AI vocabulary / grammar markers
   (see `../references/scrub-rules.md`); one marker is a slip, not a fail.
7a. A reveal bridge ("The result?", "Here's what nobody tells you", "Stop X,
   start Y") or negative parallelism ("It's not X, it's Y"), single hit.
7b. A sincerity opener ("not gonna lie", "let me be honest", "real talk",
   "storytime" with no story in frame one, "unpopular opinion:" on a popular
   take).
8. `commercialContent` set without `brandOrganic` or `brandedContent`.
9. Ends on "thanks for watching" / "don't forget to subscribe" / "let that
   sink in" (kills the loop).

### Warnings (flag with a suggested fix)

10. No odd-precision number with a referent in the hook where the claim would
    allow one (a bare number does not clear this).
11. 6 or more hashtags, or hashtags jammed mid-sentence.
12. The last frame does not restart the loop (no rewatch design).
13. Teleprompter-flat run: 4+ consecutive lines the same length AND none
    carrying a real clause. Flag that run only; never suggest inserting a punch
    line or varying length as a tactic.
13a. Staged rhythm (patterns not already blocker 7a): "No X. No Y. Just Z.", one-word lines for
    drama, an inserted punch line between long ones, a long/short/long/short
    seesaw, or more than 2 standalone fragments in the caption.
14. Stacked, perfectly parallel or hollow rule-of-three ("learn, grow,
    succeed"), or a second triad in the script (one natural triad passes).
15. A line that needs two breaths to say (read-aloud failure).
15a. A framed confession (a sincerity sentence wrapped around a fact) or a
    hedge the speaker did not write ("I think maybe", "I might be wrong but").
15b. Over-scrubbed (only when auditing a humanizer rewrite with the original in hand to compare against; a fresh draft that never had an em dash or a triad is not over-scrubbed): uniformly flat tone, the speaker's slang gone, no reaction
    anywhere, the one natural triad gone.
16. Five-deep call to action ("like, comment, follow, share, save").
17. `viewerSetting` not set, or set to a value that may post private on an
    unaudited app.
18. No clear primary goal: the script chases completion, saves, comments, and
    shares all at once. Pick one.

### Info (neutral notes)

19. Suggested video length given the one idea (shortest that fully delivers).
20. Whether on-screen captions / auto-captions are planned (lifts completion).
21. Sound choice: if a trending sound is used, is it still early (see
    `tt-trend-mapper`).

## Steps

1. Separate the hook (first 1-3 seconds) from the body. The hook gets the
   harshest scrutiny: it decides the video.
2. Run the blocker checks on the hook first, then the body, then the caption.
3. If any blockers, return **FAIL** with specific fixes; optionally offer to hand
   off to `tt-humanizer` for an auto-rewrite.
4. If no blockers, run the warnings and the completion read.
5. Report per-beat tell density. Do not estimate a detector score.
6. Return the structured report with a length and loop-close note.

## Related

- `tt-humanizer` - proportional rewrite if the audit fails
- `tt-hook-scripter` - regenerate the hook using a proven formula
- `tt-caption-writer` - fix the caption, hashtags, and settings
