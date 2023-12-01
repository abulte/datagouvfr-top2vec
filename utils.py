import csv

from pathlib import Path

from markdown_it import MarkdownIt
from mdit_plain.renderer import RendererPlain
from progressist import ProgressBar


def load_corpus(source: Path, max: int | None = None, delimiter: str = ";") -> list:
    """
    Loads catalog, parse markdown description, return concatenated title and description
    Returns [("{id}", "{text}")]
    """
    print("Loading corpus...")
    cur = 0
    corpus = []
    parser = MarkdownIt(renderer_cls=RendererPlain)
    with source.open() as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        lines = list(reader)
        bar = ProgressBar(total=len(lines))
        for line in bar.iter(lines):
            if max and cur == max:
                break
            cur += 1
            description = parser.render(line["description"])
            corpus.append((line["id"], f'{line["title"]} {description}'))

    return corpus
