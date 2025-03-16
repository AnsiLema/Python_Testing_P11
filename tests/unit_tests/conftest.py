import pytest
from server import app, clubs, competitions

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def clear_clubs_and_competitions():
    clubs.clear()
    competitions.clear()