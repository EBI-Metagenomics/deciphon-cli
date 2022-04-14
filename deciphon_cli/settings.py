from functools import lru_cache

from pydantic import BaseSettings

from deciphon_cli import __version__

__all__ = ["settings"]


class Settings(BaseSettings):
    api_host: str = "127.0.0.1"
    api_port: int = 49329
    api_prefix: str = ""
    api_key: str = "change-me"
    verbose: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        validate_assignment = True

    @property
    def api_url(self):
        return f"http://{self.api_host}:{self.api_port}{self.api_prefix}"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
