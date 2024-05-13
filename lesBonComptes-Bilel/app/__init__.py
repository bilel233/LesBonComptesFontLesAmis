from flask import Flask
import os
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .models.user import db
from .routes.auth import auth_blueprint, facebook_blueprint
from .routes.expense import expenses_blueprint
from .routes.group import group_blueprint
from .routes.reimbursement import reimbursement_blueprint
from .routes.payment import payment_blueprint
from .routes.message import messaging_blueprint
from .routes.export import export_blueprint
from .routes.statistics import statistics_blueprint


from dotenv import load_dotenv

load_dotenv()
def create_app():
    app = Flask(__name__)
    CORS(app)
    app.secret_key = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    # Configuration de MongoDB
    app.config['MONGODB_SETTINGS'] = {
        'host': os.getenv('MONGODB_URI')
    }
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')

    db.init_app(app)
    JWTManager(app)

    # Les enregistrements des bluesprints
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(group_blueprint, url_prefix='/group')
    app.register_blueprint(expenses_blueprint, url_prefix='/expenses')
    app.register_blueprint(reimbursement_blueprint, url_prefix='/reimbursement')
    app.register_blueprint(payment_blueprint, url_prefix='/payment')
    app.register_blueprint(messaging_blueprint, url_prefix='/messaging')
    app.register_blueprint(export_blueprint, url_prefix='/export')
    app.register_blueprint(statistics_blueprint, url_prefix='/statistics')
    app.register_blueprint(facebook_blueprint, url_prefix='/login')

    return app
