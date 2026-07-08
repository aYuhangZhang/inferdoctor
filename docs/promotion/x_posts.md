# X Post Drafts

0. Install InferDoctor from PyPI: `pip install inferdoctor`, then run `inferdoctor`.

1. Local AI is powerful, but debugging it is painful. InferDoctor checks Ollama, vLLM, SGLang, Xinference, Dify, CUDA, NVIDIA, Docker, Open WebUI, and local endpoints in one command. https://github.com/anguoyang/inferdoctor

2. New in InferDoctor: setup-assistant workflow. Diagnose your stack, get recommendations, generate a starter template, validate it, and run a safe smoke test before calling a model endpoint.

3. Model recommendation tools help you choose a model. InferDoctor helps you understand why your local AI stack is broken and what to try next.

4. `inferdoctor stack bootstrap --goal customer-service --dry-run` prints a beginner-friendly setup plan without installing runtimes, downloading models, or starting services.
