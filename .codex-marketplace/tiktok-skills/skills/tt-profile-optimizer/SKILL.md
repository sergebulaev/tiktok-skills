---
name: tt-profile-optimizer
description: Audit and rewrite a TikTok profile for 2026: photo, name (searchable), username, bio (80 chars, niche clarity is everything), link (unlocks at 1k followers, plus a pre-1k workaround), up to 3 pinned videos as proof, and one-line positioning. A profile visit follows a video, so the bio must instantly answer "what do I get if I follow". Triggers on "review my TikTok profile", "fix my TikTok bio", "what to pin on TikTok", "profile audit", "niche bio". Not for writing a video script (use tt-hook-scripter).
---

# TikTok Profile Optimizer

Audit the parts of a TikTok profile (photo, name, username, bio, link, pinned
videos, positioning) against what turns a one-time viewer into a follower in
2026, then rewrite each part that needs it. On TikTok the profile visit almost
always follows a video: someone watched, felt a spark, and tapped the avatar.
They land on the bio with one question in mind, "what do I get if I follow", and
the 80-character bio has about one second to answer it. This skill fixes that.

## When to use

- User pastes their TikTok profile or @handle and asks for an audit
- "Fix my TikTok bio", "rewrite my bio", "what should I pin"
- User is starting to post seriously and wants the profile to match the videos
- Any of: "review my TikTok profile", "niche bio", "profile audit"

Not for writing a video script or hook (use `tt-hook-scripter`) or the caption
(use `tt-caption-writer`).

## Input

- Profile URL / @handle (or a screenshot of the profile page)
- Goal: **grow a following** / **drive signups** / **land clients** / **sell a product**. The bio line and the pinned videos change by goal.
- Optional: their best-performing videos, to pick the (up to 3) pins
- Their current follower count (decides whether the link field is unlocked)

## Output

1. **Scorecard** (7 parts, pass / needs-work / fail)
2. **Priority fixes** ranked by impact (bio and pinned videos first, always)
3. **Before -> After** rewrites for each failing part
4. **Pinned-video pick** (up to 3) with the reason each earns its slot

## Steps

1. **Intake.** Collect the profile state, the goal, and the follower count. Below
   1,000 followers the clickable link field is locked, so plan the pre-1k
   workaround (step 6).
2. **Score the 7 parts** against the scorecard below.
3. **Rewrite the bio (80 chars).** This is the whole game. Formula:
   `who it is for + what they get + one specific`. The bio must answer "what will
   I get if I follow" in one glance. 80 characters is brutally tight, so cut every
   word that is not niche or proof. No "welcome to my page", no life motto, no
   emoji wall. One clear niche beats three vague interests.
4. **Fix the name (searchable, 30 chars).** The name field is indexed by TikTok
   search; the @username mostly is not. Put the real name plus the searchable
   niche keyword people actually type (e.g. "Sam | Backend Dev Tips"). This is the
   single highest-leverage search fix on the profile.
5. **Check the username (@handle).** Short, memorable, sayable out loud, no
   throwaway numbers or stacked underscores if it can be avoided. Renaming costs
   reach, so only change a genuinely bad handle.
6. **Set the link (unlocks at 1,000 followers).** With the field unlocked, one
   link matched to the goal (newsletter / offer / link-hub). **Pre-1k workaround:**
   the link field is locked, so route the call to action through the bio text and
   pinned videos instead: name the destination in the bio ("newsletter in
   comments" / "DM the word GUIDE"), and pin a video whose caption or comment
   carries the link. Do not leave the CTA homeless just because the field is grey.
7. **Pick the pinned videos (up to 3).** These are the profile's proof of the
   niche. Choose the videos that best say "this is what you will get every week":
   the top-performing one, one that shows range inside the niche, and one clear
   offer or intro matched to the goal. Order them so the first pin is the single
   strongest proof. An empty pin row wastes the most valuable real estate on the
   page.
8. **Photo check.** Clear face or a clean, recognizable niche mark, high contrast,
   readable as a small circle. It sits next to the name on every video, so it must
   read at thumbnail size, not just on the profile.
9. **Write the one-line positioning statement.** Distill the whole profile to a
   single sentence: "I help [who] [get what] through [format]". This is the north
   star the bio, name, and pins all serve. If they cannot agree in one line, the
   profile will read as scattered.
10. **Deliver the before/after diff** + the one-second test: read only the photo,
    name, and bio, and ask "would someone who just watched one video follow from
    this alone?"

## Seven-part scorecard

| # | Part | Pass criteria (2026) |
|---|------|----------------------|
| 1 | **Profile photo** | Clear face or clean niche mark, high contrast, readable as a small circle next to the name |
| 2 | **Name (searchable)** | Real name + a searchable niche keyword, inside 30 chars; not just the handle repeated |
| 3 | **Username (@handle)** | Short, sayable, no throwaway numbers or stacked underscores |
| 4 | **Bio (80 chars)** | Answers "what do I get if I follow" in one glance; one niche, one specific; no filler, no emoji wall; inside 80 chars |
| 5 | **Link** | Unlocked (1k+): one link matched to the goal. Locked (pre-1k): CTA routed through bio text + a pinned video, not left homeless |
| 6 | **Pinned videos** | Up to 3 present, each the best proof of the niche, ordered strongest first; not random recent uploads |
| 7 | **Positioning** | One line ("I help X get Y through Z") that the name, bio, and pins all serve |

## Hard rules

Global voice rules: see root `SKILL.md` Voice rules. Additional skill-specific
rules:

- The bio must pass the one-second test: someone who just watched one video reads
  only photo + name + bio and knows the niche and wants to follow.
- Bio hard cap is 80 characters. Never ship a truncated bio; cut, do not overflow.
- Lead the bio with the viewer's benefit and the niche, not a job title or a motto.
- One specific or one number where it fits; niche clarity always beats a clever line.
- Below 1,000 followers the link field is locked. Never write a rewrite that
  depends on a clickable link the account does not have yet; use the workaround.
- Name field is searchable, the @handle mostly is not. Put the keyword in the name.
- No em dashes. No "leverage", "fundamentally", "game-changer", no emoji wall.

## Related skills

- `tt-hook-scripter` - script the videos the optimized profile will host
- `tt-caption-writer` - the caption, settings, and hashtags for each pinned video
- `tt-content-planner` - plan the cadence that fills the profile
- `tt-trend-mapper` - find a trend a pin-worthy video can ride
