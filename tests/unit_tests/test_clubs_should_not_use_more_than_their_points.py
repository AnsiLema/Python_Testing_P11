import pytest
from server import app, clubs, competitions


def test_purchase_valid_places(client):
    """
    Tests the valid purchase of places for a given competition by a club. It ensures
    that the number of places in the competition is updated correctly after the
    purchase and that the response status code is appropriate.

    :param client: Test client instance used to simulate requests in the test
    :return: None
    """
    test_club = {"name": "Test Club", "points": 10}
    test_competition = {"name": "Test Competition", "numberOfPlaces": "20"}
    clubs.append(test_club)
    competitions.append(test_competition)

    response = client.post('/purchasePlaces', data={
        "club": "Test Club",
        "competition": "Test Competition",
        "places": "5"
    })

    assert response.status_code == 200
    assert int(test_competition["numberOfPlaces"]) == 15

def test_purchase_too_many_places(client):
    """
    Tests the behavior of the application when a club tries to purchase
    more places than its available points allow. Ensures that the number
    of places for the competition remains unchanged and the application
    responds with the correct status code.

    :param client: The test client facilitating requests to the application.
    :type client: flask.testing.FlaskClient
    :return: None
    """
    test_club = {"name": "Poor Club", "points": 3}
    test_competition = {"name": "Expensive Competition", "numberOfPlaces": "20"}
    clubs.append(test_club)
    competitions.append(test_competition)

    response = client.post('/purchasePlaces', data={
        "club": "Poor Club",
        "competition": "Expensive Competition",
        "places": "5"
    })

    assert response.status_code == 302
    assert int(test_competition["numberOfPlaces"]) == 20

def test_points_deduction(client):
    """
    Tests that points are correctly deducted from a club's account after a purchase is made
    by calling the purchasePlaces endpoint. The function ensures that the club's points are
    deducted accurately when places are purchased.

    :param client: Test client used to simulate requests to the application.
    :type client: FlaskClient
    :return: None
    """
    test_club = {"name": "Points Club", "points": "10"}
    test_competition = {"name": "Points Competition", "numberOfPlaces": "20"}
    clubs.append(test_club)
    competitions.append(test_competition)

    initial_points = int(test_club["points"])
    response = client.post("/purchasePlaces", data={
        "club": "Points Club",
        "competition": "Points Competition",
        "places": "3"
    })

    assert response.status_code == 200
    assert int(test_club["points"]) < initial_points  # Points should be deducted