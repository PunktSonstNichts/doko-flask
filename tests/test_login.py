import pytest
from app import login

def test_login(client):
    response = client.post("/login", json={
        "username": "adam",
        "passwort": "1234",
    })
    assert b"<h2>Hello, World!</h2>" in response.data