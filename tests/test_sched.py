import pytest
from typer.testing import CliRunner

from deciphon_cli.main import app

runner = CliRunner()


@pytest.mark.usefixtures("clean")
def test_sched_check_health():
    result = runner.invoke(app, ["sched", "check-health"])
    assert result.exit_code == 0
