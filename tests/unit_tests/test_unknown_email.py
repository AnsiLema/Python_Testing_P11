import pytest
from flask import render_template
from server import app


def test_showSummary_valid_email(client, mock_data, monkeypatch):
    """
    Tests the functionality of the /showSummary endpoint with a valid email.

    This test verifies that when a request is made to the /showSummary endpoint with
    a valid email address, the server responds with an HTTP 200 status code and
    renders the correct page content, which includes a welcome message and a list of
    competitions.

    Monkeypatching is used to replace the clubs and competitions datasets with the
    provided mock data to ensure predictable and isolated testing conditions.

    :param client: Flask testing client for simulating HTTP requests.
    :param mock_data: Dictionary containing mock data for 'clubs' and 'competitions'.
    :param monkeypatch: pytest's monkeypatch object for altering attributes or methods.
    :return: None
    """

    monkeypatch.setattr("server.clubs", mock_data["clubs"])
    monkeypatch.setattr("server.competitions", mock_data["competitions"])

    response = client.post('/showSummary', data={"email": "valid@email.com"}, follow_redirects=True)

    assert response.status_code == 200
    assert b"Welcome" in response.data
    assert b"<h3>Competitions:</h3>" in response.data

def test_showSummary_missing_email(client):
    """
    Tests the behavior of the '/showSummary' route when a missing email is provided.
    It ensures the application responds appropriately when an empty email is submitted,
    returning a 200 HTTP status code and displaying an appropriate error message.

    :param client: Test client for simulating HTTP requests.
    :type client: flask.testing.FlaskClient
    :return: None
    """
    response = client.post('/showSummary', data={"email": ""}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Sorry, that email is missing." in response.data

def test_showSummary_unregistered_email(client):
    """
    Tests the /showSummary route's behavior when an unregistered email is provided.

    This function tests that when a POST request is made to the /showSummary endpoint
    using an email that is not registered, the server responds with an appropriate
    error message and status code.

    :param client: The test client used to simulate HTTP requests to the application.
    :type client: flask.testing.FlaskClient
    :return: None
    """
    response = client.post('/showSummary', data={"email": "notvalid@mail.com"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Sorry, this email is not registered." in response.data
