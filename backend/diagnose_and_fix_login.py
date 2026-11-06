"""
Comprehensive diagnostic and fix script for login issues
"""
from app import create_app
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
import sys

app = create_app()

def diagnose_and_fix():
    with app.app_context():
        print("\n" + "=" * 80)
        print(" " * 20 + "LOGIN DIAGNOSTIC & FIX TOOL")
        print("=" * 80 + "\n")
        
        # Step 1: Check database connection
        print("Step 1: Checking database connection...")
        try:
            user_count = User.query.count()
            print(f"✓ Database connected successfully")
            print(f"✓ Found {user_count} users in database\n")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return
        
        # Step 2: Check if john.doe exists
        print("Step 2: Looking for test patient 'john.doe@email.com'...")
        user = User.query.filter_by(email='john.doe@email.com').first()
        
        if not user:
            print("❌ User 'john.doe@email.com' NOT FOUND!")
            print("\nExisting users:")
            all_users = User.query.all()
            for u in all_users:
                print(f"  - {u.email} ({u.full_name})")
            
            print("\n⚠ You need to run seed_data.py first!")
            print("Run: python seed_data.py")
            return
        
        print(f"✓ User found!")
        print(f"  Email: {user.email}")
        print(f"  Name: {user.full_name}")
        print(f"  ID: {user.id}")
        print(f"  Admin: {user.is_admin}")
        print(f"  Hash preview: {user.password_hash[:30]}...\n")
        
        # Step 3: Test current password
        print("Step 3: Testing password 'patient123'...")
        test_password = 'patient123'
        
        if user.check_password(test_password):
            print(f"✓ ✓ ✓ PASSWORD WORKS! ✓ ✓ ✓")
            print(f"\nYou can login with:")
            print(f"  Email: {user.email}")
            print(f"  Password: {test_password}")
            print("\nNo fix needed!\n")
        else:
            print(f"❌ Password verification FAILED!")
            print(f"\nStep 4: Fixing password...")
            
            # Try to detect what method was used
            if user.password_hash.startswith('pbkdf2:sha256'):
                print("  Current method: pbkdf2:sha256")
            elif user.password_hash.startswith('scrypt'):
                print("  Current method: scrypt")
            elif user.password_hash.startswith('bcrypt'):
                print("  Current method: bcrypt")
            else:
                print(f"  Current method: unknown")
            
            # Reset password with explicit method
            print(f"  Resetting password to: '{test_password}'")
            user.set_password(test_password)
            db.session.commit()
            print("  ✓ Password updated in database")
            
            # Verify the fix
            print("\nStep 5: Verifying fix...")
            if user.check_password(test_password):
                print("✓ ✓ ✓ PASSWORD NOW WORKS! ✓ ✓ ✓")
                print(f"\nYou can now login with:")
                print(f"  Email: {user.email}")
                print(f"  Password: {test_password}\n")
            else:
                print("❌ Password still doesn't work!")
                print("This indicates a deeper issue with werkzeug or the hashing method.")
                print("\nTrying alternative method...")
                
                # Try generating hash directly
                new_hash = generate_password_hash(test_password, method='pbkdf2:sha256')
                if check_password_hash(new_hash, test_password):
                    print("✓ Direct hash generation works")
                    user.password_hash = new_hash
                    db.session.commit()
                    
                    if user.check_password(test_password):
                        print("✓ ✓ ✓ PASSWORD FIXED WITH DIRECT METHOD! ✓ ✓ ✓\n")
                    else:
                        print("❌ Still failing - please check werkzeug version\n")
                else:
                    print("❌ Even direct hashing fails - werkzeug may need reinstalling\n")
        
        # Step 6: Fix all other accounts
        print("Step 6: Checking and fixing all accounts...")
        accounts_to_fix = [
            ('john.doe@email.com', 'patient123'),
            ('priya.sharma@email.com', 'patient123'),
            ('raj.kumar@email.com', 'patient123'),
            ('admin@hospital.com', 'admin123'),
        ]
        
        for email, password in accounts_to_fix:
            u = User.query.filter_by(email=email).first()
            if u:
                if not u.check_password(password):
                    print(f"  Fixing: {email}")
                    u.set_password(password)
                else:
                    print(f"  ✓ OK: {email}")
            else:
                print(f"  ❌ Missing: {email}")
        
        db.session.commit()
        print("\n✓ All accounts checked and fixed!\n")
        
        # Final summary
        print("=" * 80)
        print(" " * 25 + "LOGIN CREDENTIALS")
        print("=" * 80)
        print("\nPatient Accounts:")
        print("  Email: john.doe@email.com      | Password: patient123")
        print("  Email: priya.sharma@email.com  | Password: patient123")
        print("  Email: raj.kumar@email.com     | Password: patient123")
        print("\nAdmin Account:")
        print("  Email: admin@hospital.com      | Password: admin123")
        print("\n" + "=" * 80 + "\n")

if __name__ == '__main__':
    diagnose_and_fix()
