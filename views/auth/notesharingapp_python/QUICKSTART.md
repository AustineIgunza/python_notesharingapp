# Quick Start Guide - Python Flask Version

## 5-Minute Setup

### Step 1: Prerequisites
Make sure you have:
- Python 3.8+ installed
- MySQL Server running
- Basic command line knowledge

### Step 2: Download & Navigate
```bash
cd notesharingapp_python
```

### Step 3: Setup Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Configure Environment
```bash
# Copy example to actual config
cp .env.example .env

# Edit .env with your settings (use Notepad or any editor)
# Most important:
# - DB_USER and DB_PASS (your MySQL credentials)
# - MAIL_USERNAME and MAIL_PASSWORD (for Gmail)
```

### Step 6: Initialize Database
```bash
# Create tables
flask init-db

# Add sample data
flask seed-db
```

### Step 7: Run the Application
```bash
python run.py
```

### Step 8: Access the App
Open your browser and go to:
```
http://localhost:5000
```

## Default Test Accounts

After running `flask seed-db`:

### Admin Account
- **Email:** `admin12@gmail.com`
- **Password:** `admin12`
- **Access:** Admin dashboard at `/admin/dashboard`

### Regular User
- **Email:** `testuser@gmail.com`
- **Password:** `password123`
- **Access:** User dashboard at `/dashboard`

## Key URLs

| Page | URL |
|---|---|
| Home | `http://localhost:5000/` |
| Sign In | `http://localhost:5000/auth/signin` |
| Sign Up | `http://localhost:5000/auth/signup` |
| Dashboard | `http://localhost:5000/dashboard` |
| Favorites | `http://localhost:5000/favorites` |
| Create Note | `http://localhost:5000/notes/create` |
| Admin Panel | `http://localhost:5000/admin/dashboard` |

## Useful Commands

```bash
# View all Flask commands
flask --help

# Open interactive Python shell with app context
flask shell

# Check installed packages
pip list

# Add new package
pip install <package_name>

# Deactivate virtual environment
deactivate
```

## Troubleshooting

### "No module named 'flask'"
```bash
# Make sure virtual environment is activated
# Then reinstall:
pip install -r requirements.txt
```

### "Can't connect to MySQL"
- Check `.env` database credentials
- Verify MySQL is running
- Try creating database manually:
  ```sql
  CREATE DATABASE notesharingapp_python CHARACTER SET utf8mb4;
  ```

### "Address already in use"
- Another app is using port 5000
- Either close that app or change port in `run.py`:
  ```python
  app.run(debug=True, port=5001)
  ```

### Email not sending
- Enable "Less secure apps" in Gmail settings, OR
- Use App-specific password:
  1. Go to Google Account settings
  2. Enable 2-Step Verification
  3. Create App Password for Gmail
  4. Use that password in `.env`

## Project Features

✅ User registration and login
✅ Two-factor authentication (2FA)
✅ Create and manage notes
✅ File attachments
✅ Public/private notes
✅ Favorite notes
✅ Note categories
✅ Search functionality
✅ Admin dashboard
✅ User management
✅ Analytics
✅ Remember me (30 days)
✅ Password reset
✅ Responsive design

## Next Steps

1. **Explore the code:**
   - Check `app/controllers/` for routes
   - Check `app/models/` for database models
   - Check `app/templates/` for HTML templates

2. **Customize:**
   - Update branding in templates
   - Modify colors in `app/static/`
   - Add your own categories via admin

3. **Extend:**
   - Add more features
   - Integrate with external APIs
   - Create mobile app integration

## Stopping the Server

Press `Ctrl + C` in the terminal running `python run.py`

## Production Deployment

For deploying to production, see the full README.md for:
- Gunicorn setup
- Database configuration
- Email server setup
- SSL/HTTPS setup
- Security considerations

---

**Need help?** Check CONVERSION_GUIDE.md for technical details or README.md for comprehensive documentation.

**Happy coding!** 🚀
