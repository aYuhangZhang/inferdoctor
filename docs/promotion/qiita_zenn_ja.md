# Qiita / Zenn Draft - Japanese

## ローカル AI スタックの「なぜ動かない」を診断する InferDoctor

ローカル AI は便利ですが、セットアップで詰まりやすいです。

- NVIDIA driver が見えていない
- CUDA toolkit がない
- Ollama / vLLM / SGLang が起動していない
- OpenAI 互換 endpoint の `/v1` が間違っている
- Dify / Open WebUI / Docker の接続が壊れている

InferDoctor は、ローカル AI スタックを診断し、次に何をすればよいかを表示する軽量 CLI です。

```bash
inferdoctor
inferdoctor recommend --goal customer-service
inferdoctor stack bootstrap --goal customer-service --dry-run
inferdoctor template create customer-service --output ./customer-service-demo
inferdoctor template validate ./customer-service-demo
inferdoctor template smoke-test ./customer-service-demo
```

デフォルトでは runtime のインストール、モデルダウンロード、推論実行、システム設定変更は行いません。

インストール：`pip install inferdoctor`

GitHub: https://github.com/anguoyang/inferdoctor
