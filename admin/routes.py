from flask import Blueprint, request, redirect, url_for, session, render_template, flash
from flask_bcrypt import Bcrypt
import psycopg2
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.database_connection import DatabaseConnection

bcrypt = Bcrypt()

admin_bp = Blueprint('admin_bp', __name__, template_folder='templates')


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
        return "Welcome to the Admin Dashboard"
    else:
        flash("Access denied", "danger")
        return redirect(url_for('admin_bp.login'))

@admin_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out", "info")
    return redirect(url_for('admin_bp.login'))
