import importlib.resources
from enum import Enum
from pathlib import Path

import pooch

import deciphon_cli.resources
from deciphon_cli import __name__, __version__

__all__ = ["FileName", "filepath", "env_example_content"]

GOODBOY = pooch.create(
    path=pooch.os_cache(__name__),
    base_url="https://uk1s3.embassy.ebi.ac.uk/deciphon/",
    version=__version__,
    version_dev="main",
    registry={
        "minifam.hmm.bz2": "md5:6e102264a59e7bf538ce08b9ad2b46d8",
        "minifam.dcp.bz2": "md5:e460d18f3802c1f2a3b2c05246ab4199",
        "pfam1.hmm.bz2": "md5:e6e335b8798c7e0aec8c6c99e1709bf7",
        "pfam1.dcp.bz2": "md5:e6e335b8798c7e0aec8c6c99e1709bf7",
    },
)


class FileName(Enum):
    minifam_hmm = "minifam.hmm"
    minifam_db = "minifam.dcp"
    pfam1_hmm = "pfam1.hmm"
    pfam1_db = "pfam1.dcp"


def filepath(file_name: FileName) -> Path:
    name = f"{file_name.value}.bz2"
    fp = GOODBOY.fetch(name, processor=pooch.Decompress("bzip2", file_name.value))
    return Path(fp)


# def prods_file_content() -> str:
#     return importlib.resources.read_text(deciphon_cli.resources, "prods_file.tsv")


def env_example_content() -> str:
    return importlib.resources.read_text(deciphon_cli.resources, ".env.example")
