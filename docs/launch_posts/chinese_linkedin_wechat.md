# InferDoctor：一条命令诊断本地 AI 推理栈为什么跑不起来

本地 AI 很强，但调试本地推理环境经常很痛苦。

同一个“请求失败”，背后可能是完全不同的问题：

- Ollama 没启动
- vLLM 或 SGLang 的 OpenAI-compatible endpoint 配错了
- `/v1/models` 返回 404、401、HTML 或错误 JSON
- Xinference / Dify / Open WebUI 的端口映射不对
- NVIDIA driver 可见，但 CUDA toolkit 不存在
- Docker CLI 有，但 daemon 连不上

InferDoctor 是一个开源、轻量、只读的 Python CLI，用来回答一个问题：

**为什么我的本地 AI stack 不工作？**

```bash
inferdoctor
```

它会输出适合截图分享的诊断结果：

- Overall Health score
- 每个组件的 PASS / WARN / FAIL / SKIP
- Top Fixes：可能原因、影响、下一条命令、配置提示
- OpenAI-compatible endpoint 诊断
- `inferdoctor explain` 常见问题解释
- `inferdoctor scenario` 按应用场景判断 readiness
- `inferdoctor profile` 安全脱敏诊断资料导出
- `inferdoctor capacity` 轻量容量估算

InferDoctor 不安装 AI runtime，不下载模型，不运行推理，不修改系统设置，也不做模型排行榜。

模型推荐工具帮你选模型。InferDoctor 帮你搞清楚为什么本地推理栈坏了。

Install: `pip install inferdoctor`

Repository: https://github.com/anguoyang/inferdoctor
