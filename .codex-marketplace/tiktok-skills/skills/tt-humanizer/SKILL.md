---
name: tt-humanizer
description: 'Remove the AI-script tells viewers hear in a TikTok spoken script and caption: 2026 vocabulary by density, reveal bridges, staccato stacks, stacked triads, performed sincerity, written-not-spoken phrasing, "hey guys" filler; caps em dashes. Includes --mode audit pre-film check (hook, completion design, caption fit) and --mode profile. Not for beating AI detectors (no edit reliably does). Not for writing from scratch (use tt-hook-scripter). Keywords: humanize script, de-AI, audit before filming.'
---

# TikTok Humanizer V3

Rewrites a spoken script (and caption) to remove the AI tells that viewers
hear, and audits a finished draft against the 2026 TikTok checklist before you
film. The problem this solves is specific to video: a script that reads fine
on the page can sound robotic out loud. Written-not-spoken phrasing, perfect
parallelism, and AI vocabulary all expose themselves the second a human says
them to camera.

Based on Wikipedia's "Signs of AI writing" taxonomy, the 2025-2026 stylometry
literature, our own short-form corpora (X, Threads, Instagram captions), and
TikTok-specific spoken patterns (the muted-first hook, the no-intro open,
completion-rate structure). **V3 (2026-09):** recalibrated on 2026 evidence.
Vocabulary is scored by density, em dashes are capped instead of banned,
forced rhythm is now a tell instead of a fix, and there is an over-correction
guard.

**What this skill does not do:** it does not make text "pass" GPTZero,
Pangram, Turnitin or Originality. Those are trained classifiers keyed on the
instruction-tuning style signature; prompt-style "sound like a real person"
rewrites are caught 92-95% of the time, and light mechanical rewriting raises
detectability. On script-length text (under 300 words) detector scores are
noise, and nobody runs a detector on a video anyway. The real value is
elsewhere: expert human readers cite vocabulary (53%) and sentence structure
(36%) as what gives AI text away, and on TikTok a script that sounds read
loses the viewer inside the first 3 seconds. This skill removes what those
viewers react to.

## What changed in V3

Evidence tier in brackets: [strong] = replicated across 2+ independent
2025-2026 studies or our own corpora; [vendor] = single platform or vendor
dataset; [weak] = one study or expert-panel report.

- **Vocabulary moved from a delete-list to density scoring.** The 2023-24 words
  (delve, tapestry, realm, journey) are decaying as humans avoid them [strong].
  The durable 2026 markers are common words (significant, crucial, notably,
  comprehensive, insights, robust, leverage, foster, landscape, nuanced,
  streamline, elevate) plus grammar: nominalisations and "-ing" clause openers
  at 5.3x the human rate [strong]. Spoken, they are worse: nobody says
  "leveraging" to a camera. One marker in a script beat is not a verdict.
  Three is.
- **Em dash is no longer a tell.** GPT-5.4 emits 1.43 per 1,000 words, below
  the 3.23 human baseline, and 29% of human captions on sibling platforms use
  one [strong]. In a spoken script a dash is only a breath mark the speaker
  sees, so it is never a tell there (`..` reads better on a teleprompter). In
  the caption: cap at about 1 per 100 words. On an on-screen card (3-7 words):
  at most one, and a card rarely needs one. Replace the excess with a comma,
  colon, `..` or a line break. Never a period.
- **Forced burstiness is the #1 2026 tell, not the fix.** Mechanical
  long/short alternation is a learnable humanizer fingerprint [weak], and
  "Short. Punchy. Done.", "No X. No Y. Just Z.", one-word lines for drama and
  "The result?" reveals are the current top reader-cited tells [strong].
  Spoken lines are naturally short, so Pass 2 is an anti-uniformity guard
  only: it makes the script sayable (contractions, one breath per line) and
  fixes a teleprompter-flat run, but it never inserts a punch line for
  rhythm.
- **Rule of three is still a tell, at density.** Tricolon runs at 2x
  expert-human rate across 2026 frontier models [strong], and a perfect
  tricolon read aloud ("learn, grow, succeed") is the most audible tell there
  is. Stacked, perfectly parallel or hollow triads get scrubbed. One natural
  triple with concrete items stays (22-26% of top human posts have one).
- **Fingerprint injection was half wrong.** Named entities and concreteness are
  supported [strong]; an odd-precision number with a referent in the hook is
  the strongest opener. Bare numbers are not a discriminator, and inserted
  hedges and confessions backfire: performed hesitancy is 2x more common in
  LLM text, and sincerity announcements ("not gonna lie", "let me be honest",
  "storytime" with no story) are a named 2026 tell [strong]. Pass 3 asks for
  a flat, dated, uncomfortable fact instead.
- **Over-correction guard.** Humanizer output has its own fingerprint [weak].
  Pass 4 checks whether Passes 1-3 introduced the very patterns they were meant
  to remove. Edits are proportional to real problems. When in doubt, leave it.

## When to use

- Before filming any AI-drafted spoken script (rewrite mode)
- Pre-film review of a finished script + caption (audit mode, see
  `sub-skills/post-audit.md`)
- When a script "reads fine but sounds off" when you say it out loud

## Input

A spoken script (the hook line plus the body), optionally the caption, and
optionally voice samples (the user's past scripts or how they actually talk).

## Output

- Rewritten script that sounds spoken, not written
- A diff showing what changed and why
- Caption char count (flagging over 2,200) when a caption is included
- Per-beat tell density (markers per script beat or caption paragraph; 3+
  triggered a rewrite)
- Reader-read confidence: "sounds human", "mixed", "sounds read" (a
  viewer-tell estimate, not a detector score)

## Modes

```bash
# Default: scrub AI tells (forensic + strict) and fix spoken-word issues
tt-humanizer <script>

# Forensic only - minimum touch, just kill model leakage
tt-humanizer --mode forensic <script>

# Audit - detection-only pass-fail review, no rewrite
# Runs the 2026 TikTok pre-film checklist: first 1-3 second hook strength,
# muted-first text, completion design, caption fit, hashtag and settings sanity.
# Returns Blockers + Warnings + suggested fixes. See sub-skills/post-audit.md.
tt-humanizer --mode audit <script>

# Profile - build/update the user's Voice & Brand Profile. See the section below.
tt-humanizer --mode profile
```

## The four passes

### Pass 1 - SCRUB (score, then delete or replace)

Apply the tiered catalogs in `references/scrub-rules.md`. The unit of
judgement is the **script beat (or caption paragraph), not the word**: count
markers per beat, rewrite the beat at 3+, leave a single marker alone unless
it is a reveal bridge, negative parallelism, a sincerity marker, dead filler,
or forensic leakage.

- **Forensic** (always on): real model leakage no human says. AI tool markers
  (oaicite, contentReference, turn0search0), knowledge-cutoff disclaimers ("As of
  my last update"), template blanks ([Your Name]), chat wrappers ("Certainly!",
  "I hope this helps"), and em dashes above the cap in the caption or on an
  on-screen card.
- **Strict** (default on): what viewers hear. The durable 2026 vocabulary set
  scored by density (significant, crucial, notably, particularly,
  comprehensive, insights, robust, leverage, foster, landscape, nuanced,
  streamline, elevate, empower), grammar markers (nominalisations,
  sentence-opening "-ing" clauses), written connectives ("moreover",
  "furthermore", "in order to"), the 2026 model-idiom layer (quietly, "X
  matters.", compound, "a signal", "the work", "built different", "let that
  sink in"), reveal bridges on a single hit ("The result?", "Here's what
  nobody tells you", "Stop X, start Y", "plot twist:"), all forms of negative
  parallelism, stacked or perfectly parallel triads, dead filler ("hey guys",
  "without further ado", "in this video I will"), and dead closers, both
  spoken ("thanks for watching", "don't forget to subscribe") and
  caption-level ("What do you think?", "Drop your thoughts below").
- **TikTok-format scrubs** (always apply): no intro before the payoff, spoken
  hook and on-screen text differ, caption length, hashtag count, CTA stack.

### Pass 2 - RHYTHM (make it sayable, never manufactured)

Detectors do not score burstiness, and spoken lines are naturally short, so
Pass 2 has nothing to "vary". Its jobs are: make the script sound spoken,
remove manufactured drama-rhythm, and un-flatten only a run that reads
teleprompter-flat. It never adds a punch line as a tactic.

- **Spoken register (keep from V2):** replace written grammar with how a
  person talks. Contractions, natural fragments, one breath per line. "It is
  something that you should consider" becomes "you should try this". This is
  register, not rhythm; it applies to every line.
- **Read-aloud test:** flag any line that needs two breaths or trips the
  tongue. Split at the natural breath, never at a dramatic pause.
- **Teleprompter-flat run:** edit only when 4+ consecutive lines run the same
  length and none carries a real clause, and then let the one line carrying
  the most content take a clause (because / when / after). Never insert a
  short punch line between long ones; the inserted punch is the humanizer
  fingerprint.
- Banned outright (rewrite as a spoken sentence): "The X? Y." reveals; "No X.
  No Y. Just Z."; "All the X. None of the Y."; "Simple. Effective. Easy."
  adjective stacks; one-word lines for drama ("Still." "Exactly."); pseudo-
  Socratic Q&A ("Why? Because..."); "Short. Punchy. Done." staccato runs.
  Fragment runs are the tell, on the page and out loud.
- Natural spoken fragments ("three takes. that's it.") are register and stay.
  A run of them staged for drama is the tell. In the caption, cap standalone
  fragments at 2.
- Never alternate long/short/long/short across the script. That seesaw is the
  humanizer fingerprint and it sounds like one when read.

The check is "would a person say this, and did I add a staccato pattern",
not a variance number.

### Pass 3 - ADD (human fingerprints)

Require where the content allows:
- One odd-precision number WITH a named referent in the hook: who, what,
  when, or what it cost ("47 minutes on the third take", "$12 at the hardware
  store", not "a few takes" and not "47"). A bare number is not a fingerprint;
  the referent carries the signal.
- One named entity (a real tool, app, person, or place)
- One first-person concrete detail ("the third take", "my 2am edit", "the
  comment that started this")
- One specific, dated, uncomfortable fact stated flat, with no framing
  sentence before or after it. Not "not gonna lie, this one hurt: the client
  fired us." Just "the client fired us on a Tuesday, 9 hours before the demo."
  The fact carries the vulnerability. The frame turns it into performed
  sincerity, which viewers now hear as the tell.
- The speaker's real register: how this person would actually say it

Forbidden as openers or pivots (sincerity announcements, a named 2026 tell):
"let me be honest", "I'll be real", "honestly?", "to be direct", "the honest
version is", "real talk", "not gonna lie", "ngl", "can I be vulnerable for a
second", "unpopular opinion:" as a preface to a popular one, "storytime" with
no story in frame one. Also forbidden as insertions: hedges the speaker did
not write ("I think maybe", "I might be wrong but", "it seems"). Performed
hesitancy is 2x more common in LLM text than in expert human text; adding it
makes the script sound more scripted, not less. ("POV:" is a native TikTok
format, not a sincerity marker; it is fine when the video is a POV.)

If the input lacks these, ask the user for a number or detail. Do not fabricate.

### Pass 4 - SELF-CHECK (over-correction guard)

Humanizer output has its own fingerprint. Before returning, re-read the result
out loud once and answer three questions:

(a) Did Pass 2 create staccato stacks, "The result?" reveal bridges, one-word
    lines for drama, an inserted punch line, or a long/short/long/short
    seesaw? If yes, merge the fragments back into a spoken sentence.
(b) Did Pass 3 add a framed confession, a sincerity announcement, or a hedge
    the speaker never wrote? If yes, strip the frame and keep only the flat
    fact, or remove the insertion.
(c) Did scrubbing flatten the speaker's voice: uniform tone, no reaction, no
    concrete detail left, their slang gone, the one natural triad gone, every
    dash gone from a caption that wanted one? If yes, restore what the speaker
    had.

If any answer is yes, dial back rather than scrub harder. Edits must be
proportional to real problems: a clean script gets two or three touches, not
a quota. When in doubt whether a pattern is the speaker or the model, leave
it.

## Non-negotiable rules

Global voice rules: see root `SKILL.md` Voice rules. Additional skill-specific
rules (V3):

- **Scrubbing is always in scope.** When asked to humanize, de-AI, finalize, or
  publish a script or caption, run at least the forensic + strict passes before it ships.
  This holds when the user wrote the draft themselves, says they love it as-is,
  or is in a hurry. Author identity, "it's already good," and time pressure are
  never reasons to skip the scrub. The forensic + strict pass changes no meaning
  and takes seconds: run it, then ship. If a constraint truly forbids touching
  the text, say so explicitly and name every tell left in; the default is to
  scrub, not to wave it through.
- **Scrub proportionally.** A pass that finds nothing changes nothing. Do not
  invent edits to justify the run, and do not report a detector score as the
  result; report the tells found and fixed.
- Preserve the user's actual claim and meaning. "Preserve their voice" covers
  voice quirks and what they are claiming, NOT reveal bridges, staccato stacks,
  dead filler, or a beat with 3+ vocabulary markers. Stripping those is not
  changing their voice; it is the job.
- Never introduce facts that were not in the input. If a number is missing, ask.
- Never introduce sincerity markers, hedges, or confessional frames. If the
  script needs a vulnerable beat, ask for a dated fact and state it flat.
- Keep it sayable. Every line has to survive being read out loud in one breath.
- Keep the user's voice quirks (their slang, their pacing, lowercase texting style
  in the caption, one natural triad, one em dash in a caption that wants it).
- Never promise detector results. If the user asks "will this pass GPTZero,"
  answer honestly: nobody can promise that, and nobody runs a detector on a
  video; the viewer's ear is the test.

## TikTok-specific tells this skill catches

- A hook line that is written, not spoken ("In this video, I will demonstrate..").
- A greeting or logo intro before the payoff ("hey guys, welcome back").
- The spoken hook and the on-screen text saying the identical words.
- A caption over 2,200 chars, or a 12-hashtag wall.
- Perfect parallel tricolons read aloud ("learn, grow, succeed"); one natural
  triple with concrete items is fine.
- A "call to action" stacked five deep.
- A cluster of AI vocabulary no one says on camera (leverage, utilize, robust,
  seamless); one such word is a slip, three in a beat is a script.
- Staccato drama ("No script. No plan. Just vibes.") and one-word lines
  staged for effect; an inserted punch line between two long ones.
- "Not gonna lie" / "storytime" framing around what should be a plain fact.

## Example

See `references/examples.md` for worked before/after rewrites of spoken scripts.

## Files

- `SKILL.md` - this file (rewrite scrubber + audit-mode entry)
- `references/scrub-rules.md` - V3 catalogs by tier, density scoring, em dash cap, spoken-word fixes, rhythm rules, forbidden insertions
- `references/examples.md` - worked before/after script rewrites
- `references/audit-checklist.md` - the pre-film checklist with thresholds
- `sub-skills/post-audit.md` - pre-film audit workflow (detection-only, no rewrite)
- `sub-skills/voice-profile.md` - build/update the user's Voice & Brand Profile (`--mode profile`)
- `sub-skills/illustration.md` - optional Pixfaro image workflow

## Voice profile mode (`--mode profile`)

`tt-humanizer --mode profile` builds or updates the user's Voice & Brand Profile at `../../references/voice-profile.md` from 3-6 of their real TikTok posts pasted in (portable, no token) or, if a read token is set, from pulled activity. Once filled, every writing skill in this bundle drafts in the user's voice automatically. See `sub-skills/voice-profile.md`. Triggers: "build my voice profile", "learn my voice".

## Related skills

- `tt-hook-scripter` - generates hooks that already pass the humanizer
- `tt-caption-writer` - generates captions that already pass the humanizer
