"""Apify read client for the TikTok Skills project.

The read layer: scan a niche's videos, pull the commenters on a video, and read
a profile's stats, so a skill can see what is working instead of guessing. Uses
run-sync-get-dataset-items (one HTTP request, no polling).

Auth: APIFY_TOKEN env var (or constructor arg). Free token at
https://console.apify.com/account/integrations .

Actors (verified live 2026-07-14):
  - clockworks/tiktok-scraper: hashtag/search/profile videos with playCount,
      diggCount (likes), commentCount, shareCount, authorMeta {name, fans}.
  - clockworks/tiktok-comments-scraper: comments on a video (cid, text,
      diggCount, uniqueId, replyCommentTotal).

What TikTok does NOT expose: who LIKED a video (platform wall - only counts). The
engagement signal is COMMENTERS + video performance, not likers.

Caching: in-process LRU (256 entries, 6h TTL). Retries transient 429/5xx.
"""
from __future__ import annotations
import os
import random
import time
from collections import OrderedDict
from typing import Any, Optional

import requests

RUN_SYNC = "https://api.apify.com/v2/acts/{actor}/run-sync-get-dataset-items"
SCRAPER = "clockworks~tiktok-scraper"
COMMENTS = "clockworks~tiktok-comments-scraper"
RETRYABLE_STATUSES = {429, 500, 502, 503, 504}
CACHE_MAX_ENTRIES = 256
CACHE_TTL_SECONDS = 6 * 60 * 60
SIGNUP_URL = "https://console.apify.com/account/integrations"


class ApifyError(RuntimeError):
    pass


class ApifyAuthError(ApifyError):
    """No token configured. Message explains the free path + paste fallback."""


def _retry(attempts: int = 3, base_delay: float = 0.6):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            last: Optional[Exception] = None
            for i in range(attempts):
                try:
                    return fn(*args, **kwargs)
                except ApifyError as e:
                    if getattr(e, "status", None) not in RETRYABLE_STATUSES or i == attempts - 1:
                        raise
                    last = e
                    time.sleep(base_delay * (2 ** i) + random.uniform(0, 0.3))
            if last:
                raise last
        return wrapper
    return decorator


def _video(v: dict) -> dict:
    au = v.get("authorMeta") or {}
    return {
        "id": v.get("id"),
        "text": v.get("text"),
        "author": au.get("name"),
        "author_followers": au.get("fans"),
        "plays": v.get("playCount", 0),
        "likes": v.get("diggCount", 0),
        "comments": v.get("commentCount", 0),
        "shares": v.get("shareCount", 0),
        "url": v.get("webVideoUrl"),
        "created_at": v.get("createTimeISO"),
        "music": (v.get("musicMeta") or {}).get("musicName"),
    }


def _comment(c: dict) -> dict:
    return {
        "author": c.get("uniqueId") or (c.get("user") or {}).get("uniqueId"),
        "text": c.get("text"),
        "likes": c.get("diggCount", 0),
        "replies": c.get("replyCommentTotal", 0),
        "pinned": c.get("pinnedByAuthor", False),
        "liked_by_author": c.get("likedByAuthor", False),
        "created_at": c.get("createTimeISO"),
    }


class ApifyClient:
    def __init__(self, token: Optional[str] = None, timeout: int = 180):
        self.token = token or os.environ.get("APIFY_TOKEN")
        self.timeout = timeout
        self._cache: "OrderedDict[str, tuple[float, Any]]" = OrderedDict()

    def _require(self) -> str:
        if not self.token:
            raise ApifyAuthError(
                "No APIFY_TOKEN set. Get one free at "
                f"{SIGNUP_URL}. Or paste the videos/comments you already have and "
                "the skill will run the same analysis on them."
            )
        return self.token

    def _cget(self, k):
        h = self._cache.get(k)
        if h and (time.time() - h[0]) < CACHE_TTL_SECONDS:
            self._cache.move_to_end(k)
            return h[1]
        return None

    def _cput(self, k, v):
        self._cache[k] = (time.time(), v)
        self._cache.move_to_end(k)
        while len(self._cache) > CACHE_MAX_ENTRIES:
            self._cache.popitem(last=False)

    @_retry()
    def _run(self, actor: str, payload: dict) -> list[dict]:
        try:
            r = requests.post(RUN_SYNC.format(actor=actor),
                              params={"token": self._require()}, json=payload,
                              timeout=self.timeout)
        except requests.RequestException as e:
            err = ApifyError(f"network error: {e}"); err.status = 503; raise err
        if r.status_code >= 400:
            err = ApifyError(f"actor {actor} returned {r.status_code}: {r.text[:200]}")
            err.status = r.status_code; raise err
        data = r.json()
        if not isinstance(data, list):
            raise ApifyError(f"unexpected response shape: {str(data)[:150]}")
        return data

    # ---- public read methods ----
    def fetch_niche_videos(self, hashtag: str, max_items: int = 20,
                           force_refresh: bool = False) -> list[dict]:
        """Top videos for a hashtag (niche discovery). Pass the tag without '#'."""
        tag = hashtag.lstrip("#")
        ck = f"tag:{tag}:{max_items}"
        if not force_refresh and (c := self._cget(ck)) is not None:
            return c
        rows = self._run(SCRAPER, {"hashtags": [tag], "resultsPerPage": max_items,
                                   "shouldDownloadVideos": False, "shouldDownloadCovers": False})
        out = [_video(v) for v in rows if isinstance(v, dict) and v.get("id")]
        self._cput(ck, out)
        return out

    def fetch_profile_videos(self, username: str, max_items: int = 20,
                             force_refresh: bool = False) -> list[dict]:
        """A profile's recent videos (self or competitor). Pass without '@'."""
        u = username.lstrip("@")
        ck = f"profile:{u}:{max_items}"
        if not force_refresh and (c := self._cget(ck)) is not None:
            return c
        rows = self._run(SCRAPER, {"profiles": [u], "resultsPerPage": max_items,
                                   "shouldDownloadVideos": False, "shouldDownloadCovers": False})
        out = [_video(v) for v in rows if isinstance(v, dict) and v.get("id")]
        self._cput(ck, out)
        return out

    def fetch_video_comments(self, video_url: str, max_items: int = 50,
                             force_refresh: bool = False) -> list[dict]:
        """Comments on a video (the engagement signal, since likers are private)."""
        ck = f"comments:{video_url}:{max_items}"
        if not force_refresh and (c := self._cget(ck)) is not None:
            return c
        rows = self._run(COMMENTS, {"postURLs": [video_url], "commentsPerPost": max_items})
        out = [_comment(c) for c in rows if isinstance(c, dict) and c.get("text")]
        self._cput(ck, out)
        return out


if __name__ == "__main__":
    import json as _json
    print(_json.dumps(ApifyClient().fetch_niche_videos("marketing", 3), indent=2))
