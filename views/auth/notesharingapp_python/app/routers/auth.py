"""
Authentication router - Login, signup, 2FA, password reset
"""

from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.db import User, TwoFactorCode, RememberToken
from app import utils
import secrets

router = APIRouter()

def get_db():
    from main import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============ SIGNIN ============

@router.get("/signin", response_class=HTMLResponse)
async def signin_page(request: Request):
    """Sign in page"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse("auth/signin.html", {"request": request})

@router.post("/signin", response_class=HTMLResponse)
async def signin(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    remember_me: bool = Form(False),
    admin_login: bool = Form(False),
    db: Session = Depends(get_db)
):
    """Handle sign in"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="templates")
    
    email = email.lower().strip()
    
    # Validate input
    if not email or not password:
        return templates.TemplateResponse("auth/signin.html", {
            "request": request,
            "error": "Email and password are required."
        }, status_code=400)
    
    # Find user
    user = db.query(User).filter(User.email == email).first()
    
    if not user or not utils.verify_password(password, user.password):
        return templates.TemplateResponse("auth/signin.html", {
            "request": request,
            "error": "Invalid email or password."
        }, status_code=401)
    
    if not user.is_active:
        return templates.TemplateResponse("auth/signin.html", {
            "request": request,
            "error": "Your account has been deactivated."
        }, status_code=403)
    
    # Check for admin login
    if admin_login:
        if not utils.is_admin_email(user.email):
            return templates.TemplateResponse("auth/signin.html", {
                "request": request,
                "error": "Admin access denied. You are not an administrator."
            }, status_code=403)
        
        # Admin login - skip 2FA
        response = RedirectResponse(url="/admin/dashboard", status_code=303)
        response.set_cookie(key="user_id", value=str(user.id), max_age=86400)
        response.set_cookie(key="user_email", value=user.email, max_age=86400)
        response.set_cookie(key="is_admin", value="true", max_age=86400)
        
        if remember_me:
            token_value = utils.generate_token()
            expires_at = datetime.utcnow() + timedelta(days=30)
            token = RememberToken(
                user_id=user.id,
                token=token_value,
                expires_at=expires_at,
                ip_address=request.client.host
            )
            db.add(token)
            db.commit()
            response.set_cookie(key="remember_token", value=token_value, max_age=2592000)
        
        return response
    
    # Regular user login - require 2FA
    # Generate OTP
    otp_code = utils.generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=10)
    
    two_fa = TwoFactorCode(
        user_id=user.id,
        code=otp_code,
        code_type='login',
        expires_at=expires_at,
        ip_address=request.client.host
    )
    db.add(two_fa)
    db.commit()
    
    # Send OTP via email
    utils.send_otp_email(user.email, user.full_name, otp_code)
    
    # Store temporary session data in cookie
    response = RedirectResponse(url="/auth/verify-2fa", status_code=303)
    response.set_cookie(key="temp_user_id", value=str(user.id), max_age=600)  # 10 minutes
    response.set_cookie(key="temp_user_email", value=user.email, max_age=600)
    response.set_cookie(key="temp_user_name", value=user.full_name, max_age=600)
    response.set_cookie(key="temp_remember_me", value=str(remember_me), max_age=600)
    
    return response

# ============ SIGNUP ============

@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    """Sign up page"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse("auth/signup.html", {"request": request})

@router.post("/signup", response_class=HTMLResponse)
async def signup(
    request: Request,
    fullname: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Handle sign up"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="templates")
    
    full_name = fullname.strip()
    email = email.lower().strip()
    
    # Validate input
    errors = []
    
    if not full_name or not utils.is_valid_full_name(full_name):
        errors.append('Full name must contain only letters and spaces.')
    
    if not email or not utils.is_valid_email(email):
        errors.append('Invalid email format.')
    
    # Check email domain
    if email and not utils.is_valid_domain(email):
        errors.append('Email domain not whitelisted. Please use gmail.com, yahoo.com, outlook.com, etc.')
    
    if len(password) < 4:
        errors.append(f'Password must be at least 4 characters.')
    
    if password != confirm_password:
        errors.append('Passwords do not match.')
    
    if db.query(User).filter(User.email == email).first():
        errors.append('Email already registered.')
    
    if errors:
        return templates.TemplateResponse("auth/signup.html", {
            "request": request,
            "errors": errors
        }, status_code=400)
    
    # Create user
    user = User(
        full_name=full_name,
        email=email,
        password=utils.hash_password(password)
    )
    db.add(user)
    db.commit()
    
    return templates.TemplateResponse("auth/signin.html", {
        "request": request,
        "success": "Account created successfully! Please sign in."
    })

# ============ VERIFY 2FA ============

@router.get("/verify-2fa", response_class=HTMLResponse)
async def verify_2fa_page(request: Request):
    """Verify 2FA page"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="templates")
    
    temp_user_id = request.cookies.get("temp_user_id")
    if not temp_user_id:
        return RedirectResponse(url="/auth/signin")
    
    return templates.TemplateResponse("auth/verify_2fa.html", {"request": request})

@router.post("/verify-2fa", response_class=HTMLResponse)
async def verify_2fa(
    request: Request,
    verification_code: str = Form(...),
    db: Session = Depends(get_db)
):
    """Handle 2FA verification"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="templates")
    
    temp_user_id = request.cookies.get("temp_user_id")
    if not temp_user_id:
        return RedirectResponse(url="/auth/signin")
    
    verification_code = verification_code.strip()
    
    if not verification_code:
        return templates.TemplateResponse("auth/verify_2fa.html", {
            "request": request,
            "error": "Please enter the verification code."
        }, status_code=400)
    
    # Find the OTP
    two_fa = db.query(TwoFactorCode).filter(
        TwoFactorCode.user_id == int(temp_user_id),
        TwoFactorCode.code_type == 'login'
    ).order_by(TwoFactorCode.created_at.desc()).first()
    
    if not two_fa:
        return templates.TemplateResponse("auth/verify_2fa.html", {
            "request": request,
            "error": "No verification code found. Please sign in again."
        }, status_code=400)
    
    if two_fa.is_expired():
        db.delete(two_fa)
        db.commit()
        return templates.TemplateResponse("auth/verify_2fa.html", {
            "request": request,
            "error": "Verification code has expired. Please sign in again."
        }, status_code=400)
    
    if two_fa.code != verification_code:
        two_fa.attempts_used += 1
        db.commit()
        
        if two_fa.attempts_used >= 3:
            db.delete(two_fa)
            db.commit()
            return templates.TemplateResponse("auth/verify_2fa.html", {
                "request": request,
                "error": "Too many incorrect attempts. Please sign in again."
            }, status_code=403)
        
        return templates.TemplateResponse("auth/verify_2fa.html", {
            "request": request,
            "error": "Invalid verification code."
        }, status_code=400)
    
    # Code is valid
    user = db.query(User).filter(User.id == int(temp_user_id)).first()
    
    # Clean up
    db.delete(two_fa)
    db.commit()
    
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(key="user_id", value=str(user.id), max_age=86400)
    response.set_cookie(key="user_email", value=user.email, max_age=86400)
    
    if request.cookies.get("temp_remember_me") == "True":
        token_value = utils.generate_token()
        expires_at = datetime.utcnow() + timedelta(days=30)
        token = RememberToken(
            user_id=user.id,
            token=token_value,
            expires_at=expires_at,
            ip_address=request.client.host
        )
        db.add(token)
        db.commit()
        response.set_cookie(key="remember_token", value=token_value, max_age=2592000)
    
    # Clear temp cookies
    response.delete_cookie("temp_user_id")
    response.delete_cookie("temp_user_email")
    response.delete_cookie("temp_user_name")
    response.delete_cookie("temp_remember_me")
    
    return response

# ============ LOGOUT ============

@router.get("/logout")
async def logout():
    """Handle logout"""
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("user_id")
    response.delete_cookie("user_email")
    response.delete_cookie("is_admin")
    response.delete_cookie("remember_token")
    return response

# ============ FORGOT PASSWORD ============

@router.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password_page(request: Request):
    """Forgot password page"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse("auth/forgot_password.html", {"request": request})

@router.post("/forgot-password", response_class=HTMLResponse)
async def forgot_password(
    request: Request,
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    """Handle forgot password"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="templates")
    
    email = email.lower().strip()
    
    user = db.query(User).filter(User.email == email).first()
    if user:
        # Generate reset code
        reset_code = utils.generate_otp()
        expires_at = datetime.utcnow() + timedelta(minutes=30)
        
        two_fa = TwoFactorCode(
            user_id=user.id,
            code=reset_code,
            code_type='password_reset',
            expires_at=expires_at,
            ip_address=request.client.host
        )
        db.add(two_fa)
        db.commit()
        
        # Send reset code via email
        utils.send_password_reset_email(user.email, user.full_name, reset_code)
    
    # Always show success message for security
    return templates.TemplateResponse("auth/forgot_password.html", {
        "request": request,
        "success": "If an account exists with that email, a password reset code has been sent."
    })

# ============ RESET PASSWORD ============

@router.get("/reset-password", response_class=HTMLResponse)
async def reset_password_page(request: Request):
    """Reset password page"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse("auth/reset_password.html", {"request": request})

@router.post("/reset-password", response_class=HTMLResponse)
async def reset_password(
    request: Request,
    email: str = Form(...),
    code: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Handle password reset"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="templates")
    
    email = email.lower().strip()
    code = code.strip()
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return templates.TemplateResponse("auth/reset_password.html", {
            "request": request,
            "error": "User not found."
        }, status_code=404)
    
    # Find reset code
    two_fa = db.query(TwoFactorCode).filter(
        TwoFactorCode.user_id == user.id,
        TwoFactorCode.code_type == 'password_reset'
    ).order_by(TwoFactorCode.created_at.desc()).first()
    
    if not two_fa or two_fa.code != code:
        return templates.TemplateResponse("auth/reset_password.html", {
            "request": request,
            "error": "Invalid reset code."
        }, status_code=400)
    
    if two_fa.is_expired():
        db.delete(two_fa)
        db.commit()
        return templates.TemplateResponse("auth/reset_password.html", {
            "request": request,
            "error": "Reset code has expired."
        }, status_code=400)
    
    if new_password != confirm_password:
        return templates.TemplateResponse("auth/reset_password.html", {
            "request": request,
            "error": "Passwords do not match."
        }, status_code=400)
    
    if len(new_password) < 4:
        return templates.TemplateResponse("auth/reset_password.html", {
            "request": request,
            "error": "Password must be at least 4 characters."
        }, status_code=400)
    
    # Update password
    user.password = utils.hash_password(new_password)
    db.delete(two_fa)
    db.commit()
    
    return templates.TemplateResponse("auth/signin.html", {
        "request": request,
        "success": "Password reset successfully! Please sign in."
    })

# Helper for 2FA code expiration check
def is_expired(expires_at):
    """Check if code has expired"""
    return datetime.utcnow() > expires_at

# Add method to TwoFactorCode model
TwoFactorCode.is_expired = lambda self: datetime.utcnow() > self.expires_at
