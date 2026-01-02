from fastapi.testclient import TestClient

def test_cliente(client):
    assert type(client) == TestClient