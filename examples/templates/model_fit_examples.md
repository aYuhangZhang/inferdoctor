# Model Fit Examples

`inferdoctor model fit` gives rough memory heuristics. It is not a benchmark.

## 7B Q4 on 8 GiB VRAM

```bash
inferdoctor model fit --size 7b --quant q4 --vram 8
```

Expected result: maybe. Use conservative context length and easiest runtimes first.

## 14B Q4 on 24 GiB VRAM

```bash
inferdoctor model fit --size 14b --quant q4 --vram 24
```

Expected result: likely OK for a local demo, with memory caveats.

## 32B Q4 on 24 GiB VRAM

```bash
inferdoctor model fit --size 32b --quant q4 --vram 24
```

Expected result: maybe. Context length, KV cache, runtime flags, and concurrency can push memory higher.

## Next Diagnostics

```bash
inferdoctor capacity --model-size 14b --quant q4 --vram 24
inferdoctor check vllm --endpoint http://127.0.0.1:8000/v1
inferdoctor check sglang --endpoint http://127.0.0.1:30000/v1
```
