from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    language_preference = db.Column(db.String(10), default='en')  # en or ta
    accessibility_needs = db.Column(db.Text)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    appointments = db.relationship('Appointment', backref='patient', lazy=True, foreign_keys='Appointment.patient_id')
    
    def set_password(self, password):
        # Use pbkdf2:sha256 method explicitly for consistency
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'phone': self.phone,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'language_preference': self.language_preference,
            'accessibility_needs': self.accessibility_needs,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat()
        }


class Hospital(db.Model):
    __tablename__ = 'hospitals'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    name_tamil = db.Column(db.String(200))
    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    specialties = db.Column(db.Text)  # JSON array stored as text
    languages_supported = db.Column(db.Text)  # JSON array
    accessibility_features = db.Column(db.Text)  # JSON array
    emergency_available = db.Column(db.Boolean, default=True)
    rating = db.Column(db.Float, default=4.0)
    total_beds = db.Column(db.Integer, default=100)
    available_beds = db.Column(db.Integer, default=50)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    doctors = db.relationship('Doctor', backref='hospital', lazy=True, cascade='all, delete-orphan')
    appointments = db.relationship('Appointment', backref='hospital', lazy=True)
    
    def to_dict(self):
        import json
        return {
            'id': self.id,
            'name': self.name,
            'name_tamil': self.name_tamil,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'pincode': self.pincode,
            'phone': self.phone,
            'email': self.email,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'specialties': json.loads(self.specialties) if self.specialties else [],
            'languages_supported': json.loads(self.languages_supported) if self.languages_supported else [],
            'accessibility_features': json.loads(self.accessibility_features) if self.accessibility_features else [],
            'emergency_available': self.emergency_available,
            'rating': self.rating,
            'total_beds': self.total_beds,
            'available_beds': self.available_beds,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }


class Doctor(db.Model):
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    name_tamil = db.Column(db.String(100))
    specialty = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(200))
    languages = db.Column(db.Text)  # JSON array
    consultation_fee = db.Column(db.Float, default=500.0)
    available_days = db.Column(db.Text)  # JSON array of days
    available_times = db.Column(db.Text)  # JSON array of time slots
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)
    
    def to_dict(self):
        import json
        return {
            'id': self.id,
            'hospital_id': self.hospital_id,
            'name': self.name,
            'name_tamil': self.name_tamil,
            'specialty': self.specialty,
            'qualification': self.qualification,
            'languages': json.loads(self.languages) if self.languages else [],
            'consultation_fee': self.consultation_fee,
            'available_days': json.loads(self.available_days) if self.available_days else [],
            'available_times': json.loads(self.available_times) if self.available_times else [],
            'is_available': self.is_available
        }


class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled, rescheduled
    reason = db.Column(db.Text)
    notes = db.Column(db.Text)
    documents_required = db.Column(db.Text)  # JSON array
    documents_submitted = db.Column(db.Text)  # JSON array
    reminder_sent = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        import json
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'patient_name': self.patient.full_name if self.patient else None,
            'hospital_id': self.hospital_id,
            'hospital_name': self.hospital.name if self.hospital else None,
            'doctor_id': self.doctor_id,
            'doctor_name': self.doctor.name if self.doctor else None,
            'doctor_specialty': self.doctor.specialty if self.doctor else None,
            'appointment_date': self.appointment_date.isoformat() if self.appointment_date else None,
            'appointment_time': self.appointment_time,
            'status': self.status,
            'reason': self.reason,
            'notes': self.notes,
            'documents_required': json.loads(self.documents_required) if self.documents_required else [],
            'documents_submitted': json.loads(self.documents_submitted) if self.documents_submitted else [],
            'reminder_sent': self.reminder_sent,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class ConstraintLog(db.Model):
    __tablename__ = 'constraint_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    constraint_id = db.Column(db.String(10), nullable=False)  # C01-C12
    constraint_name = db.Column(db.String(100), nullable=False)
    test_case = db.Column(db.Text, nullable=False)
    system_response = db.Column(db.Text, nullable=False)
    result = db.Column(db.String(20), nullable=False)  # PASS or FAIL
    execution_time = db.Column(db.Float)  # in seconds
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.Text)  # Additional JSON details
    
    def to_dict(self):
        return {
            'id': self.id,
            'constraint_id': self.constraint_id,
            'constraint_name': self.constraint_name,
            'test_case': self.test_case,
            'system_response': self.system_response,
            'result': self.result,
            'execution_time': self.execution_time,
            'timestamp': self.timestamp.isoformat(),
            'details': self.details
        }
