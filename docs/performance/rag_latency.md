# RAG Latency

RAG apps can feel slow even when the model endpoint is healthy. Retrieval, reranking, prompt construction, and generation all add latency.

## Common Bottlenecks

- Too many retrieved chunks.
- Expensive reranking.
- Large context windows.
- Rebuilding indexes during the request path.
- Waiting silently while retrieval runs.
- Running an oversized model for an interactive app.

## Better Defaults

- Start with `top_k: 4` or `top_k: 5`.
- Cache embeddings and indexes.
- Use reranking only when answer quality needs it.
- Show retrieval progress before generation.
- Stream generation output.
- Keep a context budget and trim noisy chunks.

## Commands

```bash
inferdoctor optimize rag --docs 1000 --chunks 5000 --top-k 8 --ttft 2.5 --streaming
inferdoctor optimize rag --retrieval-ms 900 --rerank-ms 1500 --top-k 12
```

## Template Fit

The `local-doc-qa` starter uses simple keyword retrieval and no vector database by default. It is intentionally small so beginners can understand the request flow before adding embeddings, rerankers, or a vector store.
