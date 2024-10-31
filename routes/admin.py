# routes/admin.py
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import admin
from models import db, Team, Group, Match, KnockoutMatch, Institution
from forms import TeamRegistrationForm  # Assuming admin can manage teams
from datetime import datetime
from utils import assign_teams_to_groups, calculate_group_standings, setup_knockout_stage, progress_knockout_stage
from sqlalchemy.exc import SQLAlchemyError

from forms import KnockoutMatchUpdateForm

def admin_required(f):
    from functools import wraps
    from flask import abort

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@admin.route('/admin/dashboard')
@login_required
@admin_required
def dashboard():
    institutions = Institution.query.all()
    return render_template('admin/dashboard.html', institutions=institutions)


@admin.route('/admin/manage_fixtures', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_fixtures():
    # Logic to create and manage fixtures
    if request.method == 'POST':
        try:
            # Example: Create a new match
            home_team_id = request.form.get('home_team')
            away_team_id = request.form.get('away_team')
            date_str = request.form.get('date')
            round_ = request.form.get('round')
            date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')  # Adjusted for HTML datetime-local input
            match = Match(
                home_team_id=home_team_id,
                away_team_id=away_team_id,
                date=date,
                round=round_
            )
            db.session.add(match)
            db.session.commit()
            flash('Match fixture created successfully!', 'success')
        except ValueError:
            flash('Invalid date format. Please use the correct format.', 'danger')
        except SQLAlchemyError:
            db.session.rollback()
            flash('An error occurred while creating the match fixture.', 'danger')
        return redirect(url_for('admin.manage_fixtures'))
    matches = Match.query.order_by(Match.date.asc()).all()
    teams = Team.query.all()
    return render_template('admin/manage_fixtures.html', matches=matches, teams=teams)


@admin.route('/admin/update_match/<int:match_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def update_match(match_id):
    match = Match.query.get_or_404(match_id)
    if request.method == 'POST':
        try:
            score_home = int(request.form.get('score_home'))
            score_away = int(request.form.get('score_away'))
            match.score_home = score_home
            match.score_away = score_away

            # Update team statistics
            home_team = match.home_team
            away_team = match.away_team

            home_team.matches_played += 1
            away_team.matches_played += 1
            home_team.goals_for += score_home
            home_team.goals_against += score_away
            away_team.goals_for += score_away
            away_team.goals_against += score_home

            if score_home > score_away:
                home_team.wins += 1
                away_team.losses += 1
                home_team.points += 3
            elif score_home < score_away:
                away_team.wins += 1
                home_team.losses += 1
                away_team.points += 3
            else:
                home_team.draws += 1
                away_team.draws += 1
                home_team.points += 1
                away_team.points += 1

            db.session.commit()
            flash('Match updated successfully!', 'success')
        except ValueError:
            flash('Scores must be integer values.', 'danger')
        except SQLAlchemyError:
            db.session.rollback()
            flash('An error occurred while updating the match.', 'danger')
        return redirect(url_for('admin.manage_fixtures'))
    return render_template('admin/update_match.html', match=match)


@admin.route('/admin/assign_groups', methods=['POST'])
@login_required
@admin_required
def assign_groups():
    try:
        assign_teams_to_groups()
        flash('Teams have been assigned to groups successfully!', 'success')
    except ValueError as ve:
        flash(str(ve), 'danger')
    except SQLAlchemyError:
        db.session.rollback()
        flash('An error occurred while assigning teams to groups.', 'danger')
    return redirect(url_for('admin.dashboard'))


@admin.route('/admin/calculate_standings')
@login_required
@admin_required
def calculate_standings_route():
    try:
        standings = calculate_group_standings()
        return render_template('admin/standings.html', standings=standings)
    except Exception as e:
        flash('An error occurred while calculating standings.', 'danger')
        return redirect(url_for('admin.dashboard'))


@admin.route('/admin/setup_knockout', methods=['POST'])
@login_required
@admin_required
def setup_knockout():
    try:
        quarter_finals = setup_knockout_stage()
        flash('Quarter-Finals have been set up successfully!', 'success')
        return redirect(url_for('admin.knockout_stage'))
    except ValueError as ve:
        flash(str(ve), 'danger')
    except SQLAlchemyError:
        db.session.rollback()
        flash('An error occurred while setting up knockout stages.', 'danger')
    return redirect(url_for('admin.dashboard'))


@admin.route('/admin/knockout_stage')
@login_required
@admin_required
def knockout_stage():
    knockout_matches = KnockoutMatch.query.order_by(KnockoutMatch.round.asc()).all()
    return render_template('admin/knockout_stage.html', knockout_matches=knockout_matches)


@admin.route('/admin/progress_knockout/<current_round>', methods=['POST'])
@login_required
@admin_required
def progress_knockout(current_round):
    try:
        new_matches = progress_knockout_stage(current_round)
        flash(f'{current_round} has been progressed to the next round!', 'success')
    except ValueError as ve:
        flash(str(ve), 'danger')
    except SQLAlchemyError:
        db.session.rollback()
        flash('An error occurred while progressing knockout stages.', 'danger')
    return redirect(url_for('admin.knockout_stage'))

@admin.route('/admin/update_knockout_match/<int:match_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def update_knockout_match(match_id):
    match = KnockoutMatch.query.get_or_404(match_id)
    form = KnockoutMatchUpdateForm()
    if form.validate_on_submit():
        try:
            winner_id = form.winner.data
            if winner_id not in [match.team1_id, match.team2_id]:
                flash('Invalid winner selection.', 'danger')
                return redirect(url_for('admin.knockout_stage'))
            match.winner_id = winner_id
            db.session.commit()
            flash('Winner updated successfully!', 'success')
        except SQLAlchemyError:
            db.session.rollback()
            flash('An error occurred while updating the winner.', 'danger')
        return redirect(url_for('admin.knockout_stage'))
    elif request.method == 'GET':
        form.winner.choices = [
            (match.team1.id, match.team1.name),
            (match.team2.id, match.team2.name)
        ]
    return render_template('admin/update_knockout_match.html', match=match, form=form)