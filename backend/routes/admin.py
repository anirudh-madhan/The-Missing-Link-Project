from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Hospital, Doctor, Appointment, ConstraintLog
from datetime import datetime, timedelta
import json

admin_bp = Blueprint('admin', __name__)

def admin_required():
    """Decorator to check if user is admin"""
    user_id = int(get_jwt_identity())  # Convert string to int
    user = User.query.get(user_id)
    if not user or not user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
    return None

@admin_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    try:
        error = admin_required()
        if error:
            return error
        
        # Calculate statistics
        total_hospitals = Hospital.query.filter_by(is_active=True).count()
        total_doctors = Doctor.query.filter_by(is_available=True).count()
        total_patients = User.query.filter_by(is_admin=False).count()
        
        # Appointment statistics
        total_appointments = Appointment.query.count()
        scheduled_appointments = Appointment.query.filter_by(status='scheduled').count()
        completed_appointments = Appointment.query.filter_by(status='completed').count()
        cancelled_appointments = Appointment.query.filter_by(status='cancelled').count()
        
        # Recent appointments (last 7 days)
        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_appointments = Appointment.query.filter(
            Appointment.created_at >= seven_days_ago
        ).count()
        
        # Bed availability
        hospitals = Hospital.query.filter_by(is_active=True).all()
        total_beds = sum(h.total_beds for h in hospitals)
        available_beds = sum(h.available_beds for h in hospitals)
        
        return jsonify({
            'hospitals': total_hospitals,
            'doctors': total_doctors,
            'patients': total_patients,
            'appointments': {
                'total': total_appointments,
                'scheduled': scheduled_appointments,
                'completed': completed_appointments,
                'cancelled': cancelled_appointments,
                'recent': recent_appointments
            },
            'beds': {
                'total': total_beds,
                'available': available_beds,
                'occupancy_rate': round((total_beds - available_beds) / total_beds * 100, 2) if total_beds > 0 else 0
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/hospitals', methods=['POST'])
@jwt_required()
def create_hospital():
    try:
        error = admin_required()
        if error:
            return error
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'address', 'city', 'state']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        hospital = Hospital(
            name=data['name'],
            name_tamil=data.get('name_tamil'),
            address=data['address'],
            city=data['city'],
            state=data['state'],
            pincode=data.get('pincode'),
            phone=data.get('phone'),
            email=data.get('email'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            specialties=json.dumps(data.get('specialties', [])),
            languages_supported=json.dumps(data.get('languages_supported', ['English'])),
            accessibility_features=json.dumps(data.get('accessibility_features', [])),
            emergency_available=data.get('emergency_available', True),
            total_beds=data.get('total_beds', 100),
            available_beds=data.get('available_beds', 50),
            rating=data.get('rating', 4.0)
        )
        
        db.session.add(hospital)
        db.session.commit()
        
        return jsonify({
            'message': 'Hospital created successfully',
            'hospital': hospital.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/hospitals/<int:hospital_id>', methods=['PUT'])
@jwt_required()
def update_hospital(hospital_id):
    try:
        error = admin_required()
        if error:
            return error
        
        hospital = Hospital.query.get(hospital_id)
        
        if not hospital:
            return jsonify({'error': 'Hospital not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'name' in data:
            hospital.name = data['name']
        if 'name_tamil' in data:
            hospital.name_tamil = data['name_tamil']
        if 'address' in data:
            hospital.address = data['address']
        if 'city' in data:
            hospital.city = data['city']
        if 'state' in data:
            hospital.state = data['state']
        if 'pincode' in data:
            hospital.pincode = data['pincode']
        if 'phone' in data:
            hospital.phone = data['phone']
        if 'email' in data:
            hospital.email = data['email']
        if 'latitude' in data:
            hospital.latitude = data['latitude']
        if 'longitude' in data:
            hospital.longitude = data['longitude']
        if 'specialties' in data:
            hospital.specialties = json.dumps(data['specialties'])
        if 'languages_supported' in data:
            hospital.languages_supported = json.dumps(data['languages_supported'])
        if 'accessibility_features' in data:
            hospital.accessibility_features = json.dumps(data['accessibility_features'])
        if 'emergency_available' in data:
            hospital.emergency_available = data['emergency_available']
        if 'total_beds' in data:
            hospital.total_beds = data['total_beds']
        if 'available_beds' in data:
            hospital.available_beds = data['available_beds']
        if 'rating' in data:
            hospital.rating = data['rating']
        if 'is_active' in data:
            hospital.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Hospital updated successfully',
            'hospital': hospital.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/hospitals/<int:hospital_id>', methods=['DELETE'])
@jwt_required()
def delete_hospital(hospital_id):
    try:
        error = admin_required()
        if error:
            return error
        
        hospital = Hospital.query.get(hospital_id)
        
        if not hospital:
            return jsonify({'error': 'Hospital not found'}), 404
        
        # Soft delete - mark as inactive
        hospital.is_active = False
        db.session.commit()
        
        return jsonify({'message': 'Hospital deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/doctors', methods=['POST'])
@jwt_required()
def create_doctor():
    try:
        error = admin_required()
        if error:
            return error
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['hospital_id', 'name', 'specialty']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate hospital exists
        hospital = Hospital.query.get(data['hospital_id'])
        if not hospital:
            return jsonify({'error': 'Hospital not found'}), 404
        
        doctor = Doctor(
            hospital_id=data['hospital_id'],
            name=data['name'],
            name_tamil=data.get('name_tamil'),
            specialty=data['specialty'],
            qualification=data.get('qualification'),
            languages=json.dumps(data.get('languages', ['English'])),
            consultation_fee=data.get('consultation_fee', 500.0),
            available_days=json.dumps(data.get('available_days', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])),
            available_times=json.dumps(data.get('available_times', ['09:00', '10:00', '11:00', '14:00', '15:00', '16:00']))
        )
        
        db.session.add(doctor)
        db.session.commit()
        
        return jsonify({
            'message': 'Doctor created successfully',
            'doctor': doctor.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/doctors/<int:doctor_id>', methods=['PUT'])
@jwt_required()
def update_doctor(doctor_id):
    try:
        error = admin_required()
        if error:
            return error
        
        doctor = Doctor.query.get(doctor_id)
        
        if not doctor:
            return jsonify({'error': 'Doctor not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'name' in data:
            doctor.name = data['name']
        if 'name_tamil' in data:
            doctor.name_tamil = data['name_tamil']
        if 'specialty' in data:
            doctor.specialty = data['specialty']
        if 'qualification' in data:
            doctor.qualification = data['qualification']
        if 'languages' in data:
            doctor.languages = json.dumps(data['languages'])
        if 'consultation_fee' in data:
            doctor.consultation_fee = data['consultation_fee']
        if 'available_days' in data:
            doctor.available_days = json.dumps(data['available_days'])
        if 'available_times' in data:
            doctor.available_times = json.dumps(data['available_times'])
        if 'is_available' in data:
            doctor.is_available = data['is_available']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Doctor updated successfully',
            'doctor': doctor.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/appointments/<int:appointment_id>/complete', methods=['POST'])
@jwt_required()
def complete_appointment(appointment_id):
    try:
        error = admin_required()
        if error:
            return error
        
        appointment = Appointment.query.get(appointment_id)
        
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
        
        appointment.status = 'completed'
        appointment.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Appointment marked as completed',
            'appointment': appointment.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
