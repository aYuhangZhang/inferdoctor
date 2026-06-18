# Stack Plan Examples

`inferdoctor stack plan` turns a goal into a beginner-friendly local AI app plan.

## Customer Service on a 24 GiB GPU

```bash
inferdoctor stack plan --goal customer-service --vram 24
```

Expected guidance:

- Runtime: Ollama for easiest setup, with vLLM or SGLang as performance options.
- Model size class: 7B or 14B quantized.
- Template: `customer-service`.
- Next: create and validate `./customer-service-demo`.

## Document Q&A, Easiest Path

```bash
inferdoctor stack plan --goal document-qa --preference easiest
```

Expected guidance:

- Start with a simple OpenAI-compatible endpoint.
- Use the `local-doc-qa` template.
- Add Dify or embeddings later only when the simple version works.

## Safety

The command is advisory and read-only. It does not install runtimes, download models, run inference, or change system settings.
