# Lawdify RAG Demo

## Install Dependencies

- Use [asdf](https://asdf-vm.com/guide/getting-started.html) to manage Python and Node versions (specified in .tool-versions)

```bash
$ asdf install
```

- Install [poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) with the official installer:

```bash
$ curl -sSL https://install.python-poetry.org | python3 -
$ poetry install
$ cd frontend
$ npm i
```

## Running the application

⚠️* *Obtain OpenAPI API Key, Base URL, Model Name and add them to `.env`**

1. Index the documents under `./documents` via `poetry run python index_documents.py`
2. Run the FastAPI server: `poetry run fastapi dev lawdify.py`
3. Run the frontend: `cd frontend && npm start`
4. Go to `http://localhost:3000` to interact with the Lawdify RAG Demo

## Development

`lawdify.py` is the core FastAPI server with the LLM interface at `/ask` endpoint. `index_documents.py` is for indexing files under `./documents` into the vector database (ChromaDB).

`frontend/` is the folder with a React front-end for interacting with the LLM via a chatbot-like UI. See that folder's README for more info.
