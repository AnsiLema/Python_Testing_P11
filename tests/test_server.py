import pytest
from flask import url_for
from server import app  # Assure-toi que c'est bien le bon fichier où se trouve ton app Flask

@pytest.fixture
def client():
    """Créer un client de test Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_successful_booking(client):
    """Un club peut acheter un nombre de places inférieur ou égal à ses points"""
    app.config["clubs"] = [{"name": "Test Club", "points": "5"}]
    app.config["competitions"] = [{"name": "Test Competition", "numberOfPlaces": "25"}]

    response = client.post("/purchasePlaces", data={
        "competition": "Test Competition",
        "club": "Test Club",
        "places": "3"
    }, follow_redirects=True)

    assert b"Great! - Booking complete!" in response.data

def test_booking_exceeding_club_points(client):
    """Un club ne peut pas acheter plus de places qu’il n’a de points"""
    app.config["clubs"] = [{"name": "Test Club", "points": "2"}]
    app.config["competitions"] = [{"name": "Test Competition", "numberOfPlaces": "25"}]

    response = client.post("/purchasePlaces", data={
        "competition": "Test Competition",
        "club": "Test Club",
        "places": "5"  # Demande plus que les points disponibles
    }, follow_redirects=True)

    assert b"Error: You only have 2" in response.data  # Vérifie le message d'erreur

def test_points_are_deducted(client):
    """Les points utilisés doivent bien être déduits du total de points du club"""
    app.config["clubs"] = [{"name": "Test Club", "points": "10"}]
    app.config["competitions"] = [{"name": "Test Competition", "numberOfPlaces": "25"}]

    client.post("/purchasePlaces", data={
        "competition": "Test Competition",
        "club": "Test Club",
        "places": "4"
    })

    updated_club_points = int(app.config["clubs"][0]["points"])
    assert updated_club_points == 6  # 10 - 4 = 6
