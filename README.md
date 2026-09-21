# The Unofficial Guide

**Hemnaath Balasubramani** — corpus: `city_guides`

---

# Unit 1

## What This Does

This system answers practical travel questions about a fictional coastal region
using fourteen long, sectioned guides (nine towns plus region-wide notes on
eating, walking, transport, seasons, and accessibility). Ask things like
whether a town has a train station, when parking fills up, or what time
kitchens stop serving — and get an answer drawn only from those documents,
with the source file named. If nothing in the corpus is close enough, it
refuses instead of guessing.

## Chunking Strategy

**Chunk size:** 700 characters (only used when a single section is still too long)
**Overlap:** 100 characters (only between sub-chunks of an oversized section)

`city_guides` documents are 1–3 thousand characters each and organised under
`##` headings (Getting there, Eat and drink, When to go, and so on). The
starter's fixed 800-character windows cut straight through those labels —
indexing with the fallback produced 56 chunks that often started mid-section.
I replaced that with a section-aware splitter: each `##` block becomes a
chunk, prefixed with the document title so a Halden Bay "Getting there"
chunk cannot be confused with Kestrelford's. Short intro blurbs under the
title are folded into the first section so they are not left as fragments.
Only sections that still exceed 700 characters are split further, on
paragraph or sentence boundaries, with 100 characters of overlap.

I started at 800/120 (the starter defaults) and dropped to 700/100 after
seeing that most labelled sections already sit under 700 characters —
keeping the secondary split rare means most chunks stay one complete
section.

## Sample Chunks

**Chunk 1** — source: `guide_accessibility.md` — produced by: `chunker.py::split_documents`

```
Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.

## Straightforward

**Thornby Wells** is the easiest town in the region. It is flat, compact, and
everything is within three minutes of everything else. Parking is free for two
hours anywhere in town and the station is central. The pump room and gardens
are level throughout.

**Marchwood** has a modern tram network with level boarding on all four lines,
running every 8 minutes on weekdays. The city museum and covered market are both
step-free. The distances between districts are the main consideration.
```

**Chunk 2** — source: `guide_corry_vale.md` — produced by: `chunker.py::split_documents`

```
Corry Vale

## When to go

May to September. Outside those months the pub in the third village closes, the farm shop reduces its hours, and several footpaths become genuinely boggy rather than merely wet. The road is not gritted above the second village and is impassable in snow.
```

**Chunk 3** — source: `guide_givens_mill.md` — produced by: `chunker.py::split_documents`

```
Givens Mill

## What to see

The mill runs tours on the hour from 11 to 3 and the machinery is operating during them, which is loud and much more impressive than a static exhibit. The church has a Saxon doorway. The river walk downstream reaches Brightwater in about three hours.
```

**Chunk 4** — source: `guide_kestrelford.md` — produced by: `chunker.py::split_documents`

```
Kestrelford

## Practical notes

Cash is still useful at the market and in smaller places, though cards are
accepted almost everywhere now. Mobile coverage is good in the centre and
patchy on the outskirts. The nearest full hospital is in Brightwater; there is
a minor injuries unit locally with limited hours.
```

**Chunk 5** — source: `guide_regional_transport.md` — produced by: `chunker.py::split_documents`

```
Getting around the region

## Buses

Three operators run in the region and they do not accept each other's tickets,
which is the single most common source of confusion for visitors. Services
concentrate on weekday daytimes. Sunday service is minimal to non-existent
outside the Brightwater town routes.

The Kestrelford service is hourly on weekdays, two-hourly on Saturdays, and
does not run on Sundays. The Halden Bay coast service runs four times daily
year-round.
```

## Sample Answer

**Question:** Does Kestrelford have a railway station?

**Answer:**

```
No, Kestrelford does not have a railway station; the line was closed in 1963.

Source: guide_kestrelford.md

Sources retrieved: guide_kestrelford.md
```

**My relevance cutoff:** 0.65

In-corpus best distances for my five test questions sat between **0.18 and
0.48**. The five OUT_OF_SCOPE questions sat between **0.81 and 0.99**. The gap
is wide, so 0.65 sits comfortably in the middle: low enough to refuse Mongolia /
Rust / World Cup questions, high enough not to refuse a real eating-hours
question that came in at 0.48.

| Question | In corpus? | Best distance |
|---|---|---|
| Does Kestrelford have a railway station? | yes | 0.369 |
| What time do Halden Bay parking lots fill on summer weekends? | yes | 0.361 |
| When do kitchens stop serving food across most of the region? | yes | 0.482 |
| How often do buses run from Brightwater to Kestrelford on weekdays? | yes | 0.250 |
| Which months are the best time to visit Halden Bay? | yes | 0.180 |
| What is the capital of Mongolia? | no | 0.847 |
| How do I change the oil in a diesel engine? | no | 0.908 |
| Who won the 1994 World Cup? | no | 0.992 |
| What is the recommended dosage of ibuprofen for a headache? | no | 0.818 |
| How do I write a for loop in Rust? | no | 0.814 |

## How I Used AI

**1.** I asked for pressure-testing on my draft acceptance criteria: "For each
one, tell me exactly how you would test it using only what the sentence says."
It could not turn an early version of criterion 5 ("answers should feel
specific") into a test, so I rewrote it to require the place name from the
question to appear in the answer, with a 4-of-5 target.

**2.** I sketched the section-aware chunker from notes and asked the model to
implement splitting on `##` headings with overlap. The first draft ignored
overlap on oversized sections and left short intro blurbs as standalone
chunks that could not answer anything. I added the secondary
paragraph/sentence split with overlap, and the rule that folds short intros
into the next section.

---

# Unit 2

## Run Log — Before

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

## Verdicts

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

## The Improvement

**What I changed:**

**Why I picked it:**

### Run Log — After

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

## What's Still Broken

## What I'd Do Differently
