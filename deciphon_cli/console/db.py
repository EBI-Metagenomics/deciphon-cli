import typer

from deciphon_cli.requests import delete, get_json

__all__ = ["app"]

app = typer.Typer()


@app.command()
def get(
    db_id: int = typer.Argument(...),
):
    typer.echo((get_json(f"/dbs/{db_id}")))


@app.command()
def list():
    typer.echo((get_json(f"/dbs")))


@app.command()
def rm(db_id: int):
    typer.echo((delete(f"/dbs/{db_id}").json()))
