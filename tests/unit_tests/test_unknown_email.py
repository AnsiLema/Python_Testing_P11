import pytest
from server import app


def test_showSummary_valid_email(client):
    response = client.post('/showSummary', data={"email": "valid@email.com"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome" in response.data

def test_showSummary_missing_email(client):
    response = client.post('/showSummary', data={"email": ""}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Sorry, that email is missing." in response.data

def test_showSummary_unregistered_email(client):
    response = client.post('/showSummary', data={"email": "notvalid@mail.com"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Sorry, this email is not registered." in response.data
