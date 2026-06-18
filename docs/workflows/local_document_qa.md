# Local Document Q&A Workflow

## Who This Is For

Developers who want a simple local document assistant before adopting a vector database.

## What It Builds

A Markdown document Q&A starter with lightweight keyword retrieval fallback.

## Recommended Hardware

CPU-only is enough for ingestion and keyword retrieval. GPU helps only when you call a local generation endpoint.

## Runtime Options

- Easiest: Ollama or LM Studio.
- App layer: Dify when you need a fuller RAG workflow.
- Serving: vLLM or SGLang for GPU-backed OpenAI-compatible APIs.

## Commands

```bash
inferdoctor
inferdoctor recommend --goal document-qa --preference easiest
inferdoctor stack bootstrap --goal document-qa --dry-run
inferdoctor template create local-doc-qa --output ./local-doc-qa-demo
inferdoctor template validate ./local-doc-qa-demo
inferdoctor template smoke-test ./local-doc-qa-demo
```

## Configure and Run

```bash
cd ./local-doc-qa-demo
cp .env.example .env
python ingest.py
python query.py --dry-run
python query.py "What is an OpenAI-compatible endpoint?"
```

## Troubleshooting

```bash
inferdoctor check dify --endpoint http://127.0.0.1:5001
inferdoctor check xinference --endpoint http://127.0.0.1:9997
inferdoctor explain openai-compatible-invalid-json
```

## Limitations

The starter uses keyword retrieval. It is intentionally not a full vector database or production RAG system.

## Next Upgrades

Add embeddings, chunking, citations, a vector index, document upload, and a UI.
