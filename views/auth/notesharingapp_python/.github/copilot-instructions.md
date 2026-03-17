<!-- Use this file to provide workspace-specific custom instructions to Copilot. -->

# Notes Sharing Application - Python Flask Version

This is a complete conversion of the PHP Notes Sharing Application to Python using Flask.

## Project Structure

### Architecture
- **Framework**: Flask (Python web framework)
- **Database**: MySQL/SQLAlchemy ORM
- **Authentication**: Flask-Login with 2FA via email
- **Email**: Flask-Mail with Gmail SMTP

### Key Directories
- `app/` - Main application directory
  - `models/` - Database models (User, Note, Category, Favorite, etc.)
  - `controllers/` - Flask blueprints for routing
  - `services/` - Business logic and services
  - `middleware/` - Custom middleware for authentication
  - `templates/` - Jinja2 HTML templates
  - `static/` - CSS, JavaScript, and assets
  - `uploads/` - User file uploads
- `config.py` - Application configuration
- `run.py` - Application entry point
- `requirements.txt` - Python dependencies

## Key Features Implemented

### Authentication System
- User registration with email validation
- Login with Two-Factor Authentication (2FA) via OTP
- Password reset functionality
- Remember me functionality with secure tokens
- Admin login with email whitelist

### Notes Management
- Create, edit, delete notes
- File attachments support
- Note categories
- Public/private note sharing
- Note search functionality

### Favorites System
- Add/remove notes to favorites
- Favorites page for users
- Favorites analytics

### Admin Panel
- Complete admin dashboard
- User management
- Notes management
- Analytics and statistics
- Admin-only access control

## Database Models

1. **User** - User accounts with admin flag
2. **Note** - Notes with metadata and relationships
3. **Category** - Note categorization
4. **NoteFile** - File attachments for notes
5. **Favorite** - User favorite notes tracking
6. **TwoFactorCode** - 2FA authentication codes
7. **RememberToken** - Persistent login tokens

## Environment Setup

1. Copy `.env.example` to `.env`
2. Update database and email credentials
3. Install dependencies: `pip install -r requirements.txt`
4. Initialize database: `flask db-init` or `python run.py`
5. Seed sample data: `flask seed-db`
6. Run the application: `python run.py`

## Configuration

All configuration is managed through:
- Environment variables in `.env`
- `config.py` for Flask configuration
- Database credentials and email settings

## Conversion Notes

This Python version maintains feature parity with the original PHP application while adapting to Python/Flask conventions:
- PHP Classes → Python Classes
- PHP PDO → SQLAlchemy ORM
- PHP Session → Flask Session & Flask-Login
- PHP Mail → Flask-Mail
- Bootstrap 5 UI → Maintained with Jinja2 templates
- File uploads → Werkzeug file handling

## Development

- Debug mode enabled by default in development
- Hot reload on file changes
- SQLAlchemy logging available
- Email sending via Gmail SMTP

## Testing

Test users available after seeding:
- Admin: `admin12@gmail.com` / `admin12`
- User: `testuser@gmail.com` / `password123`

## Deployment

For production:
1. Set `FLASK_ENV=production` in `.env`
2. Update `SECRET_KEY` with strong value
3. Set `SESSION_COOKIE_SECURE=True`
4. Use proper WSGI server (Gunicorn, uWSGI)
5. Set up proper SSL/HTTPS
6. Configure proper database backups
