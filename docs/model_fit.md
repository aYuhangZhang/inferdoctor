# Model Fit Advisor

`inferdoctor model fit` estimates whether a model size and quantization class likely fit in available VRAM.

## Examples

```bash
inferdoctor model fit --size 14b --quant q4 --vram 24
inferdoctor model fit --size 32b --quant q4 --vram 24
inferdoctor model fit --size 14b --quant q4 --runtime ollama
```

## Output

- Estimated memory class
- Fit likelihood: `LIKELY FITS`, `MAYBE`, or `UNLIKELY`
- Runtime caveat
- Suggested next capacity command

## Accuracy

These estimates are rough heuristics, not benchmarks. Context length, KV cache, runtime settings, CPU offload, batch size, model architecture, and quantization format can all change real memory usage.
