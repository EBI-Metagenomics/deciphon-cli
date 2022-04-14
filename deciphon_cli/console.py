import json
from pathlib import Path
from typing import Dict, NoReturn

import requests
import typer
from fasta_reader import read_fasta
from requests.exceptions import ConnectionError

from deciphon_cli.core import ScanPost, SeqPost
from deciphon_cli.headers import Headers
from deciphon_cli.settings import settings
from deciphon_cli.upload import upload

run = typer.Typer()
state = {"verbose": False}


def handle_connection_error(
    conn_error: ConnectionError,
) -> NoReturn:
    if state["verbose"]:
        typer.echo(conn_error)
    else:
        typer.echo(f"Failed to connect to {settings.api_url}.")
    raise typer.Exit(1)


def get(endpoint: str, headers: Dict[str, str]) -> requests.Response:
    try:
        return requests.get(f"{settings.api_url}{endpoint}", headers=headers)
    except ConnectionError as conn_error:
        handle_connection_error(conn_error)


def delete(endpoint: str, headers: Dict[str, str]) -> requests.Response:
    try:
        return requests.delete(f"{settings.api_url}{endpoint}", headers=headers)
    except ConnectionError as conn_error:
        handle_connection_error(conn_error)


def post(endpoint: str, headers: Dict[str, str], json) -> requests.Response:
    try:
        return requests.post(
            f"{settings.api_url}{endpoint}", headers=headers, json=json
        )
    except ConnectionError as conn_error:
        handle_connection_error(conn_error)


def pretty_json(v) -> str:
    return json.dumps(v, indent=2)


@run.command()
def hmm_list():
    typer.echo(pretty_json(get("/hmms", Headers.recv).json()))


@run.command()
def hmm_rm(hmm_id: int):
    typer.echo(pretty_json(delete(f"/hmms/{hmm_id}", Headers.recv).json()))


@run.command()
def hmm_add(hmm_file: Path):
    r = upload(f"{settings.api_url}/hmms/", hmm_file, "application/octet-stream")
    # r = requests.post(
    #     f"{settings.api_url}/hmms/",
    #     headers=Headers.recv,
    #     files={
    #         "hmm_file": (
    #             hmm_file.name,
    #             open(hmm_file, "rb"),
    #             "application/octet-stream",
    #         )
    #     },
    # )
    typer.echo(pretty_json(r.json()))


@run.command()
def hmm_get(hmm_id: int = typer.Argument(...)):
    typer.echo(pretty_json(get(f"/hmms/{hmm_id}", Headers.recv).json()))


@run.command()
def db_get(
    db_id: int = typer.Argument(...),
):
    typer.echo(pretty_json(get(f"/dbs/{db_id}", Headers.recv).json()))


@run.command()
def db_list():
    typer.echo(pretty_json(get(f"/dbs", Headers.recv).json()))


@run.command()
def db_rm(db_id: int):
    typer.echo(pretty_json(delete(f"/dbs/{db_id}", Headers.recv).json()))


@run.command()
def job_pend():
    typer.echo(pretty_json(get(f"/jobs/next_pend", Headers.recv).json()))


@run.command()
def job_list():
    typer.echo(pretty_json(get(f"/jobs", Headers.recv).json()))


@run.command()
def job_get(job_id: int = typer.Argument(...)):
    typer.echo(pretty_json(get(f"/jobs/{job_id}", Headers.recv).json()))


@run.command()
def job_prod(job_id: int = typer.Argument(...)):
    typer.echo(pretty_json(get(f"/jobs/{job_id}/prods", Headers.recv).json()))


@run.command()
def job_rm(job_id: int):
    typer.echo(pretty_json(delete(f"/jobs/{job_id}", Headers.recv).json()))


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

    typer.echo(pretty_json(post(f"/scans/", Headers.both, json=scan.dict()).json()))


@run.command()
def scan_get(scan_id: int = typer.Argument(...)):
    typer.echo(pretty_json(get(f"/scans/{scan_id}", Headers.recv).json()))


@run.command()
def scan_seq_list(scan_id: int = typer.Argument(...)):
    r = get(f"/scans/{scan_id}/seqs", Headers.recv)
    typer.echo(pretty_json(r.json()))


@run.command()
def scan_list():
    typer.echo(pretty_json(get(f"/scans", Headers.recv).json()))


@run.command()
def scan_prod_list(scan_id: int = typer.Argument(...)):
    typer.echo(pretty_json(get(f"/scans/{scan_id}/prods", Headers.recv).json()))


@run.command()
def scan_prod_gff(scan_id: int = typer.Argument(...)):
    typer.echo(get(f"/scans/{scan_id}/prods/gff", Headers.plain).text, nl=False)


@run.command()
def scan_prod_path(scan_id: int = typer.Argument(...)):
    typer.echo(get(f"/scans/{scan_id}/prods/path", Headers.plain).text, nl=False)


@run.command()
def scan_prod_fragment(scan_id: int = typer.Argument(...)):
    typer.echo(get(f"/scans/{scan_id}/prods/fragment", Headers.plain).text, nl=False)


@run.command()
def scan_prod_amino(scan_id: int = typer.Argument(...)):
    typer.echo(get(f"/scans/{scan_id}/prods/amino", Headers.plain).text, nl=False)


@run.command()
def scan_prod_codon(scan_id: int = typer.Argument(...)):
    typer.echo(get(f"/scans/{scan_id}/prods/codon", Headers.plain).text, nl=False)


@run.command()
def prod_list():
    typer.echo(pretty_json(get(f"/prods", Headers.recv).json()))


@run.command()
def seq_list():
    typer.echo(pretty_json(get(f"/seqs", Headers.recv).json()))


@run.command()
def sched_wipe():
    typer.echo(delete(f"/sched/wipe", Headers.recv).text)


@run.command()
def sched_check_health():
    typer.echo(json.dumps(get(f"/sched/check_health", Headers.recv).json()))


@run.callback()
def main(verbose: bool = False):
    state["verbose"] = verbose
