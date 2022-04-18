import typer

from deciphon_cli.requests import delete, get_json

__all__ = ["app"]

app = typer.Typer()


@app.command()
def wipe():
    typer.echo(delete(f"/sched/wipe"))


@app.command()
def check_health():
    typer.echo(get_json(f"/sched/check_health"))
