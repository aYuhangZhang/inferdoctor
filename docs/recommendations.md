# Stack Recommendations

`inferdoctor recommend` gives a rough local AI setup recommendation based on your goal, preference, and hardware information.

## Examples

```bash
inferdoctor recommend
inferdoctor recommend --goal customer-service --vram 24
inferdoctor recommend --goal document-qa --preference easiest
inferdoctor recommend --goal local-api --preference performance --vram 24
```

## What It Returns

- Recommended runtime path
- Model size class
- Starter template
- Why the recommendation was made
- Next commands
- Memory and runtime caveats
- What InferDoctor does not know yet

## Beginner Flow

Use `recommend` to choose a direction, then use `stack plan` and templates to turn that direction into concrete commands:

```bash
inferdoctor recommend --goal customer-service --preference easiest
inferdoctor stack plan --goal customer-service
inferdoctor template create customer-service --output ./customer-service-demo
inferdoctor template validate ./customer-service-demo
```

## Hardware Inputs

If InferDoctor can detect your GPU, it uses that information. You can also provide a simple override:

```bash
inferdoctor recommend --goal local-api --preference performance --vram 24
```

The `--vram` value is a practical planning hint, not a benchmark input.

## What It Does Not Do

It does not rank exact model names, download models, start runtimes, or benchmark throughput. Use it as a setup direction, then verify with `inferdoctor check`, `inferdoctor capacity`, and `inferdoctor model fit`.
