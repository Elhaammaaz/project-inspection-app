# QUICK START GUIDE

## Initial Setup

### 1. Python Environment
```powershell
# Activate virtual environment
c:\Users\mosta\Dar Al Riyadh\Power BI - Reporting System - Mostafa Hammam - Shared Folder\EXPRO\checklist_app\venv\Scripts\Activate.ps1

# Verify Python
python --version
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. PostgreSQL Setup (if using local database)
```powershell
# Install PostgreSQL if not already installed
# Then create database and user:

psql -U postgres
CREATE DATABASE checklist_app;
CREATE USER checklist_user WITH PASSWORD 'your_secure_password';
ALTER ROLE checklist_user SET client_encoding TO 'utf8';
ALTER ROLE checklist_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE checklist_user SET default_transaction_deferrable TO on;
ALTER ROLE checklist_user SET default_transaction_read_only TO off;
GRANT ALL PRIVILEGES ON DATABASE checklist_app TO checklist_user;
\q
```

### 4. Environment Variables
Create a `.env` file in the app directory:
```
SECRET_KEY=your-super-secret-key-change-this-in-production
DATABASE_URL=postgresql://checklist_user:your_secure_password@localhost:5432/checklist_app
DB_USER=checklist_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=checklist_app
UPLOAD_FOLDER=uploads
FLASK_ENV=development
```

### 5. Initialize Database
```powershell
# Run the app once to create tables
python app.py

# It will automatically create all tables on first run
```

### 6. Run Application
```powershell
python app.py
# OR using Flask CLI
flask run
```

**Application will be available at:** `http://localhost:5000`

---

## User Workflow

### Step 1: Register
- Click "Register" on landing page
- Fill in Full Name, Email, Password
- Account will be pending approval

### Step 2: Admin Approval
- Admin logs in and approves account
- User receives confirmation (optional email)

### Step 3: User Login
- Login with email and password
- Directed to dashboard (empty initially)

### Step 4: Import Excel
- Click "Import Excel" button
- Select BCAR v12 Excel file
- System automatically:
  - Parses all 7 sheets
  - Creates project
  - Imports 694 assessment items
  - Imports 32+ compliance items
  - Imports tests and CAPA actions
  - Initializes system weights
  - Calculates all scores

### Step 5: View Project
- Project appears on dashboard
- Click to view executive summary
- See all calculated KPIs

### Step 6: Score Items
- Go to "Assessment" tab
- Click item to edit
- Enter score (0-100%)
- Set item weight for calculation
- Select priority (P1-P4)
- Add evidence references
- System auto-calculates weighted score and building score

### Step 7: Track Compliance
- Go to "Compliance" tab
- For each requirement, select status (Yes/No/Partial/N/A)
- Add evidence reference
- System shows compliance %

### Step 8: Manage Tests
- Go to "Tests" tab
- View/edit test results
- Mark as Pass/Fail
- Link to assessment items

### Step 9: Track CAPA
- Go to "CAPA" tab
- Update action status
- Set due dates and costs
- Track verification

### Step 10: View Reports
- Return to project summary
- See all calculated metrics:
  - Building Score
  - Inspection Result (Pass/Fail)
  - FM Performance
  - Fire & Life Safety Score
  - Age Analysis
  - Compliance Status

---

## Key Features

### Automatic Calculations
- **Building Score** = Average of all weighted assessment item scores
- **Compliance Status** = Percentage of "Yes" compliance items
- **Fire & Life Safety** = Average of fire system items only
- **Age Analysis** = Chronological Age, Effective Age, Remaining Life
- **FM Performance** = Overall system performance average

### Search & Filter
- Assessment items: Search by code or description, filter by system or priority
- Compliance: View by area
- CAPA: Filter by status or priority

### Data Entry
- **Dropdowns**: Priority, Status, Evidence Type, Responsibility (no typing, just select)
- **Number Fields**: Scores (0-100), weights (decimals), costs, areas, floors
- **Dates**: Date pickers for validation
- **Read-Only**: Original data from Excel shown but not editable
- **Editable**: Only fields that need user input (scores, weights, status, evidence)

---

## Important Notes

1. **Excel File Structure**: Must be BCAR v12 format with exact sheet names
   - User Manual
   - Executive Assessment Summary
   - Government Compliance Checklist
   - Building Assessment
   - Test Register
   - CAPA Register
   - Lists

2. **Calculations**: All formulas run automatically whenever scores change
3. **PostgreSQL**: Database is secure and password-protected
4. **Backup**: Regularly backup PostgreSQL database
5. **Admin Panel**: Add admin features to approve new users (if needed)

---

## Troubleshooting

### Issue: "Database connection failed"
**Solution**: Check PostgreSQL is running and connection string is correct
```powershell
# Test connection
psql -U checklist_user -d checklist_app -c "SELECT 1;"
```

### Issue: "Excel import error"
**Solution**: Verify Excel file is BCAR v12 format and has all required sheets

### Issue: "Port 5000 already in use"
**Solution**: Change port in `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change port number
```

### Issue: "CSRF validation failed"
**Solution**: Clear browser cookies and try again

---

## Production Deployment

For production (e.g., Railway, Heroku, or your own server):

1. Set `FLASK_ENV=production`
2. Set `DEBUG=False` in config
3. Use `gunicorn` instead of development server:
   ```
   gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
   ```
4. Configure external PostgreSQL database
5. Use HTTPS with SSL certificate
6. Set strong SECRET_KEY environment variable
7. Configure backup strategy

---

## Support

All code is documented and follows best practices:
- Models have docstrings
- Forms have field validation
- Routes have error handling
- Calculations are optimized
- Database is normalized

**Ready to deploy!** 🚀
