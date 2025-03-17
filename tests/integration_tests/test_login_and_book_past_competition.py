def test_user_cannot_book_past_competition(client, mock_data, monkeypatch):
    """
    Test to verify that a user cannot book a place in a past competition. The test
    is performed by modifying the competition dataset to include a past
    competition and then attempting to book a place for that competition.

    :param client: Test client for simulating server requests
    :type client: Flask.testing.FlaskClient
    :param mock_data: Pre-prepared mock data including clubs and competitions
    :type mock_data: dict
    :param monkeypatch: Pytest monkeypatch fixture for dynamically modifying
        attributes and methods
    :type monkeypatch: MonkeyPatch
    :return: None
    """
    mock_data["competitions"].append(
        {"name": "Past Competition", "date": "2023-01-01 13:30:00", "numberOfPlaces": "10"})

    monkeypatch.setattr("server.clubs", mock_data["clubs"])
    monkeypatch.setattr("server.competitions", mock_data["competitions"])

    response = client.get('/book/Past Competition/Test Club', follow_redirects=True)

    assert response.status_code == 200
    assert b"You cannot book places for a past competition." in response.data