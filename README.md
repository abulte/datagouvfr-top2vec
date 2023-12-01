# datagouvfr-top2vec

[data.gouv.fr's datasets catalog](https://www.data.gouv.fr/fr/datasets/catalogue-des-donnees-de-data-gouv-fr/) crunched by [Top2Vec algorithm](https://github.com/ddangelov/Top2Vec) for topic modeling and
semantic search, using `distiluse-base-multilingual-cased` pretrained model.

## Usage

Train model:

```
make data
python cli.py train-model
```

Or [use trained model](https://huggingface.co/abulte/top2vec-datagouvfr/blob/main/top2vec_distiluse-base-multilingual-cased.bin).

Launch app:

```
flask run
```
