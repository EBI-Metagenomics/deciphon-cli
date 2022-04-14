import json
from pathlib import Path

import requests
import typer
from decouple import config
from fasta_reader import read_fasta

from deciphon_cli.core import ScanPost, SeqPost

run = typer.Typer()

API_HOST = config("host", default="127.0.0.1")
API_PORT = config("port", default=49329)
API_PREFIX = config("api_prefix", default="")
API_KEY = config("api_key", default="change-me")

API_URL = f"http://{API_HOST}:{API_PORT}{API_PREFIX}"


class Headers:
    recv = {"Accept": "application/json", "X-API-KEY": API_KEY}
    send = {"Content-Type": "application/json", "X-API-KEY": API_KEY}
    both = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-API-KEY": API_KEY,
    }


@run.command()
def hmm_list():
    r = requests.get(f"{API_URL}/hmms", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def hmm_rm(hmm_id: int):
    r = requests.delete(f"{API_URL}/hmms/{hmm_id}", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def hmm_add(hmm_file: Path):
    r = requests.post(
        f"{API_URL}/hmms/",
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
    r = requests.get(f"{API_URL}/hmms/{hmm_id}", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def db_get(
    db_id: int = typer.Argument(...),
):
    r = requests.get(f"{API_URL}/dbs/{db_id}", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def db_list():
    r = requests.get(f"{API_URL}/dbs", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def db_rm(db_id: int):
    r = requests.delete(f"{API_URL}/dbs/{db_id}", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def job_pend():
    r = requests.get(f"{API_URL}/jobs/next_pend", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def job_list():
    r = requests.get(f"{API_URL}/jobs", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def job_get(job_id: int = typer.Argument(...)):
    r = requests.get(f"{API_URL}/jobs/{job_id}", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def job_prod(job_id: int = typer.Argument(...)):
    r = requests.get(f"{API_URL}/jobs/{job_id}/prods", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def job_rm(job_id: int):
    r = requests.delete(f"{API_URL}/jobs/{job_id}", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def scan_add(
    db_id: int = typer.Argument(...),
    fasta_filepath: str = typer.Argument(...),
    multi_hits: bool = typer.Argument(True),
    hmmer3_compat: bool = typer.Argument(False),
):
    scan = ScanPost(db_id=db_id, multi_hits=multi_hits, hmmer3_compat=hmmer3_compat)
    with read_fasta(fasta_filepath) as f:
        for item in f:
            seq = SeqPost(name=item.id, data=item.sequence)
            scan.seqs.append(seq)

    r = requests.post(f"{API_URL}/scans/", headers=Headers.both, json=scan.dict())
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def scan_get(scan_id: int = typer.Argument(...)):
    r = requests.get(f"{API_URL}/scans/{scan_id}", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def scan_seq_list(scan_id: int = typer.Argument(...)):
    r = requests.get(f"{API_URL}/scans/{scan_id}/seqs", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def scan_list():
    r = requests.get(f"{API_URL}/scans", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def scan_prod_list(scan_id: int = typer.Argument(...)):
    r = requests.get(f"{API_URL}/scans/{scan_id}/prods", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def scan_prod_gff(scan_id: int = typer.Argument(...)):
    headers = {"Accept": "text/plain"}
    r = requests.get(f"{API_URL}/scans/{scan_id}/prods/gff", headers=headers)
    typer.echo(r.text, nl=False)


@run.command()
def scan_prod_path(scan_id: int = typer.Argument(...)):
    headers = {"Accept": "text/plain"}
    r = requests.get(f"{API_URL}/scans/{scan_id}/prods/path", headers=headers)
    typer.echo(r.text, nl=False)


@run.command()
def scan_prod_fragment(scan_id: int = typer.Argument(...)):
    headers = {"Accept": "text/plain"}
    r = requests.get(f"{API_URL}/scans/{scan_id}/prods/fragment", headers=headers)
    typer.echo(r.text, nl=False)


@run.command()
def scan_prod_amino(scan_id: int = typer.Argument(...)):
    headers = {"Accept": "text/plain"}
    r = requests.get(f"{API_URL}/scans/{scan_id}/prods/amino", headers=headers)
    typer.echo(r.text, nl=False)


@run.command()
def scan_prod_codon(scan_id: int = typer.Argument(...)):
    headers = {"Accept": "text/plain"}
    r = requests.get(f"{API_URL}/scans/{scan_id}/prods/codon", headers=headers)
    typer.echo(r.text, nl=False)


@run.command()
def prod_list():
    r = requests.get(f"{API_URL}/prods", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def seq_list():
    r = requests.get(f"{API_URL}/seqs", headers=Headers.recv)
    typer.echo(json.dumps(r.json(), indent=2))


@run.command()
def sched_wipe():
    r = requests.delete(f"{API_URL}/sched/wipe", headers=Headers.recv)
    typer.echo(r.text)


@run.command()
def sched_check_health():
    r = requests.get(f"{API_URL}/sched/check_health", headers=Headers.recv)
    typer.echo(r.text)
