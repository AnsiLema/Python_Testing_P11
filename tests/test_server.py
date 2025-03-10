import pytest
from server import app, competitions, clubs
from flask import url_for


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_purchase_places_with_valid_number(client):
    """Test d'achat de places avec un nombre valide (moins de 12)"""
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '5'
    })
    assert b'Great-booking complete!' in response.data


def test_purchase_place_above_limitation(client):
    """Test d'achat de plus de 12 places"""
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '13'
    }, follow_redirects=True)
    assert b'Error: You cannot book more than 12 places per competition' in response.data


def test_achat_places_valeur_non_numerique(client):
    """Test d'achat avec des caractères non numériques"""
    with pytest.raises(ValueError):
        client.post('/purchasePlaces', data={
            'competition': 'Spring Festival',
            'club': 'Simply Lift',
            'places': 'abc'
        })


def test_achat_places_nombre_negatif(client):
    """Test d'achat avec un nombre négatif"""
    with pytest.raises(ValueError):
        client.post('/purchasePlaces', data={
            'competition': 'Spring Festival',
            'club': 'Simply Lift',
            'places': '-5'
        })
