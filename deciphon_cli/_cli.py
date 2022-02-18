import json
from enum import Enum

import requests
import typer

__all__ = ["cli"]


cli = typer.Typer()

url = "http://127.0.0.1:8000"
headers = {"accept": "application/json"}


class DBChoice(str, Enum):
    list = "list"


@cli.command()
def db(command: DBChoice):
    if command == command.list:
        r = requests.get(f"{url}/dbs", headers=headers)
        typer.echo(json.dumps(r.json(), indent=2))


class JOBChoice(str, Enum):
    next_pend = "next_pend"


@cli.command()
def job(command: JOBChoice):
    if command == command.next_pend:
        r = requests.get(f"{url}/jobs/next_pend", headers=headers)
        if r.status_code == 500:
            typer.echo("No pending job has been found.")
            return
        typer.echo(json.dumps(r.json(), indent=2))
