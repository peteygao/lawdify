# Lawdify RAG Demo

## Install Dependencies

- Use [asdf](https://asdf-vm.com/guide/getting-started.html) to manage Python and Node versions (specified in .tool-versions)

```bash
$ asdf install
```

- Install [poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) with the official installer:

```bash
$ curl -sSL https://install.python-poetry.org | python3 -
```

- Install Python dependencies with `poetry install`
- Install Nodejs dependencies with `cd frontend && npm i`
- **Obtain OpenAPI API Key, Base URL, Model Name and add them to `.env`**

## Running the application

1. First, index the documents under `./documents` via `poetry run python index_documents.py`
2. Launch the FastAPI server: `poetry run fastapi dev lawdify.py` (first launch will take longer due to having to download nomic-text-embed v1.5 from HuggingFace)
3. Launch the frontend: `cd frontend && npm start`
4. Go to `http://localhost:3000` to interact with the Lawdify RAG Demo
