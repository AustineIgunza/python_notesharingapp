import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    """FastAPI Configuration Settings"""
    
    # App Settings
    APP_NAME: str = "Notes Sharing App"
    DEBUG: bool = os.getenv('DEBUG', 'True').lower() == 'true'
    ENVIRONMENT: str = os.getenv('ENVIRONMENT', 'development')
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_PORT: int = int(os.getenv('DB_PORT', 3306))
    DB_USER: str = os.getenv('DB_USER', 'root')
    DB_PASS: str = os.getenv('DB_PASS', 'root')
    DB_NAME: str = os.getenv('DB_NAME', 'notesharingapp_python')
    
    DATABASE_URL: str = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # Email (SMTP)
    MAIL_SERVER: str = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT: int = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS: bool = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME: str = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD: str = os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER: str = os.getenv('MAIL_DEFAULT_SENDER', '')
    
    # Site Configuration
    SITE_NAME: str = os.getenv('SITE_NAME', 'Notes Sharing App')
    SITE_URL: str = os.getenv('SITE_URL', 'http://localhost:8000')
    ADMIN_EMAIL: str = os.getenv('ADMIN_EMAIL', 'admin@notesharingapp.com')
    
    # Security
    MIN_PASSWORD_LENGTH: int = int(os.getenv('MIN_PASSWORD_LENGTH', 4))
    ALLOWED_UPLOAD_EXTENSIONS: set = set(
        os.getenv('ALLOWED_UPLOAD_EXTENSIONS', 'pdf,docx,doc,png,jpg,jpeg,gif').split(',')
    )
    MAX_UPLOAD_SIZE: int = int(os.getenv('MAX_UPLOAD_SIZE', 16777216))  # 16MB
    
    # Admin Whitelist
    ADMIN_EMAILS: set = set(
        os.getenv('ADMIN_EMAILS', 'admin12@gmail.com,austineigunza@gmail.com').split(',')
    )
    
    # Session
    REMEMBER_ME_DAYS: int = 30
    
    # File Uploads
    UPLOAD_FOLDER: str = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    UPLOAD_SUBFOLDER_DOCUMENTS: str = 'documents'
    UPLOAD_SUBFOLDER_IMAGES: str = 'images'
    UPLOAD_SUBFOLDER_NOTES: str = 'notes'
    
    class Config:
        env_file = ".env"

# Create settings instance
settings = Settings()
