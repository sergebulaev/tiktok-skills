# Scrub Rules: spoken-script de-AI catalog by tier (V3, 2026-09)

Tiered rules for stripping AI tells from a TikTok spoken script and caption. The
key difference from text-platform humanizing: the output is **spoken out loud**,
so the bar is "would a person say this to a camera", not "is this grammatical".
V3: vocabulary is scored by **density per script beat** (or caption
paragraph), not deleted per word. Em dashes are **capped** in the caption and
on cards, and are only breath marks in the spoken script. Forced rhythm is a
tell, not a fix. See SKILL.md "What changed in V3" for the evidence.

## Contents

- Density scoring (how every vocabulary rule is applied)
- Tier 1 - Forensic (always on)
- Tier 2 - Strict (default on)
- Tier 3 - Spoken-word fixes (Pass 2, the part text humanizers miss)
- Add-back catalog (Pass 3 fingerprints) and forbidden insertions
- The read-aloud test (run last)
- Preserve these (speaker voice, do not scrub)

---

## Density scoring (how every vocabulary rule is applied)

The cluster principle: viewers hear AI from clusters of markers, not from any
single word. One "notably" in a beat is a slip. "Notably", "comprehensive" and
"leveraging" in the same 15 seconds is a script.

```python
def score_beat(beat: str, markers: dict) -> dict:
    """Count marker hits per script beat (hook / value / loop-close) or per caption paragraph.
    Returns hits and the action to take."""
    hits = []
    for name, pattern in markers.items():
        for m in re.finditer(pattern, beat, flags=re.I):
            hits.append((name, m.group(0)))
    n = len(hits)
    single_hit = [h for h in hits if h[0] in ("reveal_bridge", "neg_parallel", "sincerity_marker", "dead_filler")]
    if n >= 3:
        action = "REWRITE_BEAT"        # 3+ markers = signal. Rewrite the beat as speech, not word-by-word.
    elif single_hit:
        action = "REPLACE"             # a reveal bridge / negative parallelism / sincerity marker / dead filler is always
                                       # scrubbed on one hit, whatever else sits in the beat (checked before the 2-hit branch)
    elif n == 2:
        action = "FLAG_ONLY"           # 2 ordinary markers = borderline. Report it, leave the words: the audit allows 0-2 per unit.
    else:
        action = "LEAVE"               # a single common word is not a verdict
    return {"hits": hits, "count": n, "action": action}
```

Rules of application:
- Score forensic markers separately: one hit = delete, no density threshold.
- Script-level counts also matter for triads: a stacked, parallel or hollow
  one is scrubbed on sight; of the natural ones only the first stays, the
  second and any later one in the same script is rewritten (`triad_action()`).
- Never replace a word with a synonym from the same list. "Leverage" to
  "harness" is not a fix.
- When you rewrite a beat, rewrite it in the speaker's register (their slang,
  their pacing), not in "plain" register. Plainness at uniform temperature is
  itself a fingerprint, and it sounds like one.

---

## Tier 1 - Forensic (always on)

Real model leakage. No human ever says or types these.

| Pattern | Action |
|---|---|
| AI tool markers: `oaicite`, `contentReference`, `turn0search0`, `:contentReference[...]` | delete |
| Knowledge-cutoff disclaimers: "As of my last update", "I cannot browse" | delete |
| Template blanks: `[Your Name]`, `[insert hook]`, `[brand]` | flag, ask the user to fill |
| Em dashes above the cap in the caption or on an on-screen card (see below) | replace the excess with a comma, colon, or a line break; never a period, never `..` (that is a teleprompter mark, script only) |
| "Certainly!", "Sure, here is", "I hope this helps" wrappers | delete |

### Em dash cap (caption: about 1 per 100 words; card: at most 1; script: a breath mark)

The character is not a tell: GPT-5.4 emits 1.43 em dashes per 1,000 words,
below the human 3.23, and 29% of human captions on sibling platforms use one.
Three surfaces, three rules:

```python
def em_dash_excess(text: str, surface: str) -> int:
    """surface = 'caption' | 'card' | 'script'. Returns how many em dashes to replace. 0 = leave them."""
    em = text.count("—")
    if surface == "script":
        return 0                                   # a dash in a spoken line is a breath mark only the speaker sees;
                                                   # prefer ".." on the teleprompter, but it is never a tell
    if surface == "card":
        return max(0, em - 1)                      # a 3-7 word card rarely needs one; cap 1
    words = len(text.split())
    cap = max(1, min(2, round(words / 100)))       # caption: ~1 per 100 words, floor 1, ceiling 2
    return max(0, em - cap)

# Replacement order for the EXCESS ones (keep the one doing the most work):
#   1. comma            if the dash joins a clause (".." is script-only: a teleprompter breath mark, never visible copy)
#   2. colon            if the dash introduces a reveal or a list
#   3. line break       TikTok-native in a caption; a card gets a second line
#   4. rewrite          if none of the above reads naturally
# NEVER a period. "X. Y." from a split dash creates fragment stacking, which is a worse tell than the dash.
```

## Tier 2 - Strict (default on): vocabulary markers (density-scored)

Words no one says on camera. One in a beat is a slip; three is a script.
Swap for the spoken equivalent when the beat is over threshold.

| AI word | Say instead |
|---|---|
| significant | the number ("31 minutes", not "significant time") |
| crucial | cut, or "the" |
| notably / particularly | cut |
| comprehensive / holistic | full / whole |
| insight(s) | say the thing you learned |
| leverage / utilize / harness | use |
| facilitate | help / run |
| streamline | speed up / simplify |
| robust | solid |
| seamless | smooth |
| landscape | space / scene |
| nuanced | specific |
| multifaceted | cut |
| elevate | lift / level up (only if the speaker says that) |
| empower | let |
| delve into | look at / get into |
| navigate | handle / deal with |
| unlock | get / open up |
| foster | build |
| cultivate | grow |
| fundamentally / essentially / ultimately | (cut entirely) |
| myriad | lots of / tons of |
| in order to | to |
| moreover / furthermore | (cut, start a new sentence) |

### Grammar markers (density-scored; the 2026 structural signature)

```python
GRAMMAR_MARKERS = {
    # Present-participial clause openers: 5.3x the human rate, and unsayable.
    # "Leveraging these tools, you can..." -> "you can do this with these tools"
    "ing_opener": r"(?m)^[\s>*\-]*[A-Z][a-z]+ing\b[^.]{0,60},",
    # Nominalisations: verb-turned-noun. "the implementation of" -> "when I set it up"
    "nominalisation": r"\bthe (\w+(?:tion|sion|ment|ance|ence|ization|isation)) of\b",
    # Stacked abstract nouns
    "abstract_stack": r"\b(alignment|transformation|optimization|innovation|efficiency|scalability|synergy)\b.{0,40}\b(alignment|transformation|optimization|innovation|efficiency|scalability|synergy)\b",
}
```

### 2026 model-idiom layer (density-scored)

```python
IDIOM_LAYER_2026 = [
    r"\bquietly\b",
    r"(?m)^\w+ matters\.$",                  # "consistency matters." as a line
    r"\bcompound(s|ing)?\b",
    r"\ba signal\b|\bthe signal\b",
    r"\bthe work\b",
    r"\bbuilt different\b",
    r"\bload-bearing\b",
    r"\bdoing the heavy lifting\b",
    r"\blet that sink in\b",                 # single hit as a closer
    r"\bthat's the real story\b",
    r"\bmain character energy\b",
]
```

### Reveal bridges (single hit = replace)

```python
REVEAL_BRIDGES = [
    (r"(?im)^the (result|outcome|answer|lesson|catch|kicker|truth)\?\s*", ""),          # "The result?"
    (r"(?i)\bit'?s not \w[^,.]{0,40}, it'?s \b", None),                                 # "It's not X, it's Y" (rewrite as a flat claim)
    (r"(?i)^stop \w[^,.]{0,40}\. start \b|^stop \w[^,.]{0,40}, start \b", None),         # "Stop X, start Y"
    (r"(?im)^here'?s (what|how|why|the thing)( nobody tells you| most people miss)?\b[^:.\n]{0,40}[:.]\s*", ""),  # "Here's what nobody tells you"
    (r"(?im)^(plot twist|spoiler|the twist)[:?]\s*", ""),
]
# Fix: delete the bridge and say the thing. The next line was the point anyway.
```

### Negative parallelism (single hit = rewrite)

Strip the "not X, but Y" / "it isn't about X, it's about Y" constructions and
every sibling form. Rewrite as a flat claim in the speaker's voice.

### Rule of three (strict at density; one natural triad is allowed)

Tricolon runs at 2x the expert-human rate across 2026 models, and read aloud
a perfect one ("learn, grow, succeed") is the most audible tell there is. The
tell is the stacked, perfectly parallel or hollow triad and the repeat, not
the form: one natural triple with concrete items ("the tripod, the ring light,
the $12 clamp") is how people talk.

```python
def detect_triads(text: str) -> list:
    patterns = [
        r"(\w+), (\w+),? and (\w+)",                       # word triplets
        r"(\w+ \w+), (\w+ \w+),? and (\w+ \w+)",           # short-phrase triplets
        r"(?m)^(\w+)\. (\w+)\. (\w+)\.$",                  # "Simple. Effective. Easy." (also a Pass 2 staccato hit)
        r"\b(no \w+)[,.] (no \w+)[,.] (just|only) \w+",    # "No X. No Y. Just Z." (also a Pass 2 hit)
    ]
    return [m for p in patterns for m in re.finditer(p, text, flags=re.I)]

HOLLOW_ADJECTIVES = {"dynamic", "vibrant", "innovative", "faster", "cheaper", "better", "simple",
                     "effective", "easy", "bold", "clear", "focused", "scalable", "powerful", "easier"}
ABSTRACT_NOUNS = {"growth", "impact", "value", "alignment", "innovation", "efficiency", "results", "success",
                  "clarity", "freedom", "scale", "momentum", "consistency", "mindset", "strategy", "vision"}

def hollow(items) -> bool:
    """A triad is hollow when its items are interchangeable: every item is an abstract adjective or an
    abstract noun, and none carries a receipt (a proper name, a number, a $ or %). Equal word counts are
    NOT a tell on their own: "Stripe invoices, Vercel logs, and GitHub alerts" is a natural concrete triad."""
    def has_receipt(items) -> bool:
        for i, x in enumerate(items):
            for j, w in enumerate(x.split()):
                if re.search(r"[0-9$%]", w):
                    return True
                if w[:1].isupper() and not (i == 0 and j == 0):   # a sentence-initial capital is not a name
                    return True
        return False
    all_abstract = all(x.lower().strip() in HOLLOW_ADJECTIVES or x.lower().strip() in ABSTRACT_NOUNS
                       or x.lower().split()[-1] in ABSTRACT_NOUNS for x in items)
    return (not has_receipt(items)) and all_abstract

def triad_action(triads: list) -> list:
    """Call once per script with that script's triads. Scrub any hollow triad on sight. Of the natural
    (concrete, non-interchangeable) ones keep only the FIRST; every later triad in the same script is rewritten,
    so each script ends with at most one natural triad. Threads are not pooled: the threshold is per script."""
    actions = []
    kept_one = False
    for t in triads:
        items = t.groups()
        if hollow(items) or kept_one:
            actions.append((t, "KEEP_TWO_MAKE_ONE_SPECIFIC"))   # keep two, make one specific, or drop to two
        else:
            actions.append((t, "LEAVE"))
            kept_one = True
    return actions
```

### Dead filler (spoken-word specific; single hit = cut)

| Phrase | Action |
|---|---|
| "Hey guys" / "what's up everyone" | cut; open on the payoff |
| "In this video, I will.." / "today I want to talk about" | cut; state the promise |
| "without further ado" | cut |
| "don't forget to like and subscribe" | cut; one clear ask if any |
| "thanks for watching" | cut; end on the loop-close line |
| "at the end of the day" | cut |
| "game-changer" / "deep dive" / "dive in" | name the actual thing |
| "in today's fast-paced world" / "in the age of AI" | cut |

### Dead closers (caption and script; single hit = rewrite)

Generic engagement-bait closers read as AI on TikTok the same as everywhere.
Rewrite to one specific ask tied to this video's content, or end on the
loop-close line with no ask at all.

| Closer | Action |
|---|---|
| "What do you think?" | rewrite to a specific ask, or cut |
| "Drop your thoughts below" / "drop them below" | rewrite to a specific ask |
| "Let me know in the comments" (bare, no subject) | rewrite: name what to comment |
| "Comment below!" | rewrite to a specific ask |
| "Tag someone who needs this" | cut |
| "Let that sink in." | cut |

A specific ask names the thing: "what would you cut first?", "team 5am or team
midnight?", "what's your onboarding horror story?". If no specific ask fits,
end the caption on the claim.

## Tier 3 - Spoken-word fixes (Pass 2, the part text humanizers miss)

Register first, rhythm never manufactured. Spoken lines are naturally short,
so there is nothing to "vary"; the jobs are sayability, removing staged drama,
and un-flattening only a teleprompter-flat run.

| Tell | Fix |
|---|---|
| Full grammatical sentence | contraction + natural fragment: "It is important to note that" -> "and here is the thing" |
| Perfect tricolon ("faster, cheaper, easier") | keep two, make one specific |
| A line that needs two breaths | split it at the natural breath, never at a dramatic pause |
| Passive voice ("mistakes were made") | active: "i messed up the first take" |
| Hedges stacked ("I think maybe it could possibly") | one confident claim (and never add a hedge back) |
| The hook and the on-screen text identical | rewrite one to a different angle |
| Teleprompter-flat run: 4+ consecutive lines the same length, none carrying a real clause | let the ONE line carrying the most content take a clause (because / when / after). Once. Never insert a short punch line between long ones; the inserted punch is the humanizer fingerprint |
| Staged drama: "No X. No Y. Just Z.", "The result?", "Simple. Effective. Easy.", one-word lines for effect, "Why? Because.." | merge into one spoken sentence |
| Long/short/long/short seesaw across the script | fold the second short line back in; the seesaw sounds like a humanizer |

```python
STACCATO_TELLS = [
    r"(?m)^\w+\.$",                                              # one-word line for drama: "Still." "Exactly."
    r"(?m)^(\w+\. ){2,}\w+\.$",                                  # "Short. Punchy. Done."
    r"(?i)\bno \w+\. no \w+\. (just|only) \w+",                  # "No X. No Y. Just Z."
    r"(?i)\ball (of )?the \w+\. none of the \w+",                # "All the X. None of the Y."
    r"(?im)^the (result|outcome|answer|lesson|catch|kicker|truth)\?",  # "The result?"
    r"(?i)\b(why|how|what happened)\? (because|simple|easy)\b",  # pseudo-Socratic Q&A
    r"(?i)\b(that's it|that's all|full stop|period)\.$",         # as a drama beat; "three takes. that's it." said naturally is register and stays
]
# Natural spoken fragments are register, not a tell. The tell is a RUN of them staged for effect.
# Caption only: cap standalone fragments (<4 words) at 2 per caption.
```

## Add-back catalog (Pass 3 fingerprints) and forbidden insertions

Require at least the first two where the content allows:

- **1 odd-precision number WITH a referent** in the hook ("47 minutes on the
  third take", "3 takes", "$12 at the hardware store"). A bare "47" is not a
  fingerprint; the referent is.
- **1 named entity** (a real tool, app, person, place).
- **1 first-person concrete detail** ("the third take", "my 2am edit", "the
  comment that started this").
- **1 flat, dated, uncomfortable fact** with no framing sentence around it
  ("the client fired us 9 hours before the demo"). Not "not gonna lie, this
  one hurt: ...". The fact carries the vulnerability; the frame is the tell.
- **the speaker's real register** (their slang, their pacing). Match voice
  samples if provided.

Never fabricate a number or a detail. If the script needs one and the user did
not give it, ask.

```python
SINCERITY_MARKERS = [
    r"(?im)^(let me be (honest|real|direct|clear)|i'?ll be (honest|real|direct)|honestly\?|honest (caveat|version|answer)|the honest (version|answer|truth) is|to be (direct|honest|fair|transparent)|real talk|full transparency|can i be (honest|vulnerable)|not gonna lie|ngl|unpopular opinion|storytime)[:,.]?\s*",
    r"(?i)\b(i (might|may|could) be wrong,? but|i think maybe|perhaps|it seems (to me )?that|in my humble opinion)\b",  # inserted hedges: only scrub if NOT in the speaker's voice samples
]
# Fix: delete the marker and keep the line that follows. If the line that follows is not a specific
# fact, the marker was doing the work of vulnerability. Ask the speaker for the fact.
# "POV:" is a native TikTok format, not a sincerity marker. Leave it when the video is a POV.
# "storytime" is scrubbed only when no story starts in frame one.
```

## The read-aloud test (run last)

Read the final script out loud at TikTok pace (faster than you think). Flag any
line where you:
- run out of breath before the end,
- stumble on a clause,
- hear a word you would never say to a friend,
- hear a rhythm you would never use (a staged punch line, a "No X. No Y."
  beat, a one-word line for effect).

If a line fails the read-aloud test, it fails, no matter how clean it looks on the
page.

## Preserve these (speaker voice, do not scrub)

- The speaker's slang, pacing, and lowercase texting style in the caption
- Natural spoken fragments ("three takes. that's it.") used as register
- `..` as a breath mark; a dash in the spoken script (invisible on camera)
- One em dash in a caption that wants it; one on a card if it does real work
- One natural rule-of-three with concrete, non-interchangeable items
- "POV:" when the video is a POV
- Contractions everywhere
- Specific numbers with referents and named entities (add MORE, never remove)
- The speaker's reactions and opinions, including a blunt one. Flat tone
  across a whole script is a humanizer fingerprint, and it sounds like one
- A single common-word marker in a beat ("robust" for a tripod). One is a slip,
  not a script
- Their actual story. Never invent a detail to make a hook land
