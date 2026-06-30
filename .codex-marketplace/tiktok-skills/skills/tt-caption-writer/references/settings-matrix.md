# platformSettings.tiktok: full matrix, defaults, and known bugs

Every field Publora accepts inside `platformSettings.tiktok`, with the documented
default and the gotchas. Build the object with `lib.tiktok_settings(...)` rather
than hand-writing it; the helper enforces the commercial-disclosure rule.

## Viewer setting

`viewerSetting` is **effectively required**. The validator rejects an empty value
with "TikTok requires selecting who can view your post". The API route defaults
to `PUBLIC_TO_EVERYONE`, but always set it explicitly.

| Value | Who can view |
|---|---|
| `PUBLIC_TO_EVERYONE` | anyone (use this for reach) |
| `MUTUAL_FOLLOW_FRIENDS` | only mutual followers |
| `FOLLOWER_OF_CREATOR` | only your followers |
| `SELF_ONLY` | only you (use this to test a post end to end) |

## Interaction settings

| Field | Default | Intended meaning |
|---|---|---|
| `allowComments` | true | viewers can comment |
| `allowDuet` | false | viewers can Duet your video |
| `allowStitch` | false | viewers can Stitch your video |

> **Known boolean inversion bug.** Publora's publisher currently maps these to
> TikTok's `disable_*` flags, which inverts them: sending `allowDuet: true` can
> map to `disable_duet: true` and **disable** duets. The same applies to
> comments and stitch. The bug lives in a separate publisher service and cannot
> be confirmed from the API source alone.
>
> **How to handle it:** test with a `SELF_ONLY` draft and check the live post
> before you trust a value. If duets are off when you asked for on, send the
> opposite. The `lib.tiktok_settings` helper passes values straight through (it
> does not pre-invert), so you control the workaround explicitly.

## Commercial content settings

| Field | Default | Meaning |
|---|---|---|
| `commercialContent` | false | the video is commercial / promotional |
| `brandOrganic` | false | promoting your own brand or product |
| `brandedContent` | false | paid partnership or sponsored content |

> **Disclosure rule:** if `commercialContent` is true, at least one of
> `brandOrganic` or `brandedContent` must also be true, or Publora returns a
> validation error. `lib.tiktok_settings` raises before the request if you break
> this.

Set the right flag. Failing to disclose a paid partnership violates TikTok's
community guidelines, not just Publora's validation.

## Posting reality

- **Unaudited apps post PRIVATE only.** Until the publishing app passes TikTok's
  review, every post is forced to `SELF_ONLY` regardless of `viewerSetting`. If a
  "public" post lands private, this is why.
- **Rate limits:** 15 to 20 posts/day, 2 videos/minute. Space posts out.
- **Caption cap:** 2,200 chars on the API (hashtags included). The native app
  allows 4,000, but the API enforces 2,200.

## Examples

Public reach video, comments on, duet/stitch off (the common default):

```python
from lib import tiktok_settings
settings = tiktok_settings()  # PUBLIC_TO_EVERYONE, comments on, duet/stitch off
```

A paid partnership, public, duets enabled (remember the inversion: test it):

```python
settings = tiktok_settings(
    viewer_setting="PUBLIC_TO_EVERYONE",
    allow_duet=True,            # verify on a SELF_ONLY draft first
    commercial_content=True,
    branded_content=True,       # required because commercial_content is True
)
```

A safe end-to-end test post nobody else sees:

```python
settings = tiktok_settings(viewer_setting="SELF_ONLY")
```
