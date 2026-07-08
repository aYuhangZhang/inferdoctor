# ローカル AI スタックの「なぜ動かない？」を 1 コマンドで診断する InferDoctor

ローカル AI は便利ですが、実際に動かすとデバッグが大変です。

- Ollama が起動していない
- vLLM / SGLang の `/v1/models` が 404 になる
- Xinference や Dify のポートが違う
- CUDA toolkit はないが NVIDIA ドライバは見えている
- Docker daemon に接続できない
- OpenAI 互換 API のはずが HTML や違う JSON が返る

こうした問題は、アプリ側から見ると同じような失敗に見えます。

InferDoctor は、このローカル AI 推論スタックを軽量に診断する OSS CLI です。

```bash
inferdoctor
```

出力では、ヘルススコア、コンポーネント別の PASS/WARN/FAIL/SKIP、Top Fixes、
次に試すコマンドを表示します。スクリーンショットで共有しやすい形式を意識しています。

便利なコマンド:

```bash
inferdoctor check vllm --endpoint http://127.0.0.1:8000/v1
inferdoctor check sglang --endpoint http://127.0.0.1:30000/v1
inferdoctor explain openai-compatible-404
inferdoctor scenario
inferdoctor profile --format markdown
inferdoctor capacity --gpu "RTX 3090"
```

InferDoctor はモデル推薦ツールではありません。モデルを選ぶ、ダウンロードする、推論する、
ベンチマークする、といったことはしません。すでに手元にあるローカル AI スタックが
なぜ壊れているのかを切り分けます。

Install: `pip install inferdoctor`

Repository: https://github.com/anguoyang/inferdoctor
