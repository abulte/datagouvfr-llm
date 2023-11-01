# datagouvfr-llm

This repo provides experimental tooling using the [llm package](https://llm.datasette.io/en/stable/) and [data.gouv.fr's data](https://www.data.gouv.fr/fr/).

The inspiration comes from [Simon Willison's blog post "Embeddings: What they are and why they matter"](https://simonwillison.net/2023/Oct/23/embeddings/).

Current features:
- embed data.gouv.fr's catalog in a SQLite db, with a configurable embedding model
- query the embeddings for similiarity through a Flask web app

In order to be able to ship the embeddings database in git (required for deploy, 100Mo limit on github), the dataset corpus is filtered on `quality_score > 0.6`. This shoud also provide better results.

## Install

Use a venv.

On macOS:

```bash
make install
```

## Use

```bash
make embeddings
make test
```

This will:
- cleanup previous embeddings if any
- download the latest datasets catalog from data.gouv.fr
- create a cleaned up CSV with the rows and columns we want
- compute embeddings for every unarchived dataset title, description and tags

Launch the web app:

```bash
make serve
```

## Configuration

In `.env`:

```bash
# model used for embeddings
LLM_MODEL=sentence-transformers/all-MiniLM-L6-v2
# collection name in database for storing embeddings
LLM_COLLECTION=datasets-minilm-l6-v2
# database file
LLM_DB=embeddings.db
```
