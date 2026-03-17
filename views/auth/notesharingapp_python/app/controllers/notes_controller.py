from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models import Note, NoteFile, Category, Favorite
import os
from werkzeug.utils import secure_filename
import uuid

notes_bp = Blueprint('notes', __name__, url_prefix='/notes')

def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_UPLOAD_EXTENSIONS']

@notes_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create new note"""
    categories = Category.query.all()
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category_id = request.form.get('category_id', type=int)
        is_public = request.form.get('is_public') == 'on'
        
        if not title or not content:
            flash('Title and content are required.', 'danger')
            return render_template('note/create.html', categories=categories)
        
        # Create note
        note = Note(
            title=title,
            content=content,
            user_id=current_user.id,
            category_id=category_id if category_id else None,
            is_public=is_public
        )
        db.session.add(note)
        db.session.flush()  # Get the note ID
        
        # Handle file uploads
        if 'files' in request.files:
            files = request.files.getlist('files')
            for file in files:
                if file and allowed_file(file.filename):
                    # Generate secure filename
                    ext = file.filename.rsplit('.', 1)[1].lower()
                    filename = f"{uuid.uuid4().hex}_{int(__import__('time').time())}.{ext}"
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 
                                          current_app.config['UPLOAD_SUBFOLDER_DOCUMENTS'], 
                                          filename)
                    
                    file.save(filepath)
                    
                    # Create file record
                    note_file = NoteFile(
                        note_id=note.id,
                        filename=filename,
                        original_filename=secure_filename(file.filename),
                        file_type=ext,
                        file_size=os.path.getsize(filepath),
                        file_path=filepath
                    )
                    db.session.add(note_file)
        
        db.session.commit()
        
        flash('Note created successfully!', 'success')
        return redirect(url_for('main.view_note', note_id=note.id))
    
    return render_template('note/create.html', categories=categories)

@notes_bp.route('/edit/<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit(note_id):
    """Edit note"""
    note = Note.query.get_or_404(note_id)
    
    # Check permissions
    if note.user_id != current_user.id and not current_user.is_admin():
        flash('You do not have permission to edit this note.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    categories = Category.query.all()
    
    if request.method == 'POST':
        note.title = request.form.get('title', '').strip()
        note.content = request.form.get('content', '').strip()
        note.category_id = request.form.get('category_id', type=int) or None
        note.is_public = request.form.get('is_public') == 'on'
        
        if not note.title or not note.content:
            flash('Title and content are required.', 'danger')
            return render_template('note/edit.html', note=note, categories=categories)
        
        db.session.commit()
        
        flash('Note updated successfully!', 'success')
        return redirect(url_for('main.view_note', note_id=note.id))
    
    return render_template('note/edit.html', note=note, categories=categories)

@notes_bp.route('/delete/<int:note_id>', methods=['POST'])
@login_required
def delete(note_id):
    """Delete note"""
    note = Note.query.get_or_404(note_id)
    
    # Check permissions
    if note.user_id != current_user.id and not current_user.is_admin():
        flash('You do not have permission to delete this note.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    note.is_deleted = True
    db.session.commit()
    
    flash('Note deleted successfully!', 'success')
    return redirect(url_for('main.dashboard'))

@notes_bp.route('/favorite/<int:note_id>', methods=['POST'])
@login_required
def add_favorite(note_id):
    """Add note to favorites"""
    note = Note.query.get_or_404(note_id)
    
    favorite = Favorite.query.filter_by(user_id=current_user.id, note_id=note_id).first()
    if not favorite:
        favorite = Favorite(user_id=current_user.id, note_id=note_id)
        db.session.add(favorite)
        db.session.commit()
        flash('Note added to favorites!', 'success')
    else:
        flash('This note is already in your favorites.', 'info')
    
    return redirect(url_for('main.view_note', note_id=note_id))

@notes_bp.route('/unfavorite/<int:note_id>', methods=['POST'])
@login_required
def remove_favorite(note_id):
    """Remove note from favorites"""
    favorite = Favorite.query.filter_by(user_id=current_user.id, note_id=note_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        flash('Note removed from favorites!', 'success')
    
    return redirect(url_for('main.view_note', note_id=note_id))

@notes_bp.route('/search', methods=['GET'])
def search():
    """Search notes"""
    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    
    if not query:
        flash('Please enter a search query.', 'warning')
        return redirect(url_for('main.index'))
    
    results = Note.query.filter(
        (Note.title.ilike(f'%{query}%') | Note.content.ilike(f'%{query}%')),
        Note.is_deleted == False,
        Note.is_public == True
    ).paginate(page=page, per_page=10)
    
    return render_template('search_results.html', query=query, results=results)
