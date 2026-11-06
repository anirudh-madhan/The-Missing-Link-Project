"""
Test script to verify user credentials and password hashing
"""
from app import create_app
from models import db, User
from werkzeug.security import check_password_hash

app = create_app()

with app.app_context():
    print("=" * 60)
    print("Testing Patient Login Credentials")
    print("=" * 60)
    
    # Check if user exists
    user = User.query.filter_by(email='john.doe@email.com').first()
    
    if not user:
        print("❌ ERROR: User 'john.doe@email.com' NOT FOUND in database!")
        print("\nAll users in database:")
        all_users = User.query.all()
        for u in all_users:
            print(f"  - {u.email} (ID: {u.id}, Admin: {u.is_admin})")
    else:
        print(f"✓ User found: {user.email}")
        print(f"  Full Name: {user.full_name}")
        print(f"  Is Admin: {user.is_admin}")
        print(f"  Password Hash: {user.password_hash[:50]}...")
        print()
        
        # Test password verification
        test_password = 'patient123'
        print(f"Testing password: '{test_password}'")
        
        # Method 1: Using model method
        result1 = user.check_password(test_password)
        print(f"  user.check_password('{test_password}'): {result1}")
        
        # Method 2: Direct werkzeug check
        result2 = check_password_hash(user.password_hash, test_password)
        print(f"  check_password_hash directly: {result2}")
        
        if result1 and result2:
            print("\n✓ ✓ ✓ PASSWORD VERIFICATION WORKS! ✓ ✓ ✓")
            print("The password 'patient123' is correctly hashed and verified.")
        else:
            print("\n❌ PASSWORD VERIFICATION FAILED!")
            print("The password hash may be corrupted or incorrect.")
            
            # Try to fix by resetting password
            print("\nAttempting to reset password...")
            user.set_password('patient123')
            db.session.commit()
            print("Password reset complete. Testing again...")
            
            result3 = user.check_password('patient123')
            if result3:
                print("✓ Password now works after reset!")
            else:
                print("❌ Password still doesn't work!")
    
    print("\n" + "=" * 60)
    print("All Users Summary:")
    print("=" * 60)
    users = User.query.all()
    for u in users:
        print(f"Email: {u.email}")
        print(f"  Name: {u.full_name}")
        print(f"  Admin: {u.is_admin}")
        print(f"  Password Test: {u.check_password('patient123' if not u.is_admin else 'admin123')}")
        print()
