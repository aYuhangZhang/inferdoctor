# LinkedIn / WeChat Post - Chinese

本地 AI 很强，但本地 AI 栈调试仍然很痛苦。

一个连接失败，背后可能是 CUDA、NVIDIA 驱动、Ollama、vLLM、SGLang、Dify、Open WebUI、Docker，或者只是 `/v1` endpoint 写错了。

InferDoctor 是一个开源的 local AI stack doctor and setup assistant。

它帮助开发者：

- 一条命令检查本地 AI 栈健康状态
- 给出 Top Fixes
- 预估硬件适合的用例
- 推荐本地 AI stack 路线
- 生成 starter template
- validate / smoke-test 模板
- 输出 dry-run setup plan

它不会默认下载模型、运行推理、安装 runtime 或修改系统设置。它的目标是让你知道哪里坏了，以及下一步怎么走。

安装：`pip install inferdoctor`

GitHub: https://github.com/anguoyang/inferdoctor
