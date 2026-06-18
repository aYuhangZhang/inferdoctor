# Local AI Stacks Explained

A local AI stack is the set of pieces that make a local AI app work on your machine.

## Common Pieces

- Hardware: CPU, RAM, GPU, VRAM.
- Driver layer: NVIDIA driver and sometimes CUDA toolkit.
- Runtime: Ollama, vLLM, SGLang, LM Studio, llama.cpp server, or Xinference.
- API endpoint: the HTTP URL your app calls.
- App layer: Dify, Open WebUI, or your own Python app.
- Data layer: documents, FAQs, menus, notes, or a vector database.

## Why Stacks Break

Common causes:

- The runtime is not running.
- The app points at the wrong port or missing `/v1` base URL.
- The selected model does not fit memory.
- NVIDIA driver works, but CUDA toolkit is missing for build workflows.
- The API requires auth but the app does not send it.
- A UI is running, but the model backend behind it is not.

## What InferDoctor Checks

InferDoctor checks system information, GPU/driver signals, CUDA toolkit availability, local endpoints, OpenAI-compatible behavior, Docker availability, and common local AI services.
