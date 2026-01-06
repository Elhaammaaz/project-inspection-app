#!/usr/bin/env python
"""Initialize the database with demo data"""

from app import create_app
from models import db, User

app = create_app()
with app.app_context():
    # Create all tables
    db.create_all()
    print('✓ Database schema created')
    
    # Check if admin already exists
    admin = User.query.filter_by(email='admin@example.com').first()
    if not admin:
        admin = User(
            email='admin@example.com',
            full_name='Admin User',
            active=1,
            is_admin=1
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('✓ Admin user created: admin@example.com / admin123')
    else:
        print('✓ Admin user already exists')

print('✓ Database initialization complete!')
print('')
print('To start the app:')
print('  python app.py')
print('')
print('Login with:')
print('  Email: admin@example.com')
print('  Password: admin123')
