import pytest
from typer.testing import CliRunner

from deciphon_cli.main import app

runner = CliRunner()


@pytest.mark.usefixtures("cleandir")
def check_health():
    result = runner.invoke(app, ["sched", "check-health"])
    return result.exit_code == 0


@pytest.mark.usefixtures("cleandir")
@pytest.mark.skipif(check_health(), reason="requires connection to deciphon-api")
def test_hmm_add(minifam_hmm):
    result = runner.invoke(app, ["hmm", "add", minifam_hmm.name])
    assert result.exit_code == 0
