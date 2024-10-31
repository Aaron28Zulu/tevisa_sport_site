from flask_bcrypt import Bcrypt
from .routes import admin_bp

bcrypt = Bcrypt()

def init_app(app):
    bcrypt.init_app(app)  # Initialize bcrypt with the app
    app.register_blueprint(admin_bp, url_prefix='/admin')
