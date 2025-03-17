import pytest
from server import app


def test_showSummary_valid_email(client):
    """
    Tests the '/showSummary' route functionality with a valid email input.

    This test ensures that the application correctly handles a post request to
    '/showSummary' with a valid email. Upon successful processing, it verifies
    that the response has an HTTP status code of 200 and includes the correct
    content in the response body.

    :param client: The test client instance used to simulate HTTP requests
        to the application.
    :return: None
    """
    response = client.post('/showSummary', data={"email": "valid@email.com"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome" in response.data

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
