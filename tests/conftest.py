import pytest
from aiohttp.test_utils import TestClient, TestServer

from lib.app import create_app


@pytest.fixture
async def client() -> TestClient:
    app = create_app()
    async with TestServer(app) as server:
        async with TestClient(server) as client:
            yield client
