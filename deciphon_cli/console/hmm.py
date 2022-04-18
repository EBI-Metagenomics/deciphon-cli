import json
from enum import Enum
from pathlib import Path

import typer

from deciphon_cli.core import xxh3
from deciphon_cli.requests import delete, download
from deciphon_cli.requests import get as get_request
from deciphon_cli.requests import get_json, upload

__all__ = ["app"]

app = typer.Typer()


class HMMIDType(str, Enum):
    HMM_ID = "hmm_id"
    XXH3 = "xxh3"
    FILENAME = "filename"
    JOB_ID = "job_id"


@app.command()
def add(hmm_file: Path):
    mime = "application/octet-stream"
    params = {"id_type": HMMIDType.XXH3.value}
    r = get_request(f"/hmms/{xxh3(hmm_file)}", "application/json", params)
    if r.status_code == 200:
        typer.echo("HMM already exists.")
    else:
        typer.echo(upload("/hmms/", "hmm_file", hmm_file, mime))


@app.command()
def dl(hmm_id: int):
    txt = get_json(f"/hmms/{hmm_id}")
    data = json.loads(txt)
    if "rc" in data:
        typer.echo(txt)
    else:
        download(f"/hmms/{hmm_id}/download", data["filename"])


@app.command()
def get(
    id: str = typer.Argument(...),
    id_type: HMMIDType = typer.Option(HMMIDType.HMM_ID.value),
):
    typer.echo(get_json(f"/hmms/{id}", {"id_type": id_type.value}))


@app.command()
def list():
    typer.echo((get_json("/hmms")))


@app.command()
def rm(hmm_id: int):
    typer.echo(delete(f"/hmms/{hmm_id}"))
