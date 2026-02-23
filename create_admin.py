#!/usr/bin/env python3
"""
Create Admin Account Script
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask_app import create_app, db
from flask_app.models import User

def create_admin():
    """Create a new admin account"""
    
    app = create_app('development')
    
    with app.app_context():
        # Check if admin already exists
        existing_admin = User.query.filter_by(email='admin@demo.com').first()
        if existing_admin:
            print("Admin account already exists!")
            print(f"Email: {existing_admin.email}")
            print(f"Username: {existing_admin.username}")
            return
        
        # Create new admin
        admin = User(
            username='demo_admin',
            email='admin@demo.com',
            first_name='Demo',
            last_name='Admin',
            role='admin',
            is_admin=True
        )
        admin.set_password('admin123')
        
        db.session.add(admin)
        db.session.commit()
        
        print("✅ Admin account created successfully!")
        print("📝 Login Credentials:")
        print("   Email: admin@demo.com")
        print("   Password: admin123")
        print("   Username: demo_admin")
        print()
        print("🌐 Access Admin Panel: http://localhost:5000/admin/")

if __name__ == "__main__":
    create_admin()
