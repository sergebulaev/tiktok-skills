---
name: tt-caption-writer
description: Write a TikTok caption under 2,200 chars (hashtags included), pick a tasteful 3 to 5 hashtag set with mixed reach, and set the platformSettings.tiktok flags (viewer setting, comments, duet, stitch, commercial and branded content). Front-loads a reason to comment, runs the humanizer pass, and publishes the rendered video via Publora on approval. Use to caption a finished video. Not for the in-video hook (use tt-hook-scripter) or scrubbing a script (use tt-humanizer).
---

# TikTok Caption Writer

Write the caption that sits under the video: a tight caption inside the 2,200
char API limit, a mixed-reach hashtag set, and the `platformSettings.tiktok`
flags that control reach and interaction. On TikTok the caption supports the
video, it does not carry it. The hook is in the first 1-3 seconds of the clip
(see `tt-hook-scripter`); the caption's job is to add context and earn a comment.

## When to use

- User has a video (or a script) and needs the caption, hashtags, and settings
- User is about to upload and wants the posting flags right
- User wants Claude Code or Codex to schedule a rendered .mp4 via Publora

## What this skill produces

- **Caption** (<= 2,200 chars on the API; aim much shorter), first line front-
  loaded with a reason to read or comment
- **Hashtag set** (3 to 5, mixed reach), placed at the end
- **platformSettings.tiktok** flags with a plain-English summary
- On approval, the publish call (draft -> upload -> schedule) when a video file
  is supplied

## The TikTok settings (platformSettings.tiktok)

Build these with `lib.tiktok_settings(...)`. Defaults match Publora's.

| Setting | Values / default | What it does |
|---|---|---|
| `viewerSetting` | PUBLIC_TO_EVERYONE (default), MUTUAL_FOLLOW_FRIENDS, FOLLOWER_OF_CREATOR, SELF_ONLY | who can view. Effectively required; an empty value is rejected |
| `allowComments` | true (default) | viewers can comment |
| `allowDuet` | false (default) | viewers can Duet |
| `allowStitch` | false (default) | viewers can Stitch |
| `commercialContent` | false (default) | the video is commercial |
| `brandOrganic` | false (default) | promoting your own brand |
| `brandedContent` | false (default) | paid partnership / sponsored |

### Two gotchas you must surface to the user

1. **Boolean inversion bug.** Publora currently maps `allowComments`,
   `allowDuet`, `allowStitch` to TikTok's `disable_*` flags, so the booleans can
   land inverted (sending `allowDuet: true` may disable duets). The status cannot
   be confirmed from the API alone. **Test with a `SELF_ONLY` draft before
   trusting these values.** Tell the user this whenever they change a flag.
2. **Commercial disclosure.** If `commercialContent` is true, at least one of
   `brandOrganic` (your own brand) or `brandedContent` (paid partnership) must
   also be true, or Publora rejects it. `lib.tiktok_settings` enforces this.

### Posting reality

- **Unaudited apps post PRIVATE only.** Until the publishing app passes TikTok's
  review, posts are forced to `SELF_ONLY` regardless of `viewerSetting`. Warn the
  user if a "public" post lands private.
- For reach, use `PUBLIC_TO_EVERYONE`. For an end-to-end test, use `SELF_ONLY`.

## Steps

1. **Gather inputs, goal first.** Ask (or infer) what the caption should earn,
   then shape for it: comments -> end on one specific question tied to the video;
   saves -> promise reference value ("the 3 settings are in the caption");
   shares -> a claim people will want to show someone; profile taps -> an open
   loop the pinned video pays off. Then gather the video topic/script, the
   niche, whether it is commercial, and whether a rendered
   .mp4 path exists.
2. **Draft the caption.** Front-load the first visible line with a reason to read
   or a specific question to comment on. Keep it tight. No em dashes, no AI vocab.
   Optionally restate the hook's open loop as a comment prompt.
3. **Pick hashtags.** 3 to 5, mixed reach: one broad, one to two niche-defining,
   one to two specific to the video. Put them at the end. Never stuff.
4. **Set the flags.** Default to `PUBLIC_TO_EVERYONE`, comments on, duet/stitch
   off, no commercial flags. Adjust per the user, and surface the two gotchas.
   Build with `lib.tiktok_settings(...)`.
5. **Char check.** Confirm caption + hashtags <= 2,200. If over, tighten.
6. **Humanizer pass.** Strip em dashes, AI vocab, rule-of-three, generic openers.
7. **Approval card.** Show: caption, char count, hashtag set, settings summary,
   and the resolved `viewerSetting` (flag if it may post private).
8. **On approval.** Call `lib.publish("video", caption, target_url=<upload or
   profile URL>, video_path=<path or None>, platform_settings=<settings>,
   scheduled_time=<iso or None>, platforms=[<TIKTOK_PLATFORM_ID>])`. With a video
   path and Publora configured, it runs draft -> upload -> schedule. Without one,
   it returns the caption and settings to upload in-app.

## Hard rules

Global voice rules: see root `SKILL.md` Voice rules. Additional skill-specific
rules:

- Caption + hashtags must fit 2,200 chars (API), hashtags included. Aim far under.
- 3 to 5 hashtags, mixed reach, at the end. Never 10+, never mid-sentence.
- The caption never does the hook's job. The hook is in the video.
- Always set `viewerSetting`. Never ship an empty value.
- Surface the boolean inversion warning whenever an interaction flag changes.

## Anti-patterns (skill will refuse)

- Hashtag walls (10+), or hashtags jammed into the sentence.
- Em dashes in the caption.
- "Follow for part 2 / like and subscribe / don't forget to share" stacks.
- A caption that repeats the spoken hook word for word.
- `commercialContent: true` with neither brand flag set.
- Claiming a post will be public when the app is unaudited (it will be private).

## Resources

- `../../references/voice-rules.md` - caption and hashtag rules
- `../../references/algorithm-heuristics.md` - caption, hashtag, and settings heuristics
- `references/settings-matrix.md` - every platformSettings.tiktok value, defaults, and the known bugs
- `lib/publora_client.py` - `tiktok_settings(...)`, `publish_video(...)`, `create_draft(...)`

## Related skills

- `tt-hook-scripter` - the in-video hook (the caption does not replace it)
- `tt-humanizer` - scrub the caption before publishing
- `tt-content-planner` - schedule captions across a posting week
