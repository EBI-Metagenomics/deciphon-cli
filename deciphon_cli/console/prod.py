from pathlib import Path

import typer

from deciphon_cli.requests import get_json, upload

__all__ = ["app"]

app = typer.Typer()


@app.command()
def add(prods_file: Path):
    mime = "text/tab-separated-values"
    typer.echo(upload("/prods/", "prods_file", prods_file, mime))


@app.command()
def list():
    typer.echo(get_json(f"/prods"))
