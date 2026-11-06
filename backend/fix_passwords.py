"""
Script to verify and fix password hashing for seeded users
"""
from app import create_app
from models import db, User

app = create_app()

def fix_passwords():
    with app.app_context():
        print("=" * 70)
        print("PASSWORD VERIFICATION AND FIX SCRIPT")
        print("=" * 70)
        print()
        
        # Test credentials
        test_accounts = [
            {'email': 'john.doe@email.com', 'password': 'patient123', 'name': 'John Doe (Patient)'},
            {'email': 'priya.sharma@email.com', 'password': 'patient123', 'name': 'Priya Sharma (Patient)'},
            {'email': 'raj.kumar@email.com', 'password': 'patient123', 'name': 'Raj Kumar (Patient)'},
            {'email': 'admin@hospital.com', 'password': 'admin123', 'name': 'Admin'},
        ]
        
        users_fixed = 0
        users_ok = 0
        users_missing = 0
        
        for account in test_accounts:
            print(f"Checking: {account['name']} ({account['email']})")
            user = User.query.filter_by(email=account['email']).first()
            
            if not user:
                print(f"  ❌ User NOT FOUND in database!")
                users_missing += 1
                print()
                continue
            
            # Test if password works
            if user.check_password(account['password']):
                print(f"  ✓ Password verification WORKS")
                users_ok += 1
            else:
                print(f"  ❌ Password verification FAILED")
                print(f"  → Resetting password to: '{account['password']}'")
                user.set_password(account['password'])
                db.session.commit()
                
                # Verify fix worked
                if user.check_password(account['password']):
                    print(f"  ✓ Password FIXED and verified!")
                    users_fixed += 1
                else:
                    print(f"  ❌ Password fix FAILED - something is wrong!")
            
            print()
        
        print("=" * 70)
        print("SUMMARY:")
        print("=" * 70)
        print(f"✓ Passwords working correctly: {users_ok}")
        print(f"🔧 Passwords fixed: {users_fixed}")
        print(f"❌ Users missing from database: {users_missing}")
        print()
        
        if users_ok + users_fixed == len(test_accounts):
            print("✓ ✓ ✓ ALL ACCOUNTS READY FOR LOGIN! ✓ ✓ ✓")
            print()
            print("Test Credentials:")
            print("-" * 70)
            for account in test_accounts:
                if account['email'] != 'admin@hospital.com':
                    print(f"Patient: {account['email']} / {account['password']}")
            print(f"Admin:   admin@hospital.com / admin123")
        else:
            print("⚠ Some accounts need attention!")
        
        print("=" * 70)

if __name__ == '__main__':
    fix_passwords()
