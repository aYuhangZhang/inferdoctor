# Getting Started with InferDoctor

InferDoctor helps you diagnose a local AI machine, understand a practical stack path, and create small local AI starter projects.

## Install

```bash
pip install inferdoctor
```

For development:

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

```bash
inferdoctor
inferdoctor recommend --goal customer-service --preference easiest
inferdoctor template list
inferdoctor template create customer-service --output ./customer-service-demo
```

Then configure the generated app to point at your local OpenAI-compatible endpoint.

## Safe Defaults

InferDoctor does not install runtimes, download models, run inference, or modify system settings unless a future command explicitly says it will write files. Diagnostics are read-only by default.
