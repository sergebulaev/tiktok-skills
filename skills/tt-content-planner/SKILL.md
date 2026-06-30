---
name: tt-content-planner
description: Build a weekly TikTok posting plan from a niche, audience, and content pillars. Produces per-day picks (hook formula, angle, sound, video length, goal, posting time), a hook-batching schedule so you film several openers in one session, a sound shortlist with the trend window, and a completion-rate goal check. Use for a repeatable posting rhythm instead of ad-hoc videos. Not for scripting one hook (use tt-hook-scripter) or one caption (use tt-caption-writer).
---

# TikTok Content Planner

Produce a weekly TikTok plan built around a pillar discipline, a completion-rate
target, and the batching workflow that makes consistent posting survivable.
TikTok rewards frequency and a clear niche, so the plan locks in a rhythm,
shortlists sounds while they are still early, and batches hooks so filming does
not eat the whole week.

## When to use

- User asks "plan my week on TikTok" or "what should I post this week"
- User wants to escape ad-hoc posting and build a rhythm
- User wants to batch-film several videos in one session
- Before a launch week (the plan aligns a product pillar)

## Input

- **Niche** (required): e.g. "backend engineering tips for junior devs"
- **Audience description:** e.g. "self-taught devs, bootcamp grads, early-career"
- **Pillar mix** (optional): defaults to 40% Teach / 30% Story / 20% Trend /
  10% Promotion
- **Posting cadence** (optional): defaults to 1 video/day, 5-7 days
- **Completion-rate target** (optional): defaults to "beat your trailing 30-day
  average"
- **Voice samples** (optional): past scripts for voice calibration

## Output

A markdown plan with:

### 7-day calendar

| Day | Pillar | Formula | 1-line angle | Sound | Length | Goal | Time |
|---|---|---|---|---|---|---|---|
| Mon | Teach | T9 Tutorial Cold Start | "the git command that saved my job" | original VO | 22s | saves | 8:00 AM |
| Tue | Story | T8 Story In Medias Res | "the 11pm prod outage" | trending (early) | 34s | completion | 7:30 PM |
| Wed | Teach | T3 Number Reveal | "97% of bugs are in 3 files" | original VO | 15s | saves | 12:00 PM |
| Thu | Trend | T10 Trend-Ride | "{trend} but for backend devs" | trending sound | 12s | shares | 7:00 PM |
| Fri | Story | T5 Relatable Call-Out | "pov: the standup that should've been a slack" | trending | 18s | shares | 8:00 AM |
| Sat | Teach | T7 Listicle Promise | "5 vs code settings i never turn off" | original VO | 28s | saves | 11:00 AM |
| Sun | Promotion | T1 Cold-Open Result | "what i built that got me hired" | original VO | 30s | completion | 6:00 PM |

(The skill fills real angles from the niche. Weekends skew to story and relatable.)

### Hook-batching schedule

Filming one video at a time burns out creators. The plan groups the week's hooks
into one or two batch sessions:

- **Batch the hooks first.** Film all the 1-3 second openers in one sitting (same
  lighting, same outfit if you want them undated). Strong hooks are the scarce
  resource; batch them while you are warm.
- **Group by setup.** Videos that share a location, prop, or framing film
  together. The plan tags each day with its setup so you can cluster them.
- **Leave trend slots flexible.** Trend rides (T10) are filmed close to posting
  because the sound window moves. The plan marks them "film day-of".

### Sound-selection shortlist

For the week:
- **2 to 3 trending sounds** to watch, with a note on where each sits in the trend
  lifecycle (emerging / peaking / saturated). Ride only the early ones.
- **Original audio** for the evergreen Teach posts (builds a niche sound asset).
- A reminder: catch a sound in its first 1-3 days of climbing or skip it.

### Completion-rate goal check

- [ ] Every video has one idea and a length that fully delivers it (no padding)
- [ ] Every hook puts a result, number, or tension in frame one
- [ ] At least 3 of 7 are designed for saves (the underrated lever)
- [ ] At least 1 designed for shares (a niche-specific relatable or trend ride)
- [ ] No two days use the same formula back to back
- [ ] Trend rides are 1-2 of the week, not the whole plan
- [ ] Each video has a loop-close so a rewatch feels natural

## Goal mix (balance the week)

Every formula earns a primary signal. A week that is all saves-bait or all trend
rides reads as engineered. Spread the goals:

| Goal | Formulas | Weekly target |
|---|---|---|
| Completion | T1, T2, T8 | every video (the floor) |
| Saves | T3, T7, T9 | at least 3 (saves are the underrated lever) |
| Comments | T4, T6 | at least 1 |
| Shares | T5, T10 | at least 1 |
| Follows | any framed as a series | at least 1 series hook |

## Rules

- **1 video/day is a sustainable floor; 1-3 is fine on TikTok.** It rewards
  frequency without the cannibalization penalty other platforms impose. Quality
  still gates: do not pad to hit a count.
- **Completion rate is the goal, not views.** Plan the shortest length that fully
  delivers each idea.
- **Batch hooks, film bodies around them.** The hook is the scarce resource.
- **Trend rides are seasoning, not the meal.** 1-2 a week. Over-relying on trends
  means you never build a niche of your own.
- **One formula per day, varied across the week.** Do not stack three T7 lists.
- **Promotion pillar max 1-2 posts/week.** Overuse kills trust.

## Formula -> pillar mapping

| Pillar | Preferred formulas |
|---|---|
| Teach | T9 Tutorial Cold Start, T3 Number Reveal, T7 Listicle Promise |
| Story | T8 Story In Medias Res, T5 Relatable Call-Out |
| Trend | T10 Trend-Ride, T2 Pattern Interrupt |
| Promotion | T1 Cold-Open Result (a result that implies the product) |

## Steps

1. Gather inputs. Ask for niche, audience, pillar preferences if not provided.
2. Validate the pillar mix sums to 100%; warn if any pillar is over 60%.
3. For each day, pick: pillar, formula (do not over-repeat), angle, sound
   (trending-early or original), length, posting time (audience timezone), goal.
4. Build the hook-batching schedule by grouping shared setups.
5. Build the sound shortlist with lifecycle notes (hand specifics to
   `tt-trend-mapper`).
6. Run the completion-rate goal check and the goal-mix check; flag gaps.
7. Return as markdown, plus optional JSON for import.

## Example

See `references/example-week.md` for a filled-in 7-day plan.

## Files

- `SKILL.md` - this file
- `references/example-week.md` - worked 7-day plan with batching
- `references/pillars-framework.md` - the TikTok pillar discipline explained

## Related skills

- `tt-hook-scripter` - script each day's hook from the plan
- `tt-caption-writer` - caption and schedule each video
- `tt-trend-mapper` - vet the week's trend slots before filming
- `tt-humanizer` - scrub each script before the batch shoot
