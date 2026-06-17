import subprocess
from unittest.mock import patch

from inferdoctor.checkers.docker import DockerChecker
from inferdoctor.core.config import Config
from inferdoctor.core.models import Status


@patch("inferdoctor.checkers.docker.shutil.which", return_value=None)
def test_docker_checker_skips_without_cli(which):
    result = DockerChecker().run(Config())

    assert result.status == Status.SKIP
    assert result.raw_data["docker_path"] is None
    which.assert_called_once_with("docker")


@patch("inferdoctor.checkers.docker.shutil.which", return_value="/usr/bin/docker")
@patch("inferdoctor.checkers.docker.run_command")
def test_docker_checker_passes_when_daemon_responds(run, which):
    run.return_value = subprocess.CompletedProcess(
        args=[], returncode=0, stdout="27.0.0\n", stderr=""
    )

    result = DockerChecker().run(Config())

    assert result.status == Status.PASS
    assert result.raw_data["daemon_reachable"] is True
    assert result.raw_data["server_version"] == "27.0.0"
    run.assert_called_once_with(["/usr/bin/docker", "info", "--format", "{{.ServerVersion}}"])
    which.assert_called_once_with("docker")


@patch("inferdoctor.checkers.docker.shutil.which", return_value="/usr/bin/docker")
@patch("inferdoctor.checkers.docker.run_command")
def test_docker_checker_warns_when_daemon_is_unreachable(run, which):
    run.return_value = subprocess.CompletedProcess(
        args=[], returncode=1, stdout="", stderr="Cannot connect to Docker daemon"
    )

    result = DockerChecker().run(Config())

    assert result.status == Status.WARN
    assert result.raw_data["daemon_reachable"] is False
    assert "daemon is not reachable" in result.summary
