import sys
import os
import pytest


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from server import app as flask_app, clubs, competitions  # ✅ Import correct

@pytest.fixture
def app():
    flask_app.config["TESTING"] = True
    return flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def mock_data():
    return {
        "clubs": [
            {"name": "Test Club", "email": "valid@email.com", "points": "13"}
        ],
        "competitions": [
            {"name": "Future Competition", "date": "2025-12-31 13:30:00", "numberOfPlaces": "25"}
        ]
    }