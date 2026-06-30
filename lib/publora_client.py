"""Thin Publora REST client for the TikTok Skills project.

Wraps the Publora API endpoints this bundle uses. As of 2026-06 Publora exposes:
- POST /create-post              (create a draft or schedule a post)
- POST /get-upload-url           (pre-signed S3 URL for media)
- PUT  /update-post/:id          (set scheduledTime to schedule a draft)
- GET  /platform-connections     (list connected accounts + token health)

TikTok is a **video-only** platform: a text-only post cannot be published. Every
TikTok post follows the draft -> upload -> schedule flow:

    1. POST /create-post              -> omit scheduledTime (creates a draft)
    2. POST /get-upload-url           -> pre-signed S3 URL for the video
    3. PUT  {uploadUrl}               -> upload the .mp4 to S3
    4. PUT  /update-post/:postGroupId -> set scheduledTime to schedule it

`publish_video` orchestrates all four steps. The user supplies the video file;
this bundle's skills produce the spoken hook script, the caption, and the
`platformSettings.tiktok` flags.

Base URL: https://api.publora.com/api/v1
Auth header: x-publora-key: sk_...  (NOT Bearer)
Content-Type: application/json. Server-to-server only (custom headers are not in
the CORS allowlist, so browser calls fail preflight).

Design note: this client is deliberately minimal. Skills call it after the user
has approved a script and caption rendered via `lib/approval.py`. Write methods
retry on transient 408/429/5xx via the shared retry decorator.
"""
from __future__ import annotations
import os
import time
import random
from typing import Any, Optional

import requests


class PubloraError(RuntimeError):
    pass


RETRYABLE_STATUSES = {408, 429, 500, 502, 503, 504}


def _retry(attempts: int = 3, base_delay: float = 0.6):
    """Retry decorator for HTTP methods. Triggers on 408/429/5xx and on
    transient network errors. Exponential backoff with jitter."""

    def decorator(fn):
        def wrapper(*args, **kwargs):
            last_exc: Optional[Exception] = None
            for attempt in range(attempts):
                try:
                    return fn(*args, **kwargs)
                except PubloraError as e:
                    msg = str(e)
                    retryable = any(f"HTTP {s}" in msg for s in RETRYABLE_STATUSES)
                    if not retryable or attempt == attempts - 1:
                        raise
                    last_exc = e
                except (requests.ConnectionError, requests.Timeout) as e:
                    if attempt == attempts - 1:
                        raise
                    last_exc = e
                time.sleep(base_delay * (2**attempt) + random.uniform(0, 0.25))
            assert last_exc is not None
            raise last_exc

        return wrapper

    return decorator


# Platform IDs must match Publora's regex: /^[a-z]+-[a-zA-Z0-9_-]+$/
# For TikTok the prefix is `tiktok-` (e.g. "tiktok-7123456789").
PLATFORM_ID_PREFIX = "tiktok-"

# TikTok caption hard limit on the Content Posting API (native app allows 4,000).
TIKTOK_CAPTION_MAX = 2200


def tiktok_settings(
    *,
    viewer_setting: str = "PUBLIC_TO_EVERYONE",
    allow_comments: bool = True,
    allow_duet: bool = False,
    allow_stitch: bool = False,
    commercial_content: bool = False,
    brand_organic: bool = False,
    branded_content: bool = False,
) -> dict[str, Any]:
    """Build a `platformSettings.tiktok` object for create_post / publish_video.

    Mirrors Publora's documented defaults. `viewerSetting` is effectively
    required: the validator rejects an empty value with "TikTok requires
    selecting who can view your post". Valid values: PUBLIC_TO_EVERYONE,
    MUTUAL_FOLLOW_FRIENDS, FOLLOWER_OF_CREATOR, SELF_ONLY.

    Two gotchas the skills must surface to the user:

    1. Boolean inversion bug: Publora's publisher currently maps allowComments /
       allowDuet / allowStitch to TikTok's disable_* flags, so the booleans land
       inverted. If you need duets enabled, the field may have to be sent as
       false. Test with a SELF_ONLY draft before trusting the value. This helper
       passes values straight through; it does not pre-invert them.
    2. commercialContent=True requires brandOrganic or brandedContent to also be
       True, or Publora returns a validation error.
    """
    if commercial_content and not (brand_organic or branded_content):
        raise PubloraError(
            "commercial_content=True requires brand_organic or branded_content "
            "to also be True (TikTok commercial disclosure rule)."
        )
    return {
        "tiktok": {
            "viewerSetting": viewer_setting,
            "allowComments": allow_comments,
            "allowDuet": allow_duet,
            "allowStitch": allow_stitch,
            "commercialContent": commercial_content,
            "brandOrganic": brand_organic,
            "brandedContent": branded_content,
        }
    }


class PubloraClient:
    BASE_URL = "https://api.publora.com/api/v1"

    def __init__(self, api_key: Optional[str] = None, timeout: float = 60.0):
        self.api_key = api_key or os.getenv("PUBLORA_API_KEY")
        if not self.api_key:
            raise PubloraError(
                "PUBLORA_API_KEY not set. Export it or pass api_key= explicitly."
            )
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update(
            {
                "x-publora-key": self.api_key,
                "Content-Type": "application/json",
            }
        )

    # ---- Posts (create / schedule) ---------------------------------------

    def create_post(
        self,
        *,
        content: str,
        platforms: list[str],
        scheduled_time: Optional[str] = None,
        platform_settings: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Create a TikTok post or draft.

        For TikTok, omit `scheduled_time` to create a draft (the only valid
        first step, since the video has to be uploaded before scheduling). Then
        call `get_upload_url` + `upload_to_presigned` + `schedule_post`, or use
        the `publish_video` helper that runs the whole flow.

        Args:
            content: Caption text (<= 2,200 chars on the API). Hashtags count
                toward this limit.
            platforms: List of platform connection IDs, e.g. ["tiktok-7123"].
                Each must match /^[a-z]+-[a-zA-Z0-9_-]+$/.
            scheduled_time: ISO 8601 UTC datetime. Omit for a draft. For TikTok,
                only set this AFTER the video is uploaded (use schedule_post).
            platform_settings: Per-platform settings. Build the tiktok object
                with `tiktok_settings(...)`.

        Returns:
            { "success": true, "postGroupId": "..." } on HTTP 200.
        """
        if not content or not content.strip():
            raise PubloraError("content is required (cannot be empty or whitespace)")
        if len(content) > TIKTOK_CAPTION_MAX:
            raise PubloraError(
                f"caption is {len(content)} chars; TikTok API caps captions at "
                f"{TIKTOK_CAPTION_MAX} (hashtags included)."
            )
        if not platforms:
            raise PubloraError("at least one platform ID is required")
        payload: dict[str, Any] = {"content": content, "platforms": platforms}
        if scheduled_time:
            payload["scheduledTime"] = scheduled_time
        if platform_settings:
            payload["platformSettings"] = platform_settings
        return self._post("/create-post", payload)

    def create_draft(
        self,
        *,
        content: str,
        platforms: list[str],
        platform_settings: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Create a TikTok draft (create_post with no scheduledTime)."""
        return self.create_post(
            content=content,
            platforms=platforms,
            scheduled_time=None,
            platform_settings=platform_settings,
        )

    # ---- Media upload -----------------------------------------------------

    def get_upload_url(
        self,
        *,
        file_name: str,
        post_group_id: str,
        content_type: str = "video/mp4",
        media_type: str = "video",
    ) -> dict[str, Any]:
        """Request a pre-signed S3 URL to upload a video for a draft.

        `media_type` MUST be "video" for TikTok (it sets the S3 key prefix;
        omitting it makes the upload fail). Returns
        { success, uploadUrl, fileUrl, mediaId }. The uploadUrl expires in 1h.
        """
        return self._post(
            "/get-upload-url",
            {
                "fileName": file_name,
                "contentType": content_type,
                "type": media_type,
                "postGroupId": post_group_id,
            },
        )

    def upload_to_presigned(
        self, upload_url: str, file_path: str, content_type: str = "video/mp4"
    ) -> None:
        """PUT a local video file to the pre-signed S3 URL from get_upload_url."""
        with open(file_path, "rb") as f:
            r = requests.put(
                upload_url,
                data=f,
                headers={"Content-Type": content_type},
                timeout=max(self.timeout, 300.0),
            )
        if r.status_code >= 400:
            raise PubloraError(f"S3 upload failed HTTP {r.status_code}: {r.text[:300]}")

    def schedule_post(
        self, post_group_id: str, scheduled_time: str
    ) -> dict[str, Any]:
        """Schedule a draft by setting status=scheduled + scheduledTime.

        Call this only after the video has finished uploading to S3.
        """
        return self._put(
            f"/update-post/{post_group_id}",
            {"status": "scheduled", "scheduledTime": scheduled_time},
        )

    # ---- High-level flow --------------------------------------------------

    def publish_video(
        self,
        *,
        content: str,
        platforms: list[str],
        video_path: str,
        scheduled_time: Optional[str] = None,
        platform_settings: Optional[dict[str, Any]] = None,
        content_type: str = "video/mp4",
    ) -> dict[str, Any]:
        """Run the full TikTok publish flow: draft -> upload -> schedule.

        TikTok requires media, so this is the only reliable way to publish via
        the API. If `scheduled_time` is omitted, the post is left as a draft with
        the video attached (publish it later from the dashboard or by calling
        `schedule_post`).

        Returns the postGroupId plus the media/schedule results:
            { "postGroupId", "mediaId", "fileUrl", "scheduled": bool }
        """
        if not os.path.exists(video_path):
            raise PubloraError(f"video file not found: {video_path}")
        draft = self.create_draft(
            content=content,
            platforms=platforms,
            platform_settings=platform_settings,
        )
        post_group_id = draft.get("postGroupId")
        if not post_group_id:
            raise PubloraError(f"create_draft returned no postGroupId: {draft}")

        file_name = os.path.basename(video_path)
        up = self.get_upload_url(
            file_name=file_name,
            post_group_id=post_group_id,
            content_type=content_type,
            media_type="video",
        )
        self.upload_to_presigned(up["uploadUrl"], video_path, content_type)

        scheduled = False
        if scheduled_time:
            self.schedule_post(post_group_id, scheduled_time)
            scheduled = True
        return {
            "postGroupId": post_group_id,
            "mediaId": up.get("mediaId"),
            "fileUrl": up.get("fileUrl"),
            "scheduled": scheduled,
        }

    # ---- Connections (read) ----------------------------------------------

    def list_connections(self) -> list[dict[str, Any]]:
        """List connected social accounts with token health.

        Returns the `connections` array from GET /platform-connections. Each
        entry has platformId, username, displayName, tokenStatus, lastError,
        etc. Use it to confirm a TikTok account is connected and which
        `tiktok-<id>` to pass to `create_post` / `publish_video`.
        """
        r = self._session.get(
            self.BASE_URL + "/platform-connections", timeout=self.timeout
        )
        data = self._handle(r)
        return data.get("connections", [])

    def tiktok_connections(self) -> list[dict[str, Any]]:
        """Convenience filter: only the connected TikTok accounts."""
        return [
            c
            for c in self.list_connections()
            if str(c.get("platformId", "")).startswith(PLATFORM_ID_PREFIX)
        ]

    # ---- Internals --------------------------------------------------------

    @_retry()
    def _post(self, path: str, json_body: dict[str, Any]) -> dict[str, Any]:
        r = self._session.post(
            self.BASE_URL + path, json=json_body, timeout=self.timeout
        )
        return self._handle(r)

    @_retry()
    def _put(self, path: str, json_body: dict[str, Any]) -> dict[str, Any]:
        r = self._session.put(
            self.BASE_URL + path, json=json_body, timeout=self.timeout
        )
        return self._handle(r)

    @staticmethod
    def _handle(r: requests.Response) -> dict[str, Any]:
        if r.status_code >= 400:
            try:
                body = r.json()
            except Exception:
                body = {"error": r.text[:500]}
            raise PubloraError(f"HTTP {r.status_code}: {body}")
        return r.json()
