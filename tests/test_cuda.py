import subprocess
from unittest.mock import patch

from inferdoctor.checkers.cuda import CudaChecker
from inferdoctor.core.config import Config
from inferdoctor.core.models import Status


@patch("inferdoctor.checkers.cuda.shutil.which", return_value=None)
@patch.dict("inferdoctor.checkers.cuda.os.environ", {}, clear=True)
def test_cuda_checker_skips_without_nvcc(which):
    result = CudaChecker().run(Config())

    assert result.status == Status.SKIP
    assert result.raw_data["nvcc_path"] is None
    which.assert_called_once_with("nvcc")


@patch("inferdoctor.checkers.cuda.shutil.which", return_value="/usr/local/cuda/bin/nvcc")
@patch("inferdoctor.checkers.cuda.run_command")
def test_cuda_checker_parses_release(run, which):
    run.return_value = subprocess.CompletedProcess(
        args=[],
        returncode=0,
        stdout="Cuda compilation tools, release 12.4, V12.4.99\n",
        stderr="",
    )

    result = CudaChecker().run(Config())

    assert result.status == Status.PASS
    assert result.raw_data["cuda_version"] == "12.4"
    run.assert_called_once()
    which.assert_called_once_with("nvcc")
