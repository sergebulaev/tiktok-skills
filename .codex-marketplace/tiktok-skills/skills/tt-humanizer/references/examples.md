# Worked Before/After: spoken-script rewrites

Each example shows an AI-drafted TikTok script, what the humanizer caught, and the
rewrite. The test is always the same: would a person say this to a camera.

## Example 1: a how-to hook

**Before (AI-drafted):**

> Hey guys, welcome back to my channel. In today's video, I want to fundamentally
> change the way you think about productivity. I will delve into three powerful
> strategies that will help you leverage your time, streamline your workflow, and
> ultimately unlock your full potential. Let's dive in!

**Caught:**
- "Hey guys, welcome back" + "In today's video" (two dead intros, ~4 seconds of
  nothing before any payoff)
- the hook beat scores 6 markers ("fundamentally", "delve into", "leverage",
  "streamline", "ultimately", "unlock"): far over the 3-per-beat threshold, so
  the beat is rewritten as speech, not word-swapped
- a perfect parallel tricolon ("leverage.. streamline.. unlock"), interchangeable
  items, scrubbed on sight
- "Let's dive in" closer-as-opener
- no specific number, no concrete detail

**After:**

> i cut my work week from 50 hours to 32 and got more done. here are the 3 things
> that actually moved the needle.. and number 2 is the one nobody tries.

Notes: the result and a number with a referent (50 hours to 32, the work week)
are in the first line, the intro is gone, the tricolon is broken into a
numbered promise with an open loop ("number 2 nobody tries") that earns the
watch to the end. Pass 2 changed the register (contractions, one breath per
line) and nothing else: no punch line was inserted. Pass 4: no "not gonna lie"
frame, no hedge, nothing invented.

## Example 2: a story hook

**Before:**

> I would like to share a personal anecdote regarding a challenging situation I
> encountered. It was a moment that fundamentally tested my resolve, and the
> lessons I gleaned were truly invaluable.

**Caught:**
- written-not-spoken throughout ("I would like to share", "regarding", "gleaned")
- "fundamentally", "truly invaluable" (filler)
- starts before the story, not inside it (no tension in frame one)

**After:**

> so the client emails at 11pm: "the demo is broken and the call is in 9 hours."
> and i had not even started.

Notes: drops the viewer into the peak (T8 Story In Medias Res), a real number (9
hours), spoken punctuation, and tension in the first line.

## Example 3: caption cleanup

**Before:**

> In this comprehensive video, we delve deep into the multifaceted world of
> personal finance — exploring myriad strategies to leverage your savings and
> cultivate long-term wealth. #finance #money #wealth #invest #savings #budget
> #financialfreedom #fintok #moneytok #rich #success #motivation #grind #hustle

**Caught:**
- the paragraph scores 6 markers ("comprehensive", "delve deep",
  "multifaceted", "myriad", "leverage", "cultivate"): rewrite the paragraph
- 14 hashtags (a wall)
- says nothing the video does not already say
- not caught: the single em dash. It was under the caption cap (about 1 per
  100 words) and went only because the sentence around it was rewritten

**After:**

> the 3-account setup i wish i started at 22. which account would you open first?
>
> #personalfinance #moneytips #fintok

Notes: the marker cluster is gone, a comment prompt is in the first line, 3
mixed-reach hashtags. Caption supports the video instead of repeating it.

## The pattern across all three

1. Kill the intro and the AI vocabulary cluster (one word is a slip; three in a
   beat is a script).
2. Put a result, a number with its referent, or the tension in the first line.
3. Make it sayable: contractions, natural fragments, one breath per line. Never
   insert a punch line for rhythm; that is the humanizer's own tell.
4. Open a loop the body closes.
5. End on a line that restarts the loop, never on "thanks for watching".
