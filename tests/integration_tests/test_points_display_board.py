def test_points_display_board(client, mock_data, monkeypatch):
    """
    Test the display of the clubs and their corresponding points on the board.

    This function tests whether the '/clubs' endpoint properly renders the HTML page
    with the intended club name and points. It ensures the rendering of the page is
    successful and contains the correct information from the mock data.

    :param client: A test client fixture used for simulating HTTP requests in the test.
    :type client: FlaskClient
    :param mock_data: Mock data for the clubs and other configurations used during the test.
    :type mock_data: dict
    :param monkeypatch: Fixture used to temporarily replace modules and attributes for testing purposes.
    :type monkeypatch: MonkeyPatch
    :return: None
    """
    monkeypatch.setattr("server.clubs", mock_data["clubs"])

    response = client.get("/clubs", follow_redirects=True)

    assert response.status_code == 200
    assert b"Test Club" in response.data
    assert b"13" in response.data
    assert b"<h1>Clubs and Points</h1>" in response.data