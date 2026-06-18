# Hardware and Model Fit

Local AI performance depends mostly on memory, model size, quantization, runtime overhead, and context length.

## Terms

- RAM: system memory used by CPU workloads and apps.
- VRAM: GPU memory used by model weights, KV cache, and runtime overhead.
- Model size: often described as 7B, 14B, 32B, and so on.
- Quantization: smaller numerical formats such as Q4 or Q8 that reduce memory use.
- Context length: how much text the model can consider at once; longer context uses more memory.

## Why CUDA and Drivers Matter

For NVIDIA GPUs, the driver lets the system use the GPU. CUDA toolkit is needed for some build and compile workflows. Many prebuilt runtimes can work with only the driver, but development or custom builds may need the toolkit.

## Use InferDoctor

```bash
inferdoctor capacity --vram 24 --model-size 14b --quant q4
inferdoctor model fit --size 14b --quant q4 --vram 24
```

## Interpret Results

- Likely OK: enough memory headroom for a practical demo, still not a benchmark.
- Maybe: close to the estimate; reduce context, concurrency, or model size.
- Unlikely: estimated memory exceeds available VRAM.

InferDoctor estimates are rough heuristics. It does not know the exact model architecture, context length, KV cache size, batch size, or runtime flags until you provide them or run the actual server.
