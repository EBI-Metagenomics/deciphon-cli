import typer

from deciphon_cli.console import db, hmm, job, prod, scan, sched, seq
from deciphon_cli.settings import settings

__all__ = ["app"]

app = typer.Typer()
app.add_typer(db.app, name="db")
app.add_typer(hmm.app, name="hmm")
app.add_typer(job.app, name="job")
app.add_typer(prod.app, name="prod")
app.add_typer(scan.app, name="scan")
app.add_typer(sched.app, name="sched")
app.add_typer(seq.app, name="seq")


@app.callback()
def main(verbose: bool = False):
    settings.verbose = verbose
