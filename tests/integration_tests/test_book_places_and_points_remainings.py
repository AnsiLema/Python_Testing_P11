def test_user_can_book_places(client, mock_data, monkeypatch):
    """
    Tests whether a user can successfully book places in a competition, ensuring that the correct number
    of places is reserved and the club's points are updated accordingly. This test simulates
    a user logging in, booking places, and validates the application's responses and data updates.

    :param client: A Flask test client used to mock HTTP requests and interact with the app.
    :param mock_data: Mock data dictionary containing initial test data for clubs and competitions.
    :param monkeypatch: A pytest fixture used to safely modify or replace components during the test.
    :return: None
    """
    monkeypatch.setattr("server.clubs", mock_data["clubs"])
    monkeypatch.setattr("server.competitions", mock_data["competitions"])

    # Login
    client.post('/showSummary', data={"email": "valid@email.com"}, follow_redirects=True)

    # Reserve 3 places
    response = client.post("/purchasePlaces", data={
        "competition": "Future Competition",
        "club": "Test Club",
        "places": "3"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Great! - Booking complete!" in response.data
    assert b"Points available: 10" in response.data