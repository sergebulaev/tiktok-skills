# 2026 TikTok Posting Heuristics

Synthesized from TikTok's published "How TikTok recommends content" material,
Creator Portal guidance, public statements from the TikTok engineering and
creator teams, and observed creator data. Numbers marked "reported" are
community-measured, not officially confirmed.

## The core truth: completion rate is king

TikTok's For You ranker is a watch-time machine. The single heaviest input is
**how much of the video each viewer watches**, expressed as completion rate and
average watch time. A 20-second video watched fully beats a 90-second video
watched halfway. Everything in the hook-formulas reference exists to protect
completion.

## Signal weights (relative reach impact)

Reported relative weights from TikTok's own creator material and creator testing:

| Signal | Relative weight | Note |
|---|---|---|
| **Completion rate / full watch** | highest | the foundation of the ranker; watch to the last frame |
| **Rewatch / loop** | very high | a rewatch counts almost like a fresh view and signals replay value |
| **Share (send to a friend, repost)** | high | re-injects the video into a new follower graph |
| **Save** | high | private "I will come back to this" signal; reference-worthy content |
| **Comment** | medium-high | a real comment thread signals conversation |
| **Follow from the video** | high (long-term) | the compounding signal; one follow outweighs many likes |
| **Like** | low | cheap affirmation, light reach |
| **Negative: "not interested", swipe-away in <2s, hide, report** | heavy penalty | a fast swipe-away is the strongest negative signal |

Takeaway: optimize for **completion, rewatch, shares, and saves**, not likes.
The "save" analog that the goal-tag system targets is **saves + rewatches +
shares** together, because all three say the video was worth more than one pass.

## The first 1-3 seconds

- **The hook decides the video.** A swipe-away inside the first 2 seconds is the
  heaviest negative signal you can earn. The opening frame, the first spoken line,
  and the first on-screen text all have to fire at once. See `hook-formulas.md`.
- **No intro.** Logos, greetings, and slow zooms in the first second are the top
  completion killers. Start on the result or the tension.
- **Muted-first viewing is common.** The on-screen text must carry the promise
  with the sound off.

## Reach amplifiers

- **A strong loop.** Design the last frame so the video restarts cleanly. A
  rewatch is one of the cheapest ways to push average watch time above 100%.
- **Trending sounds, used early.** A sound on the way up carries a reach boost.
  Ride it in the first 1-3 days of its climb, and bend it to your niche (T10).
  See "Sound selection" below and `tt-trend-mapper`.
- **Native text and captions.** On-screen text, auto-captions, and a strong cover
  frame all lift completion and accessibility.
- **Replying to comments with a video.** A video reply both restarts a
  conversation and gives you a free, pre-warmed hook.
- **Consistency and a clear niche.** A recognizable niche trains the ranker on who
  to show you to, which raises the floor on every post.

## Reach suppressors (avoid)

- **A slow or vague hook.** The number-one reason a video dies is a first second
  that gives no reason to stay.
- **Watermarks from other apps** (a competing video app's logo). TikTok is
  reported to suppress re-uploaded content carrying another platform's watermark.
  Export clean.
- **Engagement bait** ("comment YES", "follow for part 2" with no part 2)
  is downranked, not rewarded.
- **Reposting near-duplicate videos** trips a similarity penalty.
- **15+ hashtags / hashtag stuffing** reads as spam and does not buy reach.
- **Long dead stretches** mid-video. If attention dips, cut faster or add a
  pattern break.

## Video length

- **There is no single best length; there is best completion.** Pick the shortest
  length that fully delivers the one idea. A 15 to 34 second video that is watched
  fully often outperforms a 3-minute one watched 40%.
- **Longer videos (1 to 10 min via the API) can work** for tutorials and stories,
  but only if retention holds. Do not pad to hit a length.
- **API caps:** caption 2,200 chars, video up to 10 minutes, up to 4 GB, MP4 /
  MOV / WebM, minimum 23 FPS. The native app allows longer captions (4,000) and
  longer video (up to 60 min), but the publishing API enforces the stricter caps.

## Sound selection

- **A trending sound is a distribution lever, not decoration.** TikTok groups
  videos by sound; riding one on its way up borrows that cluster's reach.
- **Catch the sound early.** A sound in its first 1 to 3 days of climbing carries
  the most lift. By the time it is everywhere, the boost is gone and you read as
  late.
- **Original audio builds a niche asset.** A sound you create that others reuse
  becomes its own distribution channel back to you.
- **Match the sound to the niche.** A trending sound forced onto a clashing niche
  reads as cringe and costs trust. See `tt-trend-mapper` for the fit check.

## Caption and hashtags

- **Caption <= 2,200 chars (API).** Front-load a reason to read or a reason to
  comment in the first visible line. The caption supports the video; it does not
  replace it.
- **3 to 5 hashtags, mixed reach.** One broad, one to two niche-defining, one to
  two specific to the video. Stuffing does nothing in 2026.
- **A caption can ask the comment.** A specific question in the caption ("which
  one got you?") earns the comment thread that feeds reach.

## Posting settings (platformSettings.tiktok)

- **viewerSetting is effectively required.** Use `PUBLIC_TO_EVERYONE` for reach.
  `SELF_ONLY` is a safe way to test a draft post end to end.
- **Known boolean inversion bug.** Publora currently maps `allowComments`,
  `allowDuet`, `allowStitch` to TikTok's `disable_*` flags, so the booleans can
  land inverted. Test with a `SELF_ONLY` draft before trusting a value. See the
  TikTok platform notes in `tt-caption-writer`.
- **commercialContent disclosure.** If the video promotes a brand or is a paid
  partnership, set `commercialContent` plus `brandOrganic` (your own brand) or
  `brandedContent` (paid). `commercialContent` alone is rejected.
- **Unaudited apps post PRIVATE only.** Until the publishing app passes TikTok's
  review, posts are forced to `SELF_ONLY` regardless of `viewerSetting`.

## Rate limits

| Limit | Value |
|---|---|
| Posts per day (API) | 15 to 20 |
| Videos per minute | 2 max |
| Min video length | 3 seconds |
| Max video length (API) | 10 minutes |

- Space posts out; do not bulk-dump. 1 to 3 quality videos a day beats 10 rushed
  ones.

## Timing

| Audience | Best windows (local) |
|---|---|
| US general / lifestyle | Tue-Thu 6-9 AM and 7-10 PM |
| Gen-Z / late crowd | weeknights 8 PM-midnight |
| Creators / B2B / how-to | weekday late mornings, 10 AM-1 PM |

- TikTok's evergreen tail is longer than most platforms: a strong video can keep
  surfacing for days or weeks, so a "bad time" post is rarely wasted. Consistency
  beats perfect timing.

## Pre-publish checklist

- [ ] The first second shows the result or the tension (no intro, no logo).
- [ ] Spoken hook and on-screen text differ and both carry the promise.
- [ ] One specific number in the hook where the claim allows it.
- [ ] No em dashes (`—`), en dashes (`–`), or double dashes (`--`) in caption or
      on-screen text.
- [ ] No AI vocabulary blacklist words (leverage, fundamentally, delve, etc.).
- [ ] The last frame restarts the loop (designed for a rewatch).
- [ ] Caption <= 2,200 chars; 3 to 5 mixed-reach hashtags at the end.
- [ ] One clear ask (save / comment / follow), not five stacked.
- [ ] Clean export, no competing-app watermark.
- [ ] `viewerSetting` set; commercial flags set if the video promotes a brand.
- [ ] A clear primary goal (completion / saves / comments / shares / follows).
