"""
Main router - Home and general pages
"""

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from fastapi.staticfiles import StaticFiles

router = APIRouter()

# Dependency for database
def get_db():
    from main import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page"""
    from fastapi.templating import Jinja2Templates
    from main import app
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    """User dashboard"""
    from app.models.db import User, Note
    from fastapi.templating import Jinja2Templates
    from main import app
    
    # Get current user from session (placeholder)
    user_id = request.cookies.get("user_id")
    if not user_id:
        return templates.TemplateResponse("auth/signin.html", {"request": request, "error": "Please login first"})
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        return templates.TemplateResponse("auth/signin.html", {"request": request, "error": "User not found"})
    
    page = request.query_params.get("page", 1)
    notes = db.query(Note).filter(Note.author_id == user.id, Note.is_deleted == False).offset((int(page) - 1) * 10).limit(10).all()
    total_notes = db.query(func.count(Note.id)).filter(Note.author_id == user.id, Note.is_deleted == False).scalar()
    
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "notes": notes,
        "total_notes": total_notes,
        "page": page
    })

@router.get("/favorites", response_class=HTMLResponse)
async def favorites(request: Request, db: Session = Depends(get_db)):
    """User favorites page"""
    from app.models.db import User, Favorite, Note
    from fastapi.templating import Jinja2Templates
    
    user_id = request.cookies.get("user_id")
    if not user_id:
        templates = Jinja2Templates(directory="templates")
        return templates.TemplateResponse("auth/signin.html", {"request": request, "error": "Please login first"})
    
    page = request.query_params.get("page", 1)
    favorites = db.query(Favorite).filter(Favorite.user_id == int(user_id)).offset((int(page) - 1) * 10).limit(10).all()
    total = db.query(func.count(Favorite.id)).filter(Favorite.user_id == int(user_id)).scalar()
    
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse("favorites.html", {
        "request": request,
        "favorites": favorites,
        "total": total,
        "page": page
    })

@router.get("/search", response_class=HTMLResponse)
async def search(request: Request, db: Session = Depends(get_db)):
    """Search notes"""
    from app.models.db import Note
    from fastapi.templating import Jinja2Templates
    
    query = request.query_params.get("q", "").strip()
    
    if len(query) < 3:
        templates = Jinja2Templates(directory="templates")
        return templates.TemplateResponse("search.html", {
            "request": request,
            "notes": None,
            "query": query,
            "error": "Search query must be at least 3 characters"
        })
    
    notes = db.query(Note).filter(
        (Note.title.ilike(f'%{query}%') | Note.content.ilike(f'%{query}%')),
        Note.is_deleted == False,
        Note.is_public == True
    ).limit(50).all()
    
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse("search.html", {
        "request": request,
        "notes": notes,
        "query": query
    })
