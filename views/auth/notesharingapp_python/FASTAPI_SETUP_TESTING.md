# FastAPI Notes Sharing Application - Complete Setup & Testing Guide

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Dependencies
```bash
cd c:\Apache24\htdocs\notesharingapp\views\auth\notesharingapp_python
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
# Copy the template env file
cp .env.fastapi .env

# Edit .env with your settings:
# - DB credentials (same as PHP app: root/root)
# - Gmail credentials for email
```

### Step 3: Verify Database
```bash
# The application will auto-create tables on first run
# Make sure MySQL is running and accessible
```

### Step 4: Run Application
```bash
# Start FastAPI server on port 8000
python main.py

# Or use uvicorn directly:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 5: Access the Application
- **Home**: http://localhost:8000/
- **Sign Up**: http://localhost:8000/auth/signup
- **Sign In**: http://localhost:8000/auth/signin
- **Admin**: http://localhost:8000/admin/dashboard

---

## 🧪 Testing Accounts

After the app initializes with the default database, use these credentials:

### Admin Account
- **Email**: admin12@gmail.com
- **Password**: admin12
- **Access**: http://localhost:8000/admin/dashboard

### Regular User
- **Email**: testuser@gmail.com
- **Password**: password123
- **Access**: http://localhost:8000/dashboard

---

## 📋 Test Cases & Links

### Authentication Testing

#### 1. Sign Up (New Account)
- **URL**: http://localhost:8000/auth/signup
- **Test**: 
  - Full Name: "John Doe"
  - Email: "johndoe@gmail.com"
  - Password: "password123"
  - Confirm: "password123"
- **Expected**: Account created, redirects to signin

#### 2. Sign In (Regular User)
- **URL**: http://localhost:8000/auth/signin
- **Test**:
  - Email: "testuser@gmail.com"
  - Password: "password123"
  - Check "Remember me"
- **Expected**: Receives 2FA code via email, can verify

#### 3. 2FA Verification
- **URL**: http://localhost:8000/auth/verify-2fa
- **Test**: Enter the 6-digit code from email
- **Expected**: Redirects to /dashboard

#### 4. Admin Login
- **URL**: http://localhost:8000/auth/signin
- **Test**: 
  - Click "Admin Login" tab
  - Email: "admin12@gmail.com"
  - Password: "admin12"
- **Expected**: No 2FA required, direct access to /admin/dashboard

#### 5. Forgot Password
- **URL**: http://localhost:8000/auth/forgot-password
- **Test**: Enter email "testuser@gmail.com"
- **Expected**: Reset code sent via email

#### 6. Reset Password
- **URL**: http://localhost:8000/auth/reset-password
- **Test**:
  - Email: "testuser@gmail.com"
  - Reset Code: (from email)
  - New Password: "newpassword123"
  - Confirm: "newpassword123"
- **Expected**: Password updated, can login with new password

#### 7. Logout
- **URL**: http://localhost:8000/auth/logout
- **Test**: Click logout in navbar
- **Expected**: Clears cookies, redirects to home

---

### Notes Management Testing

#### 8. Create Note
- **URL**: http://localhost:8000/notes/create
- **Test**:
  - Title: "My First Note"
  - Content: "This is a test note"
  - Category: Select one
  - Attach file: (optional)
  - Make public: Check if desired
- **Expected**: Note created, redirects to /dashboard

#### 9. View Note
- **URL**: http://localhost:8000/notes/{note_id}
- **Test**: Click on any note from dashboard
- **Expected**: Note content, author, files displayed

#### 10. Edit Note
- **URL**: http://localhost:8000/notes/{note_id}/edit
- **Test**: Change title and content
- **Expected**: Note updated

#### 11. Delete Note
- **URL**: http://localhost:8000/notes/{note_id}/edit
- **Test**: Click delete button
- **Expected**: Note soft-deleted, removed from dashboard

#### 12. Add to Favorites
- **URL**: http://localhost:8000/notes/{note_id}
- **Test**: Click "Add to Favorites" button
- **Expected**: Button changes to "Unfavorite", note appears in /favorites

#### 13. View Favorites
- **URL**: http://localhost:8000/favorites
- **Test**: Click favorites in navbar
- **Expected**: All favorited notes displayed

#### 14. Search Notes
- **URL**: http://localhost:8000/search
- **Test**: Type search query (min 3 characters)
- **Expected**: Matching notes displayed

---

### User Dashboard Testing

#### 15. View Dashboard
- **URL**: http://localhost:8000/dashboard
- **Test**: Login first, then access dashboard
- **Expected**: User's notes, stats, quick actions displayed

#### 16. Dashboard Stats
- **URL**: http://localhost:8000/dashboard
- **Test**: Check total notes, favorites count
- **Expected**: Accurate statistics displayed

---

### Admin Panel Testing

#### 17. Admin Dashboard
- **URL**: http://localhost:8000/admin/dashboard
- **Test**: Admin login required
- **Expected**: Total users, notes, favorites, recent notes, most favorited

#### 18. Manage Users
- **URL**: http://localhost:8000/admin/users
- **Test**: View all users list with pagination
- **Expected**: Users table with full details

#### 19. User Details
- **URL**: http://localhost:8000/admin/user/{user_id}
- **Test**: Click on any user
- **Expected**: User details, notes count, favorites count, recent notes

#### 20. Manage Notes
- **URL**: http://localhost:8000/admin/notes
- **Test**: View all notes with pagination
- **Expected**: All notes listed (including deleted ones)

#### 21. Delete Note (Admin)
- **URL**: http://localhost:8000/admin/notes
- **Test**: Click delete on any note
- **Expected**: Note soft-deleted

#### 22. Analytics
- **URL**: http://localhost:8000/admin/analytics
- **Test**: View analytics page
- **Expected**: Most favorited notes and top authors displayed

---

## 🗄️ Database Verification

### Connect to MySQL Workbench

1. **Open MySQL Workbench**
2. **Connection Settings**:
   - Host: `127.0.0.1`
   - Port: `3306`
   - User: `root`
   - Password: `root`
   - Database: `notesharingapp_python`

3. **Verify Tables**:
   ```sql
   SHOW TABLES;
   
   -- Check users table
   SELECT * FROM users;
   
   -- Check notes table
   SELECT * FROM notes;
   
   -- Check favorites
   SELECT * FROM favorites;
   
   -- Check 2FA codes
   SELECT * FROM two_factor_codes;
   
   -- Check remember tokens
   SELECT * FROM remember_tokens;
   ```

---

## 🔍 Troubleshooting

### Issue: "Database connection refused"
**Solution**: 
- Ensure MySQL is running: `mysql -u root -p`
- Check credentials in `.env` file match your setup
- Verify database `notesharingapp_python` exists

### Issue: "Email not sending"
**Solution**:
- Check Gmail credentials in `.env`
- For Gmail: Use "App Passwords" instead of account password
- Enable "Less secure app access" in Gmail settings
- Check spam folder for test emails

### Issue: "ModuleNotFoundError"
**Solution**:
- Reinstall requirements: `pip install -r requirements.txt`
- Activate virtual environment if using one
- Check Python version (3.8+)

### Issue: "Port 8000 already in use"
**Solution**:
- Change port in main.py: `uvicorn.run(..., port=8001)`
- Or kill process: `lsof -i :8000` then `kill -9 {PID}`

### Issue: "Template not found"
**Solution**:
- Verify all template files in `templates/` directory
- Check file paths in routers match template directory structure
- Ensure `templates` folder exists in project root

---

## 📊 Feature Verification Checklist

- [ ] Sign Up (email validation, domain whitelist)
- [ ] Sign In (password hashing, session management)
- [ ] 2FA (OTP generation, email delivery, verification)
- [ ] Admin Login (email whitelist bypass)
- [ ] Forgot Password (reset code, email)
- [ ] Reset Password (code verification, password update)
- [ ] Remember Me (30-day token persistence)
- [ ] Create Note (title, content, category, file upload)
- [ ] Edit Note (update metadata)
- [ ] Delete Note (soft delete)
- [ ] View Note (display content, files, metadata)
- [ ] Add to Favorites (unique constraint)
- [ ] Remove from Favorites
- [ ] Search Notes (full-text search)
- [ ] Dashboard (user stats, note list)
- [ ] Favorites Page (all favorited notes)
- [ ] Admin Dashboard (statistics)
- [ ] Admin Users Management (list, details)
- [ ] Admin Notes Management (list, delete)
- [ ] Admin Analytics (most favorited, top authors)
- [ ] Database Schema (7 tables, proper relationships)
- [ ] File Uploads (UUID naming, type validation)
- [ ] Security (password hashing, XSS protection, CSRF)

---

## 🚀 Production Deployment

### Using Gunicorn
```bash
pip install gunicorn

# Start with Gunicorn (4 workers)
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

### Using Docker
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables for Production
```bash
ENVIRONMENT=production
FLASK_ENV=production
DEBUG=False
SECRET_KEY=your-production-secret-key
SESSION_COOKIE_SECURE=true
SESSION_COOKIE_HTTPONLY=true
```

---

## 📞 Support

For issues or questions:
1. Check the logs in console output
2. Review error messages in browser
3. Check MySQL error logs
4. Review email configuration
5. Verify all template files exist

---

## 🎉 Success!

Your FastAPI Notes Sharing Application is ready for testing!

**Start here**: http://localhost:8000/

**Test with**: 
- Admin: admin12@gmail.com / admin12
- User: testuser@gmail.com / password123
