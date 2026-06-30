---
name: tt-humanizer
description: Strip AI-script tells from a TikTok spoken script and caption so it sounds like a person talking on camera, not a teleprompter. Removes em dashes, AI vocabulary (leverage, fundamentally, delve, harness), rule-of-three lists, written-not-spoken phrasing, and "hey guys" filler, then adds contractions and one specific number. Includes a --mode audit pre-film check (hook strength, completion design, caption fit). Use before filming any AI-drafted script. Not for writing from scratch (use tt-hook-scripter).
---

# TikTok Humanizer

Rewrites a spoken script (and caption) to remove AI tells, and audits a finished
draft against the 2026 TikTok checklist before you film. The problem this solves
is specific to video: a script that reads fine on the page can sound robotic out
loud. Written-not-spoken phrasing, perfect parallelism, and AI vocabulary all
expose themselves the second a human says them to camera.

Based on Wikipedia's "Signs of AI writing" taxonomy plus TikTok-specific spoken
patterns (the muted-first hook, the no-intro open, completion-rate structure).

## When to use

- Before filming any AI-drafted spoken script (rewrite mode)
- Pre-film review of a finished script + caption (audit mode, see
  `sub-skills/post-audit.md`)
- When a script "reads fine but sounds off" when you say it out loud

## Input

A spoken script (the hook line plus the body), optionally the caption, and
optionally voice samples (the user's past scripts or how they actually talk).

## Output

- Rewritten script that sounds spoken, not written
- A diff showing what changed and why
- Caption char count (flagging over 2,200) when a caption is included
- Confidence: "human", "mixed", "AI-likely"

## Modes

```bash
# Default: scrub AI tells and fix spoken-word issues
tt-humanizer <script>

# Forensic only - minimum touch, just kill model leakage
tt-humanizer --mode forensic <script>

# Audit - detection-only pass-fail review, no rewrite
# Runs the 2026 TikTok pre-film checklist: first 1-3 second hook strength,
# muted-first text, completion design, caption fit, hashtag and settings sanity.
# Returns Blockers + Warnings + suggested fixes. See sub-skills/post-audit.md.
tt-humanizer --mode audit <script>
```

## The three passes

### Pass 1 - SCRUB (delete or replace)

Apply the tiered catalogs in `references/scrub-rules.md`:

- **Forensic** (always on): real model leakage no human says. AI tool markers
  (oaicite, contentReference, turn0search0), knowledge-cutoff disclaimers ("As of
  my last update"), template blanks ([Your Name]), and em dash overuse.
- **Strict** (default on): bad spoken-word style regardless of origin. Vocabulary
  swaps (leverage -> use, delve -> look at, harness -> use, foster -> build),
  filler adverbs (fundamentally, essentially, ultimately), written connectives
  ("moreover", "furthermore"), dead filler ("hey guys", "without further ado"),
  and dead closers ("thanks for watching", "don't forget to subscribe").

### Pass 2 - BREAK (make it sound spoken)

- Replace full grammatical sentences with how a person actually talks:
  contractions and fragments. "It is something that you should consider" becomes
  "you should try this".
- Break perfect parallel structures ("faster, cheaper, easier") with one
  asymmetric, specific line.
- Vary line length. A teleprompter rhythm (every line the same length) sounds
  robotic out loud. Add a short punch line.
- Read-aloud test: flag any line that needs two breaths or trips the tongue.

### Pass 3 - ADD (human fingerprints)

Require where the content allows:
- 1 specific number (replace "many", "a lot", "a few")
- 1 named entity (a real tool, person, or place)
- 1 first-person concrete detail ("the third take", "my 2am edit")
- the spoken register: how this person would actually say it

If the input lacks these, ask the user for a number or detail. Do not fabricate.

## Non-negotiable rules

Global voice rules: see root `SKILL.md` Voice rules. Additional skill-specific
rules:

- Preserve the user's actual claim. Humanizing does not change meaning.
- Never introduce facts that were not in the input. If a number is missing, ask.
- Keep it sayable. Every line has to survive being read out loud in one breath.
- Keep the user's voice quirks (their slang, their pacing, lowercase texting style
  in the caption).

## TikTok-specific tells this skill catches

- A hook line that is written, not spoken ("In this video, I will demonstrate..").
- A greeting or logo intro before the payoff ("hey guys, welcome back").
- The spoken hook and the on-screen text saying the identical words.
- A caption over 2,200 chars, or a 12-hashtag wall.
- Perfect parallel tricolons read aloud ("learn, grow, succeed").
- A "call to action" stacked five deep.
- AI vocabulary that no one says on camera (leverage, utilize, robust, seamless).

## Example

See `references/examples.md` for worked before/after rewrites of spoken scripts.

## Files

- `SKILL.md` - this file (rewrite scrubber + audit-mode entry)
- `references/scrub-rules.md` - vocabulary swaps and spoken-word fixes by tier
- `references/examples.md` - worked before/after script rewrites
- `references/audit-checklist.md` - the pre-film checklist with thresholds
- `sub-skills/post-audit.md` - pre-film audit workflow (detection-only, no rewrite)

## Related skills

- `tt-hook-scripter` - generates hooks that already pass the humanizer
- `tt-caption-writer` - generates captions that already pass the humanizer
