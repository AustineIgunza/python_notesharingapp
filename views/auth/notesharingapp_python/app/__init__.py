from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import config
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.signin'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Create upload directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_SUBFOLDER_DOCUMENTS']), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_SUBFOLDER_IMAGES']), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_SUBFOLDER_NOTES']), exist_ok=True)
    
    # Register blueprints
    from app.controllers.auth_controller import auth_bp
    from app.controllers.notes_controller import notes_bp
    from app.controllers.admin_controller import admin_bp
    from app.controllers.main_controller import main_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(main_bp)
    
    # Database context
    with app.app_context():
        db.create_all()
    
    return app
