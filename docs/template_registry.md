# Template Registry

InferDoctor currently ships a local built-in template catalog. It does not fetch, execute, or install remote templates.

## Built-In Templates

Use:

```bash
inferdoctor template list
inferdoctor template show customer-service
inferdoctor template registry
```

Built-in templates are generated locally and should be validated before use:

```bash
inferdoctor template validate ./customer-service-demo
inferdoctor template smoke-test ./customer-service-demo
```

## Future Community Templates

A future registry may allow community templates, but the safety model should stay conservative:

- No remote execution by default.
- No runtime installation by default.
- No model downloads by default.
- Template generation should be local and explicit.
- Template metadata should declare files, endpoints, runtime assumptions, and safety boundaries.
- Users should validate and smoke-test generated projects before connecting live endpoints.

## Local-Only Generation

Template generation writes only to the output directory selected by the user. InferDoctor should remain a setup assistant, not a hidden installer or runtime manager.
