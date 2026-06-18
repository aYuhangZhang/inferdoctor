# Template Projects

InferDoctor templates are small starter projects for local AI apps. They are examples, not a heavy framework.

## Current Creatable Templates

- `customer-service`: FAQ assistant with realistic support data.
- `restaurant-ordering`: menu assistant with ordering policies.
- `local-doc-qa`: Markdown document Q&A with keyword retrieval fallback.

## Commands

```bash
inferdoctor template list
inferdoctor template show customer-service
inferdoctor template create customer-service --output ./customer-service-demo
inferdoctor template validate ./customer-service-demo
```

## Configuration

Generated templates use `.env` or `config.yaml`:

```bash
LOCAL_AI_BASE_URL=http://127.0.0.1:8000/v1
LOCAL_AI_MODEL=local-model
```

## What Template Validation Checks

`inferdoctor template validate <path>` checks that required files exist, endpoint config is present, data files exist, and no obvious secret-like values were added.

It does not install dependencies, call external services, or run inference.
