# Troubleshooting Slow Local AI Responses

Slow local AI apps usually fail in one of three ways:

- users wait too long before the first token;
- generation starts but the full answer takes too long;
- retrieval or reranking blocks the UI before generation starts.

InferDoctor helps you separate these symptoms without running a heavy benchmark.

## First Checks

```bash
inferdoctor
inferdoctor perf streaming --endpoint http://127.0.0.1:8000/v1 --model local-model --runs 2 --warmup 1
inferdoctor optimize endpoint --runtime vllm --vram 24 --model-size 14b --streaming
```

## If TTFT Is High

- Warm up the endpoint before a demo.
- Reduce context length.
- Use a smaller or quantized model.
- Check whether the runtime is falling back to CPU.
- Validate streaming support separately from total latency.

## If TPS Is Low

- Keep answers shorter for chat-heavy workflows.
- Use a smaller model for interactive demos.
- Check GPU memory pressure.
- Avoid treating estimated TPS as exact throughput.

## If RAG Feels Slow

```bash
inferdoctor optimize rag --retrieval-ms 900 --rerank-ms 1500 --top-k 8 --ttft 2.5 --streaming
```

- Show retrieval progress immediately.
- Cache embeddings and indexes.
- Reduce `top_k`.
- Avoid expensive reranking unless quality needs it.
- Keep a context budget.
- Separate retrieval latency from generation TTFT in logs.

## Runtime Notes

- Ollama is often the easiest local setup path, but model size and cold starts still matter.
- vLLM and SGLang can improve serving throughput, but batching and context length may affect interactive TTFT.
- Dify and Open WebUI users should show progress before generation, especially when retrieval or tool calls run first.

InferDoctor does not measure answer quality, GPU utilization, or production throughput. Use its performance commands as smoke tests and early UX guidance.
