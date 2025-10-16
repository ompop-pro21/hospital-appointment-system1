import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

load_dotenv() 

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)

    # This code works perfectly both locally and on Render
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    # This is the corrected line that ensures Postgres is always used on Render
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

    # This is the corrected mail configuration for reliable sending
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    login_manager.login_view = 'auth.login'

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # --- Register All Blueprints ---
    from .auth.routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .admin.routes import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)
    
    from .doctor.routes import doctor_bp as doctor_blueprint
    app.register_blueprint(doctor_blueprint)

    return app
