import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


def is_competition_past(competition):
    competition_date = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
    return competition_date < datetime.now()


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['GET', 'POST'])
def showSummary():
    if 'email' not in request.form or not request.form['email']:
        flash("Sorry, that email is missing.", "error")
        return redirect(url_for('index'))

    club = next((club for club in clubs if club['email'] == request.form['email']), None)

    if club is None:
        flash("Sorry, this email is not registered.", 400)
        return redirect(url_for('index'))

    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
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
    competition = next((c for c in competitions if c['name'] == request.form['competition']), None)
    club = next((c for c in clubs if c['name'] == request.form['club'] ), None)

    if not competition or not club:
        flash("Invalid competition or club.")
        return redirect(url_for('index'))

    placesRequired = int(request.form['places'])
    club_points = int(club['points'])
    availablePlaces = int(competition['numberOfPlaces'])

    places = request.form['places']
    if not places.isdigit():
        raise ValueError("The number of places must be a number")

    if placesRequired > availablePlaces:
        flash("Not enough places available.")
        return redirect(url_for('book', competition=competition['name'], club=club['name']))

    if placesRequired > club_points:
        flash(f"Error: You only have {club_points}, You cannot book {placesRequired} places")
        return redirect(url_for('book', competition=competition['name'], club=club['name']))

    if placesRequired <= 0:
        raise ValueError("The number of places must be greater than 0")

    if placesRequired > 12:
        flash("Error: You cannot book more than 12 places per competition", "error")
        return redirect(url_for('book', competition=competition['name'], club=club['name']))

    # Points deducted
    club['points'] = str(club_points - placesRequired)  # Convert to string because points are stored as string

    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    flash('Great! - Booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)



# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))