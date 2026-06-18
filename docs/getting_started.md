# Getting Started with InferDoctor

InferDoctor helps you diagnose a local AI machine, understand a practical stack path, and create small local AI starter projects.

## Install

PyPI publishing is not assumed for the current development branch. Install from GitHub for now:

```bash
python -m pip install "git+https://github.com/anguoyang/inferdoctor.git@dev"
```

For local development:

```bash
git clone https://github.com/anguoyang/inferdoctor.git
cd inferdoctor
python -m pip install -e ".[dev]"
```

## First Command

```bash
inferdoctor
```

This shows the local AI stack health dashboard, overall health score, component status table, and Top Fixes.

## Recommended Beginner Flow

Start with diagnosis:

```bash
inferdoctor
```

Pick a goal and get a practical recommendation:

```bash
inferdoctor recommend --goal customer-service --preference easiest
inferdoctor stack plan --goal customer-service
```

Create and validate a starter project:

```bash
inferdoctor template create customer-service --output ./customer-service-demo
inferdoctor template validate ./customer-service-demo
```

Configure the generated project:

```bash
cd ./customer-service-demo
cp .env.example .env
# Edit .env or config.yaml to point at your local OpenAI-compatible endpoint.
python app.py --help
python app.py --check-config
```

Then run the app when your local endpoint is ready:

```bash
python app.py
```

## Endpoint Examples

Most generated examples use a local OpenAI-compatible endpoint. Common base URLs include:

| Runtime | Example base URL |
| --- | --- |
| Ollama OpenAI-compatible API | `http://127.0.0.1:11434/v1` |
| LM Studio | `http://127.0.0.1:1234/v1` |
| vLLM | `http://127.0.0.1:8000/v1` |
| SGLang | `http://127.0.0.1:30000/v1` |
| Xinference OpenAI-compatible API | `http://127.0.0.1:9997/v1` |

## Safe Defaults

InferDoctor does not install runtimes, download models, run inference, or modify system settings by default. Template generation writes files only to the output directory you choose.
