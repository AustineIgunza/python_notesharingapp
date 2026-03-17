"""
FastAPI Application Initialization & Database Setup
This script initializes the database with seed data
"""

import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load environment
load_dotenv('.env.fastapi')

# Database setup
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', 'root')
DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'notesharingapp_python')

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"🗄️  Connecting to database: {DB_NAME}")
print(f"📍 Location: {DB_HOST}:{DB_PORT}")

try:
    engine = create_engine(DATABASE_URL, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Import models
    from app.models.db import Base, User, Category
    from app.utils import hash_password
    
    # Create all tables
    print("📋 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")
    
    # Seed sample data
    print("\n📚 Seeding sample data...")
    
    # Check if data already exists
    admin_exists = session.query(User).filter(User.email == 'admin12@gmail.com').first()
    
    if not admin_exists:
        # Create admin user
        admin = User(
            full_name='Administrator',
            email='admin12@gmail.com',
            password=hash_password('admin12'),
            is_active=True
        )
        session.add(admin)
        print("✅ Admin user created")
    
    # Create test user
    test_user_exists = session.query(User).filter(User.email == 'testuser@gmail.com').first()
    if not test_user_exists:
        test_user = User(
            full_name='Test User',
            email='testuser@gmail.com',
            password=hash_password('password123'),
            is_active=True
        )
        session.add(test_user)
        print("✅ Test user created")
    
    # Create categories
    categories_data = [
        ('Technology', 'Tech and programming notes'),
        ('Personal', 'Personal thoughts and ideas'),
        ('Business', 'Business related notes'),
        ('Education', 'Learning and academic notes'),
        ('Miscellaneous', 'Other notes'),
    ]
    
    for name, description in categories_data:
        category_exists = session.query(Category).filter(Category.name == name).first()
        if not category_exists:
            category = Category(name=name, description=description)
            session.add(category)
    
    session.commit()
    print("✅ Categories created")
    
    # Display summary
    total_users = session.query(User).count()
    total_categories = session.query(Category).count()
    
    print("\n" + "="*50)
    print("✨ Database Initialization Complete!")
    print("="*50)
    print(f"📊 Total Users: {total_users}")
    print(f"📂 Total Categories: {total_categories}")
    print("\n🔐 Test Credentials:")
    print("   Admin: admin12@gmail.com / admin12")
    print("   User: testuser@gmail.com / password123")
    print("\n🚀 Start the application with:")
    print("   python main.py")
    print("   or")
    print("   uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    print("\n🌐 Access the app at: http://localhost:8000/")
    print("="*50)
    
    session.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"\n⚠️  Make sure:")
    print("   1. MySQL is running")
    print("   2. Database credentials in .env are correct")
    print("   3. Database name exists: " + DB_NAME)
    sys.exit(1)
