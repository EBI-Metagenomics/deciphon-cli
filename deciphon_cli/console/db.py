from enum import Enum
from pathlib import Path

import typer

from deciphon_cli.core import xxh3
from deciphon_cli.requests import delete
from deciphon_cli.requests import get as get_request
from deciphon_cli.requests import get_json, upload

__all__ = ["app"]

app = typer.Typer()


class DBIDType(str, Enum):
    DB_ID = "db_id"
    XXH3 = "xxh3"
    FILENAME = "filename"
    HMM_ID = "hmm_id"


@app.command()
def add(db_file: Path):
    mime = "application/octet-stream"
    params = {"id_type": DBIDType.XXH3.value}
    r = get_request(f"/dbs/{xxh3(db_file)}", "application/json", params)
    if r.status_code == 200:
        typer.echo("DB already exists.")
        typer.Exit(1)
    else:
        typer.echo(upload("/dbs/", "db_file", db_file, mime))


@app.command()
def get(
    db_id: str = typer.Argument(...),
    id_type: DBIDType = typer.Option(DBIDType.DB_ID.value),
):
    typer.echo((get_json(f"/dbs/{db_id}", {"id_type": id_type.value})))


@app.command()
def list():
    typer.echo((get_json(f"/dbs")))


@app.command()
def rm(db_id: int):
    typer.echo((delete(f"/dbs/{db_id}")))
