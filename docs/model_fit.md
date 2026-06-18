# Model Fit Advisor

`inferdoctor model fit` estimates whether a model size and quantization class likely fit in available VRAM.

## Examples

```bash
inferdoctor model fit --size 7b --quant q4 --vram 8
inferdoctor model fit --size 14b --quant q4 --vram 24
inferdoctor model fit --size 32b --quant q4 --vram 24
inferdoctor model fit --size 14b --quant q4 --runtime ollama
```

## Output

- Estimated memory class
- Fit likelihood: `LIKELY OK`, `MAYBE`, or `UNLIKELY`
- Why the estimate was made
- Easiest runtime path
- Performance runtime path
- Memory caveats
- Suggested next commands
- What InferDoctor does not know yet

## How To Use It

Use model fit before spending time configuring a runtime:

```bash
inferdoctor model fit --size 14b --quant q4 --vram 24
inferdoctor capacity --vram 24 --model-size 14b --quant q4
```

If the result is `MAYBE`, reduce context length, use a smaller quantization footprint, try CPU offload, or choose a smaller model size class.

## Accuracy

These estimates are rough heuristics, not benchmarks. Context length, KV cache, runtime settings, CPU offload, batch size, model architecture, and quantization format can all change real memory usage.
