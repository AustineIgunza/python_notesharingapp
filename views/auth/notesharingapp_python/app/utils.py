"""
Utility functions for authentication, hashing, email, etc.
"""

import os
import secrets
import smtplib
import re
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from passlib.context import CryptContext
from typing import Optional

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

# ============ OTP and Token Generation ============

def generate_otp() -> str:
    """Generate a 6-digit OTP"""
    return str(secrets.randbelow(1000000)).zfill(6)

def generate_token(length: int = 32) -> str:
    """Generate a secure random token"""
    return secrets.token_urlsafe(length)

# ============ Admin Check ============

ADMIN_EMAILS = set(os.getenv('ADMIN_EMAILS', 'admin12@gmail.com,austineigunza@gmail.com').split(','))

def is_admin_email(email: str) -> bool:
    """Check if email is in admin whitelist"""
    return email.lower().strip() in ADMIN_EMAILS

# ============ Email Validation ============

def is_valid_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_domain(email: str) -> bool:
    """Check if email domain is whitelisted"""
    allowed_domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'example.com', 'test.com']
    domain = email.split('@')[1].lower()
    return domain in allowed_domains

def is_valid_full_name(name: str) -> bool:
    """Check if full name contains only letters and spaces"""
    return re.match(r'^[a-zA-Z\s]+$', name) is not None

# ============ Email Sending ============

def send_otp_email(email: str, name: str, otp_code: str) -> bool:
    """Send OTP email via Gmail SMTP"""
    try:
        mail_server = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
        mail_port = int(os.getenv('MAIL_PORT', 587))
        mail_username = os.getenv('MAIL_USERNAME')
        mail_password = os.getenv('MAIL_PASSWORD')
        
        if not all([mail_username, mail_password]):
            print("Email credentials not configured")
            return False
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = mail_username
        msg['To'] = email
        msg['Subject'] = 'Your Login Verification Code - Notes Sharing App'
        
        html_body = f"""
        <div style='font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;'>
            <div style='background: #007bff; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0;'>
                <h2>🔐 Login Verification Code</h2>
            </div>
            <div style='padding: 30px; background: #f8f9fa; border-radius: 0 0 5px 5px;'>
                <h3>Hello {name}!</h3>
                <p>Your verification code for logging into <strong>Notes Sharing App</strong> is:</p>
                <div style='text-align: center; margin: 30px 0;'>
                    <div style='background: #28a745; color: white; padding: 15px 30px; font-size: 24px; font-weight: bold; border-radius: 5px; display: inline-block; letter-spacing: 3px;'>
                        {otp_code}
                    </div>
                </div>
                <p style='color: #666;'>This code will expire in 10 minutes.</p>
                <p style='color: #666; font-size: 12px;'>If you didn't request this code, please ignore this email.</p>
            </div>
        </div>
        """
        
        msg.attach(MIMEText(html_body, 'html'))
        
        # Send email
        server = smtplib.SMTP(mail_server, mail_port)
        server.starttls()
        server.login(mail_username, mail_password)
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_password_reset_email(email: str, name: str, reset_code: str) -> bool:
    """Send password reset email via Gmail SMTP"""
    try:
        mail_server = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
        mail_port = int(os.getenv('MAIL_PORT', 587))
        mail_username = os.getenv('MAIL_USERNAME')
        mail_password = os.getenv('MAIL_PASSWORD')
        
        if not all([mail_username, mail_password]):
            print("Email credentials not configured")
            return False
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = mail_username
        msg['To'] = email
        msg['Subject'] = 'Password Reset Code - Notes Sharing App'
        
        html_body = f"""
        <div style='font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;'>
            <div style='background: #ff6b6b; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0;'>
                <h2>🔑 Password Reset Code</h2>
            </div>
            <div style='padding: 30px; background: #f8f9fa; border-radius: 0 0 5px 5px;'>
                <h3>Hello {name}!</h3>
                <p>You requested a password reset. Your reset code is:</p>
                <div style='text-align: center; margin: 30px 0;'>
                    <div style='background: #ffc107; color: black; padding: 15px 30px; font-size: 24px; font-weight: bold; border-radius: 5px; display: inline-block; letter-spacing: 3px;'>
                        {reset_code}
                    </div>
                </div>
                <p style='color: #666;'>This code will expire in 30 minutes.</p>
                <p style='color: #666; font-size: 12px;'>If you didn't request this, please ignore this email and your password will remain unchanged.</p>
            </div>
        </div>
        """
        
        msg.attach(MIMEText(html_body, 'html'))
        
        # Send email
        server = smtplib.SMTP(mail_server, mail_port)
        server.starttls()
        server.login(mail_username, mail_password)
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
