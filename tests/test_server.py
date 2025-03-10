import pytest
from flask import url_for
from server import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_successful_booking(client):
    sut =