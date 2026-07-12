# Local AI User Experience

Local AI apps are judged by the same standards as cloud apps: users expect the answer to start quickly, progress to be visible, and failures to be understandable.

InferDoctor treats endpoint performance checks as smoke tests, not benchmarks. The goal is to catch obvious user-experience problems early without downloading models, installing runtimes, or running long load tests.

## What Users Feel

- Time to first token (TTFT): how long the user waits before anything appears.
- Total latency: how long the full answer takes.
- Streaming: whether the UI can show partial output while generation continues.
- Cold start: the first request after startup can be much slower than a warm request.
- Endpoint stability: timeouts, 404s, auth errors, and invalid JSON feel like broken apps.

## Practical Flow

```bash
inferdoctor
inferdoctor perf endpoint --endpoint http://127.0.0.1:8000/v1 --model local-model
inferdoctor perf streaming --endpoint http://127.0.0.1:8000/v1 --model local-model
inferdoctor optimize endpoint --runtime vllm --vram 24 --model-size 14b
```

Use a tiny prompt, keep timeouts strict, and interpret the result as an early warning signal.

## What InferDoctor Does Not Measure

- It does not run formal benchmarks.
- It does not measure GPU utilization.
- It does not profile kernel-level runtime behavior.
- It does not know your model architecture, KV cache settings, batching policy, or real user traffic.
- It does not install or start Ollama, vLLM, SGLang, Dify, or any other runtime.


## Related Guides

- [Metric definitions](metric_definitions.md)
- [Performance reports](performance_reports.md)
- [Troubleshooting slow responses](troubleshooting_slow_responses.md)
- [Customer experience checklist](customer_experience_checklist.md)
