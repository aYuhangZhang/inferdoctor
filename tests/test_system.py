from unittest.mock import patch

from inferdoctor.checkers.system import SystemChecker
from inferdoctor.core.config import Config
from inferdoctor.core.models import Status


@patch("inferdoctor.checkers.system._available_memory_bytes", return_value=1024)
def test_system_checker_collects_lightweight_information(memory):
    result = SystemChecker().run(Config())

    assert result.status == Status.PASS
    assert result.raw_data["available_memory_bytes"] == 1024
    assert result.raw_data["python_version"]
    assert result.raw_data["architecture"]
    memory.assert_called_once_with()
