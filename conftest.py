import os
from dotenv import load_dotenv
import pytest
from api.disk_client import DiskClient


load_dotenv()
TOKEN_ENV = "YANDEX_DISK_TOKEN"


@pytest.fixture(scope="session")
def disk() -> DiskClient:
    token = os.getenv(TOKEN_ENV)
    if not token:
        pytest.skip(f"Не задан OAuth-токен тестового аккаунта: export {TOKEN_ENV}=<token>")
    return DiskClient(token)
