---
name: tt-audience-insights
description: Read your TikTok niche and audience from real data. Scan a hashtag for top videos with plays, likes, and comments, see which hooks and sounds are working, pull a profile's videos (yours or a competitor's), and read the commenters on a video (TikTok hides likers, so commenters are the signal). Powered by Apify, no login. Triggers on "what is trending on TikTok", "analyze this hashtag", "competitor videos", "read my comments", "which sounds are working". Not for writing a script (use tt-hook-scripter).
---

# TikTok Audience Insights

Turn real TikTok data into a read on what is working: which videos in your niche are exploding and why, what a competitor is posting, and what your commenters keep saying. The read layer sees actual play counts and comments instead of guessing.

One honest limit: TikTok keeps the list of who **liked** a video private (only counts). The engagement signal here is **commenters + video performance**, which is where the niche's questions and objections live.

## When to use

- "What is trending in [niche] on TikTok / analyze this hashtag"
- "What is [competitor] posting / analyze their profile"
- "Read the comments on this video"
- "Which sounds and hooks are working right now"

Not for writing a script (use `tt-hook-scripter`) or a caption (use `tt-caption-writer`).

## Setup (optional)

The read layer uses **Apify** (no login). Free token at `https://console.apify.com/account/integrations`, set `APIFY_TOKEN`. Video scanning is about $1.70 per 1,000, comments about $0.50 per 1,000. No token? Paste the videos or comments and the skill runs the same analysis.

## Input

- A hashtag (niche scan), a profile (self or competitor), or a video URL (comments)
- Optional: the goal (trend scan / competitor read / community management)

## Output

1. **Niche pulse** - top videos for the hashtag ranked by plays, the hooks and sounds behind the winners
2. **Competitor read** - a profile's recent videos ranked, the pattern in their hits
3. **Comment read** - what commenters keep asking, superfans, comments to reply to or pin
4. **Action list** - the hook/sound/format to try, who to engage, which comment to answer on camera

## Steps

1. **Pull the data.** Niche: `lib.ApifyClient().fetch_niche_videos(hashtag, max_items=20)`. Profile: `fetch_profile_videos(username)`. Comments: `fetch_video_comments(video_url)`. Falls back to pasted data if no token.
2. **Rank by performance.** Sort by plays, then engagement rate (likes+comments over plays). Normalize against the author's follower count so a small creator's breakout is not buried under a big account.
3. **Extract the pattern.** For the top videos, name the shared hook (first-second shape), the sound, the format (talking-head, text-overlay, skit), and the length. That is the repeatable part.
4. **Note the sounds.** Recurring sounds across the top videos are a trend to ride; flag them for `tt-trend-mapper`.
5. **Read the comments.** Cluster into questions, agreement, pushback. Recurring questions become video ideas (answer on camera); pinned/high-like comments show what the room cares about.
6. **Build the action list.** Try-this (winning hook + sound), engage (specific commenters), answer-on-camera (a recurring question). Route to `tt-hook-scripter` / `tt-caption-writer`.
7. **Deliver the report** in the Output shape, with the raw ranked videos attached.

## What the read layer exposes

| Method | Returns |
|---|---|
| `fetch_niche_videos(hashtag, max_items)` | top videos for a hashtag: text, plays, likes, comments, shares, author fans, sound |
| `fetch_profile_videos(username, max_items)` | a profile's recent videos with the same fields |
| `fetch_video_comments(video_url, max_items)` | comments (the engagement signal, since likers are private) |

## Hard rules

Global voice rules: see root `SKILL.md` Voice rules. Additional skill-specific rules:

- Be honest that this reads **commenters, not likers** (TikTok keeps likers private). Do not imply a full liker roster.
- **Normalize by follower count** before calling a video a winner, or you extract "big account" effects, not "good video" effects.
- Never invent a video, a count, a sound, or a comment. If the data is thin, say so.
- A pattern (hook or sound) is only a trend if it recurs across several top videos.

## Related skills

- `tt-hook-scripter` - script a video around the winning hook the data found
- `tt-trend-mapper` - ride a sound or format the scan surfaced
- `tt-caption-writer` - caption it
- `tt-content-planner` - feed the winning patterns into a plan
