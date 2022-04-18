import os
import shutil
import tempfile
from pathlib import Path

import pytest
from typer.testing import CliRunner

import deciphon_cli.data as data
from deciphon_cli.main import app

runner = CliRunner()


def cleansched():
    runner.invoke(app, ["sched", "wipe"])


def cleandir():
    old_cwd = os.getcwd()
    newpath = tempfile.mkdtemp()
    os.chdir(newpath)
    yield
    os.chdir(old_cwd)
    shutil.rmtree(newpath)


@pytest.fixture
def clean():
    cleansched()
    cleandir()
    runner.invoke(app, ["sched", "wipe"])


@pytest.fixture
def minifam_hmm():
    file = data.filepath(data.FileName.minifam_hmm)
    shutil.copy(file, file.name)
    return Path(file.name)


@pytest.fixture
def minifam_db():
    file = data.filepath(data.FileName.minifam_db)
    shutil.copy(file, file.name)
    return Path(file.name)


@pytest.fixture
def pfam1_hmm():
    file = data.filepath(data.FileName.pfam1_hmm)
    shutil.copy(file, file.name)
    return Path(file.name)


@pytest.fixture
def pfam1_db():
    file = data.filepath(data.FileName.pfam1_db)
    shutil.copy(file, file.name)
    return Path(file.name)
