# TTFT, TPS, And Streaming

TTFT and TPS answer different questions.

- TTFT: how long before the first visible token or chunk appears.
- TPS: rough output tokens per second after generation starts.
- Total latency: the full time until the response is complete.

For customer demos, TTFT often matters more than total latency. A streamed answer that starts in one second can feel better than a non-streamed answer that returns all text after eight seconds.

## Streaming Checklist

- Enable `streaming: true` in generated templates.
- Check streaming with `inferdoctor perf streaming`.
- Show a typing/progress state before generation starts.
- Warm up the endpoint before a live demo.
- Keep prompt and context size under control.

## Example

```bash
inferdoctor perf streaming --endpoint http://127.0.0.1:8000/v1 --model local-model
inferdoctor optimize endpoint --streaming --ttft 1.8 --tps 35
```

## Caveats

InferDoctor estimates rough output speed only when it can safely observe response text. It is not a tokenizer and does not claim benchmark-grade TPS.


## Related Guides

- [Metric definitions](metric_definitions.md)
- [Performance reports](performance_reports.md)
- [Troubleshooting slow responses](troubleshooting_slow_responses.md)
- [Customer experience checklist](customer_experience_checklist.md)
