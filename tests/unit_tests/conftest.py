import pytest
from server import app, clubs, competitions

@pytest.fixture
def mock_data():
    return {
        "clubs": [
            {"name": "Test Club", "email": "valid@email.com", "points": "10"}
        ],
        "competitions": [
            {"name": "Future Competition", "date": "2025-12-31 13:30:00", "numberOfPlaces": "25"}
        ]
    }

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def clear_clubs_and_competitions():
    clubs.clear()
    competitions.clear()