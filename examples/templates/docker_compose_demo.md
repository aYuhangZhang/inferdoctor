# Docker Compose Demo

## Goal

Generate optional Docker Compose starter files without running Docker.

## Commands

```bash
inferdoctor template compose customer-service --output ./compose-customer-service
inferdoctor template compose open-webui --output ./compose-openwebui
```

## Generated Files

- `docker-compose.yml`
- `.env.example`
- `config.yaml`
- `README.md`

## Validation

Review files first. Only after manual review should you consider Docker commands such as `docker compose config`.

## Next Steps

Run `inferdoctor` before starting services so endpoint, GPU, and Docker issues are visible.

## Limitations

InferDoctor generates files only. It does not pull images, start containers, or install Docker.
