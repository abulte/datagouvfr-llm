import os

import httpx
import llm
import mistune
import sqlite_utils

from flask import Flask, render_template, request, abort
from flask_htmx import HTMX

app = Flask(__name__)
htmx = HTMX(app)


def get_similars(query):
    """Get similar embeddings from given query's embedding"""
    db = sqlite_utils.Database(os.getenv("LLM_DB"))
    collection = llm.Collection(os.getenv("LLM_COLLECTION"), db)
    return collection.similar(query)


@app.route("/")
def home():
    if htmx and not htmx.history_restore_request:
        similars = get_similars(request.args["query"])
        return render_template("partials/search-results.html.j2", similars=similars)
    return render_template("index.html.j2")


@app.route("/embed/<id>")
def embed(id):
    """Embed a dataset"""
    r = httpx.get(f"https://www.data.gouv.fr/api/2/datasets/{id}/")
    if not r.is_success:
        return abort(r.status_code)
    dataset = r.json()
    return render_template("partials/embed-dataset.html.j2", dataset=dataset)


@app.template_filter("from_markdown")
def from_markdown(value):
    md = mistune.create_markdown(hard_wrap=True)
    return md(value)
