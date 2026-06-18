# Customer Service Chatbot Workflow

## Who This Is For

Small teams that want a local FAQ assistant before adding a full RAG system.

## What It Builds

A starter chatbot that answers from local FAQ data and talks to an existing OpenAI-compatible local endpoint.

## Recommended Hardware

CPU-only is fine for testing the template. A small NVIDIA GPU improves response latency when your runtime supports it.

## Runtime Options

- Easiest: Ollama or LM Studio with an OpenAI-compatible endpoint.
- Performance: vLLM or SGLang after GPU and endpoint checks pass.

## Commands

```bash
inferdoctor
inferdoctor recommend --goal customer-service --preference easiest
inferdoctor stack bootstrap --goal customer-service --dry-run
inferdoctor template create customer-service --output ./customer-service-demo
inferdoctor template validate ./customer-service-demo
inferdoctor template smoke-test ./customer-service-demo
```

## Configure and Run

```bash
cd ./customer-service-demo
cp .env.example .env
python app.py --dry-run
python app.py --check-config
python app.py
```

## Troubleshooting

```bash
inferdoctor check vllm --endpoint http://127.0.0.1:8000/v1
inferdoctor check sglang --endpoint http://127.0.0.1:30000/v1
inferdoctor explain openai-compatible-connection-refused
```

## Limitations

This starter uses static FAQ data. It does not include user accounts, ticketing integration, or production authentication.

## Next Upgrades

Add your real FAQ, add retrieval, connect to a ticketing system, and introduce auth before production use.
