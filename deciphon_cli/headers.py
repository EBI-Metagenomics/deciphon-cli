from deciphon_cli.settings import settings

__all__ = ["Headers"]


class Headers:
    recv = {"Accept": "application/json", "X-API-KEY": settings.api_key}
    send = {"Content-Type": "application/json", "X-API-KEY": settings.api_key}
    both = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-API-KEY": settings.api_key,
    }
    plain = {"Accept": "text/plain"}
