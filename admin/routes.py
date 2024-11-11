from flask import Blueprint, request, redirect, url_for, session, render_template, flash
from flask_bcrypt import Bcrypt

from  utils.group_manager import GroupManager
from utils.tournament_manager import TournamentManager
from utils.fixture_manager import FixtureManager
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.database_connection import DatabaseConnection


bcrypt = Bcrypt()

admin_bp = Blueprint('admin_bp', __name__, template_folder='templates')

group_manager = GroupManager()
tournament_manager = TournamentManager()
fixture_manager = FixtureManager()

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Check if the user is already logged in
    if 'user_id' in session and session.get('is_admin'):
        flash("You are already logged in.", "info")
        return redirect(url_for('admin_bp.admin_dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Fetch the user from the database
        with DatabaseConnection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, password_hash, is_admin FROM admins WHERE username = %s", (username,))
            user = cur.fetchone()

        # Check if user exists and password matches
        if user and bcrypt.check_password_hash(user[1], password):
            is_admin = user[2]

            # Start a session and store user info
            session['user_id'] = user[0]
            session['username'] = username
            session['is_admin'] = is_admin

            # Check if the user is an admin
            if is_admin:
                flash("Logged in as admin successfully", "success")
                return redirect(url_for('admin_bp.admin_dashboard'))
            else:
                flash("You do not have admin privileges", "danger")
                return redirect(url_for('home'))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for('admin_bp.login'))
    return render_template('login.html')

@admin_bp.route('/admin_dashboard')
def admin_dashboard():
    # Only allow access if the user is logged in and is an admin
    if 'user_id' in session and session.get('is_admin'):
        return render_template("admin/dashboard.html")
    else:
        flash("Access denied", "danger")
        return redirect(url_for('admin_bp.login'))

@admin_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out", "info")
    return redirect(url_for('admin_bp.login'))


@admin_bp.route('/tournaments', methods=['GET', 'POST'])
def show_tournaments():
    if 'user_id' in session and session.get('is_admin'):
        if request.method == 'POST':
            if 'add_tournament' in request.form:  # Check if 'add_tournament' was in the form submission
                tournament_name = request.form.get('tournament_name')
                start_date = request.form.get('start_date')
                end_date = request.form.get('end_date')

                if tournament_name and start_date and end_date:
                    try:
                        tournament_manager.add_tournament(tournament_name, start_date, end_date)
                        flash("Tournament added successfully!", "success")
                    except Exception as e:
                        flash("Error adding tournament. Please try again.", "danger")
                        print(e)  # Log for debugging
                return redirect(url_for('admin_bp.show_tournaments'))

            # Handle tournament update
            tournament_id = request.form.get('tournament_id')
            tournament_name = request.form.get('tournament_name')
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')

            if tournament_id and tournament_name and start_date and end_date:
                try:
                    tournament_manager.update_tournament(tournament_name, start_date, end_date, tournament_id)
                    flash("Tournament updated successfully!", "success")
                except Exception as e:
                    flash("Error updating tournament. Please try again.", "danger")
                    print(e)  # Log for debugging
                return redirect(url_for('admin_bp.show_tournaments'))

        # Fetch all tournaments
        tournaments = []
        try:
            tournaments = tournament_manager.list_tournaments()
        except Exception as e:
            flash("Error fetching tournaments. Please try again.", "danger")
            print(e)  # Log for debugging

        return render_template('admin/tournaments.html', tournaments=tournaments)
    else:
        flash("Log in as admin to view tournaments", "danger")
        return redirect(url_for('admin_bp.login'))


@admin_bp.route('/tournaments/edit/<int:tournament_id>', methods=['POST'])
def delete_tournament(tournament_id):
    try:
        tournament_manager.delete_tournament(tournament_id)
        flash("Tournament deleted successfully.", "success")
    except Exception as e:
        flash("Error deleting tournament. Please try again.", "danger")
        print(e)  # For debugging; log errors in production

    return redirect(url_for('admin_bp.show_tournaments'))



@admin_bp.route('/teams', methods=['GET', 'POST'])
def show_teams():
    if 'user_id' in session and session.get('is_admin'):
        if request.method == 'POST':
            team_name = request.form.get('team_name')
            group_id = request.form.get('group_id')

            # Update team to assign it to a group
            if team_name and group_id:
                try:
                    group_manager.add_team_to_group(team_name=team_name, to_group=group_id)
                    flash("Team successfully assigned to group!", "success")
                except Exception as e:
                    flash("Error assigning team to group. Please try again.", "danger")
                    print(e)  # Log for debugging in production
                return redirect(url_for('admin_bp.show_teams'))

        # Fetch all teams and their groups
        teams = []
        try:
            teams = group_manager.list_teams_with_groups()
        except Exception as e:
            flash("Error fetching teams. Please try again.", "danger")
            print(e)  # Log error in production

        # Fetch all groups for the dropdown
        groups = []
        try:
            groups = group_manager.list_groups()
        except Exception as e:
            flash("Error fetching groups. Please try again.", "danger")
            print(e)  # Log error in production

        return render_template('admin/teams.html', teams=teams, groups=groups)
    else:
        flash("Log in as admin to view teams", "danger")
        return redirect(url_for('admin_bp.login'))


@admin_bp.route('/groups', methods=['GET', 'POST'])
def register_group():
    if 'user_id' in session and session.get('is_admin'):
        if request.method == 'POST':
            # Fetch the group name and tournament ID from the form
            group_name = request.form.get('group_name')
            tournament_id = request.form.get('tournament_id')  # Assuming dropdown selection for tournaments

            # Add the group to the database if a name and tournament are provided
            if group_name and tournament_id:
                try:
                    group_manager.add_group(group_name, tournament_id)
                    flash(f"Group '{group_name}' successfully registered!", "success")
                except Exception as e:
                    flash("Error registering group. Please try again.", "danger")
                    print(e)  # For debugging; log errors in console
                return redirect(url_for('admin_bp.register_group'))

        # Fetch all groups with their associated tournaments
        groups = []
        try:
            groups = group_manager.list_groups()
        except Exception as e:
            flash("Error fetching groups. Please try again.", "danger")
            print(e)  # For debugging; log errors in production

        # Fetch all tournaments for the dropdown
        tournaments = []
        try:
            tournaments = tournament_manager.list_tournaments()
        except Exception as e:
            flash("Error fetching tournaments. Please try again.", "danger")
            print(e)  # For debugging

        return render_template('admin/groups.html', groups=groups, tournaments=tournaments)
    else:
        flash("Log in as admin to view groups", "danger")
        return redirect(url_for('admin_bp.login'))


@admin_bp.route('/delete_group/<group_name>', methods=['POST'])
def delete_group(group_name):
    try:
        group_manager.delete_group(group_name)
        flash("Group deleted successfully.", "success")
    except Exception as e:
        flash("Error deleting group. Please try again.", "danger")
        print(e)  # For debugging; log errors in production

    return redirect(url_for('admin_bp.register_group'))


@admin_bp.route('/fixtures', methods=['GET', 'POST'])
def manage_fixtures():
    # Fetch tournaments

    tournaments = tournament_manager.list_tournaments()

    # Fetch teams and group them
    grouped_teams = {}
    teams_with_groups = group_manager.list_teams()

    for team in teams_with_groups:
        group_id = team['group_id'] or 'Not Assigned'  # Handle None group_id as "Not Assigned"

        # Initialize list if group_id is not in grouped_teams
        if group_id not in grouped_teams:
            grouped_teams[group_id] = []

        # Append team to the appropriate group
        grouped_teams[group_id].append({'team_id': team['team_id'], 'name': team['name']})


    # Fetch fixtures
    fixtures = []

    try:
        fixtures = fixture_manager.list_fixtures()
    except Exception as e:
        flash("Error fetching fixtures")
        print(e) # For Debugging

    return render_template('admin/fixtures.html', tournaments=tournaments, grouped_teams=grouped_teams, fixtures=fixtures)


@admin_bp.route('/add_fixture', methods=['POST'])
def add_fixture():
    fixture_date = request.form['fixture_date']
    tournament_id = int(request.form['tournament_id'])
    team1_id = request.form['team1_id']
    team2_id = request.form['team2_id']

    # Insert new fixture into the database
    fixture_manager.add_fixture(fixture_date=fixture_date, tournament_id=tournament_id, team1_id=team1_id, team2_id=team2_id)

    flash("Fixture added successfully!", "success")
    return redirect(url_for('admin_bp.manage_fixtures'))

# 2. Endpoint to Edit a Fixture
@admin_bp.route('/edit_fixture/<int:fixture_id>', methods=['GET', 'POST'])
def edit_fixture(fixture_id):
    # Handle POST request to update fixture
    if request.method == 'POST':
        fixture_date = request.form['fixture_date']
        tournament_id = request.form['tournament_id']
        team1_id = request.form['team1_id']
        team2_id = request.form['team2_id']

        with DatabaseConnection() as conn:
            cur = conn.cursor()
            cur.execute("""
                UPDATE fixtures
                SET fixture_date = %s, tournament_id = %s, team1_id = %s, team2_id = %s
                WHERE fixture_id = %s
            """, (fixture_date, tournament_id, team1_id, team2_id, fixture_id))
            conn.commit()

        flash("Fixture updated successfully!", "success")
        return redirect(url_for('admin_bp.manage_fixtures'))

    # Fetch fixture details for GET request to pre-fill form
    with DatabaseConnection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT fixture_id, fixture_date, tournament_id, team1_id, team2_id
            FROM fixtures
            WHERE fixture_id = %s
        """, (fixture_id,))
        fixture = cur.fetchone()

    return render_template('admin/edit_fixture.html', fixture=fixture)

# 3. Endpoint to Delete a Fixture
@admin_bp.route('/delete_fixture/<fixture_id>', methods=['POST'])
def delete_fixture(fixture_id):
    fixture_manager.delete_fixture(fixture_id)
    flash("Fixture deleted successfully!", "success")
    return redirect(url_for('admin_bp.manage_fixtures'))


# Endpoint to Display and Manage Scores
@admin_bp.route('/manage_scores', methods=['GET', 'POST'])
def manage_scores():

    # GET request: Display the list of fixtures with current scores

    fixtures = fixture_manager.list_fixtures()

    return render_template('admin/manage_scores.html', fixtures=fixtures)


# Endpoint to Update Scores
@admin_bp.route('/update_score/<int:fixture_id>', methods=['POST'])
def update_score(fixture_id):
    # Retrieve new scores from the form
    team1_score = request.form['team1_score']
    team2_score = request.form['team2_score']

    # Update scores in the database
    with DatabaseConnection() as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE scores_results 
            SET team1_score = %s, team2_score = %s 
            WHERE fixture_id = %s
        """, (team1_score, team2_score, fixture_id))
        conn.commit()

    flash("Score updated successfully!", "success")
    return redirect(url_for('admin_bp.manage_scores'))