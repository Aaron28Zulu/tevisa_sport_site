from flask import Flask, render_template, redirect, request, url_for, flash, jsonify
from flask_bcrypt import Bcrypt
from psycopg2.errors import UniqueViolation
import spacy
import random

from admin import init_app as init_admin_blueprint
from admin.routes import tournament_manager, group_manager, fixture_manager

from utils.database_connection import DatabaseConnection
from utils.tournament_manager import TournamentManager


app = Flask(__name__)
app.secret_key = "just a dummy key"

bcrypt = Bcrypt(app)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# try:
#     # Connection to Database | DatabaseConnection as context manager
#     with DatabaseConnection() as connection:
#
#         cursor = connection.cursor()
#
#         cursor.execute("SELECT version();")
#         record = cursor.fetchone()
#
#         print("You are connected to - ", record, "\n")
#
# except (Exception, psycopg2.Error) as error:
#     print("Error while connecting to Database", error)


INSTITUTIONS = {
    'ZUT': 'Zambia University of Technology',
    'ZAST': 'Zambia Air Services Training',
    'NORTEC': 'Northern Technical College',
    'EVHONE': 'Evelyn Hone College',
    'LBTC': 'Lusaka Business And Technical College',
    'NIC': 'Nkumbi International College',
    'LIBES': 'Livingstone institute of Business And Engineering Studies',
    'COTBC': 'Copperbelt Technical Business College',
    'MATTI': 'Mansa Trades Training institute',
    'MOTTI': 'Mongu Trades Training Institute',
    'CHTTI': 'Chipata Trades Training Institute',
    'SOTTI': 'Solwezi Trades Training Institute',
    'PETTI': 'Pemba Trades Training Institute',
    'KATTI': 'Kaoma Trades Training institute',
    'NCTTI': 'Nchanga Trades Training Institute',
    'KVTC': 'Kitwe Vocational Training Centre',
    'KIT': 'Kabwe Institue Of Technology',
    'LTBT': 'Luanshya Technical and business Training',
    'CHITTI': 'Chinsali Trades Training Institute',
    'ZIBST': 'Zambia Institute Of Business Studies and Technology',
    'MTC': 'Mufulira Technical College',
    'CU': 'Cavendish University',
    'CHRESO': 'Chreso University',
    'ZASTI': 'Zambia Air Services Training Institute'
}

def main() -> None:

    init_admin_blueprint(app)

    @app.route('/')
    def home():
        return render_template('./public/index.html')


    @app.route('/about')
    def about():
        return render_template('./public/about.html')


    @app.route('/inst_registration', methods=['GET', 'POST'])
    def add_institution():
        if request.method == 'POST':
            institution_name = request.form['Institution']
            institution_town = request.form['institution_town']

            record_to_insert = (institution_name, institution_town)

            try:
                with DatabaseConnection() as connect:
                    cur = connect.cursor()
                    cur.execute('SELECT * FROM institution')
                    if not cur.fetchall():
                        cur.execute("""
                        ALTER SEQUENCE public.institution_institution_id_seq RESTART WITH 1
                        """)

                    else:
                        cur.execute("""
                                    SELECT setval('public.institution_institution_id_seq', 
                                    (SELECT COALESCE(MAX(institution_id), 1) FROM institution))
                                    """)

                    insert_query = """INSERT INTO institution(institution_name, institution_town ) VALUES(%s, %s)"""

                    cur.execute(insert_query, record_to_insert)
                flash(f"{institution_name} successfully registered!", "success")

            except UniqueViolation as e:

                flash(f"{institution_name} is already registered!", "danger")

            return redirect(url_for('add_team'))
        else:
            return render_template('./public/registration.html', INSTITUTIONS=INSTITUTIONS)


    @app.route('/team_registration', methods=['GET', 'POST'])
    def add_team():
        if request.method == 'GET':
            tournaments = tournament_manager.list_tournaments()
            return render_template('./public/team_register.html', INSTITUTIONS=INSTITUTIONS, tournaments=tournaments)
        else:
            team_name = request.form['team_name']
            institution = request.form['Institution']
            coach_name = request.form['coach']
            tournament_entry = request.form['tournament']

            with DatabaseConnection() as connect:
                cur = connect.cursor()
                cur.execute("SELECT * FROM coach")
                if not cur.fetchall():
                    cur.execute("ALTER SEQUENCE public.coach_coach_id_seq RESTART WITH 1")

                # noinspection PyBroadException
                try:
                    cur.execute(f"INSERT INTO coach(coach_name) VALUES('{coach_name}');")
                except:
                    # return f'Coach with name, ({coach_name}) already exists. Enter team details and Leave Blank'
                    pass

            try:
                with DatabaseConnection() as connect:
                    cur = connect.cursor()

                    cur.execute("""
                                SELECT setval('public.coach_coach_id_seq', 
                                (SELECT COALESCE(MAX(coach_id), 1) FROM coach))
                                """)

                    cur.execute(f"SELECT coach_id FROM coach WHERE coach_name='{coach_name}'")
                    coach_id = cur.fetchone()[0]

                    # noinspection PyBroadException
                    try:
                        cur.execute(f"SELECT institution_id FROM institution WHERE institution_name='{institution}'")
                        institution_id = cur.fetchone()[0]
                    except Exception:
                        flash("Institution not registered!", "danger")
                        return redirect(url_for('add_team'))

                    cur.execute(f"SELECT tournament_id FROM tournament WHERE tournament_name='{tournament_entry}'")
                    tournament_id = cur.fetchone()[0]

                    # return f'{str(coach_id)}<br>{institution_id}<br>{tournament_id}'


                    record_to_insert = (team_name, institution_id, coach_id, tournament_id) # tournament_id -> 2
                    # #
                    insert_query = """INSERT INTO teams(team_name, institution_id, coach_id, tournament_id) VALUES(%s, %s, %s, %s)"""

                    cur.execute("SELECT * FROM teams")
                    if not cur.fetchall():
                        cur.execute("ALTER SEQUENCE public.teams_team_id_seq RESTART WITH 1")
                    try:
                        cur.execute(insert_query, record_to_insert)
                        flash(f"{team_name} added successfully!", "success")
                    except Exception as error:
                        print(error)
                        flash(f"{team_name} alread exist", "danger")
                    return redirect(url_for('add_player'))
            except Exception as e:
                print(e)
                return redirect(url_for('add_player'))

    # noinspection PyBroadException
    @app.route('/player_registration', methods=['GET', 'POST'])
    def add_player():
        if request.method == 'GET':
            teams = group_manager.list_teams()
            return render_template('./public/player_registration.html', teams = teams)
        else:
            player_name = request.form['player']
            player_age = request.form['age']
            player_gender = request.form['gender']
            player_team = request.form['team']

            with DatabaseConnection() as connect:
                cur = connect.cursor()
                try:
                    cur.execute(f"SELECT team_id FROM teams WHERE team_name='{player_team}'")
                    team_id = cur.fetchone()[0]
                except Exception:
                    return f'<i>{player_team}</i> is not registered<br />Can&apos;t register player'

                record_to_insert = (player_name, team_id, player_gender, player_age)

                insert_query = """INSERT INTO players(player_name, team_id, player_gender, age) VALUES(%s, %s, %s, %s)"""
                cur.execute("SELECT * FROM players")
                if not cur.fetchall():
                    cur.execute("""
                    ALTER SEQUENCE public.players_player_id_seq RESTART WITH 1                
                    """)
                cur.execute(insert_query, record_to_insert)

                flash(f"{player_name} added successfully", "success")

                return redirect(url_for('add_player'))



    @app.route('/tournaments')
    def show_tournaments():
        pass


    @app.route('/tournaments/<int:tournament_id>')
    def tournament():
        pass


    @app.route('/sports')
    def sport():
        try:
            fixtures = fixture_manager.list_fixtures()
            game_results = fixture_manager.get_game_results()
            game_standings = group_manager.get_group_standings()
            tournaments = tournament_manager.list_tournaments()

            return render_template('./public/sports.html',
                                   fixtures=fixtures,
                                   game_results=game_results,
                                   game_standings=game_standings,
                                   tournaments=tournaments)
        except Exception as e:
            print(e)
        return render_template('./public/sports.html')


    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('./public/errors/404.html'), 404


    ## ChatBot

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
            ORDER BY f.fixture_date DESC;
            """
            cursor.execute(query, (team_name, team_name))

            # print(cursor.fetchone())
            result = cursor.fetchone()


        if result:
            text = [
                    "Regarding the recent game,",
                    "Concerning the recent match,",
                    "In terms of the latest game,",
                    "About the recent match,",
                    "On the topic of the latest game,",
                    "With respect to the recent game,",
                    "Speaking of the recent match,",
                    "Turning to the latest game,",
                    "Looking at the recent game,",
                    "As for the latest match,",
                "Proceeding with the recent game,"
                ]
            output = f"{random.choice(text)} {result[1]} vs {result[3]} came out {result[2]} - {result[4]}"
            return output
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
            [
                f"{result[0]} - {result[5]} points, {result[1]} played, {result[2]} won, {result[3]} drawn, {result[4]} lost"
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
        # Convert the message to uppercase to allow for case-insensitive matching
        message_upper = message.upper()

        TEAM_NAMES = []
        for team in group_manager.list_teams():
            TEAM_NAMES.append(team['name'])

        # Check if any team name is present in the message
        for team in TEAM_NAMES:
            if team in message_upper:
                return team  # Return the team name as soon as it's found

        return None

    # Chatbot endpoint
    @app.route('/chatbot', methods=['POST'])
    def chatbot():
        user_message = request.json.get("message")
        intent = detect_intent(user_message)

        if intent == "match_result":
            team_name = extract_team_name(user_message)
            response = get_match_result(team_name) if team_name else "Please specify a team name for match results."
        elif intent == "upcoming_fixtures":
            team_name = extract_team_name(user_message)
            response = get_upcoming_fixtures(
                team_name) if team_name else "Please specify a team name for upcoming fixtures."
        elif intent == "group_standings":
            response = get_group_standings()
        else:
            response = "I'm sorry, I didn't understand that."

        return jsonify({"reply": response})


if __name__ == '__main__':
    admin = TournamentManager()
    # admin.insert_tournament(('ZUT TNMT', '2024-12-16', '2024-12-28',))
    # admin.delete_tournament('Youth Tournament')
    main()
    app.run(debug=True)