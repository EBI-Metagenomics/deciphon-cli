import typer

import deciphon_cli.data as data

__all__ = ["app"]

app = typer.Typer()


@app.command()
def default():
    typer.echo(data.env_example_content(), nl=False)
