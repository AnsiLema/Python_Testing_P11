import pytest
from unittest.mock import patch
from datetime import datetime
from server import app, is_competition_past


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

def test_book_for_passed_competitions_is_not_allowed(mock_data):
   pass

def test_book_for_future_competitions_is_allowed(mock_data):
    pass



