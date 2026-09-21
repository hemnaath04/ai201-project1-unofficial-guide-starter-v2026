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
One of my five questions (Halden Bay best months) can also be answered from the
cross-cutting seasons guide, not only the Halden Bay town guide, so the right
chunk may not always be the top hit. Allowing one miss keeps the target honest
without pretending every question has a single obvious source.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
All five, not four, because the grounding instruction and the prompt both tell
the model to name the filename, and the retrieved excerpts already carry
`[from filename]` labels. If a produced answer still omits a source, that is a
prompt or generation failure, not a hard retrieval edge case.

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
4 of 5 rather than 5 of 5 because a travel-guide embedding space can
occasionally pull a weakly related "practical notes" chunk for an unrelated
how-to question. One miss is tolerable; two would mean the cutoff is too loose
for this corpus.

---

## 4. Chunks keep section boundaries intact

At least 4 of 5 sampled chunks begin with a section heading (or the document
title) and do not cut mid-sentence at either end.

**Why this target:**
city_guides documents are organised under `##` headings. The starter's
fixed-size windows sliced straight through those labels. A chunk that still
ends mid-sentence after my section-aware splitter is a real failure, but
requiring 5 of 5 would punish one leftover sub-chunk when a long section still
needs a secondary split.

---

## 5. Answers stay specific to the place asked about

For at least 4 of 5 test questions, the answer mentions the place named in the
question (for example "Kestrelford" or "Halden Bay") and does not substitute a
different town from the retrieved context.

**Why this target:**
Several town guides share the same section labels ("Getting there", "When to
go"), so retrieval can return the right *kind* of section from the wrong town.
4 of 5 is the bar I care about: if the system confuses Halden Bay parking with
Kestrelford's car park more than once, the chunking/retrieval design is wrong
for this corpus.

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
