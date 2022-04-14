import typer

from deciphon_cli.requests import get_json

__all__ = ["app"]

app = typer.Typer()


@app.command()
def seq_list():
    typer.echo((get_json(f"/seqs")))
