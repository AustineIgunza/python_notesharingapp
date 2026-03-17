#!/usr/bin/env python
"""
Flask Application Entry Point
Notes Sharing Application - Python Version
"""

import os
from dotenv import load_dotenv
from app import create_app, db
from app.models import User, Note, Category, Favorite, NoteFile, TwoFactorCode, RememberToken

# Load environment variables
load_dotenv()

# Create Flask app
app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    """Make models available in shell context"""
    return {
        'db': db,
        'User': User,
        'Note': Note,
        'Category': Category,
        'Favorite': Favorite,
        'NoteFile': NoteFile,
        'TwoFactorCode': TwoFactorCode,
        'RememberToken': RememberToken
    }

@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print('Database initialized!')

@app.cli.command()
def seed_db():
    """Seed database with sample data"""
    if User.query.first():
        print('Database already has data!')
        return
    
    # Create admin user
    admin = User(full_name='Admin User', email='admin12@gmail.com')
    admin.set_password('admin12')
    db.session.add(admin)
    
    # Create test user
    user = User(full_name='Test User', email='testuser@gmail.com')
    user.set_password('password123')
    db.session.add(user)
    
    # Create categories
    categories = [
        Category(name='Technology', description='Tech notes and tutorials'),
        Category(name='Science', description='Science and research notes'),
        Category(name='Business', description='Business and entrepreneurship'),
        Category(name='Personal', description='Personal development notes'),
        Category(name='Other', description='Miscellaneous notes')
    ]
    for cat in categories:
        db.session.add(cat)
    
    db.session.commit()
    print('Database seeded with sample data!')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
