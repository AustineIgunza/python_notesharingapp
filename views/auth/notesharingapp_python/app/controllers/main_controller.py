from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_required, current_user
from app.models import Note, Category, Favorite
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page"""
    # Get popular notes (most favorited)
    popular_notes = db.session.query(Note).join(Favorite).filter(
        Note.is_deleted == False,
        Note.is_public == True
    ).group_by(Note.id).order_by(db.func.count(Favorite.id).desc()).limit(10).all()
    
    # Get recent notes
    recent_notes = Note.query.filter_by(is_deleted=False, is_public=True).order_by(Note.created_at.desc()).limit(10).all()
    
    return render_template('index.html', popular_notes=popular_notes, recent_notes=recent_notes)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    page = request.args.get('page', 1, type=int)
    user_notes = current_user.notes.filter_by(is_deleted=False).paginate(page=page, per_page=10)
    
    # Get user stats
    total_notes = current_user.notes.filter_by(is_deleted=False).count()
    total_favorites = current_user.favorites.count()
    
    return render_template('user/dashboard.html', 
                         notes=user_notes, 
                         total_notes=total_notes,
                         total_favorites=total_favorites)

@main_bp.route('/favorites')
@login_required
def favorites():
    """User favorites page"""
    page = request.args.get('page', 1, type=int)
    favorites = Favorite.query.filter_by(user_id=current_user.id).join(Note).paginate(page=page, per_page=10)
    
    return render_template('user/favorites.html', favorites=favorites)

@main_bp.route('/shared-notes')
def shared_notes():
    """Shared notes page"""
    page = request.args.get('page', 1, type=int)
    notes = Note.query.filter_by(is_public=True, is_deleted=False).order_by(Note.created_at.desc()).paginate(page=page, per_page=10)
    
    return render_template('shared_notes.html', notes=notes)

@main_bp.route('/note/<int:note_id>')
def view_note(note_id):
    """View single note"""
    note = Note.query.get_or_404(note_id)
    
    # Check access permissions
    if not note.is_public and (not current_user.is_authenticated or note.user_id != current_user.id):
        flash('You do not have permission to view this note.', 'danger')
        return redirect(url_for('main.index'))
    
    is_favorite = False
    if current_user.is_authenticated:
        is_favorite = Favorite.query.filter_by(user_id=current_user.id, note_id=note_id).first() is not None
    
    return render_template('note/view.html', note=note, is_favorite=is_favorite)

@main_bp.route('/categories')
def categories():
    """Categories page"""
    all_categories = Category.query.all()
    return render_template('categories.html', categories=all_categories)

@main_bp.route('/category/<int:category_id>')
def category_notes(category_id):
    """Notes by category"""
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    notes = Note.query.filter_by(category_id=category_id, is_deleted=False, is_public=True).paginate(page=page, per_page=10)
    
    return render_template('category_notes.html', category=category, notes=notes)

@main_bp.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors"""
    return render_template('errors/404.html'), 404

@main_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('errors/500.html'), 500
