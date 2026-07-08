# Beginner Guide: From Machine to Local AI App

InferDoctor is for the moment when you have a machine, Python works, and you want to know what local AI setup is realistic.

## Install

```bash
pip install inferdoctor
```

Then start with one command.

## What to Do First

```bash
inferdoctor
```

Read the health dashboard and Top Fixes first. Fix endpoint, driver, or runtime problems before building an app.

## Pick a Goal

Common beginner goals:

- Customer service chatbot
- Restaurant ordering assistant
- Local document Q&A
- Local OpenAI-compatible API demo
- Browser chat with Open WebUI

Ask InferDoctor for a plan:

```bash
inferdoctor init --goal customer-service --preference easiest
inferdoctor recommend --goal document-qa --preference easiest
inferdoctor stack plan --goal customer-service
inferdoctor stack bootstrap --goal customer-service --dry-run
```

## Create a Starter Project

```bash
inferdoctor template list
inferdoctor template create customer-service --output ./customer-service-demo
inferdoctor template validate ./customer-service-demo
inferdoctor template smoke-test ./customer-service-demo
```

Then edit `.env` or `config.yaml` in the generated directory. Before calling a live endpoint, run the generated dry-run command:

```bash
cd ./customer-service-demo
python app.py --dry-run
python app.py --check-config
```

## Keep the Safety Model Simple

InferDoctor does not install AI runtimes, download models, run inference, or change system settings by default. It diagnoses and guides; you choose what to install and run.
