# Dify RAG Debugging Workflow

## Who This Is For

Developers running Dify locally or on a private server and trying to connect it to local model backends.

## What It Builds

A troubleshooting path for separating Dify reachability from model endpoint and hardware issues.

## Recommended Hardware

Dify itself can run on modest hardware. The model backend determines CPU/GPU needs.

## Runtime Options

- Dify app layer with Ollama, Xinference, vLLM, or SGLang as model backend.
- Docker if your Dify deployment uses containers.

## Commands

```bash
inferdoctor
inferdoctor check dify --endpoint http://127.0.0.1:5001
inferdoctor check xinference --endpoint http://127.0.0.1:9997
inferdoctor check docker
inferdoctor recommend --goal document-qa --preference easiest
```

## Validate

Confirm Dify is reachable first, then diagnose the model endpoint separately. Do not assume a Dify error means CUDA or GPU is broken.

## Troubleshooting

```bash
inferdoctor explain openai-compatible-connection-refused
inferdoctor explain openai-compatible-unauthorized
inferdoctor profile --format markdown
```

## Limitations

InferDoctor does not inspect Dify internals, databases, credentials, or workflows. It performs lightweight external diagnostics.

## Next Upgrades

Add a Dify workflow template, endpoint examples, and deployment-specific checklists.
