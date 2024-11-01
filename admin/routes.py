from flask import Blueprint, request, redirect, url_for, session, render_template, flash
from flask_bcrypt import Bcrypt
from  utils.groupmanager import GroupManager
from utils.tournament_manager import TournamentManager
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.database_connection import DatabaseConnection


bcrypt = Bcrypt()

admin_bp = Blueprint('admin_bp', __name__, template_folder='templates')

group_manager = GroupManager()
tournament_manager = TournamentManager()


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
                flash("You do not have admin privileges", "warning")
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
    if request.method == 'POST':
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


@admin_bp.route('/tournaments/edit/<int:tournament_id>', methods=['GET', 'POST'])
def edit_tournament(tournament_id):
    if request.method == 'POST':
        # Pass placeholder
        flash("Tournament updated successfully", "success")
        return redirect(url_for('admin_bp.show_tournaments'))

    # Pass placeholder
    return render_template('admin/edit_tournament.html', tournament={"id": tournament_id, "name": "Sample Tournament"})



@admin_bp.route('/teams', methods=['GET', 'POST'])
def show_teams():
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


@admin_bp.route('/record_performance', methods=['GET', 'POST'])
def record_performance():
    if request.method == 'POST':
        # Pass placeholder
        flash("Performance recorded successfully", "success")
        return redirect(url_for('admin_bp.record_performance'))

    # Pass placeholder with sample data for dropdown
    teams = [(1, "Team A"), (2, "Team B")]
    return render_template('admin/record_performance.html', teams=teams)


@admin_bp.route('/groups', methods=['GET', 'POST'])
def register_group():
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


@admin_bp.route('/delete_group/<group_name>', methods=['POST'])
def delete_group(group_name):
    try:
        group_manager.delete_group(group_name)
        flash("Group deleted successfully.", "success")
    except Exception as e:
        flash("Error deleting group. Please try again.", "danger")
        print(e)  # For debugging; log errors in production

    return redirect(url_for('admin_bp.register_group'))
