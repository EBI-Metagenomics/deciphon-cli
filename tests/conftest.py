import os
import shutil
import tempfile
from pathlib import Path

import pytest

import deciphon_cli.data as data


@pytest.fixture
def cleandir():
    old_cwd = os.getcwd()
    newpath = tempfile.mkdtemp()
    os.chdir(newpath)
    yield
    os.chdir(old_cwd)
    shutil.rmtree(newpath)


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
