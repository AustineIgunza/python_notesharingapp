import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Database
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    
    # Flask-Mail
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    
    # Site Configuration
    SITE_NAME = os.getenv('SITE_NAME', 'Notes Sharing App')
    SITE_URL = os.getenv('SITE_URL', 'http://localhost:5000')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
    
    # Security
    MIN_PASSWORD_LENGTH = int(os.getenv('MIN_PASSWORD_LENGTH', 4))
    ALLOWED_UPLOAD_EXTENSIONS = set(os.getenv('ALLOWED_UPLOAD_EXTENSIONS', 'pdf,docx,doc,png,jpg,jpeg,gif').split(','))
    MAX_UPLOAD_SIZE = int(os.getenv('MAX_UPLOAD_SIZE', 16777216))
    
    # Admin Whitelist
    ADMIN_EMAILS = set(os.getenv('ADMIN_EMAILS', 'admin12@gmail.com,austineigunza@gmail.com').split(','))
    
    # Session
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # File Uploads
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'app', 'uploads')
    UPLOAD_SUBFOLDER_DOCUMENTS = 'documents'
    UPLOAD_SUBFOLDER_IMAGES = 'images'
    UPLOAD_SUBFOLDER_NOTES = 'notes'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
