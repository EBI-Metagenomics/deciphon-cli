from pathlib import Path

import requests
import typer
from requests_toolbelt.multipart import encoder
from requests_toolbelt.multipart.encoder import MultipartEncoderMonitor

from deciphon_cli.headers import Headers

__all__ = ["upload"]


class UploadProgress:
    def __init__(self, total_bytes: int, filename: str):
        self._bar = typer.progressbar(length=total_bytes, label=filename)
        self._bytes_read = 0

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        del exc
        self._bar.finish()

    def __call__(self, monitor: MultipartEncoderMonitor):
        increment = monitor.bytes_read - self._bytes_read
        self._bar.update(increment)
        self._bytes_read += increment


def upload(field_name: str, filepath: Path, mime: str):
    e = encoder.MultipartEncoder(
        fields={
            field_name: (
                filepath.name,
                open(filepath, "rb"),
                mime,
            )
        }
    )
    with UploadProgress(e.len, filepath.name) as up:
        m = encoder.MultipartEncoderMonitor(e, up)
        r = requests.post(
            "http://httpbin.org/post",
            data=m,
            headers={"Content-Type": m.content_type}.update(Headers.recv),
        )
    return r
