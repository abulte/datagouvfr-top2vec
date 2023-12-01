import base64

from functools import cache
from io import BytesIO

import httpx

from flask import Flask, render_template, request
from top2vec import Top2Vec
from matplotlib.figure import Figure
from scipy.special import softmax
from wordcloud import WordCloud


MODEL_FILE = "top2vec_distiluse-base-multilingual-cased.bin"
model = Top2Vec.load(MODEL_FILE)

app = Flask(__name__)


@app.template_filter(name="wordcloud")
@cache
def topic_word_cloud(topic_num: int):
    word_score_dict = dict(
        zip(model.topic_words[topic_num], softmax(model.topic_word_scores[topic_num]))
    )
    fig = Figure(figsize=(16, 4), dpi=200)
    ax = fig.add_subplot(111)
    ax.axis("off")
    ax.imshow(
        WordCloud(
            width=1600, height=400, background_color="white"
        ).generate_from_frequencies(word_score_dict)
    )
    ax.set_title("Topic " + str(topic_num), loc="left", fontsize=25, pad=20)
    fig.tight_layout()
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    return base64.b64encode(buf.getbuffer()).decode("ascii")


@app.route("/")
def home():
    topic_words, word_scores, topic_nums = model.get_topics(10)
    return render_template("index.html.j2", topics=topic_nums)


@app.route("/search")
def search():
    return render_template("search.html.j2")


@app.route("/partials/search", methods=["POST"])
def search_results():
    query = request.form.get("query")
    topics_words, word_scores, topic_scores, topic_nums = model.query_topics(query, 10)
    return render_template("partials/search-results.html.j2", topics=topic_nums)


@app.route("/topic/<int:topic_num>")
def topic_details(topic_num: int):
    document_scores, document_ids = model.search_documents_by_topic(
        topic_num=topic_num, num_docs=model.topic_sizes[topic_num]
    )
    return render_template(
        "topic.html.j2",
        documents=zip(document_ids, document_scores),
        topic_num=topic_num,
    )


@app.route("/partials/topic_cloud/<int:topic_num>")
def topic_cloud_view(topic_num):
    data = topic_word_cloud(topic_num)
    return render_template("partials/cloud.html.j2", data=data, topic_num=topic_num)


@app.route("/partials/datasets/<dataset_id>")
def dataset_view(dataset_id):
    r = httpx.get(f"https://www.data.gouv.fr/api/2/datasets/{dataset_id}/")
    data = r.json()
    data["score"] = request.args.get("score")
    return render_template("partials/dataset.html.j2", data=data)
