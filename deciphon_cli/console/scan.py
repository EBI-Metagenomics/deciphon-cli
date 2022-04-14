import typer
from fasta_reader import read_fasta

from deciphon_cli.core import ScanPost, SeqPost
from deciphon_cli.requests import get_json, get_plain, post

__all__ = ["app"]

app = typer.Typer()


@app.command()
def add(
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

    typer.echo((post(f"/scans/", scan.dict()).json()))


@app.command()
def get(scan_id: int = typer.Argument(...)):
    typer.echo((get_json(f"/scans/{scan_id}")))


@app.command()
def seq_list(scan_id: int = typer.Argument(...)):
    typer.echo((get_json(f"/scans/{scan_id}/seqs")))


@app.command()
def list():
    typer.echo((get_json(f"/scans")))


@app.command()
def prod_list(scan_id: int = typer.Argument(...)):
    typer.echo((get_json(f"/scans/{scan_id}/prods")))


@app.command()
def prod_gff(scan_id: int = typer.Argument(...)):
    typer.echo(get_plain(f"/scans/{scan_id}/prods/gff"), nl=False)


@app.command()
def prod_path(scan_id: int = typer.Argument(...)):
    typer.echo(get_plain(f"/scans/{scan_id}/prods/path"), nl=False)


@app.command()
def prod_fragment(scan_id: int = typer.Argument(...)):
    typer.echo(get_plain(f"/scans/{scan_id}/prods/fragment"), nl=False)


@app.command()
def prod_amino(scan_id: int = typer.Argument(...)):
    typer.echo(get_plain(f"/scans/{scan_id}/prods/amino"), nl=False)


@app.command()
def prod_codon(scan_id: int = typer.Argument(...)):
    typer.echo(get_plain(f"/scans/{scan_id}/prods/codon"), nl=False)
