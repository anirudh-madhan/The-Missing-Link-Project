from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Appointment, Hospital, Doctor, User
from datetime import datetime, timedelta
import json

appointments_bp = Blueprint('appointments', __name__)

@appointments_bp.route('', methods=['GET'])
@jwt_required()
def get_appointments():
    try:
        user_id = int(get_jwt_identity())  # Convert string to int
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Admin can see all appointments
        if user.is_admin:
            appointments = Appointment.query.order_by(Appointment.appointment_date.desc()).all()
        else:
            appointments = Appointment.query.filter_by(patient_id=user_id).order_by(Appointment.appointment_date.desc()).all()
        
        return jsonify({
            'appointments': [apt.to_dict() for apt in appointments],
            'count': len(appointments)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@appointments_bp.route('/<int:appointment_id>', methods=['GET'])
@jwt_required()
def get_appointment(appointment_id):
    try:
        user_id = int(get_jwt_identity())  # Convert string to int
        user = User.query.get(user_id)
        
        appointment = Appointment.query.get(appointment_id)
        
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
        
        # Check permission
        if not user.is_admin and appointment.patient_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        return jsonify({'appointment': appointment.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@appointments_bp.route('', methods=['POST'])
@jwt_required()
def book_appointment():
    try:
        user_id = int(get_jwt_identity())  # Convert string to int
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['hospital_id', 'doctor_id', 'appointment_date', 'appointment_time']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate hospital and doctor
        hospital = Hospital.query.get(data['hospital_id'])
        if not hospital:
            return jsonify({'error': 'Hospital not found'}), 404
        
        doctor = Doctor.query.get(data['doctor_id'])
        if not doctor or doctor.hospital_id != hospital.id:
            return jsonify({'error': 'Doctor not found or not associated with this hospital'}), 404
        
        if not doctor.is_available:
            return jsonify({'error': 'Doctor is not available'}), 400
        
        # Parse and validate date
        try:
            appointment_date = datetime.strptime(data['appointment_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        # Check if date is in the future
        if appointment_date < datetime.now().date():
            return jsonify({'error': 'Cannot book appointments in the past'}), 400
        
        # Check for conflicting appointments (prevent overbooking)
        existing = Appointment.query.filter_by(
            doctor_id=data['doctor_id'],
            appointment_date=appointment_date,
            appointment_time=data['appointment_time']
        ).filter(Appointment.status.in_(['scheduled', 'rescheduled'])).first()
        
        if existing:
            return jsonify({'error': 'This time slot is already booked. Please choose another time.'}), 409
        
        # Check for duplicate booking by same patient
        duplicate = Appointment.query.filter_by(
            patient_id=user_id,
            hospital_id=data['hospital_id'],
            doctor_id=data['doctor_id'],
            appointment_date=appointment_date,
            appointment_time=data['appointment_time']
        ).filter(Appointment.status.in_(['scheduled', 'rescheduled'])).first()
        
        if duplicate:
            return jsonify({'error': 'You already have an appointment at this time'}), 409
        
        # Create appointment
        appointment = Appointment(
            patient_id=user_id,
            hospital_id=data['hospital_id'],
            doctor_id=data['doctor_id'],
            appointment_date=appointment_date,
            appointment_time=data['appointment_time'],
            reason=data.get('reason'),
            notes=data.get('notes'),
            documents_required=json.dumps(data.get('documents_required', [])),
            documents_submitted=json.dumps([]),
            status='scheduled'
        )
        
        db.session.add(appointment)
        
        # Update hospital bed availability (simulate)
        if hospital.available_beds > 0:
            hospital.available_beds -= 1
        
        db.session.commit()
        
        return jsonify({
            'message': 'Appointment booked successfully',
            'appointment': appointment.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@appointments_bp.route('/<int:appointment_id>', methods=['PUT'])
@jwt_required()
def update_appointment(appointment_id):
    try:
        user_id = int(get_jwt_identity())  # Convert string to int
        user = User.query.get(user_id)
        
        appointment = Appointment.query.get(appointment_id)
        
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
        
        # Check permission
        if not user.is_admin and appointment.patient_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        # Reschedule appointment
        if 'appointment_date' in data or 'appointment_time' in data:
            new_date = data.get('appointment_date', appointment.appointment_date.isoformat())
            new_time = data.get('appointment_time', appointment.appointment_time)
            
            try:
                new_date_obj = datetime.strptime(new_date if isinstance(new_date, str) else new_date.isoformat(), '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
            
            # Check if new date is in the future
            if new_date_obj < datetime.now().date():
                return jsonify({'error': 'Cannot reschedule to past dates'}), 400
            
            # Check for conflicts
            existing = Appointment.query.filter(
                Appointment.id != appointment_id,
                Appointment.doctor_id == appointment.doctor_id,
                Appointment.appointment_date == new_date_obj,
                Appointment.appointment_time == new_time
            ).filter(Appointment.status.in_(['scheduled', 'rescheduled'])).first()
            
            if existing:
                return jsonify({'error': 'This time slot is already booked. Please choose another time.'}), 409
            
            appointment.appointment_date = new_date_obj
            appointment.appointment_time = new_time
            appointment.status = 'rescheduled'
        
        # Update other fields
        if 'reason' in data:
            appointment.reason = data['reason']
        if 'notes' in data:
            appointment.notes = data['notes']
        if 'documents_submitted' in data:
            appointment.documents_submitted = json.dumps(data['documents_submitted'])
        
        appointment.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Appointment updated successfully',
            'appointment': appointment.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@appointments_bp.route('/<int:appointment_id>', methods=['DELETE'])
@jwt_required()
def cancel_appointment(appointment_id):
    try:
        user_id = int(get_jwt_identity())  # Convert string to int
        user = User.query.get(user_id)
        
        appointment = Appointment.query.get(appointment_id)
        
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
        
        # Check permission
        if not user.is_admin and appointment.patient_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Update status instead of deleting
        appointment.status = 'cancelled'
        appointment.updated_at = datetime.utcnow()
        
        # Restore hospital bed availability
        hospital = Hospital.query.get(appointment.hospital_id)
        if hospital and hospital.available_beds < hospital.total_beds:
            hospital.available_beds += 1
        
        db.session.commit()
        
        return jsonify({'message': 'Appointment cancelled successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@appointments_bp.route('/available-slots', methods=['GET'])
def get_available_slots():
    try:
        doctor_id = request.args.get('doctor_id', type=int)
        date_str = request.args.get('date')
        
        if not doctor_id or not date_str:
            return jsonify({'error': 'doctor_id and date are required'}), 400
        
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return jsonify({'error': 'Doctor not found'}), 404
        
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        # Get all available time slots for the doctor
        available_times = json.loads(doctor.available_times) if doctor.available_times else []
        
        # Get booked slots for this date
        booked = Appointment.query.filter_by(
            doctor_id=doctor_id,
            appointment_date=date_obj
        ).filter(Appointment.status.in_(['scheduled', 'rescheduled'])).all()
        
        booked_times = {apt.appointment_time for apt in booked}
        
        # Filter out booked slots
        free_slots = [time for time in available_times if time not in booked_times]
        
        return jsonify({
            'date': date_str,
            'doctor_id': doctor_id,
            'available_slots': free_slots,
            'booked_slots': list(booked_times)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@appointments_bp.route('/documents/checklist', methods=['GET'])
@jwt_required()
def get_document_checklist():
    try:
        # Return standard document checklist for healthcare appointments
        checklist = [
            {
                'id': 'govt_id',
                'name': 'Government ID',
                'name_tamil': 'அரசு அடையாள அட்டை',
                'required': True,
                'description': 'Aadhaar Card, Driving License, or Passport'
            },
            {
                'id': 'insurance',
                'name': 'Insurance Card',
                'name_tamil': 'காப்பீட்டு அட்டை',
                'required': False,
                'description': 'Health insurance card if applicable'
            },
            {
                'id': 'medical_records',
                'name': 'Previous Medical Records',
                'name_tamil': 'முந்தைய மருத்துவ பதிவுகள்',
                'required': False,
                'description': 'Past medical history, test reports'
            },
            {
                'id': 'prescription',
                'name': 'Current Prescriptions',
                'name_tamil': 'தற்போதைய மருந்து பரிந்துரைகள்',
                'required': False,
                'description': 'List of current medications'
            },
            {
                'id': 'referral',
                'name': 'Referral Letter',
                'name_tamil': 'பரிந்துரை கடிதம்',
                'required': False,
                'description': 'Referral from primary care physician if applicable'
            }
        ]
        
        return jsonify({'checklist': checklist}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
