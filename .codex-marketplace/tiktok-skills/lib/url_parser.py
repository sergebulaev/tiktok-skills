"""TikTok URL parser.

Handles the common shapes for TikTok videos and profiles:

1. Canonical video URL (from "Copy link" on web):
   https://www.tiktok.com/@HANDLE/video/VIDEO_ID
   ...with optional query params (?is_from_webapp=1&...).

2. Short share URLs (from the in-app "Copy link"):
   https://vm.tiktok.com/ZMabcdef/        (mobile share)
   https://www.tiktok.com/t/ZTabcdef/     (web short)
   These redirect to the canonical URL; we cannot resolve the VIDEO_ID without a
   network request, so we return url_type "short" and the short code.

3. Profile URL:
   https://www.tiktok.com/@HANDLE

4. Bare numeric video ID.

Returns a normalized dict:
    {
      "handle": "<username without @>" | None,
      "video_id": "<numeric>" | None,
      "short_code": "<ZM.../ZT...>" | None,
      "url_type": "video" | "profile" | "short" | "unknown",
      "canonical_url": "https://www.tiktok.com/..." | None,
    }

Note: a TikTok handle keeps its `@` on the platform but the parser strips it in
the `handle` field. Short links must be opened (HTTP redirect) to recover the
numeric video id; this parser does not make network calls.
"""
from __future__ import annotations
import re
from typing import Optional, TypedDict


class ParsedTikTokUrl(TypedDict, total=False):
    handle: Optional[str]
    video_id: Optional[str]
    short_code: Optional[str]
    url_type: str
    canonical_url: Optional[str]


# /@HANDLE/video/VIDEO_ID
_VIDEO_RE = re.compile(
    r"(?:https?://)?(?:www\.|m\.)?tiktok\.com/"
    r"@(?P<handle>[A-Za-z0-9_.]{1,24})"
    r"/video/(?P<id>\d{6,25})",
    re.IGNORECASE,
)
# Short share links: vm.tiktok.com/CODE  or  www.tiktok.com/t/CODE
_SHORT_RE = re.compile(
    r"(?:https?://)?(?:vm|vt)\.tiktok\.com/(?P<code>[A-Za-z0-9]{5,20})"
    r"|(?:https?://)?(?:www\.)?tiktok\.com/t/(?P<code2>[A-Za-z0-9]{5,20})",
    re.IGNORECASE,
)
# Profile: /@HANDLE  (no /video)
_PROFILE_RE = re.compile(
    r"(?:https?://)?(?:www\.|m\.)?tiktok\.com/"
    r"@(?P<handle>[A-Za-z0-9_.]{1,24})/?(?:\?.*)?$",
    re.IGNORECASE,
)


def parse_tiktok_url(url: str) -> ParsedTikTokUrl:
    """Parse any TikTok video, profile, or short-share URL into structured fields.

    >>> p = parse_tiktok_url("https://www.tiktok.com/@levelsio/video/7300000000000000000")
    >>> p["handle"]
    'levelsio'
    >>> p["video_id"]
    '7300000000000000000'
    >>> p["url_type"]
    'video'
    """
    out: ParsedTikTokUrl = {
        "handle": None,
        "video_id": None,
        "short_code": None,
        "url_type": "unknown",
        "canonical_url": None,
    }
    if not url:
        return out

    text = url.strip()

    m = _VIDEO_RE.search(text)
    if m:
        handle = m.group("handle")
        video_id = m.group("id")
        out["handle"] = handle
        out["video_id"] = video_id
        out["url_type"] = "video"
        out["canonical_url"] = f"https://www.tiktok.com/@{handle}/video/{video_id}"
        return out

    m = _SHORT_RE.search(text)
    if m:
        code = m.group("code") or m.group("code2")
        out["short_code"] = code
        out["url_type"] = "short"
        out["canonical_url"] = text.split("?")[0]
        return out

    m = _PROFILE_RE.search(text)
    if m:
        handle = m.group("handle")
        out["handle"] = handle
        out["url_type"] = "profile"
        out["canonical_url"] = f"https://www.tiktok.com/@{handle}"
        return out

    # Bare numeric video id with no host.
    if re.fullmatch(r"\d{6,25}", text):
        out["video_id"] = text
        out["url_type"] = "video"
        out["canonical_url"] = f"https://www.tiktok.com/@i/video/{text}"
        return out

    return out


def build_video_url(handle: str, video_id: str) -> str:
    """Format a canonical tiktok.com video URL from a handle and video id."""
    handle = handle.lstrip("@")
    return f"https://www.tiktok.com/@{handle}/video/{video_id}"


if __name__ == "__main__":
    import json
    import sys

    examples = sys.argv[1:] or [
        "https://www.tiktok.com/@levelsio/video/7300000000000000000?is_from_webapp=1",
        "https://vm.tiktok.com/ZMabcdef12/",
        "https://www.tiktok.com/t/ZTxyz98765/",
        "https://www.tiktok.com/@nasa",
    ]
    for u in examples:
        print(u)
        print(json.dumps(parse_tiktok_url(u), indent=2))
        print()
