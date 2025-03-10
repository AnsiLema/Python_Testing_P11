import pytest
from server import app, clubs, competitions
from flask import url_for

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_purchase_valid_places(client):
    # Configuration initiale
    test_club = {"name": "Test Club", "points": 10}
    test_competition = {"name": "Test Competition", "numberOfPlaces": "20"}
    clubs.append(test_club)
    competitions.append(test_competition)

    # Test d'achat de places
    response = client.post('/purchasePlaces', data={
        "club": "Test Club",
        "competition": "Test Competition",
        "places": "5"
    })

    # Vérifications
    assert response.status_code == 200
    assert int(test_competition["numberOfPlaces"]) == 15

def test_purchase_too_many_places(client):
    # Configuration initiale
    test_club = {"name": "Poor Club", "points": 3}
    test_competition = {"name": "Expensive Competition", "numberOfPlaces": "20"}
    clubs.append(test_club)
    competitions.append(test_competition)

    # Places purchase test
    response = client.post('/purchasePlaces', data={
        "club": "Poor Club",
        "competition": "Expensive Competition",
        "places": "5"
    })

    # Verifications
    assert response.status_code == 302  # Redirection
    assert int(test_competition["numberOfPlaces"]) == 20

def test_points_deduction(client):
    # Initial set up
    test_club = {"name": "Points Club", "points": "10"}
    test_competition = {"name": "Points Competition", "numberOfPlaces": "20"}
    clubs.append(test_club)
    competitions.append(test_competition)

    # Places purchase test
    initial_points = int(test_club["points"])
    response = client.post("/purchasePlaces", data={
        "club": "Points Club",
        "competition": "Points Competition",
        "places": "3"
    })

    assert response.status_code == 200
    assert int(test_club["points"]) < initial_points  # Points should be deducted