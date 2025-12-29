# Project Inspection Management System

A professional, production-ready Flask web application for managing comprehensive project inspections. Features user authentication, responsive mobile-friendly design, SQLite database persistence, and extensive inspection documentation fields.

## Features

- ✓ User registration and authentication (Flask-Login)
- ✓ Create, read, update, and delete project inspections
- ✓ Comprehensive project information capture:
  - Project details (name, city, address, GPS coordinates)
  - Building information (type, use, area, floors)
  - Timeline and dates (construction year, renovation date, inspection date)
  - Management details (FM contractor, system threshold)
  - Assessment results (inspection result, compliance status)
  - Performance metrics (building score, FM performance, fire safety rating)
  - Life expectancy calculations (economic life, effective age, remaining life)
- ✓ Notes and additional comments for each inspection
- ✓ Dashboard with project overview (table view on desktop, cards on mobile)
- ✓ Detailed project view with all information displayed
- ✓ Responsive design (mobile and desktop optimized)
- ✓ Bootstrap 5 UI with professional styling
- ✓ SQLite database with SQLAlchemy ORM
- ✓ Complete form validation with Flask-WTF
- ✓ Pagination support for large project lists

## Requirements

- Python 3.7+
- Flask 2.3.3
- Flask-SQLAlchemy 3.0.5
- Flask-Login 0.6.2
- Flask-WTF 1.1.1
- WTForms 3.0.1

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd checklist_app
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   
   On Windows:
   ```bash
   venv\Scripts\activate
   ```
   
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Access the application:**
   Open your browser and navigate to: `http://localhost:5000`

## Usage

### First Time Setup

1. The app will automatically create a demo account:
   - **Email:** demo@example.com
   - **Password:** demo123

2. Visit the login page: `http://localhost:5000/login`
3. Log in with demo credentials
4. Access the dashboard to start creating project inspections

### Main Features

- **Dashboard:** View all project inspections in a professional table (desktop) or card view (mobile)
- **New Inspection:** Create detailed project inspections with comprehensive data fields
- **View Details:** Click "View" to see all inspection details in a formatted display
- **Edit Inspection:** Modify existing inspections with a user-friendly form
- **Delete Inspection:** Remove inspections no longer needed
- **Pagination:** Projects are paginated for easy navigation

### Data Fields Captured

**Project Information:**
- Project/Building Name, City, Address
- GPS Coordinates (Latitude, Longitude)

**Building Details:**
- Building Type, Primary Use
- Gross Built Area (m²), Number of Floors

**Dates & Timeline:**
- Construction Year, Last Renovation Date
- Current Year, Inspection Date
- Estimated Life Time, Planned Retirement Year

**Management & Assessment:**
- FM Contractor/Service Provider
- System Threshold (%)
- Inspection Result, Government Compliance Status

**Assessment Metrics:**
- Building Score, FM Performance
- Fire & Life Safety Rating
- High Priority Items Classified
- Total Economic Life, Chronological Age
- Estimated Effective Age, Estimated Remaining Life

**Additional:**
- Notes and detailed comments

## Project Structure

```
checklist_app/
├── app.py                      # Main Flask application with all routes
├── config.py                   # Configuration settings
├── models.py                   # SQLAlchemy models (User, ProjectInspection)
├── forms.py                    # WTForms (LoginForm, ProjectInspectionForm)
├── requirements.txt            # Python dependencies
│
├── templates/
│   ├── base.html              # Base template with navbar and layout
│   ├── login.html             # Login page
│   ├── register.html          # User registration page
│   ├── dashboard.html         # Main dashboard with project list
│   ├── form.html              # Create/edit inspection form
│   ├── view.html              # Detailed project inspection view
│   ├── 404.html               # Page not found error
│   └── 500.html               # Server error page
│
├── static/
│   └── css/                   # Custom CSS (optional)
│
└── instance/
    └── app.db                 # SQLite database (auto-created)
```

## Database

- **Type:** SQLite
- **Location:** `instance/app.db` (auto-created on first run)
- **ORM:** SQLAlchemy

### Models

**User:**
- id (Primary Key)
- email (Unique, Required, Indexed)
- password_hash (Hashed, Secure)
- created_at (Timestamp)

**ProjectInspection:**
- id (Primary Key)
- user_id (Foreign Key → User, Indexed)
- All project information fields (as listed above)
- created_at (Timestamp, Indexed)
- updated_at (Timestamp)

## Security Features

- Password hashing with Werkzeug
- CSRF protection on all forms
- Login required decorators on protected routes
- User-specific data isolation (users can only see their own entries)
- Session management with Flask-Login

## Deployment Notes

For production deployment:

1. Set `SECRET_KEY` environment variable:
   ```bash
   export SECRET_KEY='your-secret-key-here'
   ```

2. Set `debug=False` in `app.py` before deployment

3. Use a production WSGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"
   ```

4. Use a production database (PostgreSQL, MySQL) instead of SQLite for better performance

5. Implement proper logging and monitoring

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## License

Open source - free to use and modify.

## Support

For issues or questions, ensure all dependencies are installed and the database is properly initialized.
