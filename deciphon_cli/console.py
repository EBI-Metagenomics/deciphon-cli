import json

import requests
import typer
from decouple import config

run = typer.Typer()

SCHED_API_URL = config("SCHED_API_URL", default="http://127.0.0.1:8000/api")


class Headers:
    recv = {"Accept": "application/json"}
    send = {"Content-Type": "application/json"}
    both = {"Accept": "application/json", "Content-Type": "application/json"}


@run.command()
def db_list():
    r = requests.get(f"{SCHED_API_URL}/dbs", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def job_pend():
    r = requests.get(f"{SCHED_API_URL}/jobs/next_pend", headers=Headers.recv)
    if r.status_code == 500:
        typer.echo("No pending job has been found.")
        return
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def job_add(db_filename: str, fasta_filename: str):
    r = requests.post(f"{SCHED_API_URL}/jobs/", headers=Headers.both, json=json)
    typer.echo(json.dumps(r.json(), indent=2))
