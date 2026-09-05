# Voice Rules for TikTok (spoken and on-camera)

These are the canonical voice rules for the whole bundle. Every skill inherits
them. TikTok is different from text platforms: the words are spoken out loud and
read off the screen, not scanned in a feed. The rules below cover both the
**spoken script** (what you say to camera) and the **caption** (what gets typed
under the video).

## Hard rules

1. **Em dashes (`—`) capped:** about 1 per 100 words in the caption, at most
   one on an on-screen card (a 3-7 word card rarely needs one), and only a
   breath mark in the spoken script (`..` reads better on a teleprompter). The
   character is no longer a tell (2026 models use fewer than humans); the
   density is. Replace the excess with a comma, colon or line break, never a
   period. No en dashes (`–`) between clauses, no double dashes (`--`).
2. **Write the script the way a person talks, not the way a person writes.**
   Contractions, short sentences, sentence fragments. If you would not say it out
   loud to a friend, cut it.
3. **Capitalize personal, company, and product names** (Notion, CapCut, Stripe).
   Lowercase a brand name and it reads as careless.
4. **Specific numbers beat adjectives.** "3 takes" beats "a few takes". "47
   minutes" beats "ages". One concrete number in the hook earns the watch.
5. **One idea per video.** A 30-second clip carries exactly one promise. Two
   ideas means two videos.
6. **Say the hook, do not bury it.** The first spoken line and the first
   on-screen text both land in the first 1-3 seconds, before the viewer decides
   to swipe.

## Spoken-script rules

- **Read it out loud before you trust it.** A line that looks fine on the page
  but trips your tongue will trip on camera. Cut the clause that makes you
  stumble.
- **Cut throat-clearing.** "Hey guys, so today I wanted to talk about.." is three
  seconds of nothing. Open on the payoff or the tension.
- **Sentence fragments are good on camera.** "No tripod. No mic. One light." reads
  as a real person, not a teleprompter.
- **One breath per line.** If a line needs two breaths, split it. Pacing on TikTok
  is faster than you think.
- **Pronounce the number.** "two-point-four times" lands harder spoken than "2.4x"
  flashed on screen with no voiceover.

## On-screen text rules

- **The first on-screen text is a second hook.** Many viewers watch muted at
  first. The text has to carry the promise even with the sound off.
- **Short. 3 to 7 words a card.** Long captions on screen do not get read at
  scroll speed.
- **No dashes, minimal punctuation.** A line break beats a comma. A period is
  often unnecessary.

## Caption rules

- **<= 2,200 characters on the TikTok API** (the native app allows 4,000, but
  the API caps captions at 2,200, hashtags included). Aim much shorter: the
  caption supports the video, it does not replace it.
- **First line of the caption is visible before "more".** Put a reason to read or
  a reason to comment there, not a hashtag wall.
- **The caption can ask the question the video opened.** A caption that prompts a
  specific comment ("which one got you?") earns comments, which feed reach.

## Vocabulary markers (density-scored)

Count these per script beat or caption paragraph. One is English; two is borderline (flag it in the report, leave the words);
three in one script beat reads as AI and the whole script beat gets rewritten (see `tt-humanizer` V3).
The durable 2026 set (significant, crucial, notably, particularly,
comprehensive, insights, robust, leverage, foster, landscape, nuanced,
streamline, elevate, empower) counts alongside the older corporate words:
- leverage, utilize, facilitate, streamline, robust, seamless, delve, navigate,
  unlock, harness, foster, cultivate
- fundamentally, essentially, ultimately, crucially, notably
- landscape, ecosystem, paradigm, realm, tapestry, journey

## Always forbidden (single hit, regardless of density)

These are scrubbed on sight. They are reveal bridges, negative parallelism,
dead phrases or performed sincerity, not vocabulary:
- "It's not just X, it's Y"
- "In today's fast-paced world"
- "game-changer", "deep dive", "at the end of the day", "dive in"
- "Hey guys", "don't forget to like and subscribe", "without further ado"
- Sincerity announcements as an opener or pivot: "let me be honest", "I'll be
  real", "honestly?", "real talk", "not gonna lie", "unpopular opinion:" on a
  take that is actually popular. State the fact flat instead.

## Hashtags

- **3 to 5 hashtags, mixed reach.** One broad (#fyp tier rarely helps in 2026),
  one to two niche-defining (#notiontips), one to two specific-to-the-video.
  Stuffing 15 hashtags reads as spam and does not buy reach.
- Put hashtags at the end of the caption, not mid-sentence.

## Anti-patterns

- A script that opens with a greeting or a logo animation (dead air kills
  completion).
- Reading the caption out loud word for word (the script and caption are two
  different jobs).
- A "hook" that is actually setup ("so I was thinking the other day about..").
- ALL CAPS spoken-word scripts (you cannot shout for 30 seconds).
- Stacked or hollow rule of three in the script ("faster, cheaper, easier");
  one natural triple with concrete items is how people talk.
- A staged punch line, "No X. No Y. Just Z." beat, or "The result?" reveal
  inserted for rhythm. Spoken lines are naturally short; do not manufacture
  drama-rhythm on top.
- A call to action stacked three deep ("like, comment, follow, share, save").
  One clear ask.

## Algorithmic note

TikTok's ranker optimizes for **completion rate and rewatches** above all. The
script and the on-screen text exist to keep a viewer watching to the last frame,
then watching again. Before you trust a draft, ask: does the first line make a
swipe feel like a loss? Does the last line make the loop want to restart? If the
script only earns a passive view, the video will not travel.
