# Bootstrap Local Document Q&A Demo

## Goal

Generate a local document Q&A starter project plus a bootstrap plan.

## Commands

```bash
inferdoctor stack bootstrap --goal document-qa --output ./docqa-bootstrap
cd ./docqa-bootstrap
inferdoctor template validate .
inferdoctor template smoke-test .
```

## Generated Files

- `ingest.py`
- `query.py`
- `docs/sample.md`
- `.env.example`
- `config.yaml`
- `bootstrap_plan.md`
- `next_steps.md`
- `config_summary.yaml`

## Next Steps

Run `python query.py --dry-run`, then configure a local OpenAI-compatible endpoint when ready.

## Limitations

The starter uses lightweight keyword retrieval. It does not install a vector database, download models, or run inference.
