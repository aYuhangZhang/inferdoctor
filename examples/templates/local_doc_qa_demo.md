# Local Document Q&A Template Demo

Use this when you want a simple local document assistant before adding a vector database or RAG framework.

## Command

```bash
inferdoctor template create local-doc-qa --output ./local-doc-qa-demo
inferdoctor template validate ./local-doc-qa-demo
```

## Generated Files

- `README.md`
- `ingest.py`
- `query.py`
- `requirements.txt`
- `.env.example`
- `config.yaml`
- `docs/sample.md`
- `troubleshooting.md`

## How It Works

```bash
cd ./local-doc-qa-demo
python ingest.py
python query.py
```

The first version uses keyword retrieval over Markdown files. It does not require a vector database, embeddings service, or internet access.

## Connect a Local Endpoint

Use the printed context with a local OpenAI-compatible endpoint, or extend `query.py` to call `/chat/completions`.

## Validate

```bash
inferdoctor template validate ./local-doc-qa-demo
```
