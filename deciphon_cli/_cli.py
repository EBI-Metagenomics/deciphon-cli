import json
from enum import Enum

import requests
import typer

__all__ = ["cli"]


cli = typer.Typer()

url = "http://127.0.0.1:8000"
headers = {"accept": "application/json"}


@cli.command()
def db_list():
    r = requests.get(f"{url}/dbs", headers=headers)
    typer.echo(json.dumps(r.json(), indent=2))


@cli.command()
def job_pend():
    r = requests.get(f"{url}/jobs/next_pend", headers=headers)
    if r.status_code == 500:
        typer.echo("No pending job has been found.")
        return
    typer.echo(json.dumps(r.json(), indent=2))


@cli.command()
def job_add(db_filename: str, fasta_filename: str):
    r = requests.post(f"{url}/jobs/", headers=headers, json=json)
    typer.echo(json.dumps(r.json(), indent=2))
