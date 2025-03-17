import pytest
from server import is_competition_past


@pytest.fixture
def mock_data():
    return {
        "clubs": [{"name": "Test Club", "email": "test@club.com", "points": "10"}],
        "competitions": [
            {"name": "Future Competition", "date": "2025-12-31 13:30:00", "numberOfPlaces": "25"},
            {"name": "Past Competition", "date": "2023-01-01 13:30:00", "numberOfPlaces": "30"}
        ]
    }


def test_is_competition_past(mock_data):
    """
    Determine if a competition date has passed.

    This function checks the date of a given competition and determines whether
    it has already passed or not. The decision is based on comparing the
    competition date to the current date.

    :param mock_data: Mocked data containing a list of competitions with their
        respective dates under the 'competitions' key.
    :type mock_data: dict
    :return: None. The function performs assertions to verify the expected
        behavior of the `is_competition_past` logic against the mock data.
    :rtype: None
    """
    assert is_competition_past(mock_data['competitions'][0]) == False
    assert is_competition_past(mock_data['competitions'][1]) == True


def test_book_places_for_a_past_competition(client, mock_data, monkeypatch):
    """
    Test booking places for a past competition to ensure the system prevents bookings
    for competitions that have already concluded. This test modifies the server's data
    to simulate a scenario with a past competition and a valid club.

    :param client: Test client used to simulate HTTP requests in the test environment.
    :type client: flask.testing.FlaskClient
    :param mock_data: A dictionary containing mocked data for clubs and competitions.
    :type mock_data: dict
    :param monkeypatch: Fixture provided by pytest to dynamically modify object attributes
        or replace dependencies during testing.
    :type monkeypatch: pytest.MonkeyPatch
    :return: None
    """
    monkeypatch.setattr('server.clubs', mock_data['clubs'])
    monkeypatch.setattr('server.competitions', mock_data['competitions'])

    response = client.get('/book/Past Competition/Test Club')

    assert response.status_code == 200
    assert b"You cannot book places for a past competition." in response.data


def test_book_places_for_a_future_competition(client, mock_data, monkeypatch):
    """
    Test booking places for a future competition.

    This function tests the functionality of booking places in a future competition and ensures that the correct response
    is returned upon attempting to access the booking page. It verifies both the HTTP status code and the presence of a
    specific substring in the response data, confirming the booking page's expected behavior.

    :param client: Flask testing client used to simulate HTTP requests.
    :param mock_data: Mock data containing dummy information for clubs and competitions.
    :param monkeypatch: Fixture used to dynamically modify attributes or functions during testing.
    :return: None.
    """
    monkeypatch.setattr("server.clubs", mock_data["clubs"])
    monkeypatch.setattr("server.competitions", mock_data["competitions"])

    response = client.get(f'/book/Future Competition/Test Club')

    assert response.status_code == 200
    assert b"Booking for" in response.data


def test_valid_purchase(client, mock_data, monkeypatch):
    """
    Test the functionality of a valid purchase within the application.

    This test ensures that the system correctly processes a valid purchase request
    when provided with proper input data and system state is properly patched. It
    verifies that the response status is successful and contains the expected output
    message.

    :param client: The test client used to simulate HTTP requests.
    :param mock_data: Dictionary containing mock data for clubs and competitions.
    :param monkeypatch: A pytest fixture to override or patch attributes or methods.
    :return: None
    """
    monkeypatch.setattr('server.clubs', mock_data['clubs'])
    monkeypatch.setattr('server.competitions', mock_data['competitions'])

    response = client.post('/purchasePlaces', data={
        'competition': 'Future Competition',
        'club': 'Test Club',
        'places': '5'
    })

    assert response.status_code == 200
    assert b"Great! - Booking complete!" in response.data
