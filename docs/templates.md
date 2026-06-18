# InferDoctor Templates

Templates are lightweight starter projects for common local AI application ideas. They are designed to show what you can build after the machine and endpoint are healthy.

## List Templates

```bash
inferdoctor template list
inferdoctor template show customer-service
```

## Create a Starter

```bash
inferdoctor template create customer-service --output ./customer-service-demo
inferdoctor template create restaurant-ordering --output ./restaurant-ordering-demo
inferdoctor template create local-doc-qa --output ./local-doc-qa-demo
```

Template creation writes files only to the explicit `--output` directory. It does not install packages or contact remote services.

## Current Creatable Templates

- `customer-service`: FAQ chatbot against a local OpenAI-compatible endpoint.
- `restaurant-ordering`: menu and policy assistant for a concrete ordering demo.
- `local-doc-qa`: local Markdown keyword retrieval fallback for document Q&A experiments.

## Endpoint Assumption

Generated chat templates default to:

```text
http://127.0.0.1:8000/v1
```

Override with:

```bash
export LOCAL_AI_BASE_URL=http://127.0.0.1:30000/v1
export LOCAL_AI_MODEL=local-model
```
