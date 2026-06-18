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

Template creation writes files only to the explicit `--output` directory. It does not install packages, download models, or contact remote services.

## Validate and Smoke-Test a Starter

After generating a project, run:

```bash
inferdoctor template validate ./customer-service-demo
inferdoctor template smoke-test ./customer-service-demo
```

Validation checks for the expected README, config, `.env.example`, sample data, endpoint settings, entrypoint files, and obvious secret-looking values. Smoke tests run only allowlisted help, dry-run, and config-check commands inside the template directory. They do not install dependencies, call model endpoints, start services, or run inference.

## Generated Self-Checks

Generated templates include lightweight help, dry-run, and config checks that do not require a live model:

```bash
cd ./customer-service-demo
python app.py --help
python app.py --dry-run
python app.py --check-config
```

For document Q&A templates:

```bash
cd ./local-doc-qa-demo
python ingest.py --help
python query.py --help
python query.py --dry-run
python query.py --check-config
```

## Current Creatable Templates

- `customer-service`: FAQ chatbot against a local OpenAI-compatible endpoint.
- `restaurant-ordering`: menu and policy assistant for a concrete ordering demo.
- `local-doc-qa`: local Markdown keyword retrieval fallback for document Q&A experiments.

## Endpoint Assumption

Generated chat templates default to:

```text
http://127.0.0.1:8000/v1
```

Override with environment variables or `config.yaml`:

```bash
export LOCAL_AI_BASE_URL=http://127.0.0.1:30000/v1
export LOCAL_AI_MODEL=local-model
```

Common endpoints:

| Runtime | Example base URL |
| --- | --- |
| Ollama OpenAI-compatible API | `http://127.0.0.1:11434/v1` |
| LM Studio | `http://127.0.0.1:1234/v1` |
| vLLM | `http://127.0.0.1:8000/v1` |
| SGLang | `http://127.0.0.1:30000/v1` |

## What Templates Are Not

Templates are starter examples. They are not production frameworks, hosted services, model installers, or benchmark tools. Use them to learn the flow, then adapt them to your own application.
