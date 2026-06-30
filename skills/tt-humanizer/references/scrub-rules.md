# Scrub Rules: spoken-script de-AI catalog by tier

Tiered rules for stripping AI tells from a TikTok spoken script and caption. The
key difference from text-platform humanizing: the output is **spoken out loud**,
so the bar is "would a person say this to a camera", not "is this grammatical".

## Tier 1 - Forensic (always on)

Real model leakage. No human ever says or types these.

| Pattern | Action |
|---|---|
| AI tool markers: `oaicite`, `contentReference`, `turn0search0`, `:contentReference[...]` | delete |
| Knowledge-cutoff disclaimers: "As of my last update", "I cannot browse" | delete |
| Template blanks: `[Your Name]`, `[insert hook]`, `[brand]` | flag, ask the user to fill |
| Em dash `—`, en dash `–`, double dash `--` | replace with `..` or a line break |
| "Certainly!", "Sure, here is", "I hope this helps" wrappers | delete |

## Tier 2 - Strict (default on): vocabulary swaps

Words no one says on camera. Swap for the spoken equivalent.

| AI word | Say instead |
|---|---|
| leverage | use |
| utilize | use |
| facilitate | help / run |
| streamline | speed up / simplify |
| robust | solid |
| seamless | smooth |
| delve into | look at / get into |
| navigate | handle / deal with |
| unlock | get / open up |
| harness | use |
| foster | build |
| cultivate | grow |
| fundamentally / essentially / ultimately | (cut entirely) |
| myriad | lots of / tons of |
| in order to | to |
| moreover / furthermore | (cut, start a new sentence) |

## Tier 2 - Strict: dead phrases (spoken-word specific)

| Phrase | Action |
|---|---|
| "Hey guys" / "what's up everyone" | cut; open on the payoff |
| "In this video, I will.." / "today I want to talk about" | cut; state the promise |
| "without further ado" | cut |
| "don't forget to like and subscribe" | cut; one clear ask if any |
| "thanks for watching" | cut; end on the loop-close line |
| "at the end of the day" | cut |
| "game-changer" / "deep dive" / "dive in" | name the actual thing |
| "it's not just X, it's Y" | rewrite as a flat claim |

## Tier 3 - Spoken-word fixes (the part text humanizers miss)

| Tell | Fix |
|---|---|
| Full grammatical sentence | contraction + fragment: "It is important to note that" -> "and here is the thing" |
| Perfect tricolon ("faster, cheaper, easier") | break it: keep two, make one specific |
| Teleprompter rhythm (every line same length) | add a short punch line between long ones |
| A line that needs two breaths | split it at the natural breath |
| Passive voice ("mistakes were made") | active: "i messed up the first take" |
| Hedges stacked ("I think maybe it could possibly") | one confident claim |
| The hook and the on-screen text identical | rewrite one to a different angle |

## Add-back catalog (Pass 3 fingerprints)

Require at least the first two where the content allows:

- **1 specific number** in the hook ("47 minutes", "3 takes", "$12").
- **1 named entity** (a real tool, app, person, place).
- **1 first-person concrete detail** ("the third take", "my 2am edit", "the
  comment that started this").
- **the speaker's real register** (their slang, their pacing). Match voice
  samples if provided.

Never fabricate a number or a detail. If the script needs one and the user did
not give it, ask.

## The read-aloud test (run last)

Read the final script out loud at TikTok pace (faster than you think). Flag any
line where you:
- run out of breath before the end,
- stumble on a clause,
- hear a word you would never say to a friend.

If a line fails the read-aloud test, it fails, no matter how clean it looks on the
page.
