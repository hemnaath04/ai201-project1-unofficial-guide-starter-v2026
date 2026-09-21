# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
One of my questions (best months for Halden Bay) also shows up in the seasons
guide, not just the Halden Bay town file. So the "right" chunk might not always
be obvious. I'm fine missing one. Saying 5/5 would be pretending every question
has one clean source.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
Going for all five here. The prompt already says to name the file, and each
chunk is labeled `[from filename]`. If it still skips the source, that's on the
model side, not some weird retrieval edge case. Missing even one would bug me.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
4 of 5, not 5 of 5. These are travel guides, so sometimes a random how-to
question still grabs a weak "practical notes" chunk. One miss is whatever. Two
means my cutoff is too high.

---

## 4. Chunks keep section boundaries intact

At least 4 of 5 sampled chunks begin with a section heading (or the document
title) and do not cut mid-sentence at either end.

**Why this target:**
The whole point of picking `city_guides` was the `##` headings. Starter chunking
cut right through them. If my chunks still end mid-sentence, that's a real fail.
But 5/5 feels harsh because long sections still get a secondary split sometimes,
and one of those leftovers might look a little rough.

---

## 5. Answers stay specific to the place asked about

For at least 4 of my 5 test questions, the answer mentions the place named in the
question (for example "Kestrelford" or "Halden Bay") and does not substitute a
different town from the retrieved context.

**Why this target:**
Every town guide has the same section names ("Getting there", "When to go"), so
it's easy for retrieval to grab the right *type* of section from the wrong town.
If it mixes up Halden Bay parking with Kestrelford more than once, something's
off with how I chunked or retrieved. 4 of 5 is the bar I actually care about.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
