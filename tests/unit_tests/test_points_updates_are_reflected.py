import pytest
from server import url_for


@pytest.fixture
def mock_data():
    return {
        "clubs": [
            {
                "name": "Test Club",
                "points": 10
            }
        ],
        "competitions": [
            {
                "name": "Future Competition",
                "date": "2025-12-31 13:30:00",
                "numberOfPlaces": "25"
            }
        ]
    }

def test_valid_purchase(client, mock_data, monkeypatch):
    """
    Test the functionality of purchasing places for a valid competition and club. This test
    verifies that the points of the club are correctly deducted, the number of competition
    places is updated, and the server responds with the correct status code.

    :param client: Test client simulating the request to the server.
    :param mock_data: Dictionary containing mock data for testing purposes,
        including club and competition information.
    :param monkeypatch: pytest fixture allowing dynamic modification of attributes during
        test execution.
    :return: None
    """
    monkeypatch.setattr("server.clubs", mock_data["clubs"])
    monkeypatch.setattr("server.competitions", mock_data["competitions"])

    initial_points = int(mock_data["clubs"][0]["points"])
    initial_places = int(mock_data["competitions"][0]["numberOfPlaces"])

    response = client.post("/purchasePlaces", data={
        "competition": "Future Competition",
        "club": "Test Club",
        "places": "3"
    }, follow_redirects=True)

    updated_points = int(mock_data["clubs"][0]["points"])
    updated_places = int(mock_data["competitions"][0]["numberOfPlaces"])

    assert response.status_code == 200
    assert updated_points == initial_points - 3  # Check that the points are reduced correctly
    assert updated_places == initial_places - 3  # Check that the places are updated correctly


def test_not_enough_points(client, mock_data, monkeypatch):
    """
    Test to verify that the system handles cases where a club attempts to purchase
    more places than it has points for. The test mocks server data for clubs
    and competitions to simulate a valid environment. Finally, the response and
    data consistency are asserted to confirm that over-purchasing prevents
    point deduction.

    :param client: Flask test client used to simulate HTTP requests
    :param mock_data: Fixture providing mock data for testing
    :param monkeypatch: Utility to temporarily modify or replace attributes or
        dictionaries during test execution
    :return: None
    """

    monkeypatch.setattr("server.clubs", mock_data["clubs"])
    monkeypatch.setattr("server.competitions", mock_data["competitions"])

    response = client.post("/purchasePlaces", data={
        "competition": "Future Competition",
        "club": "Test Club",
        "places": "20"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert int(mock_data["clubs"][0]["points"]) == 10  # Check that the points have not changed


def test_not_enough_places(client, mock_data, monkeypatch):
    """
    Tests the functionality where the number of places requested exceeds the available
    places in a competition. This ensures that the system does not allow overbooking
    and keeps the state of competition places unchanged.

    :param client: Flask testing client used to simulate requests to the application.
    :type client: flask.testing.FlaskClient
    :param mock_data: Mock data containing sample clubs and competitions for the test.
    :type mock_data: dict
    :param monkeypatch: Pytest fixture to mock attributes or methods during tests.
    :type monkeypatch: pytest.MonkeyPatch
    :return: None
    """

    monkeypatch.setattr("server.clubs", mock_data["clubs"])
    monkeypatch.setattr("server.competitions", mock_data["competitions"])

    response = client.post("/purchasePlaces", data={
        "competition": "Future Competition",
        "club": "Test Club",
        "places": "30"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Not enough places available." in response.data
    assert int(mock_data["competitions"][0]["numberOfPlaces"]) == 25 # Check that the  number of places has not changed


def test_nonexistent_club(client, mock_data, monkeypatch):
    """
    Tests the behavior when attempting to purchase places using a club that does not
    exist in the system. Simulates the scenario where a client tries to make a
    purchase with invalid club information, and verifies that the server redirects
    to the expected location.

    :param client: An instance of the test client used to simulate HTTP requests
        to the server.
    :param mock_data: A dictionary containing mock data for clubs and competitions
        used to patch the server's data during testing.
    :param monkeypatch: A pytest fixture used to dynamically modify the behavior
        of the server functions or objects by patching attributes.
    :return: Asserts that the response status code is 302 and ensures that the
        server redirects the client to the index page.
    """
    monkeypatch.setattr("server.clubs", mock_data["clubs"])
    monkeypatch.setattr("server.competitions", mock_data["competitions"])

    response = client.post("/purchasePlaces", data={
        "competition": "Future Competition",
        "club": "Fake Club",
        "places": "5"
    })

    assert response.status_code == 302
    assert response.headers["Location"] == url_for("index", _external=False)


def test_nonexistent_competition(client, mock_data, monkeypatch):
    """
    Tests the behavior when attempting to purchase places for a nonexistent competition.

    The function verifies that the application properly handles cases where a club
    attempts to buy places in a competition that does not exist in the system. It
    ensures that the server redirects to the main index page without crashing or
    exposing any vulnerabilities.

    :param client: A flask testing client to simulate requests to the server.
    :param mock_data: A dictionary containing mock data for clubs and competitions.
    :param monkeypatch: A pytest fixture that allows modifying and controlling
        the behavior of objects or functions during testing.
    :return: None
    """

    monkeypatch.setattr("server.clubs", mock_data["clubs"])
    monkeypatch.setattr("server.competitions", mock_data["competitions"])

    response = client.post("/purchasePlaces", data={
        "competition": "Fake Competition",
        "club": "Test Club",
        "places": "5"
    })

    assert response.status_code == 302
    assert response.headers["Location"] == url_for("index", _external=False)


