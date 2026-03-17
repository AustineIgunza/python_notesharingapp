"""
Admin router - Admin dashboard, user management, analytics
"""

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from app.models.db import User, Note, Favorite

router = APIRouter()

def get_db():
    from main import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def require_admin(request: Request):
    """Check if user is admin"""
    user_id = request.cookies.get("user_id")
    is_admin = request.cookies.get("is_admin")
    
    if not user_id or is_admin != "true":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return int(user_id)

# ============ ADMIN DASHBOARD ============

@router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    admin_id: int = Depends(require_admin)
):
    """Admin dashboard"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="templates")
    
    total_users = db.query(func.count(User.id)).scalar()
    total_notes = db.query(func.count(Note.id)).filter(Note.is_deleted == False).scalar()
    total_favorites = db.query(func.count(Favorite.id)).scalar()
    
    # Recent notes
    recent_notes = db.query(Note).filter(Note.is_deleted == False).order_by(Note.created_at.desc()).limit(10).all()
    
    # Most favorited notes
    from sqlalchemy import and_
    most_favorited = db.query(
        Note,
        func.count(Favorite.id).label('favorite_count')
    ).join(Favorite).filter(
        Note.is_deleted == False
    ).group_by(Note.id).order_by(desc('favorite_count')).limit(10).all()
    
    return templates.TemplateResponse("admin/dashboard.html", {
        "request": request,
        "total_users": total_users,
        "total_notes": total_notes,
        "total_favorites": total_favorites,
        "recent_notes": recent_notes,
        "most_favorited": most_favorited
    })

# ============ ADMIN USERS ============

@router.get("/users", response_class=HTMLResponse)
async def admin_users(
    request: Request,
    page: int = 1,
    db: Session = Depends(get_db),
    admin_id: int = Depends(require_admin)
):
    """Manage users"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="templates")
    
    per_page = 20
    users = db.query(User).offset((page - 1) * per_page).limit(per_page).all()
    total = db.query(func.count(User.id)).scalar()
    total_pages = (total + per_page - 1) // per_page
    
    return templates.TemplateResponse("admin/users.html", {
        "request": request,
        "users": users,
        "page": page,
        "total_pages": total_pages,
        "total": total
    })

@router.get("/user/{user_id}", response_class=HTMLResponse)
async def admin_user_details(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    admin_id: int = Depends(require_admin)
):
    """View user details"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="templates")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "User not found"
        }, status_code=404)
    
    total_notes = db.query(func.count(Note.id)).filter(
        Note.author_id == user_id,
        Note.is_deleted == False
    ).scalar()
    total_favorites = db.query(func.count(Favorite.id)).filter(Favorite.user_id == user_id).scalar()
    recent_notes = db.query(Note).filter(
        Note.author_id == user_id,
        Note.is_deleted == False
    ).order_by(Note.created_at.desc()).limit(10).all()
    
    return templates.TemplateResponse("admin/user_details.html", {
        "request": request,
        "user": user,
        "total_notes": total_notes,
        "total_favorites": total_favorites,
        "recent_notes": recent_notes
    })

# ============ ADMIN NOTES ============

@router.get("/notes", response_class=HTMLResponse)
async def admin_notes(
    request: Request,
    page: int = 1,
    db: Session = Depends(get_db),
    admin_id: int = Depends(require_admin)
):
    """Manage notes"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="templates")
    
    per_page = 20
    notes = db.query(Note).order_by(Note.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()
    total = db.query(func.count(Note.id)).filter(Note.is_deleted == False).scalar()
    total_pages = (total + per_page - 1) // per_page
    
    return templates.TemplateResponse("admin/notes.html", {
        "request": request,
        "notes": notes,
        "page": page,
        "total_pages": total_pages,
        "total": total
    })

@router.post("/note/{note_id}/delete", response_class=HTMLResponse)
async def admin_delete_note(
    request: Request,
    note_id: int,
    db: Session = Depends(get_db),
    admin_id: int = Depends(require_admin)
):
    """Delete note"""
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        return RedirectResponse(url="/admin/notes")
    
    note.is_deleted = True
    db.commit()
    
    return RedirectResponse(url="/admin/notes", status_code=303)

# ============ ADMIN ANALYTICS ============

@router.get("/analytics", response_class=HTMLResponse)
async def admin_analytics(
    request: Request,
    db: Session = Depends(get_db),
    admin_id: int = Depends(require_admin)
):
    """Analytics page"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="templates")
    
    # Most favorited notes
    most_favorited = db.query(
        Note,
        func.count(Favorite.id).label('favorite_count')
    ).join(Favorite).filter(
        Note.is_deleted == False
    ).group_by(Note.id).order_by(desc('favorite_count')).limit(10).all()
    
    # Top authors
    top_authors = db.query(
        User,
        func.count(Note.id).label('note_count')
    ).join(Note).filter(
        Note.is_deleted == False
    ).group_by(User.id).order_by(desc('note_count')).limit(10).all()
    
    return templates.TemplateResponse("admin/analytics.html", {
        "request": request,
        "most_favorited": most_favorited,
        "top_authors": top_authors
    })
