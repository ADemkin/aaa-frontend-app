from pathlib import Path
from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from lib.app import app as _app
from lib.models import Reader
from lib.models import get_model


@pytest.fixture()
def app() -> FastAPI:
    return _app


@pytest.fixture()
def client(app) -> TestClient:
    with TestClient(app) as client:
        yield client


@pytest.fixture()
def model_mock(app):
    mock = MagicMock(spec=Reader)
    app.dependency_overrides[get_model] = lambda: mock
    yield mock
    app.dependency_overrides.clear()


@pytest.fixture()
def image_file():
    image_path = Path("images/signs.jpg")
    assert image_path.exists()
    with open(image_path, "rb") as file:
        yield file


@pytest.fixture()
def save_artifact():
    def _save_artifact(artifact: str, path: str) -> None:
        base = Path("tests/.artifacts")
        base.mkdir(exist_ok=True)
        (base / path).write_text(artifact)

    return _save_artifact
