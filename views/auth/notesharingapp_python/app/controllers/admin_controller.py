from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models import User, Note, Favorite, TwoFactorCode

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    """Decorator to require admin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Admin access required.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard"""
    # Get statistics
    total_users = User.query.count()
    total_notes = Note.query.filter_by(is_deleted=False).count()
    total_favorites = Favorite.query.count()
    public_notes = Note.query.filter_by(is_deleted=False, is_public=True).count()
    
    # Get recent activity
    recent_notes = Note.query.filter_by(is_deleted=False).order_by(Note.created_at.desc()).limit(10).all()
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_notes=total_notes,
                         total_favorites=total_favorites,
                         public_notes=public_notes,
                         recent_notes=recent_notes,
                         recent_users=recent_users)

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """Manage users"""
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=20)
    
    return render_template('admin/users.html', users=users)

@admin_bp.route('/user/<int:user_id>')
@login_required
@admin_required
def user_details(user_id):
    """View user details"""
    user = User.query.get_or_404(user_id)
    user_notes = user.notes.filter_by(is_deleted=False).all()
    user_favorites = user.favorites.all()
    
    return render_template('admin/user_details.html', 
                         user=user, 
                         user_notes=user_notes, 
                         user_favorites=user_favorites)

@admin_bp.route('/notes')
@login_required
@admin_required
def notes():
    """Manage notes"""
    page = request.args.get('page', 1, type=int)
    notes = Note.query.filter_by(is_deleted=False).paginate(page=page, per_page=20)
    
    return render_template('admin/notes.html', notes=notes)

@admin_bp.route('/analytics')
@login_required
@admin_required
def analytics():
    """Analytics page"""
    # Get statistics
    total_users = User.query.count()
    total_notes = Note.query.filter_by(is_deleted=False).count()
    
    # Get most favorited notes
    most_favorited = db.session.query(Note).join(Favorite).filter(
        Note.is_deleted == False
    ).group_by(Note.id).order_by(db.func.count(Favorite.id).desc()).limit(10).all()
    
    # Get users with most notes
    top_authors = db.session.query(User, db.func.count(Note.id)).join(Note).filter(
        Note.is_deleted == False
    ).group_by(User.id).order_by(db.func.count(Note.id).desc()).limit(10).all()
    
    return render_template('admin/analytics.html',
                         total_users=total_users,
                         total_notes=total_notes,
                         most_favorited=most_favorited,
                         top_authors=top_authors)

@admin_bp.route('/delete-note/<int:note_id>', methods=['POST'])
@login_required
@admin_required
def delete_note(note_id):
    """Admin delete note"""
    note = Note.query.get_or_404(note_id)
    note.is_deleted = True
    db.session.commit()
    
    flash(f'Note "{note.title}" deleted.', 'success')
    return redirect(url_for('admin.notes'))

@admin_bp.route('/delete-user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Admin delete user"""
    if user_id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('admin.users'))
    
    user = User.query.get_or_404(user_id)
    user.is_active = False
    db.session.commit()
    
    flash(f'User "{user.email}" deactivated.', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/export')
@login_required
@admin_required
def export_data():
    """Export admin data"""
    import csv
    from io import StringIO
    from flask import make_response
    
    # This would generate CSV exports
    # Implementation depends on requirements
    
    flash('Export functionality coming soon!', 'info')
    return redirect(url_for('admin.dashboard'))
