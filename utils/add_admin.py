from flask import Flask
from database_connection import DatabaseConnection
from flask_bcrypt import Bcrypt

app = Flask(__name__)

bcrypt = Bcrypt(app)

class AddAdmin:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

        hashed_password = bcrypt.generate_password_hash(self.password).decode('utf-8')


        with DatabaseConnection() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO admins(username, email, password_hash) VALUES (%s, %s, %s)", (self.username, self.email, hashed_password))



admin1 = AddAdmin("admin", "admin123", "admin@tevisa.com")