import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def loadClubs():
    """
    Loads a list of clubs from a JSON file named 'clubs.json'.

    This function opens the 'clubs.json' file, reads its data, and extracts a list
    of clubs from the JSON structure. It assumes the JSON file contains a top-level
    key 'clubs' that maps to the desired club list.

    :return: A list of clubs extracted from the 'clubs.json' file.
    :rtype: list
    """
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    """
    Loads competition data from a JSON file and returns a list of competition details.

    This function reads a JSON file named 'competitions.json' and extracts the competition
    data from the file. The expected file is assumed to contain a key 'competitions' holding
    the list of competitions. This function ensures proper loading and parsing from the JSON
    source.

    :return: The list of competition details parsed from the JSON file.
    :rtype: list
    """
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


def is_competition_past(competition):
    """
    Determines whether a competition date is in the past.

    This function evaluates whether the provided competition's date is earlier
    than the current datetime. It returns a boolean value indicating whether
    the competition has already occurred.

    :param competition: A dictionary containing competition information, where
        the key 'date' specifies the competition date in the format 'YYYY-MM-DD
        HH:MM:SS'.
    :type competition: dict
    :return: A boolean value indicating if the competition date is in the past.
        Returns True if the competition is past, otherwise False.
    :rtype: bool
    """
    competition_date = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
    return competition_date < datetime.now()


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    """
    Handles the routing for the root URL of the application.

    This function is registered as the handler for the root URL ('/'). When
    accessed, it renders and returns the 'index.html' template. This is
    commonly used as the landing page for the application.

    :return: Renders and returns the 'index.html' template.
    :rtype: flask.wrappers.Response
    """
    return render_template('index.html')


@app.route('/showSummary', methods=['GET', 'POST'])
def showSummary():
    """
    Handles the display of the summary page after validating the email input.

    The function processes a POST request to the `/showSummary` endpoint by checking
    if an email is present in the request form. If the email is missing or invalid,
    an error message is flashed to the user, and they are redirected to the home page.
    If the email matches an existing club, the summary page containing club details
    and related competition information is rendered.

    :return: A template rendering welcome.html with club and competitions details if
             the email is valid and found, or a redirection to the index page with
             appropriate flash messages if the validation fails.
    :rtype: flask.Response
    :raises KeyError: When the required key ('email') is missing in request.form.
    """
    if 'email' not in request.form or not request.form['email']:
        flash("Sorry, that email is missing.", "error")
        return redirect(url_for('index'))

    club = next((club for club in clubs if club['email'] == request.form['email']), None)

    if club is None:
        flash("Sorry, this email is not registered.")
        return redirect(url_for('index'))

    return render_template('welcome.html',club=club,competitions=competitions)

@app.route('/book/<competition>/<club>')
def book(competition, club):
    """
    Books a club for a specific competition, verifying the validity of the club
    and the competition, as well as ensuring the competition is not in the past.
    If either the club or competition is invalid, or the competition is in the
    past, redirects the user back to the welcome page with an appropriate
    message. Otherwise, it renders the booking page.

    :param competition: The name of the competition to be booked.
    :param club: The name of the club attempting to book for the competition.
    :return: A rendered HTML template, either the booking page if the operation
        is valid or the welcome page if there is an error.
    """
    foundClub = next((c for c in clubs if c['name'] == club), None)
    foundCompetition = next((c for c in competitions if c['name'] == competition), None)

    if not foundClub or not foundCompetition:
        flash("Something went wrong - please try again.")
        return render_template('welcome.html', club=foundClub, competitions=competitions)

    if is_competition_past(foundCompetition):
        flash("You cannot book places for a past competition.")
        return render_template('welcome.html', club=foundClub, competitions=competitions)

    return render_template('booking.html', club=foundClub, competition=foundCompetition)

@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    """
    Handles the purchase of places for a competition by a club, ensuring all validations and conditions are met.

    The function validates user input, such as competition and club existence, and the requested number of places.
    It also performs checks to ensure constraints like the availability of places, club points, and maximum limits
    are adhered to. Upon successful validation, it adjusts the competition's and club's attributes accordingly and
    provides feedback to the user.

    :raises ValueError: If the provided number of places is not a valid integer.

    :return: Rendered HTML template for the welcome page if the booking is successful, otherwise redirects to
        appropriate pages with error flash messages.
    :rtype: Union[werkzeug.wrappers.response.Response, str]
    """
    competition = next((c for c in competitions if c['name'] == request.form['competition']), None)
    club = next((c for c in clubs if c['name'] == request.form['club']), None)

    if not competition or not club:
        flash("Invalid competition or club.", "error")
        return redirect(url_for('index'))

    places = request.form.get('places', '').strip()

    try:
        placesRequired = int(places)
    except ValueError:
        flash("Error: The number of places must be a valid integer.", "error")
        return redirect(url_for('book', competition=competition['name'], club=club['name']))

    if placesRequired <= 0:
        flash("Error: The number of places must be greater than 0", "error")
        return redirect(url_for('book', competition=competition['name'], club=club['name']))

    club_points = int(club['points'])
    availablePlaces = int(competition['numberOfPlaces'])

    if placesRequired > availablePlaces:
        flash("Not enough places available.", "error")
        return redirect(url_for('book', competition=competition['name'], club=club['name']))

    if placesRequired > club_points:
        flash(f"Error: You only have {club_points} points, You cannot book {placesRequired} places", "error")
        return redirect(url_for('book', competition=competition['name'], club=club['name']))

    if placesRequired > 12:
        flash("Error: You cannot book more than 12 places per competition", "error")
        return redirect(url_for('book', competition=competition['name'], club=club['name']))

    club['points'] = str(club_points - placesRequired)
    competition['numberOfPlaces'] = str(availablePlaces - placesRequired)
    flash('Great! - Booking complete!')

    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/clubs')
def showClubs():
    """
    Handles requests to the '/clubs' endpoint and returns the rendered 'clubs.html'
    template populated with the clubs data.
    """
    return render_template('clubs.html',clubs=clubs)


@app.route('/logout')
def logout():
    """
    Handles the logout functionality by redirecting the user to the index page.
    This function is registered as a route for the '/logout' endpoint in a Flask
    application.
    """
    return redirect(url_for('index'))