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
- **Blockers** (must fix before filming)
- **Warnings** (ship-risky)
- **Suggested fixes** for each issue
- **Completion read:** where in the script attention is likely to drop

## Checks

### Blockers (auto-fail)

1. Em dash / en dash / double dash in the caption or on-screen text.
2. The first 1-3 seconds open on a greeting, a logo, or a slow zoom (no payoff or
   tension in frame one).
3. The spoken hook is written-not-spoken ("In this video I will demonstrate..").
4. The spoken hook and the on-screen text are the identical words.
5. The hook promises a result the script never shows on screen.
6. Caption over 2,200 chars (API limit, hashtags included).
7. Contains AI vocabulary blacklist words (see `../references/scrub-rules.md`).
8. `commercialContent` set without `brandOrganic` or `brandedContent`.
9. Ends on "thanks for watching" / "don't forget to subscribe" (kills the loop).

### Warnings (flag with a suggested fix)

10. No specific number in the hook where the claim would allow one.
11. 6 or more hashtags, or hashtags jammed mid-sentence.
12. The last frame does not restart the loop (no rewatch design).
13. Teleprompter rhythm: every line roughly the same length.
14. Rule-of-three list with no concrete items ("learn, grow, succeed").
15. A line that needs two breaths to say (read-aloud failure).
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
5. Return the structured report with a length and loop-close note.

## Related

- `tt-humanizer` - aggressive rewrite if the audit fails
- `tt-hook-scripter` - regenerate the hook using a proven formula
- `tt-caption-writer` - fix the caption, hashtags, and settings
