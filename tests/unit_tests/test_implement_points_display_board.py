import pytest
from flask import json

from server import app, loadClubs, loadCompetitions, logout
from unittest.mock import mock_open, patch


@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_show_clubs_route_status_code(test_client):
    response = test_client.get('/clubs')
    assert response.status_code == 200


def test_loadClubs_correctly_loads_json(mocker):
    mock_clubs_data = '{"clubs": [{"name": "Club A"}, {"name": "Club B"}]}'
    mocker.patch("builtins.open", mock_open(read_data=mock_clubs_data))

    clubs = loadClubs()
    assert clubs == [{"name": "Club A"}, {"name": "Club B"}]


def test_loadClubs_with_empty_file(mocker):
    mocker.patch("builtins.open", mock_open(read_data='{"clubs": []}'))
    clubs = loadClubs()
    assert clubs == []

def test_loadCompetitions_correctly_loads_json(mocker):
    mock_competitions_data = '{"competitions": [{"name": "Competition A"}, {"name": "Competition B"}]}'
    mocker.patch("builtins.open", mock_open(read_data=mock_competitions_data))

    competitions = loadCompetitions()
    assert competitions == [{"name": "Competition A"}, {"name": "Competition B"}]


def test_loadCompetitions_with_empty_file(mocker):
    mocker.patch("builtins.open", mock_open(read_data='{"competitions": []}'))

    competitions = loadCompetitions()
    assert competitions == []


def test_index_route_status_code(test_client):
    response = test_client.get('/')
    assert response.status_code == 200


def test_index_route_renders_template(mocker, test_client):
    mock_render = mocker.patch('server.render_template', return_value='Mocked Index Page')
    response = test_client.get('/')
    mock_render.assert_called_once_with('index.html')
    assert response.data == b'Mocked Index Page'


def test_logout_redirects_to_index(test_client):
    response = test_client.get('/logout', follow_redirects=False)
    assert response.status_code == 302

def test_showClubs_route_status_code(test_client):
    response = test_client.get('/clubs')
    assert response.status_code == 200

