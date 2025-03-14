import pytest
from flask import Flask
from server import app, is_competition_past


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


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
    assert is_competition_past(mock_data['competitions'][0]) == False
    assert is_competition_past(mock_data['competitions'][1]) == True


def test_book_places_for_a_past_competition(client, mock_data, monkeypatch):
    monkeypatch.setattr('server.clubs', mock_data['clubs'])
    monkeypatch.setattr('server.competitions', mock_data['competitions'])

    response = client.get('/book/Past Competition/Test Club')

    assert response.status_code == 200
    assert b"You cannot book places for a past competition." in response.data


def test_book_places_for_a_future_competition(client, mock_data, monkeypatch):
    """Tester qu'on peut accéder à la page de réservation pour une compétition valide"""
    monkeypatch.setattr("server.clubs", mock_data["clubs"])
    monkeypatch.setattr("server.competitions", mock_data["competitions"])

    response = client.get(f'/book/Future Competition/Test Club')

    assert response.status_code == 200
    assert b"Booking for" in response.data


def test_valid_purchase(client, mock_data, monkeypatch):
    """Test d'un achat valide"""
    monkeypatch.setattr('server.clubs', mock_data['clubs'])
    monkeypatch.setattr('server.competitions', mock_data['competitions'])

    response = client.post('/purchasePlaces', data={
        'competition': 'Future Competition',
        'club': 'Test Club',
        'places': '5'
    })

    assert response.status_code == 200
    assert b"Great - booking complete!" in response.data
