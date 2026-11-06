@echo off
echo ========================================
echo THE MISSING LINK - Setup Script
echo ========================================
echo.

echo Step 1: Setting up Backend...
cd backend
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat
echo Installing Python dependencies...
pip install -r requirements.txt
echo.

echo Step 2: Database Setup Instructions
echo ========================================
echo Please run the following MySQL commands:
echo.
echo mysql -u root -p
echo CREATE DATABASE missing_link_db;
echo exit;
echo.
echo Then run: python seed_data.py
echo ========================================
echo.

cd ..

echo Step 3: Setting up Frontend...
cd frontend
echo Installing Node dependencies...
call npm install
echo.

cd ..

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next Steps:
echo 1. Create MySQL database: missing_link_db
echo 2. Update backend/config.py with your MySQL credentials
echo 3. Run: cd backend ^&^& python seed_data.py
echo 4. Start backend: cd backend ^&^& python app.py
echo 5. Start frontend: cd frontend ^&^& npm run dev
echo.
echo Test Credentials:
echo Patient: john.doe@email.com / patient123
echo Admin: admin@hospital.com / admin123
echo ========================================

pause
