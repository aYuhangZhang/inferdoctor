# Performance Smoke-Test Reports

`inferdoctor perf endpoint` and `inferdoctor perf streaming` can write console, JSON, or Markdown reports.

```bash
inferdoctor perf endpoint --endpoint http://127.0.0.1:8000/v1 --model local-model --format json --output perf.json
inferdoctor perf streaming --endpoint http://127.0.0.1:8000/v1 --model local-model --format markdown --output perf.md
```

Reports are designed for debugging and GitHub issues, not benchmark publication.

## JSON Fields

The JSON report includes:

- `schema_version`
- `timestamp`
- sanitized `endpoint`
- `model`
- `test_type`
- `streaming_requested`
- `streaming_observed`
- `successful_runs`
- `failed_runs`
- `metrics`
- `metric_quality`
- `experience_read`
- `suggestions`
- `warnings`
- `errors`
- per-run summaries without raw response bodies

## Redaction

InferDoctor strips URL usernames and passwords and redacts query parameters whose names look like keys, tokens, secrets, passwords, auth values, or credentials. It never records authorization headers or full raw response bodies.

## Metric Quality

Token counts are marked as exact only when the endpoint reports usage fields. Otherwise InferDoctor labels them as estimates or unknown.
