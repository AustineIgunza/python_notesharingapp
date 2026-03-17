"""
Notes router - CRUD operations, favorites, search
"""

from fastapi import APIRouter, Request, Form, Depends, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime
import os
import uuid
from app.models.db import Note, NoteFile, Favorite, Category
import shutil

router = APIRouter()

def get_db():
    from main import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(request: Request):
    """Get current user from cookie"""
    user_id = request.cookies.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return int(user_id)

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = "uploads"

def allowed_file(filename):
    """Check if file type is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ============ CREATE NOTE ============

@router.get("/create", response_class=HTMLResponse)
async def create_note_page(request: Request, db: Session = Depends(get_db)):
    """Create note page"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="templates")
    
    try:
        user_id = get_current_user(request)
    except:
        return RedirectResponse(url="/auth/signin")
    
    categories = db.query(Category).all()
    return templates.TemplateResponse("notes/create.html", {
        "request": request,
        "categories": categories
    })

@router.post("/create", response_class=HTMLResponse)
async def create_note(
    request: Request,
    title: str = Form(...),
    content: str = Form(None),
    category_id: int = Form(None),
    is_public: bool = Form(False),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    """Handle note creation"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="templates")
    
    try:
        user_id = get_current_user(request)
    except:
        return RedirectResponse(url="/auth/signin")
    
    title = title.strip()
    if not title:
        categories = db.query(Category).all()
        return templates.TemplateResponse("notes/create.html", {
            "request": request,
            "error": "Title is required",
            "categories": categories
        }, status_code=400)
    
    # Create note
    note = Note(
        title=title,
        content=content.strip() if content else None,
        author_id=user_id,
        category_id=category_id if category_id else None,
        is_public=is_public
    )
    db.add(note)
    db.commit()
    
    # Handle file upload if present
    if file and allowed_file(file.filename):
        os.makedirs(os.path.join(UPLOAD_FOLDER, "documents"), exist_ok=True)
        
        file_ext = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}_{int(datetime.utcnow().timestamp())}.{file_ext}"
        file_path = os.path.join(UPLOAD_FOLDER, "documents", unique_filename)
        
        with open(file_path, "wb") as f:
            contents = await file.read()
            f.write(contents)
        
        note_file = NoteFile(
            note_id=note.id,
            file_name=file.filename,
            file_size=len(contents),
            file_type=file_ext,
            file_path=file_path
        )
        db.add(note_file)
        db.commit()
    
    return RedirectResponse(url="/dashboard", status_code=303)

# ============ EDIT NOTE ============

@router.get("/{note_id}/edit", response_class=HTMLResponse)
async def edit_note_page(
    request: Request,
    note_id: int,
    db: Session = Depends(get_db)
):
    """Edit note page"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="templates")
    
    try:
        user_id = get_current_user(request)
    except:
        return RedirectResponse(url="/auth/signin")
    
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note or note.author_id != user_id:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Note not found or access denied"
        }, status_code=404)
    
    categories = db.query(Category).all()
    return templates.TemplateResponse("notes/edit.html", {
        "request": request,
        "note": note,
        "categories": categories
    })

@router.post("/{note_id}/edit", response_class=HTMLResponse)
async def edit_note(
    request: Request,
    note_id: int,
    title: str = Form(...),
    content: str = Form(None),
    category_id: int = Form(None),
    is_public: bool = Form(False),
    db: Session = Depends(get_db)
):
    """Handle note update"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="templates")
    
    try:
        user_id = get_current_user(request)
    except:
        return RedirectResponse(url="/auth/signin")
    
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note or note.author_id != user_id:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Note not found or access denied"
        }, status_code=404)
    
    note.title = title.strip()
    note.content = content.strip() if content else None
    note.category_id = category_id if category_id else None
    note.is_public = is_public
    db.commit()
    
    return RedirectResponse(url="/dashboard", status_code=303)

# ============ DELETE NOTE ============

@router.post("/{note_id}/delete", response_class=HTMLResponse)
async def delete_note(
    request: Request,
    note_id: int,
    db: Session = Depends(get_db)
):
    """Delete note (soft delete)"""
    try:
        user_id = get_current_user(request)
    except:
        return RedirectResponse(url="/auth/signin")
    
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note or note.author_id != user_id:
        return RedirectResponse(url="/dashboard")
    
    note.is_deleted = True
    db.commit()
    
    return RedirectResponse(url="/dashboard", status_code=303)

# ============ VIEW NOTE ============

@router.get("/{note_id}", response_class=HTMLResponse)
async def view_note(
    request: Request,
    note_id: int,
    db: Session = Depends(get_db)
):
    """View note"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="templates")
    
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.is_deleted == False
    ).first()
    
    if not note:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Note not found"
        }, status_code=404)
    
    # Check if note is public or user is author
    user_id = request.cookies.get("user_id")
    if not note.is_public and (not user_id or int(user_id) != note.author_id):
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Access denied"
        }, status_code=403)
    
    files = db.query(NoteFile).filter(NoteFile.note_id == note_id).all()
    is_favorite = False
    if user_id:
        is_favorite = db.query(Favorite).filter(
            Favorite.user_id == int(user_id),
            Favorite.note_id == note_id
        ).first() is not None
    
    return templates.TemplateResponse("notes/view.html", {
        "request": request,
        "note": note,
        "files": files,
        "is_favorite": is_favorite
    })

# ============ FAVORITE/UNFAVORITE ============

@router.post("/{note_id}/favorite")
async def favorite_note(
    request: Request,
    note_id: int,
    db: Session = Depends(get_db)
):
    """Add note to favorites"""
    try:
        user_id = get_current_user(request)
    except:
        return RedirectResponse(url="/auth/signin")
    
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    existing = db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.note_id == note_id
    ).first()
    
    if not existing:
        favorite = Favorite(user_id=user_id, note_id=note_id)
        db.add(favorite)
        db.commit()
    
    return RedirectResponse(url=f"/notes/{note_id}", status_code=303)

@router.post("/{note_id}/unfavorite")
async def unfavorite_note(
    request: Request,
    note_id: int,
    db: Session = Depends(get_db)
):
    """Remove note from favorites"""
    try:
        user_id = get_current_user(request)
    except:
        return RedirectResponse(url="/auth/signin")
    
    favorite = db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.note_id == note_id
    ).first()
    
    if favorite:
        db.delete(favorite)
        db.commit()
    
    return RedirectResponse(url=f"/notes/{note_id}", status_code=303)

# ============ SEARCH ============

@router.get("/search/results", response_class=HTMLResponse)
async def search_results(
    request: Request,
    q: str = None,
    db: Session = Depends(get_db)
):
    """Search notes"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="templates")
    
    query = q.strip() if q else ""
    
    if len(query) < 3:
        return templates.TemplateResponse("notes/search.html", {
            "request": request,
            "notes": None,
            "query": query,
            "error": "Search query must be at least 3 characters"
        })
    
    notes = db.query(Note).filter(
        or_(
            Note.title.ilike(f'%{query}%'),
            Note.content.ilike(f'%{query}%')
        ),
        Note.is_deleted == False,
        Note.is_public == True
    ).limit(50).all()
    
    return templates.TemplateResponse("notes/search.html", {
        "request": request,
        "notes": notes,
        "query": query
    })
