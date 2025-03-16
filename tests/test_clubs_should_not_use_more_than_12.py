import pytest
from server import app


@pytest.fixture
def mock_clubs():
    """
    Fixture that provides mock data representing a collection of club dictionaries. Each
    club dictionary contains information such as the club name, email address, and the
    current number of points. This is used in tests to simulate actual club data without
    relying on real-world data, ensuring consistent, isolated, and repeatable test
    environments.

    :return: A dictionary containing a list of mock club data.
    """
    return {
        "clubs": [
            {
            "name": "Test Club",
            "email": "test@mail.com",
            "points": "13"
            },
            {
            "name": "Test Club 2",
            "email": "test2@mail.com",
            "points": "4"
            }
        ]
    }

@pytest.fixture
def mock_competition():
    """
    Creates and returns a mock data structure representing sample competition
    information. Designed to be used as a pytest fixture for testing purposes.

    :rtype: dict
    :return: A dictionary containing mock competition data with one or more
        competition entries. Each entry includes the competition's name and the
        number of available places in the competition.
    """
    return {
        "competitions": [
            {
                "name": "Test Competition",
                "numberOfPlaces": "25"
            }
        ]
    }


@pytest.fixture
def client(mocker, mock_clubs, mock_competition):
    """
    Fixture that creates a test client for the Flask application with mocked dependencies.
    The function utilizes the `mocker` library to replace the calls to `server.loadClubs`
    and `server.loadCompetitions` with mocked versions. It also patches the application
    state to utilize the provided mock data for clubs and competitions. Configures the
    application to be in testing mode.

    :param mocker: The pytest-mock fixture used to mock object dependencies.
    :type mocker: pytest_mock.MockerFixture
    :param mock_clubs: Dictionary containing mock data for clubs.
    :type mock_clubs: dict
    :param mock_competition: Dictionary containing mock data for competitions.
    :type mock_competition: dict
    :return: Yields a test client for the application configured with mocked dependencies.
    :rtype: flask.testing.FlaskClient
    """
    mocker.patch('server.loadClubs', return_value=mock_clubs['clubs'])
    mocker.patch('server.loadCompetitions', return_value=mock_competition['competitions'])
    mocker.patch('server.competitions', mock_competition['competitions'])
    mocker.patch('server.clubs', mock_clubs['clubs'])
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_purchase_places_with_valid_number(client):
    """
    Tests the purchase places functionality with a valid number of places to ensure that the
    process completes successfully and returns the expected response. This verifies the
    correct behavior of the system when valid input is provided.
    Valid number =< 12
    """
    response = client.post('/purchasePlaces', data={
        'competition': 'Test Competition',
        'club': 'Test Club',
        'places': '5'
    })
    assert b'Great! - Booking complete!' in response.data


def test_purchase_place_above_limitation(client):
    """
    Tests if the purchase endpoint prevents booking more than the allowed number
    of places for a competition. This ensures that a club cannot book more than
    12 places, maintaining fairness and compliance with booking rules.
    """
    response = client.post('/purchasePlaces', data={
        'competition': 'Test Competition',
        'club': 'Test Club',
        'places': '13'
    }, follow_redirects=True)
    assert b'Error: You cannot book more than 12 places per competition' in response.data


def test_purchase_places_non_numeric_value(client):
    """
    Tests the behavior of the `/purchasePlaces` endpoint when a non-numeric value
    is provided for the `places` field.
    This test verifies that a `ValueError` is raised when an invalid non-numeric
    input is sent as the number of places to purchase.
    """
    with pytest.raises(ValueError):
        client.post('/purchasePlaces', data={
            'competition': 'Test Competition',
            'club': 'Test Club',
            'places': 'abc'
        })


def test_purchase_places_with_negative_value(client):
    """
    Tests the behavior of the purchasePlaces endpoint when a negative
    value for 'places' is submitted. Ensures that the system properly
    handles invalid input and verifies that a `ValueError` is raised
    under such circumstances.
    """
    with pytest.raises(ValueError):
        client.post('/purchasePlaces', data={
            'competition': 'Test Competition',
            'club': 'Test Club',
            'places': '-5'
        }, follow_redirects=True)
