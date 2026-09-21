# The Unofficial Guide

**Hemnaath Balasubramani** — corpus: `city_guides`

---

# Unit 1

## What This Does

I indexed the `city_guides` corpus: 14 travel guides for a fake coastal
region (9 towns, plus eating / walking / transport / seasons /
accessibility). You can ask stuff like "does Kestrelford have a train?" or
"when does parking fill at Halden Bay?" and it answers from those docs only,
with the filename attached. If the closest chunk is too far off, it just says
it doesn't know instead of making something up.

## Chunking Strategy

**Chunk size:** 700 characters (only kicks in if one section is still too long)
**Overlap:** 100 characters (only between those sub-chunks)

These guides are long and already split under `##` headings (Getting there,
Eat and drink, When to go, etc.). The starter just cuts every 800 characters,
so when I first indexed I got 56 chunks and a bunch of them started halfway
through a section. That felt wrong for this corpus.

So I chunk on the headings instead. Each `##` block is one chunk, and I stick
the doc title on top so "Getting there" from Halden Bay doesn't look the same
as "Getting there" from Kestrelford. Tiny intro blurbs under the title get
merged into the first real section, otherwise they're useless on their own.
If a section is still over 700 chars, I split it on paragraph/sentence breaks
with 100 overlap.

I tried the starter 800/120 first. Most sections were already under 700, so I
dropped to 700/100 and let the secondary split stay rare.

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

My five real questions landed between 0.18 and 0.48 on best distance. The five
out-of-scope ones were 0.81 to 0.99. Pretty clean gap, so I put the cutoff at
0.65. That still refuses Mongolia / Rust / World Cup stuff, and it doesn't
kill the eating-hours question that came in at 0.48.

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

**1.** I pasted my draft criteria and asked: "for each one, tell me exactly how
you'd test it using only what the sentence says." Criterion 5 was originally
something vague like "answers should feel specific," and it basically said it
couldn't test that. So I changed it to: the answer has to mention the place
from the question, 4 out of 5 times.

**2.** I wrote out how I wanted chunking to work (split on `##`, keep the title,
handle overlap) and asked it to code that. First version skipped overlap on
long sections and left those short intro paragraphs as their own chunks, which
couldn't answer anything alone. I fixed both: secondary split with overlap, and
merge short intros into the next section.

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
