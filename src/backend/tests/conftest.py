import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Fixture para criar um cliente de teste"""
    with TestClient(app) as c:
        yield c