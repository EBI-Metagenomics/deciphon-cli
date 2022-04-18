import json

import pytest
from typer.testing import CliRunner

from deciphon_cli.main import app

runner = CliRunner()


@pytest.mark.usefixtures("clean")
def check_health():
    result = runner.invoke(app, ["sched", "check-health"])
    return result.exit_code == 0


online = check_health()
reason = "requires connection to deciphon-api"


@pytest.mark.usefixtures("clean")
@pytest.mark.skipif(not online, reason=reason)
def test_db_add(minifam_hmm, minifam_db):
    result = runner.invoke(app, ["sched", "wipe"])
    assert result.exit_code == 0

    result = runner.invoke(app, ["hmm", "add", minifam_hmm.name])
    assert result.exit_code == 0

    result = runner.invoke(app, ["db", "add", minifam_db.name])
    assert result.exit_code == 0


@pytest.mark.usefixtures("clean")
@pytest.mark.skipif(not online, reason=reason)
def test_db_add_fail(minifam_db):
    result = runner.invoke(app, ["sched", "wipe"])
    assert result.exit_code == 0

    result = runner.invoke(app, ["db", "add", minifam_db.name])
    assert result.exit_code == 0


@pytest.mark.usefixtures("clean")
@pytest.mark.skipif(not online, reason=reason)
def test_hmm_add_get(minifam_hmm):
    result = runner.invoke(app, ["sched", "wipe"])
    assert result.exit_code == 0

    result = runner.invoke(app, ["hmm", "add", minifam_hmm.name])
    assert result.exit_code == 0

    ids = ["1", "-1400478458576472411", minifam_hmm.name, "1"]
    id_types = ["hmm_id", "xxh3", "filename", "job_id"]

    for id, id_type in zip(ids, id_types):
        result = runner.invoke(app, ["hmm", "get", "--id-type", id_type, "--", id])
        assert result.exit_code == 0
        data = json.loads(result.stdout)

        assert data["id"] == 1
        assert data["xxh3"] == -1400478458576472411
        assert data["filename"] == minifam_hmm.name
        assert data["job_id"] == 1


@pytest.mark.usefixtures("clean")
@pytest.mark.skipif(not online, reason=reason)
def test_hmm_add_rm(minifam_hmm):
    result = runner.invoke(app, ["sched", "wipe"])
    assert result.exit_code == 0

    result = runner.invoke(app, ["hmm", "add", minifam_hmm.name])
    assert result.exit_code == 0

    result = runner.invoke(app, ["hmm", "rm", "1"])
    assert result.exit_code == 0


@pytest.mark.usefixtures("clean")
@pytest.mark.skipif(not online, reason=reason)
def test_hmm_list(minifam_hmm, pfam1_hmm):
    result = runner.invoke(app, ["sched", "wipe"])
    assert result.exit_code == 0

    result = runner.invoke(app, ["hmm", "add", minifam_hmm.name])
    assert result.exit_code == 0

    result = runner.invoke(app, ["hmm", "add", pfam1_hmm.name])
    assert result.exit_code == 0

    result = runner.invoke(app, ["hmm", "list"])
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert len(data) == 2

    assert data[0]["id"] == 1
    assert data[0]["xxh3"] == -1400478458576472411
    assert data[0]["filename"] == minifam_hmm.name
    assert data[0]["job_id"] == 1

    assert data[1]["id"] == 2
    assert data[1]["xxh3"] == -1370598402004110900
    assert data[1]["filename"] == pfam1_hmm.name
    assert data[1]["job_id"] == 2
