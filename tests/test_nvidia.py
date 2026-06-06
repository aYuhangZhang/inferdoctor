import subprocess
from unittest.mock import patch

from inferdoctor.checkers.nvidia import NvidiaChecker
from inferdoctor.core.config import Config
from inferdoctor.core.models import Status


@patch("inferdoctor.checkers.nvidia.shutil.which", return_value=None)
def test_nvidia_checker_skips_without_nvidia_smi(which):
    result = NvidiaChecker().run(Config())

    assert result.status == Status.SKIP
    assert result.raw_data["nvidia_smi_path"] is None
    which.assert_called_once_with("nvidia-smi")


@patch("inferdoctor.checkers.nvidia.shutil.which", return_value="/usr/bin/nvidia-smi")
@patch("inferdoctor.checkers.nvidia.run_command")
def test_nvidia_checker_parses_gpu_rows(run, which):
    run.return_value = subprocess.CompletedProcess(
        args=[],
        returncode=0,
        stdout="NVIDIA RTX 4090, 24564, 550.54.14\n",
        stderr="",
    )

    result = NvidiaChecker().run(Config())

    assert result.status == Status.PASS
    assert result.raw_data["gpus"][0] == {
        "name": "NVIDIA RTX 4090",
        "memory_total_mib": 24564,
        "driver_version": "550.54.14",
    }
    run.assert_called_once()
    which.assert_called_once_with("nvidia-smi")
