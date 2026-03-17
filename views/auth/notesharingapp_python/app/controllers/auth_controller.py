from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
from app import db, mail
from app.models import User, TwoFactorCode, RememberToken
from datetime import datetime, timedelta
import secrets
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.before_request
def before_request():
    """Check for remember token before each request"""
    if not current_user.is_authenticated and 'remember_token' in session:
        token_value = session.get('remember_token')
        token = RememberToken.query.filter_by(token=token_value).first()
        if token and not token.is_expired():
            login_user(token.user)
            return

@auth_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    """Sign in page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password', '')
        remember_me = request.form.get('remember_me') == 'on'
        admin_login = request.form.get('admin_login') == '1'
        
        # Validate input
        if not email or not password:
            flash('Email and password are required.', 'danger')
            return render_template('auth/signin.html')
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            flash('Invalid email or password.', 'danger')
            return render_template('auth/signin.html')
        
        if not user.is_active:
            flash('Your account has been deactivated.', 'danger')
            return render_template('auth/signin.html')
        
        # Check for admin login
        if admin_login:
            if not user.is_admin():
                flash('Admin access denied. You are not an administrator.', 'danger')
                return render_template('auth/signin.html')
            
            # Admin login - skip 2FA
            login_user(user, remember=remember_me)
            
            if remember_me:
                create_remember_token(user.id)
            
            return redirect(url_for('admin.dashboard'))
        
        # Regular user login - require 2FA
        # Generate OTP
        otp_code = str(secrets.randbelow(1000000)).zfill(6)
        expires_at = datetime.utcnow() + timedelta(minutes=10)
        
        two_fa = TwoFactorCode(
            user_id=user.id,
            code=otp_code,
            code_type='login',
            expires_at=expires_at,
            ip_address=request.remote_addr
        )
        db.session.add(two_fa)
        db.session.commit()
        
        # Send OTP via email
        send_otp_email(user.email, user.full_name, otp_code)
        
        # Store temporary session data
        session['temp_user_id'] = user.id
        session['temp_user_email'] = user.email
        session['temp_user_name'] = user.full_name
        session['temp_remember_me'] = remember_me
        
        flash(f'Verification code sent to {user.email}. Please check your email.', 'info')
        return redirect(url_for('auth.verify_2fa'))
    
    return render_template('auth/signin.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """Sign up page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        full_name = request.form.get('fullname', '').strip()
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validate input
        errors = []
        
        if not full_name or not re.match(r'^[a-zA-Z\s]+$', full_name):
            errors.append('Full name must contain only letters and spaces.')
        
        if not email or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors.append('Invalid email format.')
        
        # Check email domain
        email_domain = email.split('@')[1]
        allowed_domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'example.com', 'test.com']
        if email_domain not in allowed_domains:
            errors.append(f'Email domain must be one of: {", ".join(allowed_domains)}')
        
        if len(password) < current_app.config['MIN_PASSWORD_LENGTH']:
            errors.append(f'Password must be at least {current_app.config["MIN_PASSWORD_LENGTH"]} characters.')
        
        if password != confirm_password:
            errors.append('Passwords do not match.')
        
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered.')
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('auth/signup.html')
        
        # Create user
        user = User(full_name=full_name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Account created successfully! Please sign in.', 'success')
        return redirect(url_for('auth.signin'))
    
    return render_template('auth/signup.html')

@auth_bp.route('/verify-2fa', methods=['GET', 'POST'])
def verify_2fa():
    """Verify 2FA code"""
    if 'temp_user_id' not in session:
        flash('Invalid session. Please sign in again.', 'danger')
        return redirect(url_for('auth.signin'))
    
    if request.method == 'POST':
        code = request.form.get('verification_code', '').strip()
        
        if not code:
            flash('Please enter the verification code.', 'danger')
            return render_template('auth/verify_2fa.html')
        
        # Find the OTP
        two_fa = TwoFactorCode.query.filter(
            TwoFactorCode.user_id == session['temp_user_id'],
            TwoFactorCode.code_type == 'login'
        ).order_by(TwoFactorCode.created_at.desc()).first()
        
        if not two_fa:
            flash('No verification code found. Please sign in again.', 'danger')
            return redirect(url_for('auth.signin'))
        
        if two_fa.is_expired():
            db.session.delete(two_fa)
            db.session.commit()
            flash('Verification code has expired. Please sign in again.', 'danger')
            return redirect(url_for('auth.signin'))
        
        if two_fa.code != code:
            two_fa.attempts_used += 1
            db.session.commit()
            
            if two_fa.attempts_used >= 3:
                db.session.delete(two_fa)
                db.session.commit()
                flash('Too many incorrect attempts. Please sign in again.', 'danger')
                return redirect(url_for('auth.signin'))
            
            flash('Invalid verification code.', 'danger')
            return render_template('auth/verify_2fa.html')
        
        # Code is valid
        user = User.query.get(session['temp_user_id'])
        login_user(user, remember=session.get('temp_remember_me', False))
        
        if session.get('temp_remember_me'):
            create_remember_token(user.id)
        
        # Clean up session
        db.session.delete(two_fa)
        db.session.commit()
        session.pop('temp_user_id', None)
        session.pop('temp_user_email', None)
        session.pop('temp_user_name', None)
        session.pop('temp_remember_me', None)
        
        flash('Signed in successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('auth/verify_2fa.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Sign out"""
    logout_user()
    session.clear()
    flash('You have been signed out.', 'success')
    return redirect(url_for('main.index'))

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').lower().strip()
        
        user = User.query.filter_by(email=email).first()
        if user:
            # Generate reset code
            reset_code = str(secrets.randbelow(1000000)).zfill(6)
            expires_at = datetime.utcnow() + timedelta(minutes=30)
            
            two_fa = TwoFactorCode(
                user_id=user.id,
                code=reset_code,
                code_type='password_reset',
                expires_at=expires_at,
                ip_address=request.remote_addr
            )
            db.session.add(two_fa)
            db.session.commit()
            
            # Send reset code via email
            send_password_reset_email(user.email, user.full_name, reset_code)
        
        # Always show success message for security
        flash('If an account exists with that email, a password reset code has been sent.', 'info')
        return render_template('auth/forgot_password.html')
    
    return render_template('auth/forgot_password.html')

@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    """Reset password page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').lower().strip()
        code = request.form.get('code', '').strip()
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('User not found.', 'danger')
            return render_template('auth/reset_password.html')
        
        # Find reset code
        two_fa = TwoFactorCode.query.filter(
            TwoFactorCode.user_id == user.id,
            TwoFactorCode.code_type == 'password_reset'
        ).order_by(TwoFactorCode.created_at.desc()).first()
        
        if not two_fa or two_fa.code != code:
            flash('Invalid reset code.', 'danger')
            return render_template('auth/reset_password.html')
        
        if two_fa.is_expired():
            db.session.delete(two_fa)
            db.session.commit()
            flash('Reset code has expired.', 'danger')
            return render_template('auth/reset_password.html')
        
        if new_password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/reset_password.html')
        
        if len(new_password) < current_app.config['MIN_PASSWORD_LENGTH']:
            flash(f'Password must be at least {current_app.config["MIN_PASSWORD_LENGTH"]} characters.', 'danger')
            return render_template('auth/reset_password.html')
        
        # Update password
        user.set_password(new_password)
        db.session.delete(two_fa)
        db.session.commit()
        
        flash('Password reset successfully! Please sign in.', 'success')
        return redirect(url_for('auth.signin'))
    
    return render_template('auth/reset_password.html')

def send_otp_email(email, name, otp_code):
    """Send OTP email"""
    msg = Message(
        subject='Your Login Verification Code - Notes Sharing App',
        recipients=[email],
        html=f"""
        <div style='font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;'>
            <div style='background: #007bff; color: white; padding: 20px; text-align: center;'>
                <h2>🔐 Login Verification Code</h2>
            </div>
            <div style='padding: 30px; background: #f8f9fa;'>
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
    )
    mail.send(msg)

def send_password_reset_email(email, name, reset_code):
    """Send password reset email"""
    msg = Message(
        subject='Password Reset Code - Notes Sharing App',
        recipients=[email],
        html=f"""
        <div style='font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;'>
            <div style='background: #ff6b6b; color: white; padding: 20px; text-align: center;'>
                <h2>🔑 Password Reset Code</h2>
            </div>
            <div style='padding: 30px; background: #f8f9fa;'>
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
    )
    mail.send(msg)

def create_remember_token(user_id):
    """Create remember me token"""
    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(days=30)
    
    remember_token = RememberToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at,
        device_info=request.headers.get('User-Agent', ''),
        ip_address=request.remote_addr
    )
    db.session.add(remember_token)
    db.session.commit()
    
    session['remember_token'] = token
