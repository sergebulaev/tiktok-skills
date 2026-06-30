---
name: tt-trend-mapper
description: Map a trending TikTok sound or format to your niche so the ride is authentic, not cringe. Runs a fit check (does it match your niche, is it still early, what is the native joke), then scripts the twist that makes the trend yours: the recognizable beat plus a niche-specific turn. Covers sound timing, the trend lifecycle, and when to skip a trend entirely. Use to ride a trend without looking late or forced. Not for a from-scratch hook (use tt-hook-scripter) or a posting plan (use tt-content-planner).
---

# TikTok Trend Mapper

Riding a trend is a distribution lever: a trending sound carries built-in reach,
and a familiar format lowers the barrier to watch. But a trend copied with no
twist is forgettable, and a trend forced onto a clashing niche reads as cringe
and costs trust. This skill decides whether to ride, and if so, scripts the twist
that makes the trend yours.

## When to use

- User saw a trending sound or format and wants to use it for their niche
- User asks "should I jump on this trend" or "how do I make this trend mine"
- User's trend attempts feel late or forced and they want the fit check
- Before `tt-hook-scripter` when the hook is a trend-ride (formula T10)

## What this skill produces

- **A fit verdict:** ride it, bend it hard, or skip it (with the reason)
- **The trend teardown:** the native joke / structure / beat, and why it works
- **The twist:** the recognizable beat plus the niche-specific turn, scripted as
  a hook (spoken line + on-screen text + visual)
- **A timing read:** is the trend still early, peaking, or stale
- **A skip recommendation** when the trend does not fit (saying no is a feature)

## The fit check (run this first)

Four questions. A trend has to clear all four to be worth riding.

1. **Does it match your niche?** Can your audience tell why you, specifically,
   did this trend? If the only connection is "it was trending", skip it.
2. **Is it still early?** A sound in its first 1 to 3 days of climbing carries the
   most lift. If it is already on every third video, you read as late. Check how
   saturated the sound and format already are.
3. **Is there a native structure to honor?** Most trends have an expected beat (a
   setup line, a specific cut, a punchline placement). Riding it means hitting that
   beat, then twisting it, not ignoring it.
4. **Can you add a real twist?** The twist is the whole point. If you cannot bend
   the trend to say something only your niche would say, the ride is filler.

If a trend fails the fit check, **recommend skipping it.** A skipped trend costs
nothing. A cringe ride costs trust.

## The trend lifecycle

| Stage | What you see | Move |
|---|---|---|
| **Emerging** | a sound or format on a few breakout videos, climbing fast | ride now, this is the window |
| **Peaking** | it is everywhere, big accounts are on it | ride only with a strong twist, expect less lift |
| **Saturated** | every third video uses it, the joke is worn | skip, or subvert it (do the opposite) |
| **Dead** | it stopped climbing days ago | skip; using it now reads as late |

The reach boost lives in the emerging stage. By saturation the sound is just a
sound.

## Scripting the twist

Once a trend clears the fit check, build the ride as a hook (formula T10):

1. **Hit the recognizable beat first.** The first second has to read as the trend,
   or you lose the built-in recognition.
2. **Twist into your niche by the turn.** "{the trend's expected setup}, but for
   {your niche}" is the core move. The twist is the surprise that makes it
   shareable inside your audience ("they did the trend, but for us").
3. **Keep the native structure.** If the trend has a cut on the beat drop, cut on
   the beat drop. Honoring the format is what signals you get it.
4. **Hand the spoken line to `tt-humanizer`** so the script does not sound
   written. Hand the full hook to `tt-caption-writer` for the caption.

## Steps

1. **Gather inputs.** The trend (a sound link, a format description, or an example
   video URL), the user's niche, and what they usually post.
2. **Parse any URL.** `lib.url_parser.parse_tiktok_url(url)` extracts the handle
   and video id from an example video.
3. **Run the fit check.** Score all four questions. If it fails, recommend skip
   and explain why (saying no honestly builds more trust than a forced ride).
4. **Read the lifecycle stage.** Ask the user how saturated they have seen it;
   place it on the emerging-to-dead scale.
5. **Tear down the native structure.** Name the beat, the joke, the expected cut.
6. **Script the twist** as a T10 hook (spoken line + on-screen text + visual).
7. **Humanizer pass** on the spoken line.
8. **Hand off.** `tt-caption-writer` for the caption and a sound-credit note;
   `tt-content-planner` if the trend ride is one slot in the week.

## Hard rules

Global voice rules: see root `SKILL.md` Voice rules. Additional skill-specific
rules:

- A trend with no niche fit gets a skip recommendation. Do not force it.
- The twist is mandatory. A trend copied straight is filler.
- Ride early or do not ride. A stale trend reads as late.
- Honor the native structure (the beat, the cut, the joke placement).
- Never fabricate a trend's popularity. If you do not know the saturation, ask.

## Anti-patterns (skill will refuse)

- "Just do the trend because it is trending" with no twist and no fit.
- Forcing a sound onto a niche it clashes with.
- Riding a sound that is already saturated and calling it timely.
- Ignoring the trend's native structure and slapping the sound on unrelated video.
- A twist that punches down or mocks the original creator.

## Resources

- `../../references/algorithm-heuristics.md` - sound selection, the trend window, original audio
- `../../references/hook-formulas.md` - T10 Trend-Ride With A Twist (three layers)
- `references/trend-fit-rubric.md` - the scored fit check and lifecycle examples

## Related skills

- `tt-hook-scripter` - script the trend ride as a T10 hook
- `tt-caption-writer` - caption and sound credit for the ride
- `tt-content-planner` - slot trend rides into the week without over-relying on them
