import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Сам тест
def test_hello_world(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Hello, Docker!" in response.data