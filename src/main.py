from flask import Flask, jsonify
from marshmallow.exceptions import ValidationError
from flask_sqlalchemy import  SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    from dotenv import load_dotenv
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object('default_settings.app_config')

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    from models.User import get_user
    @login_manager.user_loader
    def load_user(user_id):
        return get_user(user_id)

    from commands import db_commands
    app.register_blueprint(db_commands)

    from controllers import registerable_controllers
    for controller in registerable_controllers:
        app.register_blueprint(controller)
    
    @app.errorhandler(ValidationError)
    def handle_bad_request(error):  
        return(jsonify(error.messages), 400)

    @app.errorhandler(500)
    def handle_500(error):
        app.logger.error(error)
        return ("Server error: AKA bad stuff", 500)

    return app