"""Approval gate helpers.

Every skill that posts to TikTok MUST present a draft (hook script + caption +
settings) to the user and wait for explicit approval before calling Publora.
This file is a thin conventions layer, not runtime enforcement. Skills call
`render_approval_card` to format the draft consistently and then stop until the
user says go.
"""
from __future__ import annotations
from typing import Optional


def render_approval_card(
    *,
    kind: str,  # "video" | "caption" | "hook-script" | "plan"
    preview_text: str,
    target_url: Optional[str] = None,
    char_count: Optional[int] = None,
    settings_summary: Optional[str] = None,
    extra_context: Optional[dict] = None,
) -> str:
    """Format a standardized approval card for the user to review.

    The card MUST contain:
    - What the action is (video / caption / hook-script / plan)
    - The full preview text (the spoken hook + on-screen text, or the caption)
    - Caption char count (TikTok API caps captions at 2,200)
    - A `platformSettings.tiktok` summary if relevant
    - A clear prompt: "reply post / yes to publish, or suggest edits"
    """
    lines = [f"## Draft ready for approval - {kind}", ""]
    if target_url:
        lines.append(f"**Target:** {target_url}")
    if char_count is None and kind == "caption":
        char_count = len(preview_text)
    if char_count is not None:
        flag = "  (over 2,200 limit)" if char_count > 2200 else ""
        lines.append(f"**Caption chars:** {char_count}{flag}")
    if settings_summary:
        lines.append(f"**TikTok settings:** {settings_summary}")
    lines.append("")
    lines.append("**Preview:**")
    lines.append("")
    for pl in preview_text.splitlines() or [""]:
        lines.append(f"> {pl}")
    lines.append("")
    if extra_context:
        lines.append("**Context:**")
        for k, v in extra_context.items():
            lines.append(f"- **{k}**: {v}")
        lines.append("")
    lines.append("Reply **post** / **yes** to publish, or suggest edits.")
    return "\n".join(lines)
