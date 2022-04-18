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


@app.command()
def list():
    typer.echo((get_json("/hmms")))


@app.command()
def rm(hmm_id: int):
    typer.echo(delete(f"/hmms/{hmm_id}"))


@app.command()
def add(hmm_file: Path):
    mime = "application/octet-stream"
    r = get_request(f"/hmms/by-xxh3/{xxh3(hmm_file)}", "application/json")
    if r.status_code == 200:
        typer.echo("HMM already exists.")
    else:
        typer.echo(upload("/hmms/", "hmm_file", hmm_file, mime))


class GetBy(str, Enum):
    ID = "id"
    JOB_ID = "job_id"
    XXH3 = "xxh3"
    FILENAME = "filename"


@app.command()
def get(hmm_id: str = typer.Argument(...), by: GetBy = typer.Option(GetBy.ID)):
    if by == GetBy.ID:
        typer.echo(get_json(f"/hmms/{hmm_id}"))
    elif by == GetBy.JOB_ID:
        typer.echo(get_json(f"/hmms/by-job-id/{hmm_id}"))
    elif by == GetBy.XXH3:
        typer.echo(get_json(f"/hmms/by-xxh3/{hmm_id}"))
    elif by == GetBy.FILENAME:
        typer.echo(get_json(f"/hmms/by-filename/{hmm_id}"))


@app.command()
def dl(hmm_id: int):
    txt = get_json(f"/hmms/{hmm_id}")
    data = json.loads(txt)
    if "rc" in data:
        typer.echo(txt)
    else:
        download(f"/hmms/{hmm_id}/download", data["filename"])
