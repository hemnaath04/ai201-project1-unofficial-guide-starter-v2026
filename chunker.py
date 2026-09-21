"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


_HEADING = re.compile(r"^##\s+", re.MULTILINE)
_SENTENCE_END = re.compile(r"[.!?]\s+")


def _find_cut(window: str, min_pos: int) -> int:
    """Pick the latest clean break in window at or after min_pos; else -1."""
    # Prefer paragraph, then sentence, then whitespace — never mid-word.
    for finder in (
        lambda w: w.rfind("\n\n"),
        lambda w: max((m.end() for m in _SENTENCE_END.finditer(w)), default=-1),
        lambda w: max(w.rfind(" "), w.rfind("\n")),
    ):
        cut = finder(window)
        if cut >= min_pos:
            return cut
    return -1


def _split_oversized(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Split a long section on paragraph / sentence boundaries, with overlap."""
    if len(text) <= chunk_size:
        return [text]

    pieces: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            window = text[start:end]
            cut = _find_cut(window, chunk_size // 3)
            if cut > 0:
                end = start + cut

        piece = text[start:end].strip()
        if piece:
            pieces.append(piece)

        if end >= len(text):
            break
        # Advance with overlap, but land on a word boundary going forward.
        next_start = max(end - overlap, start + 1)
        while next_start < len(text) and not text[next_start].isspace():
            next_start += 1
        while next_start < len(text) and text[next_start].isspace():
            next_start += 1
        start = next_start if next_start > start else end

    return pieces


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split city_guides-style documents on ## section headings.

    Each labelled section becomes its own chunk, with the document title (the
    first # heading, or the first line) kept as a one-line prefix so a chunk
    still names which town or guide it belongs to. Sections longer than
    CHUNK_SIZE are split further on paragraph/sentence boundaries with overlap.
    """
    chunk_size = config.CHUNK_SIZE
    overlap = config.CHUNK_OVERLAP
    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        text = doc.text.strip()
        if not text:
            continue

        # Document title: first markdown H1, else the first non-empty line.
        title = ""
        body = text
        if text.startswith("# "):
            first_line, _, rest = text.partition("\n")
            title = first_line.lstrip("# ").strip()
            body = rest.lstrip("\n")
        else:
            first_line = text.split("\n", 1)[0].strip()
            if first_line:
                title = first_line

        # Split on ## headings, keeping the heading with its section body.
        parts = _HEADING.split(body)
        headings = _HEADING.findall(body)

        sections: list[str] = []
        # Text before the first ## (intro blurb under the title).
        intro = parts[0].strip() if parts else ""
        if intro:
            sections.append(intro)

        for i, _ in enumerate(headings):
            section_body = parts[i + 1] if i + 1 < len(parts) else ""
            # After re.split on ^##\s+, the heading words sit at the start of
            # each subsequent part, up to the first newline.
            heading_line, _, remainder = section_body.partition("\n")
            heading_text = heading_line.strip()
            content = remainder.lstrip("\n").strip()
            block = f"## {heading_text}"
            if content:
                block = f"{block}\n\n{content}"
            sections.append(block)

        if not sections:
            sections = [body]

        # Fold a short title-only intro into the first real section so it isn't
        # left as a fragment that can't answer anything on its own.
        if (
            len(sections) >= 2
            and len(sections[0]) < 250
            and not sections[0].lstrip().startswith("## ")
        ):
            sections[1] = f"{sections[0]}\n\n{sections[1]}"
            sections = sections[1:]

        index = 0
        for section in sections:
            prefix = f"{title}\n\n" if title else ""
            full = f"{prefix}{section}".strip()
            for i, piece in enumerate(_split_oversized(full, chunk_size, overlap)):
                # Continuations of a long section lose the title line — put it back
                # so each chunk still names which guide it came from.
                if (
                    i > 0
                    and title
                    and not piece.startswith(title)
                ):
                    piece = f"{title}\n\n{piece}".strip()
                if len(piece) < 40:
                    continue
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::split_documents",
                    )
                )
                index += 1

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
