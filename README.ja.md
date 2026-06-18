# InferDoctor 日本語クイックスタート

[English README](README.md)

**ローカル AI スタックを診断し、アプリ作成の次の一手を案内します。**

InferDoctor は、ローカル AI スタックの doctor 兼 setup assistant です。Ollama、vLLM、SGLang、Xinference、Dify、CUDA、NVIDIA ドライバ、llama.cpp server、LM Studio、Open WebUI などを軽量に診断し、このマシンで何を作れそうか、どのテンプレートから始めるべきかを示します。

```bash
inferdoctor
```

モデル推薦だけを行うツールではありません。InferDoctor は、ローカル AI スタックがなぜ動かないのかを調べ、実用的なセットアップ手順と starter template につなげます。

## なぜローカル AI スタックは壊れやすいのか

アプリケーションから見ると同じエラーでも、原因は複数あります。

- NVIDIA ドライバや `nvidia-smi` が見えない
- CUDA toolkit や `nvcc` がない
- Ollama、vLLM、SGLang などの runtime が起動していない
- `/v1/models` の URL が間違っている
- Dify や Open WebUI のポート設定が違う
- Docker daemon に接続できない
- 認証、リバースプロキシ、JSON 形式が期待と違う

InferDoctor は各レイヤーを分けて確認し、次に試すべきコマンドを表示します。

## インストール

Python 3.9 以上が必要です。PyPI 公開前の開発版は GitHub からインストールしてください。

```bash
python -m pip install "git+https://github.com/anguoyang/inferdoctor.git@dev"
inferdoctor
```

開発用に clone する場合:

```bash
git clone https://github.com/anguoyang/inferdoctor.git
cd inferdoctor
python -m pip install -e ".[dev]"
inferdoctor
```

## クイックスタート

```bash
inferdoctor                                      # 全体のヘルスチェック
inferdoctor recommend --goal customer-service   # 目的に合う構成を提案
inferdoctor stack plan --goal customer-service  # 次に実行する手順を表示
inferdoctor template list                       # 利用できるテンプレート
inferdoctor template create customer-service --output ./customer-service-demo
inferdoctor template validate ./customer-service-demo
inferdoctor model fit --size 14b --quant q4 --vram 24
```

生成されたテンプレートは OpenAI 互換のローカル endpoint を前提にしています。`config.yaml` または `.env` で Ollama、LM Studio、vLLM、SGLang などの endpoint を指定できます。

## 出力例

```text
InferDoctor - Local AI Stack Health Check
=========================================================
Overall Health: 82 / 100  (Mostly healthy)
Stack Summary: 3 working | 2 needs attention | 3 optional/offline | 0 failed

Component   Status   Summary
----------- -------- --------------------------------------------------
System      PASS     System information collected
NVIDIA      PASS     1 NVIDIA GPU(s) detected
CUDA        SKIP     CUDA compiler was not found
Ollama      PASS     Ollama CLI and API are available
vLLM        WARN     vLLM models route returned HTTP 404
SGLang      SKIP     SGLang endpoint is not reachable

Top recommended fixes (most useful first):
1. vLLM: vLLM models route returned HTTP 404
   Try: inferdoctor check vllm --endpoint http://127.0.0.1:8000/v1
```

## 対応しているチェック

| 対象 | 内容 |
| --- | --- |
| System | OS、Python、CPU アーキテクチャ、メモリ |
| NVIDIA | `nvidia-smi`、GPU 名、VRAM、ドライバ |
| CUDA | `nvcc`、CUDA toolkit、関連環境変数 |
| Ollama | CLI と `/api/tags` |
| vLLM / SGLang | OpenAI 互換 `/v1/models` |
| llama.cpp server / LM Studio | OpenAI 互換 API の疎通 |
| Xinference / Dify | SDK なしの軽量 HTTP 診断 |
| Open WebUI | Web endpoint の疎通 |
| Docker | CLI と daemon の疎通。コンテナは起動しません |

## テンプレート機能

InferDoctor は、次のような starter project を生成できます。

- customer-service: FAQ 対応チャットボット
- restaurant-ordering: メニューと注文ポリシーを使う接客アシスタント
- local-doc-qa: Markdown ドキュメントの軽量 Q&A

テンプレート生成は指定した出力ディレクトリにファイルを書くだけです。依存関係のインストール、モデルのダウンロード、推論実行は行いません。

## 安全ポリシー

InferDoctor は軽量で、デフォルトでは読み取り専用です。

- AI runtime、CUDA、GPU framework をインストールしません。
- モデルをダウンロードしません。
- 推論を実行しません。
- systemd、Docker container、OS 設定を変更しません。
- GPU がない CPU-only マシンでも動作します。

## 次に読むもの

- [English README](README.md)
- [Getting Started](docs/getting_started.md)
- [Templates](docs/templates.md)
- [Stack Recommendations](docs/recommendations.md)
- [Model Fit Advisor](docs/model_fit.md)
- [Release Checklist](docs/release_checklist.md)
