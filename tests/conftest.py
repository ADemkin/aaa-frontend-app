import pytest

from fastapi import FastAPI
from lib.app import app as _app

from fastapi.testclient import TestClient


@pytest.fixture
def app() -> FastAPI:
    return _app


@pytest.fixture
def client(app) -> TestClient:
    with TestClient(app) as client:
        yield client
