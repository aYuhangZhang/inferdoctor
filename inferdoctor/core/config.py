from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.parse import urlsplit


DEFAULT_ENDPOINTS = {
    "ollama": "http://127.0.0.1:11434",
    "vllm": "http://127.0.0.1:8000/v1",
    "sglang": "http://127.0.0.1:30000/v1",
    "llamacpp": "http://127.0.0.1:8080",
    "lmstudio": "http://127.0.0.1:1234/v1",
    "xinference": "http://127.0.0.1:9997",
    "dify": "http://127.0.0.1:5001",
    "openwebui": "http://127.0.0.1:3000",
}


class ConfigError(ValueError):
    pass


def normalize_endpoint(name: str, url: str) -> str:
    normalized = url.strip().rstrip("/")
    parts = urlsplit(normalized)
    if parts.scheme not in ("http", "https") or not parts.netloc:
        raise ConfigError(
            "Endpoint '{0}' must be an http:// or https:// URL".format(name)
        )
    return normalized


@dataclass
class Config:
    endpoints: Dict[str, str] = field(
        default_factory=lambda: dict(DEFAULT_ENDPOINTS)
    )
    timeout: float = 2.0
    language: str = "auto"  # "auto", "en", "zh", "ja"


def _parse_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        return value[1:-1]
    return value


def _parse_simple_yaml(text: str) -> Dict[str, Any]:
    """Parse the small configuration subset documented by InferDoctor."""
    data: Dict[str, Any] = {}
    section: Optional[str] = None

    for line_number, original in enumerate(text.splitlines(), start=1):
        if not original.strip() or original.lstrip().startswith("#"):
            continue

        indent = len(original) - len(original.lstrip())
        line = original.strip()
        if ":" not in line:
            raise ConfigError(
                "Invalid config line {0}: expected key: value".format(line_number)
            )

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if indent == 0:
            if not value:
                section = key
                data[section] = {}
            else:
                section = None
                data[key] = _parse_scalar(value)
        elif section:
            mapping = data.get(section)
            if not isinstance(mapping, dict):
                raise ConfigError(
                    "Invalid config line {0}: parent is not a mapping".format(
                        line_number
                    )
                )
            mapping[key] = _parse_scalar(value)
        else:
            raise ConfigError(
                "Invalid config line {0}: unexpected indentation".format(line_number)
            )

    return data


def _validate_config(data: Dict[str, Any]) -> Config:
    unknown = set(data) - {"endpoints", "timeout", "language"}
    if unknown:
        raise ConfigError(
            "Unknown config key(s): {0}".format(", ".join(sorted(unknown)))
        )

    endpoints = dict(DEFAULT_ENDPOINTS)
    configured_endpoints = data.get("endpoints", {})
    if not isinstance(configured_endpoints, dict):
        raise ConfigError("'endpoints' must be a mapping")

    for name, url in configured_endpoints.items():
        if name not in DEFAULT_ENDPOINTS:
            raise ConfigError("Unknown endpoint: {0}".format(name))
        if not isinstance(url, str) or not url.strip():
            raise ConfigError("Endpoint '{0}' must be a non-empty URL".format(name))
        endpoints[name] = normalize_endpoint(name, url)

    try:
        timeout = float(data.get("timeout", 2.0))
    except (TypeError, ValueError) as exc:
        raise ConfigError("'timeout' must be a number") from exc
    if timeout <= 0:
        raise ConfigError("'timeout' must be greater than zero")

    language = data.get("language", "auto")
    if not isinstance(language, str) or not language.strip():
        raise ConfigError("'language' must be a non-empty string")

    return Config(endpoints=endpoints, timeout=timeout, language=language.strip())


def load_config(path: Optional[str] = None) -> Config:
    if path is None:
        return Config()

    config_path = Path(path)
    try:
        text = config_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ConfigError("Could not read config '{0}': {1}".format(path, exc)) from exc

    try:
        if config_path.suffix.lower() == ".json" or text.lstrip().startswith("{"):
            data = json.loads(text)
        else:
            data = _parse_simple_yaml(text)
    except json.JSONDecodeError as exc:
        raise ConfigError("Invalid JSON config: {0}".format(exc)) from exc

    if not isinstance(data, dict):
        raise ConfigError("Configuration root must be a mapping")
    return _validate_config(data)
