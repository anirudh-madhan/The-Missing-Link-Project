"""
Database seeder with realistic healthcare data for The Missing Link
"""
from app import create_app
from models import db, User, Hospital, Doctor, Appointment
from datetime import datetime, timedelta
import json

app = create_app()

def seed_database():
    with app.app_context():
        # Drop and recreate all tables
        print("Creating database tables...")
        db.drop_all()
        db.create_all()
        
        # Create admin user
        print("Creating admin user...")
        admin = User(
            email='admin@hospital.com',
            full_name='System Administrator',
            phone='+91-9876543210',
            language_preference='en',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create test patient users
        print("Creating test patients...")
        patients = [
            {
                'email': 'john.doe@email.com',
                'full_name': 'John Doe',
                'phone': '+91-9876543211',
                'language_preference': 'en',
                'date_of_birth': datetime(1985, 5, 15).date(),
                'password': 'patient123'
            },
            {
                'email': 'priya.sharma@email.com',
                'full_name': 'Priya Sharma',
                'phone': '+91-9876543212',
                'language_preference': 'ta',
                'date_of_birth': datetime(1990, 8, 20).date(),
                'password': 'patient123'
            },
            {
                'email': 'raj.kumar@email.com',
                'full_name': 'Raj Kumar',
                'phone': '+91-9876543213',
                'language_preference': 'en',
                'date_of_birth': datetime(1978, 12, 10).date(),
                'accessibility_needs': 'Wheelchair accessibility required',
                'password': 'patient123'
            }
        ]
        
        for patient_data in patients:
            password = patient_data.pop('password')
            patient = User(**patient_data, is_admin=False)
            patient.set_password(password)
            db.session.add(patient)
        
        db.session.commit()
        
        # Create hospitals
        print("Creating hospitals...")
        hospitals_data = [
            {
                'name': 'Apollo Hospital',
                'name_tamil': 'அப்போலோ மருத்துவமனை',
                'address': '21, Greams Lane, Off Greams Road',
                'city': 'Chennai',
                'state': 'Tamil Nadu',
                'pincode': '600006',
                'phone': '+91-44-28296000',
                'email': 'info@apollohospitals.com',
                'latitude': 13.0569,
                'longitude': 80.2508,
                'specialties': json.dumps(['Cardiology', 'Neurology', 'Orthopedics', 'Oncology', 'Pediatrics']),
                'languages_supported': json.dumps(['English', 'Tamil', 'Hindi']),
                'accessibility_features': json.dumps(['Wheelchair Access', 'Elevators', 'Accessible Restrooms', 'Sign Language Interpreter']),
                'emergency_available': True,
                'rating': 4.7,
                'total_beds': 200,
                'available_beds': 45
            },
            {
                'name': 'Fortis Hospital',
                'name_tamil': 'ஃபோர்டிஸ் மருத்துவமனை',
                'address': '154/9, Opp. IIM-B, Bannerghatta Road',
                'city': 'Bangalore',
                'state': 'Karnataka',
                'pincode': '560076',
                'phone': '+91-80-66214444',
                'email': 'contact@fortishealthcare.com',
                'latitude': 12.8996,
                'longitude': 77.5993,
                'specialties': json.dumps(['Cardiology', 'Neurosurgery', 'Gastroenterology', 'Urology', 'Emergency Medicine']),
                'languages_supported': json.dumps(['English', 'Kannada', 'Hindi', 'Tamil']),
                'accessibility_features': json.dumps(['Wheelchair Access', 'Ramps', 'Accessible Parking']),
                'emergency_available': True,
                'rating': 4.5,
                'total_beds': 150,
                'available_beds': 30
            },
            {
                'name': 'AIIMS Delhi',
                'name_tamil': 'எய்ம்ஸ் டெல்லி',
                'address': 'Ansari Nagar',
                'city': 'New Delhi',
                'state': 'Delhi',
                'pincode': '110029',
                'phone': '+91-11-26588500',
                'email': 'aiims@aiims.edu',
                'latitude': 28.5672,
                'longitude': 77.2100,
                'specialties': json.dumps(['General Medicine', 'Surgery', 'Pediatrics', 'Radiology', 'Emergency Medicine']),
                'languages_supported': json.dumps(['English', 'Hindi']),
                'accessibility_features': json.dumps(['Wheelchair Access', 'Elevators', 'Accessible Restrooms']),
                'emergency_available': True,
                'rating': 4.8,
                'total_beds': 300,
                'available_beds': 80
            },
            {
                'name': 'Manipal Hospital',
                'name_tamil': 'மணிப்பால் மருத்துவமனை',
                'address': '98, HAL Airport Road',
                'city': 'Bangalore',
                'state': 'Karnataka',
                'pincode': '560017',
                'phone': '+91-80-25024444',
                'email': 'info@manipalhospitals.com',
                'latitude': 12.9594,
                'longitude': 77.6462,
                'specialties': json.dumps(['Orthopedics', 'Cardiology', 'Nephrology', 'Pulmonology', 'Dermatology']),
                'languages_supported': json.dumps(['English', 'Kannada', 'Tamil']),
                'accessibility_features': json.dumps(['Wheelchair Access', 'Ramps', 'Elevators']),
                'emergency_available': True,
                'rating': 4.6,
                'total_beds': 180,
                'available_beds': 55
            },
            {
                'name': 'Max Super Speciality Hospital',
                'name_tamil': 'மேக்ஸ் சூப்பர் ஸ்பெஷாலிட்டி மருத்துவமனை',
                'address': '1, Press Enclave Road, Saket',
                'city': 'New Delhi',
                'state': 'Delhi',
                'pincode': '110017',
                'phone': '+91-11-26515050',
                'email': 'info@maxhealthcare.com',
                'latitude': 28.5244,
                'longitude': 77.2066,
                'specialties': json.dumps(['Oncology', 'Cardiology', 'Neurosciences', 'Orthopedics', 'Gastroenterology']),
                'languages_supported': json.dumps(['English', 'Hindi', 'Punjabi']),
                'accessibility_features': json.dumps(['Wheelchair Access', 'Accessible Restrooms', 'Braille Signage']),
                'emergency_available': True,
                'rating': 4.4,
                'total_beds': 220,
                'available_beds': 65
            },
            {
                'name': 'Government General Hospital',
                'name_tamil': 'அரசு பொது மருத்துவமனை',
                'address': 'Park Town',
                'city': 'Chennai',
                'state': 'Tamil Nadu',
                'pincode': '600003',
                'phone': '+91-44-25305000',
                'email': 'contact@ggh.tn.gov.in',
                'latitude': 13.0878,
                'longitude': 80.2785,
                'specialties': json.dumps(['General Medicine', 'Surgery', 'Pediatrics', 'Obstetrics', 'Emergency Medicine']),
                'languages_supported': json.dumps(['Tamil', 'English']),
                'accessibility_features': json.dumps(['Wheelchair Access', 'Ramps']),
                'emergency_available': True,
                'rating': 4.0,
                'total_beds': 400,
                'available_beds': 120
            },
            {
                'name': 'Columbia Asia Hospital',
                'name_tamil': 'கொலம்பியா ஏசியா மருத்துவமனை',
                'address': 'Kirloskar Business Park, Hebbal',
                'city': 'Bangalore',
                'state': 'Karnataka',
                'pincode': '560024',
                'phone': '+91-80-39895000',
                'email': 'info@columbiaasia.com',
                'latitude': 13.0358,
                'longitude': 77.5977,
                'specialties': json.dumps(['General Surgery', 'Internal Medicine', 'Pediatrics', 'Orthopedics']),
                'languages_supported': json.dumps(['English', 'Kannada', 'Hindi']),
                'accessibility_features': json.dumps(['Wheelchair Access', 'Elevators']),
                'emergency_available': False,
                'rating': 4.3,
                'total_beds': 100,
                'available_beds': 25
            }
        ]
        
        hospitals = []
        for hospital_data in hospitals_data:
            hospital = Hospital(**hospital_data)
            db.session.add(hospital)
            hospitals.append(hospital)
        
        db.session.commit()
        
        # Create doctors
        print("Creating doctors...")
        doctors_data = [
            # Apollo Hospital - Chennai
            {
                'hospital_id': hospitals[0].id,
                'name': 'Dr. Rajesh Kumar',
                'name_tamil': 'டாக்டர். ராஜேஷ் குமார்',
                'specialty': 'Cardiology',
                'qualification': 'MD, DM (Cardiology)',
                'languages': json.dumps(['English', 'Tamil', 'Hindi']),
                'consultation_fee': 1000.0,
                'available_days': json.dumps(['Monday', 'Wednesday', 'Friday']),
                'available_times': json.dumps(['09:00', '10:00', '11:00', '14:00', '15:00', '16:00'])
            },
            {
                'hospital_id': hospitals[0].id,
                'name': 'Dr. Priya Menon',
                'name_tamil': 'டாக்டர். பிரியா மேனன்',
                'specialty': 'Neurology',
                'qualification': 'MD, DM (Neurology)',
                'languages': json.dumps(['English', 'Tamil']),
                'consultation_fee': 1200.0,
                'available_days': json.dumps(['Tuesday', 'Thursday', 'Saturday']),
                'available_times': json.dumps(['09:00', '10:00', '11:00', '14:00', '15:00'])
            },
            {
                'hospital_id': hospitals[0].id,
                'name': 'Dr. Suresh Raman',
                'name_tamil': 'டாக்டர். சுரேஷ் ராமன்',
                'specialty': 'Orthopedics',
                'qualification': 'MS (Ortho)',
                'languages': json.dumps(['English', 'Tamil']),
                'consultation_fee': 800.0,
                'available_days': json.dumps(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']),
                'available_times': json.dumps(['09:00', '10:00', '14:00', '15:00', '16:00', '17:00'])
            },
            # Fortis Hospital - Bangalore
            {
                'hospital_id': hospitals[1].id,
                'name': 'Dr. Amit Sharma',
                'name_tamil': 'டாக்டர். அமித் சர்மா',
                'specialty': 'Cardiology',
                'qualification': 'MD, DM (Cardiology)',
                'languages': json.dumps(['English', 'Hindi', 'Kannada']),
                'consultation_fee': 1100.0,
                'available_days': json.dumps(['Monday', 'Wednesday', 'Friday']),
                'available_times': json.dumps(['10:00', '11:00', '14:00', '15:00', '16:00'])
            },
            {
                'hospital_id': hospitals[1].id,
                'name': 'Dr. Kavitha Reddy',
                'name_tamil': 'டாக்டர். கவிதா ரெட்டி',
                'specialty': 'Gastroenterology',
                'qualification': 'MD, DM (Gastro)',
                'languages': json.dumps(['English', 'Kannada', 'Tamil']),
                'consultation_fee': 900.0,
                'available_days': json.dumps(['Tuesday', 'Thursday', 'Friday']),
                'available_times': json.dumps(['09:00', '10:00', '11:00', '14:00', '15:00'])
            },
            # AIIMS Delhi
            {
                'hospital_id': hospitals[2].id,
                'name': 'Dr. Vikram Singh',
                'name_tamil': 'டாக்டர். விக்ரம் சிங்',
                'specialty': 'General Medicine',
                'qualification': 'MBBS, MD',
                'languages': json.dumps(['English', 'Hindi']),
                'consultation_fee': 500.0,
                'available_days': json.dumps(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']),
                'available_times': json.dumps(['09:00', '10:00', '11:00', '12:00', '14:00', '15:00'])
            },
            {
                'hospital_id': hospitals[2].id,
                'name': 'Dr. Anjali Gupta',
                'name_tamil': 'டாக்டர். அஞ்சலி குப்தா',
                'specialty': 'Pediatrics',
                'qualification': 'MBBS, MD (Pediatrics)',
                'languages': json.dumps(['English', 'Hindi']),
                'consultation_fee': 600.0,
                'available_days': json.dumps(['Monday', 'Wednesday', 'Friday', 'Saturday']),
                'available_times': json.dumps(['09:00', '10:00', '11:00', '14:00', '15:00'])
            },
            # Manipal Hospital - Bangalore
            {
                'hospital_id': hospitals[3].id,
                'name': 'Dr. Ramesh Rao',
                'name_tamil': 'டாக்டர். ரமேஷ் ராவ்',
                'specialty': 'Orthopedics',
                'qualification': 'MS (Ortho), MCh',
                'languages': json.dumps(['English', 'Kannada']),
                'consultation_fee': 950.0,
                'available_days': json.dumps(['Monday', 'Tuesday', 'Thursday', 'Friday']),
                'available_times': json.dumps(['09:00', '10:00', '11:00', '15:00', '16:00'])
            },
            {
                'hospital_id': hospitals[3].id,
                'name': 'Dr. Lakshmi Iyer',
                'name_tamil': 'டாக்டர். லட்சுமி ஐயர்',
                'specialty': 'Dermatology',
                'qualification': 'MD (Dermatology)',
                'languages': json.dumps(['English', 'Tamil', 'Kannada']),
                'consultation_fee': 750.0,
                'available_days': json.dumps(['Tuesday', 'Wednesday', 'Thursday', 'Saturday']),
                'available_times': json.dumps(['10:00', '11:00', '14:00', '15:00', '16:00'])
            },
            # Max Hospital - Delhi
            {
                'hospital_id': hospitals[4].id,
                'name': 'Dr. Anil Kapoor',
                'name_tamil': 'டாக்டர். அனில் கபூர்',
                'specialty': 'Oncology',
                'qualification': 'MD, DM (Medical Oncology)',
                'languages': json.dumps(['English', 'Hindi', 'Punjabi']),
                'consultation_fee': 1500.0,
                'available_days': json.dumps(['Monday', 'Wednesday', 'Thursday']),
                'available_times': json.dumps(['10:00', '11:00', '14:00', '15:00'])
            },
            # Government General Hospital - Chennai
            {
                'hospital_id': hospitals[5].id,
                'name': 'Dr. Murugan Selvam',
                'name_tamil': 'டாக்டர். முருகன் செல்வம்',
                'specialty': 'General Surgery',
                'qualification': 'MBBS, MS (General Surgery)',
                'languages': json.dumps(['Tamil', 'English']),
                'consultation_fee': 200.0,
                'available_days': json.dumps(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']),
                'available_times': json.dumps(['09:00', '10:00', '11:00', '12:00', '14:00', '15:00', '16:00'])
            },
            # Columbia Asia - Bangalore
            {
                'hospital_id': hospitals[6].id,
                'name': 'Dr. Sneha Patil',
                'name_tamil': 'டாக்டர். ஸ்னேகா பாடீல்',
                'specialty': 'Internal Medicine',
                'qualification': 'MBBS, MD',
                'languages': json.dumps(['English', 'Kannada', 'Hindi']),
                'consultation_fee': 650.0,
                'available_days': json.dumps(['Monday', 'Tuesday', 'Wednesday', 'Friday']),
                'available_times': json.dumps(['09:00', '10:00', '11:00', '14:00', '15:00', '16:00'])
            }
        ]
        
        doctors = []
        for doctor_data in doctors_data:
            doctor = Doctor(**doctor_data)
            db.session.add(doctor)
            doctors.append(doctor)
        
        db.session.commit()
        
        # Create sample appointments
        print("Creating sample appointments...")
        patients_list = User.query.filter_by(is_admin=False).all()
        
        if len(patients_list) > 0 and len(doctors) > 0:
            appointments_data = [
                {
                    'patient_id': patients_list[0].id,
                    'hospital_id': hospitals[0].id,
                    'doctor_id': doctors[0].id,
                    'appointment_date': (datetime.now() + timedelta(days=3)).date(),
                    'appointment_time': '10:00',
                    'reason': 'Regular cardiac checkup',
                    'documents_required': json.dumps(['govt_id', 'insurance', 'medical_records']),
                    'documents_submitted': json.dumps(['govt_id']),
                    'status': 'scheduled'
                },
                {
                    'patient_id': patients_list[0].id,
                    'hospital_id': hospitals[2].id,
                    'doctor_id': doctors[5].id,
                    'appointment_date': (datetime.now() - timedelta(days=10)).date(),
                    'appointment_time': '14:00',
                    'reason': 'General health consultation',
                    'documents_required': json.dumps(['govt_id']),
                    'documents_submitted': json.dumps(['govt_id']),
                    'status': 'completed'
                },
                {
                    'patient_id': patients_list[1].id if len(patients_list) > 1 else patients_list[0].id,
                    'hospital_id': hospitals[1].id,
                    'doctor_id': doctors[3].id,
                    'appointment_date': (datetime.now() + timedelta(days=5)).date(),
                    'appointment_time': '11:00',
                    'reason': 'Heart consultation',
                    'documents_required': json.dumps(['govt_id', 'referral']),
                    'documents_submitted': json.dumps([]),
                    'status': 'scheduled'
                }
            ]
            
            for appointment_data in appointments_data:
                appointment = Appointment(**appointment_data)
                db.session.add(appointment)
            
            db.session.commit()
        
        print("\n" + "="*60)
        print("Database seeded successfully!")
        print("="*60)
        print("\n📊 Summary:")
        print(f"  ✓ {User.query.count()} users created")
        print(f"  ✓ {Hospital.query.count()} hospitals created")
        print(f"  ✓ {Doctor.query.count()} doctors created")
        print(f"  ✓ {Appointment.query.count()} appointments created")
        print("\n🔐 Test Credentials:")
        print("  Admin: admin@hospital.com / admin123")
        print("  Patient: john.doe@email.com / patient123")
        print("="*60)


if __name__ == '__main__':
    seed_database()
