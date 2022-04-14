from typing import NoReturn

import typer
from requests.exceptions import ConnectionError

from deciphon_cli.settings import settings

__all__ = ["handle_connection_error"]


def handle_connection_error(
    conn_error: ConnectionError,
) -> NoReturn:
    if settings.verbose:
        typer.echo(conn_error)
    else:
        typer.echo(f"Failed to connect to {settings.api_url}.")
    raise typer.Exit(1)
