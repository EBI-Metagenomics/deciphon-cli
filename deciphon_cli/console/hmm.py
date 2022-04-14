import json
from pathlib import Path

import typer

from deciphon_cli.requests import delete, download, get_json, upload

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
    typer.echo(upload("/hmms/", "hmm_file", hmm_file, mime))


@app.command()
def get(hmm_id: int = typer.Argument(...)):
    typer.echo(get_json(f"/hmms/{hmm_id}"))


@app.command()
def dl(hmm_id: int):
    txt = get_json(f"/hmms/{hmm_id}")
    data = json.loads(txt)
    if "rc" in data:
        typer.echo(txt)
    else:
        download(f"/hmms/{hmm_id}/download", data["filename"])
