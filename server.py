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
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html', club=club, competitions=competitions)


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
    club = next((c for c in clubs if c['name'] == request.form['club']), None)

    if not competition or not club:
        flash("Invalid competition or club.")
        return redirect(url_for('showSummary'))

    if is_competition_past(competition):
        flash("You cannot purchase places for a past competition.")
        return redirect(url_for('showSummary'))

    placesRequired = int(request.form['places'])

    if placesRequired > int(competition['numberOfPlaces']):
        flash("Not enough places available.")
    else:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
        flash("Great - booking complete!")

    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)