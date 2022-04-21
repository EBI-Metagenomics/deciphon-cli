import typer

from deciphon_cli.requests import delete, get_json, patch_json

__all__ = ["app"]

app = typer.Typer()


@app.command()
def pend():
    typer.echo(get_json(f"/jobs/next_pend"))


@app.command()
def list():
    typer.echo(get_json(f"/jobs"))


@app.command()
def get(job_id: int = typer.Argument(...)):
    typer.echo(get_json(f"/jobs/{job_id}"))


@app.command()
def rm(job_id: int):
    typer.echo(delete(f"/jobs/{job_id}"))


@app.command()
def set_run(job_id: int = typer.Argument(...)):
    typer.echo(patch_json(f"/jobs/{job_id}/state", {"state": "run"}))


@app.command()
def set_done(job_id: int = typer.Argument(...)):
    typer.echo(patch_json(f"/jobs/{job_id}/state", {"state": "done"}))


@app.command()
def set_fail(job_id: int = typer.Argument(...), error: str = typer.Argument(...)):
    typer.echo(patch_json(f"/jobs/{job_id}/state", {"state": "fail", "error": error}))
