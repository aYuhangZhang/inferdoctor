# Customer Experience Checklist

Use this checklist before a customer demo, internal prototype review, or screenshot/video walkthrough.

## Diagnose

```bash
inferdoctor
```

Confirm that the runtime, endpoint, GPU/driver, and optional services are in the expected state.

## Validate The App

```bash
inferdoctor template validate ./customer-service-demo
inferdoctor template smoke-test ./customer-service-demo
```

Smoke tests should pass without calling a model endpoint.

## Measure Responsiveness

```bash
inferdoctor perf streaming --endpoint http://127.0.0.1:8000/v1 --model local-model --runs 2 --warmup 1
```

Look for:

- TTFT: how long before the first visible answer content appears.
- Total latency: how long the full turn takes.
- Streaming observed: whether stream=true produced real content chunks.
- Metric quality: exact, estimated, or unknown.
- Run variation: whether cold/warm behavior is unstable.

## Optimize

```bash
inferdoctor optimize endpoint --runtime vllm --vram 24 --model-size 14b --streaming --ttft 2.5
inferdoctor optimize rag --top-k 8 --retrieval-ms 900 --ttft 2.5 --streaming
```

Prioritize:

1. Show progress before generation.
2. Enable streaming.
3. Warm up before demos.
4. Reduce context size.
5. Use a smaller or quantized model for interactive workflows.
6. Measure retrieval and generation separately.

## Workflow Examples

- Customer-service chatbot: validate the generated template, run `app.py --dry-run`, then check streaming TTFT.
- Restaurant-ordering assistant: keep responses short and stream answers quickly.
- Local document Q&A: show retrieval progress, keep `top_k` small, and use a context budget.
- Dify RAG: separate retrieval/rerank latency from LLM TTFT.
- Open WebUI: verify the backend endpoint separately from the web UI.
- vLLM/SGLang serving: check `/v1/models`, streaming, and model/context fit before tuning throughput.

## What This Does Not Prove

- It is not a benchmark.
- It does not measure answer quality.
- It does not prove production capacity.
- It does not inspect private runtime internals.
- It does not download models or install runtimes.
