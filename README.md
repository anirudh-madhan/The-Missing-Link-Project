# The Missing Link

### Patient Journey & Healthcare Access Navigator

The Missing Link is a healthcare access platform designed to simplify the patient journey by connecting patients with hospitals, doctors, and essential healthcare services through a single application.

The platform helps users discover healthcare facilities, explore available services, manage appointments, access visit history, and review important accessibility and language information.

---

## Overview

Navigating healthcare services often involves multiple steps, from finding a suitable hospital to booking an appointment and keeping track of visits.

The Missing Link brings these essential steps together in one platform, helping patients make more informed decisions and manage their healthcare journey more conveniently.

The application provides separate interfaces for patients and administrators, along with a dedicated system validation module.

## Features

### Patient Features

- **Hospital Discovery:** Browse and search hospitals using available filters such as city, specialty, language, and accessibility.
- **Hospital Details:** Explore hospital information, available specialties, and associated doctors.
- **Appointment Booking:** Book appointments with available doctors.
- **Appointment Management:** View, reschedule, and cancel appointments.
- **Past Records:** Access previous and upcoming appointment history.
- **Hospital Recommendations:** Receive hospital suggestions based on preferences such as specialty, location, language, and accessibility requirements.
- **Multilingual Support:** Switch between English and Tamil.
- **Accessibility Information:** Review available accessibility features of healthcare facilities.
- **Profile Management:** View and update personal profile information.

### Admin Features

- **Admin Dashboard:** View hospital and appointment statistics.
- **Hospital Management:** Add, update, and manage hospital records.
- **Doctor Management:** Maintain doctor information and availability.
- **Appointment Management:** View appointments and update their completion status.

### System Validation

- **Constraint Lab:** Run predefined healthcare-related scenario checks.
- **Test Results:** View pass/fail results for executed scenarios.
- **Audit Logs:** Review recorded constraint test executions.

---

## Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | React 18, React Router, Axios, Vite, CSS3 |
| Backend | Python, Flask |
| Authentication | Flask-JWT-Extended, Werkzeug |
| API | REST API, Flask-CORS |
| ORM | SQLAlchemy, Flask-SQLAlchemy |
| Database | MySQL |
| Database Driver | PyMySQL |

---

## System Architecture

The application follows a client-server architecture.

1. The React frontend provides the user interface.
2. The Flask backend handles API requests, authentication, and application logic.
3. SQLAlchemy manages database operations.
4. MySQL stores application data.

```text
        User
         |
         v
   React Frontend
      (Vite)
         |
         | REST API
         v
    Flask Backend
         |
         v
     SQLAlchemy
         |
         v
      MySQL DB
```

---

## Project Structure

```text
The-Missing-Link-Project/
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── models.py
│   ├── requirements.txt
│   ├── seed_data.py
│   │
│   └── routes/
│       ├── auth.py
│       ├── hospitals.py
│       ├── appointments.py
│       ├── admin.py
│       └── constraints.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── config.js
│   │
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

Make sure the following are installed:

- Python 3.8 or later
- Node.js and npm
- MySQL Server
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/anirudh-madhan/The-Missing-Link-Project.git

cd The-Missing-Link-Project
```

### 2. Configure the MySQL Database

Start your MySQL server and create the database:

```sql
CREATE DATABASE missing_link_db;
```

Update the database credentials in `backend/config.py`, or provide the corresponding environment variables:

```text
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=missing_link_db
MYSQL_PORT=3306
```

Use your own MySQL credentials.

### 3. Set Up the Backend

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

**Windows PowerShell**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python -m venv venv
source venv/bin/activate
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Start the Flask application:

```bash
python app.py
```

The application creates the required database tables when it starts.

Backend URL:

```text
http://localhost:5000
```

### 4. Set Up the Frontend

Open a separate terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the Vite development server:

```bash
npm run dev
```

Frontend URL (default):

```text
http://localhost:5173
```

### 5. Access the Application

Open the frontend URL in your browser.

Make sure both the Flask backend and React frontend development servers are running.

---

## Demo Credentials

The following sample accounts are created by the database seeding script.

**Patient Account**

```text
Email: john.doe@email.com
Password: patient123
```

**Admin Account**

```text
Email: admin@hospital.com
Password: admin123
```

These credentials are intended only for local demonstration and testing. Do not use them in a deployed environment.

### Loading Sample Data

To populate the database with sample users, hospitals, doctors, and appointments:

```bash
cd backend
python seed_data.py
```

**Important:** The current seeding script drops and recreates the database tables before inserting sample data. Run it only when you are comfortable replacing the existing data.

---

## API Modules

The Flask backend provides REST API endpoints organized into the following modules:

| Module | Description |
|---|---|
| Authentication | User registration, login, and profile management |
| Hospitals | Hospital listings, details, specialties, cities, and recommendations |
| Appointments | Booking, retrieval, updates, cancellation, and availability |
| Administration | Hospital and doctor management, statistics, and appointment operations |
| Constraint Lab | Scenario retrieval, test execution, and audit logs |

The `backend/routes/` directory contains the API implementation and should be referred to for exact endpoint paths and request formats.

---

## Security

The application includes the following security-related mechanisms:

- JWT-based authentication.
- Password hashing using Werkzeug.
- Backend request validation.
- SQLAlchemy ORM for database operations.
- Configured CORS handling.
- Protected endpoints for authenticated operations.

For deployment, configure strong and unique application secrets, disable debug mode, restrict allowed origins, and use HTTPS with appropriate database access controls.

---

## Running the Application

The application requires two separate terminal sessions.

**Terminal 1 – Backend**

```bash
cd backend
venv\Scripts\activate
python app.py
```

**Terminal 2 – Frontend**

```bash
cd frontend
npm run dev
```

Open the frontend URL displayed by Vite to use the application.

---

## Future Enhancements

Potential areas for further development include:

- Integration with real-time hospital and doctor availability.
- Secure medical document storage and management.
- Appointment reminders and follow-up notifications.
- Expanded language support.
- Enhanced accessibility features.
- Integration with external healthcare services.

---

## License

No license has currently been specified for this repository.

---

**The Missing Link — Connecting patients to the healthcare services they need.**
