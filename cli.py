from pathlib import Path

from minicli import cli, run
from top2vec import Top2Vec

from utils import load_corpus


catalog = Path("datasets-filtered.csv")


@cli
def train_model(embedding_model="distiluse-base-multilingual-cased"):
    ids, corpus = zip(*load_corpus(catalog, delimiter=","))
    model = Top2Vec(
        list(corpus), embedding_model=embedding_model, document_ids=list(ids),
        split_documents=True, keep_documents=False, workers=4,
    )
    Path("models").mkdir(exist_ok=True)
    model.save(f"models/top2vec_{embedding_model}.bin")


if __name__ == "__main__":
    run()
