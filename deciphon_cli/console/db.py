from enum import Enum

import typer

from deciphon_cli.requests import delete, get_json

__all__ = ["app"]

app = typer.Typer()


class DBIDType(str, Enum):
    DB_ID = "db_id"
    XXH3 = "xxh3"
    FILENAME = "filename"
    HMM_ID = "hmm_id"


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
