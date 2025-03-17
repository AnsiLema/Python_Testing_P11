def test_user_cannot_book_more_than_12_places(client, mock_data, monkeypatch):
    """
    Test case to verify that users cannot book more than 12 places for a competition.

    This test ensures that the server enforces a restriction on the maximum number of places
    a user can book for a single competition. If a request is made to book more than
    the allowed limit, the server should return an appropriate error message.

    :param client: Test client used to simulate HTTP requests to the server
    :param mock_data: Mock data representing the initial state of clubs and competitions
    :param monkeypatch: Fixture for dynamically modifying or replacing objects during tests
    :return: None
    """
    monkeypatch.setattr("server.clubs", mock_data["clubs"])
    monkeypatch.setattr("server.competitions", mock_data["competitions"])

    # Login
    client.post('/showSummary', data={"email": "valid@email.com"}, follow_redirects=True)

    # Try to reserve 13 places
    response = client.post("/purchasePlaces", data={
        "competition": "Future Competition",
        "club": "Test Club",
        "places": "13"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Error: You cannot book more than 12 places per competition" in response.data