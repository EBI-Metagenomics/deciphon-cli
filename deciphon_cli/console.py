import json
from pathlib import Path

import requests
import typer
from decouple import config
from fasta_reader import read_fasta

from deciphon_cli.core import JobPost, SeqPost

run = typer.Typer()

SCHED_API_URL = config("SCHED_API_URL", default="http://127.0.0.1:8000/api")


class Headers:
    recv = {"Accept": "application/json"}
    send = {"Content-Type": "application/json"}
    both = {"Accept": "application/json", "Content-Type": "application/json"}


@run.command()
def hmm_list():
    r = requests.get(f"{SCHED_API_URL}/hmms", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def hmm_rm(hmm_id: int):
    r = requests.delete(f"{SCHED_API_URL}/hmms/{hmm_id}", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def hmm_add(hmm_file: Path):
    r = requests.post(
        f"{SCHED_API_URL}/hmms/",
        headers=Headers.recv,
        files={
            "hmm_file": (
                hmm_file.name,
                open(hmm_file, "rb"),
                "application/octet-stream",
            )
        },
    )
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def hmm_get(hmm_id: int = typer.Argument(...)):
    r = requests.get(f"{SCHED_API_URL}/hmms/{hmm_id}", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def db_get(
    db_id: int = typer.Argument(...),
):
    r = requests.get(f"{SCHED_API_URL}/dbs/{db_id}", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def db_list():
    r = requests.get(f"{SCHED_API_URL}/dbs", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def db_rm(db_id: int):
    r = requests.delete(f"{SCHED_API_URL}/dbs/{db_id}", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def job_pend():
    r = requests.get(f"{SCHED_API_URL}/jobs/next_pend", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def job_list():
    r = requests.get(f"{SCHED_API_URL}/jobs", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def job_get(job_id: int = typer.Argument(...)):
    r = requests.get(f"{SCHED_API_URL}/jobs/{job_id}", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def job_prods(job_id: int = typer.Argument(...)):
    r = requests.get(f"{SCHED_API_URL}/jobs/{job_id}/prods", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def job_prods_gff(job_id: int = typer.Argument(...)):
    headers = {"Accept": "text/plain"}
    r = requests.get(f"{SCHED_API_URL}/jobs/{job_id}/prods/gff", headers=headers)
    typer.echo(r.text)


@run.command()
def job_add(
    db_id: int = typer.Argument(...),
    fasta_filepath: str = typer.Argument(...),
    multi_hits: bool = typer.Argument(True),
    hmmer3_compat: bool = typer.Argument(False),
):
    job = JobPost(db_id=db_id, multi_hits=multi_hits, hmmer3_compat=hmmer3_compat)
    with read_fasta(fasta_filepath) as f:
        for item in f:
            seq = SeqPost(name=item.id, data=item.sequence)
            job.seqs.append(seq)

    r = requests.post(f"{SCHED_API_URL}/jobs/", headers=Headers.both, json=job.dict())
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def job_rm(job_id: int):
    r = requests.delete(f"{SCHED_API_URL}/jobs/{job_id}", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def scan_list():
    r = requests.get(f"{SCHED_API_URL}/scans", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def prod_list():
    r = requests.get(f"{SCHED_API_URL}/prods", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def seq_list():
    r = requests.get(f"{SCHED_API_URL}/seqs", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def check_health():
    r = requests.get(f"{SCHED_API_URL}/sched/check_health", headers=Headers.recv)
    typer.echo(r.text)
