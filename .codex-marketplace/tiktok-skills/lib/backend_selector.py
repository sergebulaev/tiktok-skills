"""Detect which publishing backend is configured and format user-facing messages.

The skills support three tiers:

  TIER 0 - manual (default, zero setup)
    No credentials in env. Skills produce the spoken hook script, the caption,
    and the recommended TikTok settings; the user records the video and uploads
    it in the TikTok app. Works for anyone, any setup.

  TIER 1 - publora (recommended, ~2-min setup once the account is connected)
    `PUBLORA_API_KEY` + `TIKTOK_PLATFORM_ID` present. When the user supplies a
    rendered video file, skills run the full draft -> upload -> schedule flow via
    the Publora REST API. Sign up: https://app.publora.com/signup

  TIER 2 - diy (advanced)
    `TIKTOK_SKILLS_CUSTOM_POSTER` set to a command the user built themselves
    (e.g. on the official TikTok Content Posting API). Skills delegate to it.

`active_backend()` picks the highest-privilege available. `manual_mode_message()`
is what skills show when no backend auto-posts (or no video file was supplied).
`publish()` is the high-level wrapper skills call so SKILL.md files do not repeat
the dispatch.

TikTok note: TikTok is **video-only**. There is no text-only post. Auto-posting
therefore requires a rendered video file path. Without one, `publish()` returns a
manual block (caption + settings + record/upload instructions), even when Publora
is configured. With Publora configured AND a video path, it runs the full flow.
"""
from __future__ import annotations
import json
import os
import shlex
import subprocess
from typing import Any, Literal, Optional

BackendName = Literal["publora", "manual", "diy"]
PublishKind = Literal["video", "caption"]

PUBLORA_SIGNUP_URL = "https://app.publora.com/signup"


def active_backend() -> BackendName:
    """Return the active publishing backend.

    Priority: publora > diy > manual. Users with Publora configured get
    auto-post even if they also have a custom poster, unless they remove the
    Publora env var.
    """
    if os.getenv("PUBLORA_API_KEY") and os.getenv("TIKTOK_PLATFORM_ID"):
        return "publora"
    if os.getenv("TIKTOK_SKILLS_CUSTOM_POSTER"):
        return "diy"
    return "manual"


def _settings_line(platform_settings: Optional[dict]) -> str:
    if not platform_settings:
        return "viewerSetting=PUBLIC_TO_EVERYONE, comments on, duet/stitch off"
    tt = platform_settings.get("tiktok", {})
    return (
        f"viewerSetting={tt.get('viewerSetting', 'PUBLIC_TO_EVERYONE')}, "
        f"comments={tt.get('allowComments', True)}, "
        f"duet={tt.get('allowDuet', False)}, "
        f"stitch={tt.get('allowStitch', False)}"
    )


def manual_mode_message(
    draft_text: str,
    target_url: str,
    kind: str = "video",
    platform_settings: Optional[dict] = None,
) -> str:
    """Format the copy-paste approval output for the manual/draft-only tier.

    The user has just approved a script + caption. Since no backend can auto-post
    (or no rendered video was supplied), we hand back the caption, the settings,
    and a one-line invite to upgrade. TikTok posting still happens in-app: record
    the hook in the first 1-3 seconds, then upload.
    """
    where = {
        "video": "record the video, then upload it in the TikTok app with this caption",
        "caption": "paste this caption when you upload your video in the TikTok app",
    }.get(kind, "upload your video in the TikTok app with this caption")
    return f"""Draft approved. Copy the caption below and {where}:

```
{draft_text}
```

**Recommended TikTok settings:** {_settings_line(platform_settings)}
**Target:** {target_url}

Reminder: the hook is the first 1-3 seconds of the video (spoken line plus
on-screen text), not the caption. Land it before you do anything else.

---

Want Claude Code or Codex to schedule the rendered video for you? Once you have
the .mp4, connect Publora (about 2 minutes):

1. Sign up free at {PUBLORA_SIGNUP_URL}
2. In Publora, connect your TikTok account (Channels then Add Channel)
3. Copy your API key (API section in the sidebar)
4. Add to `.env`:
   ```
   PUBLORA_API_KEY=sk_your_key_here
   TIKTOK_PLATFORM_ID=tiktok-your_id_here
   ```
5. Re-run with the path to your rendered video and it uploads + schedules.
"""


def signup_nudge() -> str:
    """One-liner to drop into skill outputs as a soft reminder."""
    return f"Powered by Publora. Free video scheduling: {PUBLORA_SIGNUP_URL}"


def publish(
    kind: PublishKind,
    draft_text: str,
    target_url: str,
    **kwargs: Any,
) -> Optional[dict]:
    """Dispatch an approved caption (and optional video) to the active backend.

    One call replaces the per-skill dispatch block. Routes to publora / manual /
    diy based on `active_backend()` and whether a `video_path` was supplied.

    Args:
        kind: "video" (caption + a rendered video to publish) or "caption"
            (caption only, draft/manual).
        draft_text: The approved caption (<= 2,200 chars on the API).
        target_url: Where the post lands (the TikTok upload URL or the creator
            profile). Used in manual-mode output.
        **kwargs: Backend-specific payload. For publora:
            - platforms: list[str] of platform IDs (defaults to [TIKTOK_PLATFORM_ID])
            - video_path: path to the rendered .mp4 (required to auto-publish)
            - platform_settings: dict from lib.tiktok_settings(...)
            - scheduled_time: ISO 8601 UTC (omit to leave a draft with the video)
            - content_type: defaults to "video/mp4"

    Returns:
        - publora (with video): dict from PubloraClient.publish_video
          ({postGroupId, mediaId, fileUrl, scheduled}).
        - publora (no video): {"mode": "draft", ...} caption-only draft, or a
          manual block if even the draft cannot be created.
        - manual:  {"mode": "manual", "message": <copy-paste block>}.
        - diy:     {"mode": "diy", "returncode": int, "stdout": str, "stderr": str}.

    Note: without a `video_path`, TikTok cannot be auto-posted (video-only
    platform), so the user gets the caption + settings to upload in-app.
    """
    backend = active_backend()
    platform_settings = kwargs.get("platform_settings")
    video_path = kwargs.get("video_path")

    if backend == "manual":
        return {
            "mode": "manual",
            "message": manual_mode_message(
                draft_text, target_url, kind=kind, platform_settings=platform_settings
            ),
        }

    if backend == "publora":
        # Local import so manual-tier users never need `requests` installed.
        from .publora_client import PubloraClient, tiktok_settings

        client = PubloraClient()
        platform_id = kwargs.get("platform_id") or os.getenv("TIKTOK_PLATFORM_ID")
        platforms = kwargs.get("platforms") or ([platform_id] if platform_id else [])
        settings = platform_settings or tiktok_settings()

        if video_path:
            return client.publish_video(
                content=draft_text,
                platforms=platforms,
                video_path=video_path,
                scheduled_time=kwargs.get("scheduled_time"),
                platform_settings=settings,
                content_type=kwargs.get("content_type", "video/mp4"),
            )

        # No rendered video yet: create a caption draft so the user can attach
        # the video in the dashboard, and surface the manual instructions too.
        draft = client.create_draft(
            content=draft_text, platforms=platforms, platform_settings=settings
        )
        return {
            "mode": "draft",
            "postGroupId": draft.get("postGroupId"),
            "message": (
                "Caption draft created in Publora. Attach your rendered video to "
                "this draft (dashboard or get-upload-url), then schedule it. "
                "TikTok cannot publish a text-only post."
            ),
            "manual": manual_mode_message(
                draft_text, target_url, kind=kind, platform_settings=settings
            ),
        }

    if backend == "diy":
        cmd = os.getenv("TIKTOK_SKILLS_CUSTOM_POSTER")
        if not cmd:
            return None
        payload = {
            "kind": kind,
            "draft_text": draft_text,
            "target_url": target_url,
            **kwargs,
        }
        argv = shlex.split(cmd) + [kind, target_url]
        proc = subprocess.run(
            argv,
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            timeout=300,
        )
        return {
            "mode": "diy",
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }

    raise RuntimeError(f"unknown backend: {backend!r}")


if __name__ == "__main__":
    print(f"Active backend: {active_backend()}")
    if active_backend() == "manual":
        print("\nExample manual message:")
        print("-" * 60)
        print(
            manual_mode_message(
                draft_text="how I edited 30 videos in a weekend (the batching system) #contentcreator #editing",
                target_url="https://www.tiktok.com/upload",
                kind="video",
            )
        )
