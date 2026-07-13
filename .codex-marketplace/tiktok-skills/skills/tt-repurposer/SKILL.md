---
name: tt-repurposer
description: Repurpose content into a native TikTok script and caption. Take a LinkedIn post, blog, newsletter, or X thread that worked elsewhere and rebuild it as a spoken script: hook in the first second, every line sayable in one breath, open on the payoff, a trend angle where it fits, plus a caption, published via Publora on approval. Adapts content across platforms. Not for a fresh hook (use tt-hook-scripter), not the caption only (use tt-caption-writer), not auditing a script (use tt-humanizer --mode audit).
---

# TikTok Repurposer

Turn something you already made into a TikTok video script that sounds like it was born on camera. Repurposing is not copy-paste. A post that killed on LinkedIn will die on TikTok if you read it aloud: wrong open, wrong rhythm, sentences no one can say in one breath, and artifacts ("link in bio", hashtag walls, corporate phrasing) that scream off-platform.

This skill transforms, it does not generate. It reads your source, keeps the idea, and rebuilds the delivery as a spoken script plus a short caption for TikTok.

## When to use

- "Turn this LinkedIn post into a TikTok script"
- "Repurpose my blog post / newsletter / X thread for TikTok"
- "This worked on Instagram, adapt it into a video I can film"
- "I have a rough idea in another format, make it native here"

Not for a blank-page hook (use `tt-hook-scripter`), not for the caption on its own (use `tt-caption-writer`), and not for reviewing an already-TikTok script (use `tt-humanizer --mode audit`).

## How it works

1. **Take the source.** Any format: a post, a paragraph, a newsletter, a thread, a caption, a transcript, a bullet list, a link to read. Ask for the source and the goal (completion / saves / comments / shares) if not given.
2. **Extract the spine.** Strip the source platform's shell and pull out the one claim, the one story, or the one number worth keeping. Most repurposing fails because it keeps the words instead of the point.
3. **Open on the payoff.** TikTok decides in the first second. Lead with the result, not the setup. "Here is the fix" beats "let me walk you through the context". The source's opener almost never survives.
4. **Re-hook for the first second.** Hand the opening line to `tt-hook-scripter`: the spoken line, the on-screen text, and the opening visual firing at once, picked by the goal.
5. **Choose the native shape.** A blog or long post -> a 3-part spoken script (hook, value, loop-close). A listicle -> a fast on-screen-text list script, one item per beat. A long video or transcript -> a script that delivers the single payoff, not a summary.
6. **Make every line sayable.** Rewrite each line so it can be said out loud in one breath: contractions, fragments, short lines. If you cannot read it without stopping for air, cut it.
7. **Add a trend or sound angle where it fits.** If a trending sound or format carries the idea, reference `tt-trend-mapper` to check fit and script the twist. Skip it if forcing a trend would bury the point.
8. **Write the caption.** Hand the short caption to `tt-caption-writer`: under 2,200 chars, 3 to 5 mixed-reach hashtags, TikTok settings.
9. **Strip off-platform artifacts.** Remove "link in bio" from other platforms, hashtag walls beyond a few, "smash subscribe", @-handles that only exist elsewhere, corporate phrasing, and any "as I posted on LinkedIn" throat-clearing. A repurposed script should not admit it was repurposed.
10. **Humanizer pass.** Run `tt-humanizer`: it scrubs em dashes, AI vocab, "hey guys" filler, and teleprompter rhythm, and checks every line is sayable out loud in one breath. Keep the user's real numbers and named entities from the source.
11. **Approval card.** Show: source -> TikTok mapping (what became what), the script (hook / value / loop-close), on-screen text, the trend or sound angle if any, the caption, char counts, primary goal.
12. **On approval.** Publish the caption via `lib.publish("video", draft_text=<approved caption>, target_url="https://www.tiktok.com/upload", video_path=<render_or_None>, platforms=[<TIKTOK_PLATFORM_ID>], scheduled_time=<iso_or_None>)`. Without a rendered .mp4, `lib.publish` returns the script, caption, and settings as a copy-paste block to upload in the TikTok app.

## Native-fit rules (source -> TikTok)

- **LinkedIn post -> TikTok:** cut the warm-up. LinkedIn tolerates a slow build; TikTok does not. Rewrite the hook to open on the payoff, and turn the body into lines you can say out loud.
- **Blog / newsletter -> script:** pick the single most repeatable claim as the spoken hook, then a 3-part script (hook, value, loop-close). Do not narrate the whole piece.
- **Listicle -> on-screen-text list:** one item per beat, each a short spoken line with matching on-screen text, not a wall of bullets.
- **X thread -> script:** the thread's best tweet becomes the hook; the rest become beats you speak. Drop the numbering and the "1/" scaffolding.
- **Long video / transcript -> script:** lead with the payoff, deliver one idea, close the loop. Never a summary.
- **Instagram / any caption -> caption:** strip hashtag blocks down to 3 to 5, drop off-platform CTAs, keep it short.

## Hard rules

Global voice rules: see root `SKILL.md` Voice rules. Additional skill-specific rules:

- Keep the source's **claim and facts** intact. Repurposing changes the delivery, never the meaning or the numbers.
- Every line must be sayable out loud in one breath. If it needs a pause for air, cut it.
- The first second must land the whole promise. Open on the payoff, not the setup.
- Never read the source verbatim. Rebuild the hook and rhythm from the spine.
- One specific number where the source offers one. Keep it.
- Do not hard-sell the user's product. One natural mention max.

## Anti-patterns (skill will refuse)

- Copy-pasting the source and reading it aloud (that is not repurposing).
- Keeping the source platform's artifacts ("link in bio", "smash subscribe", hashtag walls, corporate phrasing).
- A slow open that saves the payoff for the end.
- Lines too long to say in one breath.
- Em dashes anywhere.
- Rule-of-three lists without specifics.
- "leverage", "fundamentally", "game-changer", "deep dive", "hey guys".
- Forcing a trending sound that buries the point.

## Resources

- `../../references/hook-formulas.md` - the 10 TikTok 3-second hook formulas to re-hook with
- `../../references/algorithm-heuristics.md` - 2026 TikTok ranking rules (completion, rewatch, shares, sound timing)
- `../../references/voice-rules.md` - the canonical spoken-script and caption voice rules

## Related skills

- `tt-hook-scripter` - script the first-second hook (repurposer hands the open here)
- `tt-trend-mapper` - check trend fit and script the twist for a sound angle
- `tt-caption-writer` - write the caption, hashtags, and settings (repurposer hands the caption here)
- `tt-humanizer` - scrub AI tells and check lines are sayable, plus `--mode audit` to review the result
