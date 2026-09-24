import pytest
from fastapi.testclient import TestClient

from app.container import reset_state
from app.main import app


@pytest.fixture(autouse=True)
def _reset_state():
    reset_state()
    yield


@pytest.fixture
def client():
    return TestClient(app)
