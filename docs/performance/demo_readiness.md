# Demo Readiness

Before showing a local AI app to a customer or teammate, verify the user journey, not just the endpoint.

## Checklist

```bash
inferdoctor
inferdoctor template validate ./customer-service-demo
inferdoctor template smoke-test ./customer-service-demo
inferdoctor perf streaming --endpoint http://127.0.0.1:8000/v1 --model local-model
inferdoctor optimize endpoint --runtime vllm --vram 24 --model-size 14b
```

## What Good Looks Like

- The app starts without installing heavy runtimes.
- `--dry-run` and `--check-config` are clear.
- Streaming is enabled or the UI shows useful progress.
- The first live request has been warmed up.
- Slow retrieval has a progress message.
- Error messages explain endpoint, auth, 404, timeout, and invalid JSON cases.

## If The Demo Feels Slow

- Warm up the endpoint with a tiny question.
- Reduce context length or `top_k`.
- Use a smaller or quantized model.
- Check whether the runtime is falling back to CPU.
- Use Ollama for easiest setup or vLLM/SGLang for higher-throughput serving when appropriate.
- Separate retrieval latency from generation latency in your logs.


## Related Guides

- [Metric definitions](metric_definitions.md)
- [Performance reports](performance_reports.md)
- [Troubleshooting slow responses](troubleshooting_slow_responses.md)
- [Customer experience checklist](customer_experience_checklist.md)
