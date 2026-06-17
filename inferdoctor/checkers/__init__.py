"""Built-in InferDoctor checkers."""

from inferdoctor.checkers.cuda import CudaChecker
from inferdoctor.checkers.dify import DifyChecker
from inferdoctor.checkers.llamacpp import LlamaCppChecker
from inferdoctor.checkers.lmstudio import LMStudioChecker
from inferdoctor.checkers.docker import DockerChecker
from inferdoctor.checkers.nvidia import NvidiaChecker
from inferdoctor.checkers.ollama import OllamaChecker
from inferdoctor.checkers.openwebui import OpenWebUIChecker
from inferdoctor.checkers.sglang import SGLangChecker
from inferdoctor.checkers.system import SystemChecker
from inferdoctor.checkers.vllm import VLLMChecker
from inferdoctor.checkers.xinference import XinferenceChecker
from inferdoctor.core.registry import CheckerRegistry


def default_registry() -> CheckerRegistry:
    return CheckerRegistry(
        [
            SystemChecker(),
            NvidiaChecker(),
            CudaChecker(),
            OllamaChecker(),
            VLLMChecker(),
            SGLangChecker(),
            LlamaCppChecker(),
            LMStudioChecker(),
            XinferenceChecker(),
            DifyChecker(),
            OpenWebUIChecker(),
            DockerChecker(),
        ]
    )


__all__ = ["default_registry"]
