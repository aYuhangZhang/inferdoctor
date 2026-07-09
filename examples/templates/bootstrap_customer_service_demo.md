# Bootstrap Customer Service Demo

## Goal

Generate a customer-service starter project plus a bootstrap plan.

## Commands

```bash
inferdoctor stack bootstrap --goal customer-service --output ./customer-service-bootstrap
cd ./customer-service-bootstrap
inferdoctor template validate .
inferdoctor template smoke-test .
```

## Generated Files

- Starter app files such as `app.py`, `.env.example`, `config.yaml`, and sample FAQ data
- `bootstrap_plan.md`
- `next_steps.md`
- `config_summary.yaml`

## Next Steps

Copy `.env.example` to `.env`, set your local endpoint, and try `python app.py --dry-run` before using a live model.

## Limitations

Bootstrap generation does not install dependencies, start services, call endpoints, or run inference.
