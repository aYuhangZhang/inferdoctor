# InferDoctor 日本語クイックスタート

[English README](README.md)

**ローカル AI 推論スタックを 1 コマンドで診断します。**

InferDoctor は、Ollama、vLLM、SGLang、Xinference、Dify、CUDA、NVIDIA
ドライバ、llama.cpp server、LM Studio、Open WebUI などのローカル AI
環境が「なぜ動かないのか」を調べるための軽量 CLI ツールです。

```bash
inferdoctor
```

モデルを選ぶツールではありません。InferDoctor は、すでに運用している
ローカル AI スタックの状態を診断します。

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

Python 3.9 以上が必要です。

```bash
git clone https://github.com/anguoyang/inferdoctor.git
cd inferdoctor
python -m pip install -e .
inferdoctor
```

## クイックスタート

```bash
inferdoctor                              # 全体のヘルスチェック
inferdoctor check nvidia                 # NVIDIA ドライバ/GPU
inferdoctor check ollama                 # Ollama CLI と API
inferdoctor check vllm --endpoint http://127.0.0.1:8000/v1
inferdoctor check sglang --endpoint http://127.0.0.1:30000/v1
inferdoctor scenario                     # 目的別の readiness
inferdoctor profile --format markdown    # 共有しやすい診断プロフィール
inferdoctor capacity --gpu "RTX 3090"    # 軽量な容量見積もり
```

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

## 安全ポリシー

InferDoctor は軽量で、デフォルトでは読み取り専用です。

- AI runtime、CUDA、GPU framework をインストールしません。
- モデルをダウンロードしません。
- 推論を実行しません。
- systemd、Docker container、OS 設定を変更しません。
- GPU がない CPU-only マシンでも動作します。

## 次に読むもの

- [English README](README.md)
- [PyPI release workflow](docs/pypi_release.md)
- [v0.2.0 release checklist](docs/release_checklist.md)
