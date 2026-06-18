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
- Caveats

## What It Does Not Do

It does not rank specific model names, download models, start runtimes, or benchmark throughput. Use it as a setup direction, then verify with `inferdoctor check` and `inferdoctor capacity`.
