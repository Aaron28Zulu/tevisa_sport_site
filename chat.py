from http.client import responses

from flask import Flask, jsonify, request, render_template
import psycopg2
import spacy
from utils.database_connection import DatabaseConnection
from utils.group_manager import GroupManager
from utils.tournament_manager import TournamentManager
from utils.fixture_manager import FixtureManager

app = Flask(__name__)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")



# Define helper functions to fetch match result, fixtures, and standings
def get_match_result(team_name):
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        query = """
        SELECT f.fixture_date AS date, 
               t1.team_name AS team1, s.team1_score, 
               t2.team_name AS team2, s.team2_score
        FROM fixtures f
        JOIN scores_results s ON f.fixture_id = s.fixture_id
        JOIN teams t1 ON f.team1_id = t1.team_id
        JOIN teams t2 ON f.team2_id = t2.team_id
        WHERE t1.team_name = %s OR t2.team_name = %s
        ORDER BY f.fixture_date DESC
        LIMIT 1;
        """
        cursor.execute(query, (team_name, team_name))
        result = cursor.fetchone()

    if result:
        return f"{result[1]} vs {result[3]} on {result[0]}, Score: {result[2]} - {result[4]}"
    else:
        return "No recent match results found."


def get_upcoming_fixtures(team_name):
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        query = """
        SELECT f.fixture_date AS date, 
               t1.team_name AS team1, 
               t2.team_name AS team2
        FROM fixtures f
        JOIN teams t1 ON f.team1_id = t1.team_id
        JOIN teams t2 ON f.team2_id = t2.team_id
        WHERE (t1.team_name = %s OR t2.team_name = %s) AND f.fixture_date > NOW()
        ORDER BY f.fixture_date ASC
        LIMIT 3;
        """
        cursor.execute(query, (team_name, team_name))
        results = cursor.fetchall()

        if results:
            fixtures = ", ".join([f"{result[1]} vs {result[2]} on {result[0]}" for result in results])
            return f"Upcoming matches: {fixtures}"
        else:
            return "No upcoming matches found."


def get_group_standings():
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        query = """
        SELECT t.team_name AS team,
               COUNT(f.fixture_id) AS played,
               SUM(CASE WHEN (t.team_id = f.team1_id AND s.team1_score > s.team2_score) OR 
                            (t.team_id = f.team2_id AND s.team2_score > s.team1_score) THEN 1 ELSE 0 END) AS won,
               SUM(CASE WHEN s.team1_score = s.team2_score THEN 1 ELSE 0 END) AS drawn,
               SUM(CASE WHEN (t.team_id = f.team1_id AND s.team1_score < s.team2_score) OR 
                            (t.team_id = f.team2_id AND s.team2_score < s.team1_score) THEN 1 ELSE 0 END) AS lost,
               (SUM(CASE WHEN (t.team_id = f.team1_id AND s.team1_score > s.team2_score) OR 
                             (t.team_id = f.team2_id AND s.team2_score > s.team1_score) THEN 3 ELSE 0 END) +
                SUM(CASE WHEN s.team1_score = s.team2_score THEN 1 ELSE 0 END)) AS points
        FROM fixtures f
        JOIN scores_results s ON f.fixture_id = s.fixture_id
        JOIN teams t ON t.team_id IN (f.team1_id, f.team2_id)
        GROUP BY t.team_name
        ORDER BY points DESC, won DESC, played ASC;
        """
        cursor.execute(query)
        results = cursor.fetchall()

    standings = "\n".join(
        [f"{result[0]} - {result[5]} points, {result[1]} played, {result[2]} won, {result[3]} drawn, {result[4]} lost"
         for result in results])
    return f"Group Standings:\n{standings}"


# Intent detection with spaCy
def detect_intent(user_message):
    doc = nlp(user_message.lower())
    if "result" in user_message or "score" in user_message:
        return "match_result"
    elif "next match" in user_message or "upcoming" in user_message:
        return "upcoming_fixtures"
    elif "standings" in user_message or "leaderboard" in user_message:
        return "group_standings"
    else:
        return "unknown"


# Extract team name from user message
def extract_team_name(message):
    doc = nlp(message)
    for ent in doc.ents:
        if ent.label_ == "ORG":  # Assuming team names are labeled as ORG
            return ent.text
    return None


# Chatbot endpoint
@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.json.get("message")
    print(f"User: {user_message})") # For Debugging
    intent = detect_intent(user_message)
    print(f"Intent: {intent}") # For Debugging

    if intent == "match_result":
        # team_name = extract_team_name(user_message)
        # response = get_match_result(team_name) if team_name else "Please specify a team name for match results."

        response = "Working"
    elif intent == "upcoming_fixtures":
        team_name = extract_team_name(user_message)
        response = get_upcoming_fixtures(
            team_name) if team_name else "Please specify a team name for upcoming fixtures."
    elif intent == "group_standings":
        response = get_group_standings()
    else:
        response = "I'm sorry, I didn't understand that."

    return jsonify({"reply": response})


