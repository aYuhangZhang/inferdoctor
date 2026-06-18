# Restaurant Ordering Assistant Workflow

## Who This Is For

Restaurant operators, demo builders, and local AI learners who want a concrete assistant scenario.

## What It Builds

A local ordering assistant with menu data, ordering policies, sample orders, and a system prompt.

## Recommended Hardware

CPU-only works for smoke tests and small models. GPU improves interactive response speed.

## Runtime Options

- Easiest: Ollama or LM Studio.
- Higher throughput: vLLM or SGLang on a suitable NVIDIA GPU.

## Commands

```bash
inferdoctor
inferdoctor recommend --goal restaurant-ordering --preference easiest
inferdoctor stack plan --goal restaurant-ordering
inferdoctor template create restaurant-ordering --output ./restaurant-ordering-demo
inferdoctor template validate ./restaurant-ordering-demo
inferdoctor template smoke-test ./restaurant-ordering-demo
```

## Configure and Run

```bash
cd ./restaurant-ordering-demo
cp .env.example .env
python app.py --dry-run
python app.py --check-config
python app.py
```

## Troubleshooting

Run endpoint checks before blaming the template:

```bash
inferdoctor check ollama
inferdoctor check lmstudio --endpoint http://127.0.0.1:1234/v1
inferdoctor explain openai-compatible-404
```

## Limitations

This is not a POS system. It does not accept payments, reserve inventory, or place real orders.

## Next Upgrades

Add real menu data, connect to order management, add allergen review, and add human confirmation before payment.
