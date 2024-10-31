# routes/main.py
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required
from . import main
from forms import InstitutionRegistrationForm, TeamRegistrationForm, PlayerRegistrationForm
from models import db, Institution, Team, Player, Match, Group
from datetime import datetime

from utils import calculate_group_standings

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/register/institution', methods=['GET', 'POST'])
def register_institution():
    form = InstitutionRegistrationForm()
    if form.validate_on_submit():
        institution = Institution(name=form.name.data)
        db.session.add(institution)
        db.session.commit()
        flash('Institution registered successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template('register_institution.html', form=form)


@main.route('/register/team', methods=['GET', 'POST'])
def register_team():
    form = TeamRegistrationForm()
    form.institution.choices = [(inst.id, inst.name) for inst in Institution.query.all()]
    if form.validate_on_submit():
        team = Team(
            name=form.name.data,
            sport=form.sport.data,
            institution_id=form.institution.data
        )
        db.session.add(team)
        db.session.commit()
        flash('Team registered successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template('register_team.html', form=form)


@main.route('/register/player', methods=['GET', 'POST'])
def register_player():
    form = PlayerRegistrationForm()
    form.team.choices = [(team.id, team.name) for team in Team.query.all()]
    if form.validate_on_submit():
        player = Player(
            name=form.name.data,
            position=form.position.data,
            team_id=form.team.data
        )
        db.session.add(player)
        db.session.commit()
        flash('Player registered successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template('register_player.html', form=form)

@main.route('/fixtures')
def fixtures():
    try:
        current_time = datetime.utcnow()
        # Fetch matches that are scheduled in the future
        upcoming_matches = Match.query.filter(Match.date >= current_time).order_by(Match.date.asc()).all()
        return render_template('fixtures.html', matches=upcoming_matches)
    except Exception as e:
        flash('An error occurred while fetching fixtures.', 'danger')
        return redirect(url_for('main.index'))
    
@main.route('/standings')
def standings_view():
    try:
        standings = calculate_group_standings()
        return render_template('standings.html', standings=standings)
    except Exception as e:
        flash('An error occurred while fetching standings.', 'danger')
        return redirect(url_for('main.index'))
    
@main.route('/results')
def results():
    try:
        # Fetch matches that have scores assigned (i.e., completed)
        completed_matches = Match.query.filter(Match.score_home != None, Match.score_away != None).order_by(Match.date.desc()).all()
        return render_template('results.html', matches=completed_matches)
    except Exception as e:
        flash('An error occurred while fetching results.', 'danger')
        return redirect(url_for('main.index'))
    

@main.route('/chatbot', methods=['POST'])
def chatbot():
    try:
        data = request.get_json()
        user_message = data.get('message', '').lower()

        # Simple rule-based responses
        if 'hello' in user_message or 'hi' in user_message:
            reply = "Hello! How can I assist you today?"
        elif 'fixtures' in user_message:
            reply = "You can view all upcoming fixtures by visiting the Fixtures page."
        elif 'standings' in user_message:
            reply = "You can check the latest group standings on the Standings page."
        elif 'results' in user_message:
            reply = "View all match results on the Results page."
        elif 'register' in user_message:
            reply = "You can register institutions, teams, and players using the Register links in the navigation bar."
        elif 'who won' in user_message or 'winner' in user_message:
            # Example: "Who won the final?"
            final_match = Match.query.filter_by(round='Final').first()
            if final_match and final_match.score_home and final_match.score_away:
                if final_match.score_home > final_match.score_away:
                    winner = final_match.home_team.name
                elif final_match.score_home < final_match.score_away:
                    winner = final_match.away_team.name
                else:
                    winner = "It's a draw!"
                reply = f"The winner of the Final is {winner}."
            else:
                reply = "The Final match has not been played yet."
        elif 'help' in user_message:
            reply = "I can help you with information about fixtures, standings, results, and registration processes."
        else:
            # If message doesn't match any rule
            reply = "I'm sorry, I didn't understand that. You can ask me about fixtures, standings, results, or registration."

        return jsonify({'reply': reply})
    except Exception as e:
        print(f"Error in chatbot: {e}")
        return jsonify({'reply': "An error occurred while processing your message."}), 500


# routes/main.py (continued)

import spacy
from flask import jsonify
from flask import request
from models import db, Team, Institution, Match, Group
from utils import get_upcoming_fixtures, get_current_standings, get_completed_matches, get_live_scores
from datetime import datetime

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Define intents
INTENTS = {
    "greeting": ["hello", "hi", "hey", "good morning", "good evening"],
    "ask_fixtures": ["fixture", "match schedule", "upcoming match", "when is the next match", "show me upcoming fixtures"],
    "ask_standings": ["standings", "rankings", "group rankings", "current standings", "show standings"],
    "ask_results": ["result", "who won", "match result", "past match", "show results"],
    "registration_help": ["register", "how to register", "help with registration", "sign up"],
    "bye": ["bye", "goodbye", "see you", "later"]
}

@main.route('/chatbot', methods=['POST'])
def chatbot():
    try:
        data = request.get_json()
        user_message = data.get('message', '').lower()
        doc = nlp(user_message)

        # Intent classification using keyword matching
        user_intents = []
        for token in doc:
            for intent, keywords in INTENTS.items():
                if token.text in keywords:
                    user_intents.append(intent)

        # Determine the most probable intent
        if user_intents:
            intent = user_intents[0]  # Simple approach: take the first matched intent
        else:
            intent = "unknown"

        # Generate response based on intent
        if intent == "greeting":
            reply = "Hello! How can I assist you today?"
        elif intent == "ask_fixtures":
            fixtures = get_upcoming_fixtures()
            if fixtures:
                reply = "Here are the upcoming fixtures:\n"
                for match in fixtures:
                    reply += f"Match {match.id}: {match.home_team.name} vs {match.away_team.name} on {match.date.strftime('%Y-%m-%d %H:%M')} UTC\n"
            else:
                reply = "There are no upcoming fixtures at the moment."
        elif intent == "ask_standings":
            standings = get_current_standings()
            if standings:
                reply = "Current Group Standings:\n"
                for group, teams in standings.items():
                    reply += f"\nGroup {group}:\n"
                    for team_info in teams:
                        reply += f"{team_info['team'].name}: {team_info['points']} points (MP: {team_info['matches_played']}, W: {team_info['wins']}, D: {team_info['draws']}, L: {team_info['losses']})\n"
            else:
                reply = "Standings are not available at the moment."
        elif intent == "ask_results":
            results = get_completed_matches()
            if results:
                reply = "Here are the recent match results:\n"
                for match in results:
                    reply += f"Match {match.id}: {match.home_team.name} {match.score_home} - {match.score_away} {match.away_team.name} on {match.date.strftime('%Y-%m-%d %H:%M')} UTC\n"
            else:
                reply = "No match results are available at the moment."
        elif intent == "registration_help":
            reply = "You can register institutions, teams, and players using the Register links in the navigation bar."
        elif intent == "bye":
            reply = "Goodbye! Feel free to reach out if you have more questions."
        else:
            reply = "I'm sorry, I didn't understand that. You can ask me about fixtures, standings, results, or registration processes."

        return jsonify({'reply': reply})
    except Exception as e:
        print(f"Error in chatbot: {e}")
        return jsonify({'reply': "An error occurred while processing your message."}), 500


# routes/main.py (continued)

# Load the trained intent classification model
intent_nlp = spacy.load("models/chatbot_intent_model")

@main.route('/chatbot', methods=['POST'])
def chatbot():
    try:
        data = request.get_json()
        user_message = data.get('message', '').lower()
        doc = intent_nlp(user_message)

        # Get the highest scoring intent
        intent_scores = doc.cats
        intent = max(intent_scores, key=intent_scores.get)

        # Threshold to handle unknown intents
        if intent_scores[intent] < 0.5:
            intent = "unknown"

        # Generate response based on intent
        if intent == "greeting":
            reply = "Hello! How can I assist you today?"
        elif intent == "ask_fixtures":
            fixtures = get_upcoming_fixtures()
            if fixtures:
                reply = "Here are the upcoming fixtures:\n"
                for match in fixtures:
                    reply += f"Match {match.id}: {match.home_team.name} vs {match.away_team.name} on {match.date.strftime('%Y-%m-%d %H:%M')} UTC\n"
            else:
                reply = "There are no upcoming fixtures at the moment."
        elif intent == "ask_standings":
            standings = get_current_standings()
            if standings:
                reply = "Current Group Standings:\n"
                for group, teams in standings.items():
                    reply += f"\nGroup {group}:\n"
                    for team_info in teams:
                        reply += f"{team_info['team'].name}: {team_info['points']} points (MP: {team_info['matches_played']}, W: {team_info['wins']}, D: {team_info['draws']}, L: {team_info['losses']})\n"
            else:
                reply = "Standings are not available at the moment."
        elif intent == "ask_results":
            results = get_completed_matches()
            if results:
                reply = "Here are the recent match results:\n"
                for match in results:
                    reply += f"Match {match.id}: {match.home_team.name} {match.score_home} - {match.score_away} {match.away_team.name} on {match.date.strftime('%Y-%m-%d %H:%M')} UTC\n"
            else:
                reply = "No match results are available at the moment."
        elif intent == "registration_help":
            reply = "You can register institutions, teams, and players using the Register links in the navigation bar."
        elif intent == "bye":
            reply = "Goodbye! Feel free to reach out if you have more questions."
        else:
            # Attempt to handle unknown intents with external API or default response
            # Example: Live Scores
            if "live scores" in user_message:
                # Extract sport using entity recognition or keyword matching
                # For simplicity, default to "football"
                sport = "football"
                live_scores = get_live_scores(sport)
                if live_scores:
                    reply = f"Live scores for {sport.title()}:\n"
                    for event in live_scores.get('events', []):
                        reply += f"{event['homeTeam']} {event['homeScore']} - {event['awayScore']} {event['awayTeam']} on {event['dateEvent']}\n"
                else:
                    reply = f"Live scores for {sport.title()} are not available at the moment."
            else:
                reply = "I'm sorry, I didn't understand that. You can ask me about fixtures, standings, results, or registration processes."

        return jsonify({'reply': reply})
    except Exception as e:
        print(f"Error in chatbot: {e}")
        return jsonify({'reply': "An error occurred while processing your message."}), 500
