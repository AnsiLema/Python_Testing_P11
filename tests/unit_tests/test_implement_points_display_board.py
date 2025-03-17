import pytest
from server import app, loadClubs, loadCompetitions
from unittest.mock import mock_open


@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_show_clubs_route_status_code(test_client):
    """
    Tests the status code of the '/clubs' route to ensure it returns a successful
    HTTP response.

    :param test_client: The test client to simulate HTTP requests.
    :type test_client: FlaskClient
    :return: None
    """
    response = test_client.get('/clubs')
    assert response.status_code == 200


def test_loadClubs_correctly_loads_json(mocker):
    """
    Tests that the function `loadClubs` correctly loads and parses club data
    provided in a JSON file.

    This test uses a mocked representation of a JSON file containing
    information about clubs and verifies if the parsed output matches
    the expected structure.

    :param mocker: Mocking framework fixture used to patch and simulate
        the built-in `open` method.
    :return: None
    """
    mock_clubs_data = '{"clubs": [{"name": "Club A"}, {"name": "Club B"}]}'
    mocker.patch("builtins.open", mock_open(read_data=mock_clubs_data))

    clubs = loadClubs()
    assert clubs == [{"name": "Club A"}, {"name": "Club B"}]


def test_loadClubs_with_empty_file(mocker):
    """
    Tests the `loadClubs` function when provided an empty file. This test uses the
    `mocker` library to simulate an empty JSON structure in the file being read
    by `loadClubs`. It ensures the function returns an empty list, as the JSON
    file contains no club data.

    :param mocker: Mocking library object to simulate file reading behavior.
    :type mocker: MockFixture
    :return: None
    """
    mocker.patch("builtins.open", mock_open(read_data='{"clubs": []}'))
    clubs = loadClubs()
    assert clubs == []

def test_loadCompetitions_correctly_loads_json(mocker):
    """
    Tests the `loadCompetitions` function to ensure it correctly loads competition
    data from a JSON file. The test uses the `mocker` library to mock the file
    reading process and verify that the returned data matches the expected
    structure.

    :param mocker: Mocking utility for replacing file operations.
    :type mocker: pytest_mock.plugin.MockerFixture
    :return: None
    """
    mock_competitions_data = '{"competitions": [{"name": "Competition A"}, {"name": "Competition B"}]}'
    mocker.patch("builtins.open", mock_open(read_data=mock_competitions_data))

    competitions = loadCompetitions()
    assert competitions == [{"name": "Competition A"}, {"name": "Competition B"}]


def test_loadCompetitions_with_empty_file(mocker):
    """
    This function tests the behavior of the `loadCompetitions` function when it is provided
    an empty JSON file containing an empty 'competitions' list. It ensures that the function
    correctly parses the empty structure and returns an empty list.

    :param mocker: A pytest-mock mocker object used to mock the behavior
        of the `open` function in Python.
    :return: None
    """
    mocker.patch("builtins.open", mock_open(read_data='{"competitions": []}'))

    competitions = loadCompetitions()
    assert competitions == []


def test_index_route_status_code(test_client):
    """
    Tests the status code returned by the index route. This function ensures that
    when sending a GET request to the specified endpoint ('/'), the returned
    response has a status code indicating successful operation (200).

    :param test_client: Fixture or instance used to simulate HTTP requests and
        interact with the Flask application under test.
    :return: None
    """
    response = test_client.get('/')
    assert response.status_code == 200


def test_index_route_renders_template(mocker, test_client):
    """
    Tests the index route of the application by mocking the `render_template` function
    to verify the correct template is rendered and returned.

    The test ensures the Flask server correctly handles the root ('/') GET request,
    verifying the template rendering and its response content.

    :param mocker: A pytest-mock mocker instance used to patch and mock the
                   `render_template` function.
    :param test_client: A Flask test client instance used to simulate HTTP requests
                        against the application.
    :return: None
    """
    mock_render = mocker.patch('server.render_template', return_value='Mocked Index Page')
    response = test_client.get('/')
    mock_render.assert_called_once_with('index.html')
    assert response.data == b'Mocked Index Page'


def test_logout_redirects_to_index(test_client):
    """
    Logs out a user and ensures that the response is redirected to the index page.

    This function tests a logout behavior by sending a GET request to the
    `/logout` route. It verifies that the HTTP response status code equals
    302, indicating redirection.

    :param test_client: The test client used to simulate HTTP requests.
    :type test_client: FlaskClient
    :return: None
    """
    response = test_client.get('/logout', follow_redirects=False)
    assert response.status_code == 302

def test_showClubs_route_status_code(test_client):
    """
    Tests the status code returned by the '/clubs' route of the application.

    This function sends a GET request to the '/clubs' route using the provided
    test client and asserts that the returned HTTP status code is 200, indicating
    a successful request and a proper setup of the route.

    :param test_client: The test client used to simulate requests to the application.
    :type test_client: Any
    :return: None. Asserts whether the status code of the response is 200.
    :rtype: None
    """
    response = test_client.get('/clubs')
    assert response.status_code == 200

