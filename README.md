# THE MISSING LINK

A professional healthcare platform connecting patients with hospitals and healthcare services. Built with React, Flask, and MySQL.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- MySQL 5.7+

### 1. Backend Setup

```bash
cd backend

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure database
# Edit config.py with your MySQL credentials
# Default: localhost, root, missing_link_db

# Run migrations (creates tables)
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"

# Seed demo data
python seed_data.py

# Start server
python app.py
```

Backend runs on: **http://localhost:5000**

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs on: **http://localhost:5173**

---

## 🔐 Demo Credentials

### Patient Account
- **Email:** john.doe@email.com
- **Password:** patient123
- Access: Dashboard, Appointments, Hospitals, Profile

### Admin Account
- **Email:** admin@hospital.com
- **Password:** admin123
- Access: All patient features + Admin Dashboard

---

## 🏗️ Tech Stack

### Frontend
- **React 18** - UI framework
- **React Router** - Navigation
- **Axios** - HTTP client
- **Vite** - Build tool
- **CSS3** - Styling (custom dark theme)

### Backend
- **Flask** - Web framework
- **Flask-JWT-Extended** - Authentication
- **Flask-CORS** - Cross-origin requests
- **SQLAlchemy** - ORM
- **PyMySQL** - MySQL driver
- **Werkzeug** - Password hashing

### Database
- **MySQL** - Primary database
- Tables: users, hospitals, doctors, appointments, constraint_logs

---

## 📁 Project Structure

```
missing-link-proj/
├── backend/
│   ├── app.py                 # Flask application entry point
│   ├── config.py              # Configuration (DB, JWT)
│   ├── models.py              # Database models
│   ├── requirements.txt       # Python dependencies
│   ├── seed_data.py          # Demo data seeder
│   ├── routes/
│   │   ├── auth.py           # Authentication endpoints
│   │   ├── hospitals.py      # Hospital CRUD
│   │   ├── appointments.py   # Appointment management
│   │   ├── admin.py          # Admin operations
│   │   └── constraints.py    # Constraint testing
│   └── venv/                 # Virtual environment
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Main application component
│   │   ├── App.css           # Global theme styles
│   │   ├── index.css         # Base styles
│   │   ├── theme-fixes.css   # Theme consistency fixes
│   │   ├── config.js         # API URL & translations
│   │   ├── components/
│   │   │   └── Navbar.jsx    # Navigation bar
│   │   ├── pages/
│   │   │   ├── Landing.jsx   # Landing page
│   │   │   ├── Login.jsx     # Login page
│   │   │   ├── Register.jsx  # Registration page
│   │   │   ├── Dashboard.jsx # User dashboard
│   │   │   ├── Hospitals.jsx # Hospital search
│   │   │   ├── HospitalDetails.jsx
│   │   │   ├── BookAppointment.jsx
│   │   │   ├── Appointments.jsx
│   │   │   ├── PastRecords.jsx
│   │   │   ├── Recommendations.jsx
│   │   │   ├── Profile.jsx
│   │   │   ├── ConstraintLab.jsx
│   │   │   └── AdminDashboard.jsx
│   │   └── services/
│   │       └── api.js        # API service layer
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## 🎨 Design System

### Color Palette
- **Background:** `#090909` - Deep black
- **Cards:** `#191719` - Dark charcoal
- **Borders:** `#383033` - Subtle grey
- **Primary Text:** `#F5F0E8` - Warm white
- **Secondary Text:** `#B8ADA5` - Muted beige
- **Headings:** `#C52B3B` - Professional red
- **Buttons:** `#B52637` - Burgundy
- **Hover:** `#D8BD91` - Golden beige
- **Success:** `#65C995` - Mint green
- **Error:** `#E35B65` - Coral red

### Typography
- **Headings:** Manrope (800 weight)
- **Body:** DM Sans (400-700 weight)
- Professional, healthcare-focused aesthetic

---

## 🌟 Features

### For Patients
- 🔍 **Hospital Search** - Find hospitals by location, specialty, language
- 📅 **Appointment Booking** - Book, reschedule, or cancel appointments
- 🏥 **Hospital Details** - View doctors, specialties, bed availability
- 💡 **Smart Recommendations** - AI-powered hospital suggestions
- 📋 **Past Records** - View appointment history
- 🌐 **Multilingual** - English and Tamil support
- ♿ **Accessibility Info** - Wheelchair access, special needs support

### For Admins
- 📊 **Dashboard Analytics** - Hospital stats, appointment metrics
- 🏥 **Hospital Management** - Add/edit/delete hospitals
- 👨‍⚕️ **Doctor Management** - Manage doctor profiles
- 📋 **Appointment Overview** - View and manage all appointments
- ✅ **Complete Appointments** - Mark appointments as completed

### For Developers
- 🧪 **Constraint Lab** - Test system against 12 healthcare scenarios
- 📝 **Audit Logs** - Track all constraint test executions
- 🔬 **Real-time Testing** - Run constraint tests with live results

---

## 🔧 Configuration

### Backend Configuration (`backend/config.py`)

```python
# Database
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'YOUR_PASSWORD'
MYSQL_DB = 'missing_link_db'
MYSQL_PORT = 3306

# JWT
JWT_SECRET_KEY = 'your-secret-key-change-in-production'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

# CORS
CORS_ORIGINS = ['http://localhost:5173', 'http://localhost:3000']
```

### Frontend Configuration (`frontend/src/config.js`)

```javascript
export const API_BASE_URL = 'http://localhost:5000/api';

export const LANGUAGES = {
  en: 'English',
  ta: 'Tamil'
};
```

---

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile (requires JWT)
- `PUT /api/auth/profile` - Update profile (requires JWT)

### Hospitals
- `GET /api/hospitals` - List all hospitals (with filters)
- `GET /api/hospitals/:id` - Get hospital details
- `POST /api/hospitals/recommendations` - Get personalized recommendations
- `GET /api/hospitals/:id/doctors` - Get hospital doctors
- `GET /api/hospitals/specialties` - List all specialties
- `GET /api/hospitals/cities` - List all cities

### Appointments
- `GET /api/appointments` - List user appointments
- `GET /api/appointments/:id` - Get appointment details
- `POST /api/appointments` - Book appointment
- `PUT /api/appointments/:id` - Update appointment
- `DELETE /api/appointments/:id` - Cancel appointment
- `GET /api/appointments/available-slots` - Get doctor availability

### Admin (Admin only)
- `GET /api/admin/stats` - Dashboard statistics
- `POST /api/admin/hospitals` - Create hospital
- `PUT /api/admin/hospitals/:id` - Update hospital
- `DELETE /api/admin/hospitals/:id` - Delete hospital
- `POST /api/admin/doctors` - Create doctor
- `PUT /api/admin/doctors/:id` - Update doctor
- `POST /api/admin/appointments/:id/complete` - Mark complete

### Constraint Lab
- `GET /api/constraints` - List all constraints
- `GET /api/constraints/:id` - Get constraint details
- `POST /api/constraints/:id/test` - Run constraint test
- `GET /api/constraints/logs` - Get test logs

---

## 🧪 Testing

### Manual Testing Checklist

**Patient Flow:**
1. ✅ Register new account (with age)
2. ✅ Login as patient
3. ✅ Search hospitals
4. ✅ View hospital details
5. ✅ Book appointment
6. ✅ View appointments
7. ✅ Check past records
8. ✅ Update profile
9. ✅ Change language

**Admin Flow:**
1. ✅ Login as admin
2. ✅ View admin dashboard
3. ✅ Manage hospitals
4. ✅ Manage doctors
5. ✅ Complete appointments

**Constraint Lab:**
1. ✅ Run test scenarios (C01-C12)
2. ✅ View results (PASS/FAIL)
3. ✅ Check audit logs

### Automated Testing

```bash
# Backend tests
cd backend
python test_authentication.py
```

---

## 🔒 Security Features

- **JWT Authentication** - Secure token-based auth
- **Password Hashing** - Werkzeug PBKDF2-SHA256
- **CORS Protection** - Configured allowed origins
- **Input Validation** - Server-side validation
- **SQL Injection Prevention** - SQLAlchemy ORM
- **XSS Protection** - React auto-escaping

---

## 🌐 Browser Support

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ Safari 14+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

---

## 📱 Responsive Design

- **Desktop:** 1920px and above - Full layout
- **Laptop:** 1366px - Optimized layout
- **Tablet:** 768px - Adjusted grids
- **Mobile:** 375px and above - Single column

---

## 🐛 Troubleshooting

### Backend Issues

**Database connection error:**
```bash
# Check MySQL is running
mysql -u root -p

# Verify database exists
SHOW DATABASES;

# Update config.py with correct credentials
```

**Module not found:**
```bash
pip install -r requirements.txt
```

### Frontend Issues

**Can't see text (white on white):**
```bash
# Hard refresh browser
Ctrl + F5 (Windows)
Cmd + Shift + R (Mac)
```

**API connection refused:**
- Verify backend is running on port 5000
- Check `frontend/src/config.js` has correct API_BASE_URL

**401 Unauthorized:**
- Logout and login again
- Check localStorage has token
- Verify JWT_SECRET_KEY matches in backend

### Common Fixes

```bash
# Clear browser cache and storage
# Open DevTools (F12) > Application > Clear Storage

# Restart backend
cd backend
python app.py

# Restart frontend
cd frontend
npm run dev
```

---

## 🚀 Deployment

### Production Checklist

**Backend:**
- [ ] Change JWT_SECRET_KEY to strong random value
- [ ] Change SECRET_KEY to strong random value
- [ ] Set DEBUG = False
- [ ] Configure production database
- [ ] Set up HTTPS
- [ ] Configure production CORS origins
- [ ] Use production WSGI server (gunicorn)
- [ ] Set up logging

**Frontend:**
- [ ] Update API_BASE_URL to production backend
- [ ] Build production bundle: `npm run build`
- [ ] Deploy `dist/` folder to hosting
- [ ] Configure HTTPS
- [ ] Set up CDN (optional)

**Database:**
- [ ] Backup database regularly
- [ ] Use strong passwords
- [ ] Limit remote access
- [ ] Enable SSL connections

---

## 📄 License

This project is created for educational and demonstration purposes.

---

## 👥 Contributors

Built for healthcare accessibility and patient empowerment.

---

## 📞 Support

For issues or questions:
1. Check troubleshooting section above
2. Verify all dependencies are installed
3. Check browser console for errors
4. Verify backend logs for API errors

---

## 🎯 Project Status

**Status:** ✅ **Production Ready**

**Last Updated:** 2024

**Version:** 2.0

---

## 📝 Notes

### Registration
- Age input field (1-120 years)
- Backend calculates approximate birth year
- Age is optional

### Authentication
- JWT tokens expire after 24 hours
- String identity used for consistency
- Tokens stored in localStorage

### Data
- Demo data included via `seed_data.py`
- Contains sample hospitals, doctors, appointments
- Safe to use for testing and demos

---

**Ready for hackathon demonstration and production deployment! 🚀**
