def test_user_can_login_and_see_competitions(client, mock_data, monkeypatch):
    """
    Tests if the user can log in successfully and see the list of competitions.

    This test verifies the following:
    - The user is able to log in using valid credentials.
    - The response status code after logging in is 200, indicating a successful response.
    - After login, the user can see the homepage ("Welcome" message).
    - Future competitions are displayed on the homepage.

    :param client: Test client fixture used to simulate requests to the application.
    :param mock_data: Dictionary containing mock data for clubs and competitions.
    :param monkeypatch: Fixture used to safely override the attributes of the server module.
    :return: None
    """
    monkeypatch.setattr("server.clubs", mock_data["clubs"])
    monkeypatch.setattr("server.competitions", mock_data["competitions"])

    response = client.post('/showSummary', data={"email": "valid@email.com"}, follow_redirects=True)

    assert response.status_code == 200
    assert b"Welcome" in response.data
    assert b"Future Competition" in response.data