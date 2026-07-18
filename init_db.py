# =========================================================
# DATABASE INITIALIZATION SCRIPT
# =========================================================

import os
from dotenv import load_dotenv
from app import app, db
from models import User, Admin, Settings, UserRole
from auth import generate_token

load_dotenv()

def init_database():
    """Initialize database with default data"""
    
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        print("✓ Tables created")
        
        # Create default admin if not exists
        admin = Admin.query.filter_by(email='admin@numeroannand.com').first()
        if not admin:
            print("Creating default admin user...")
            admin = Admin(
                email='admin@numeroannand.com',
                name='Annand Sarma',
                role='admin'
            )
            admin.set_password('ChangeMe@2024')
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin created (email: admin@numeroannand.com, password: ChangeMe@2024)")
            print("  ⚠️  IMPORTANT: Change admin password on first login!")
        else:
            print("✓ Admin already exists")
        
        # Initialize default settings
        print("Initializing settings...")
        settings_defaults = {
            'platform_name': 'Numero Annand AI Premium',
            'founder_name': 'Annand Sarma',
            'founder_mobile': '+91 7099805039',
            'upi_id': '7099805039-2@axl',
            'payee_name': 'Ananda Sarmah',
            'digital_report_price': '201',
            'printed_report_price': '501',
            'premium_membership_price': '500',
            'support_email': 'support@numeroannand.com',
            'support_whatsapp': 'https://wa.me/917099805039',
            'whatsapp_community': 'https://chat.whatsapp.com/G23u7Yf3PuIC6Gw7GCJIMJ'
        }
        
        for key, value in settings_defaults.items():
            existing = Settings.query.filter_by(key=key).first()
            if not existing:
                setting = Settings(key=key, value=value)
                db.session.add(setting)
        
        db.session.commit()
        print("✓ Settings initialized")
        
        # Print summary
        print("\n" + "="*60)
        print("DATABASE INITIALIZATION COMPLETE")
        print("="*60)
        print(f"Database URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print(f"\nDefault Admin Credentials:")
        print(f"  Email: admin@numeroannand.com")
        print(f"  Password: ChangeMe@2024")
        print(f"\nNext Steps:")
        print(f"  1. Change the default admin password")
        print(f"  2. Update environment variables in .env file")
        print(f"  3. Run 'python app.py' to start the server")
        print("="*60 + "\n")

if __name__ == '__main__':
    init_database()
