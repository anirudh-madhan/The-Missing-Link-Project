from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Hospital, Doctor
import json
import math

hospitals_bp = Blueprint('hospitals', __name__)

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points using Haversine formula"""
    if not all([lat1, lon1, lat2, lon2]):
        return None
    
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

@hospitals_bp.route('', methods=['GET'])
def get_hospitals():
    try:
        # Get query parameters
        specialty = request.args.get('specialty')
        city = request.args.get('city')
        language = request.args.get('language')
        emergency = request.args.get('emergency', '').lower() == 'true'
        accessibility = request.args.get('accessibility')
        
        # Build query
        query = Hospital.query.filter_by(is_active=True)
        
        if city:
            query = query.filter(Hospital.city.ilike(f'%{city}%'))
        
        if emergency:
            query = query.filter_by(emergency_available=True)
        
        hospitals = query.all()
        
        # Filter by specialty (JSON field)
        if specialty:
            hospitals = [h for h in hospitals if specialty.lower() in [s.lower() for s in json.loads(h.specialties or '[]')]]
        
        # Filter by language (JSON field)
        if language:
            hospitals = [h for h in hospitals if language.lower() in [l.lower() for l in json.loads(h.languages_supported or '[]')]]
        
        # Filter by accessibility (JSON field)
        if accessibility:
            hospitals = [h for h in hospitals if accessibility.lower() in [a.lower() for a in json.loads(h.accessibility_features or '[]')]]
        
        return jsonify({
            'hospitals': [h.to_dict() for h in hospitals],
            'count': len(hospitals)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@hospitals_bp.route('/<int:hospital_id>', methods=['GET'])
def get_hospital(hospital_id):
    try:
        hospital = Hospital.query.get(hospital_id)
        
        if not hospital:
            return jsonify({'error': 'Hospital not found'}), 404
        
        # Get doctors for this hospital
        doctors = Doctor.query.filter_by(hospital_id=hospital_id, is_available=True).all()
        
        hospital_data = hospital.to_dict()
        hospital_data['doctors'] = [d.to_dict() for d in doctors]
        
        return jsonify({'hospital': hospital_data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@hospitals_bp.route('/recommendations', methods=['POST'])
@jwt_required()
def get_recommendations():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        # Get user preferences
        user_lat = data.get('latitude')
        user_lon = data.get('longitude')
        preferred_specialty = data.get('specialty')
        preferred_language = data.get('language')
        accessibility_need = data.get('accessibility')
        
        # Get all active hospitals
        hospitals = Hospital.query.filter_by(is_active=True).all()
        
        recommendations = []
        
        for hospital in hospitals:
            score = 0
            reasons = []
            
            # Availability score (30 points)
            if hospital.available_beds > 0:
                availability_ratio = hospital.available_beds / hospital.total_beds
                score += availability_ratio * 30
                if availability_ratio > 0.3:
                    reasons.append('Good bed availability')
            
            # Distance score (25 points)
            if user_lat and user_lon and hospital.latitude and hospital.longitude:
                distance = calculate_distance(user_lat, user_lon, hospital.latitude, hospital.longitude)
                if distance is not None:
                    if distance < 5:
                        score += 25
                        reasons.append('Very close to your location')
                    elif distance < 10:
                        score += 20
                        reasons.append('Near your location')
                    elif distance < 20:
                        score += 15
                    else:
                        score += 5
            else:
                score += 10  # Default if no location data
            
            # Specialty match (20 points)
            if preferred_specialty:
                specialties = json.loads(hospital.specialties or '[]')
                if preferred_specialty.lower() in [s.lower() for s in specialties]:
                    score += 20
                    reasons.append(f'Specializes in {preferred_specialty}')
            else:
                score += 10  # Default if no preference
            
            # Language support (15 points)
            if preferred_language:
                languages = json.loads(hospital.languages_supported or '[]')
                if preferred_language.lower() in [l.lower() for l in languages]:
                    score += 15
                    reasons.append(f'Staff speaks {preferred_language}')
            else:
                score += 7  # Default if no preference
            
            # Accessibility (10 points)
            if accessibility_need:
                features = json.loads(hospital.accessibility_features or '[]')
                if accessibility_need.lower() in [f.lower() for f in features]:
                    score += 10
                    reasons.append(f'Has {accessibility_need} accessibility')
            else:
                score += 5  # Default if no special need
            
            # Rating bonus (max 10 points)
            score += (hospital.rating / 5.0) * 10
            
            hospital_dict = hospital.to_dict()
            hospital_dict['recommendation_score'] = round(score, 2)
            hospital_dict['recommendation_reasons'] = reasons
            
            if user_lat and user_lon and hospital.latitude and hospital.longitude:
                distance = calculate_distance(user_lat, user_lon, hospital.latitude, hospital.longitude)
                hospital_dict['distance_km'] = round(distance, 2) if distance else None
            
            recommendations.append(hospital_dict)
        
        # Sort by score
        recommendations.sort(key=lambda x: x['recommendation_score'], reverse=True)
        
        return jsonify({
            'recommendations': recommendations[:10],  # Top 10
            'count': len(recommendations)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@hospitals_bp.route('/<int:hospital_id>/doctors', methods=['GET'])
def get_hospital_doctors(hospital_id):
    try:
        hospital = Hospital.query.get(hospital_id)
        
        if not hospital:
            return jsonify({'error': 'Hospital not found'}), 404
        
        specialty = request.args.get('specialty')
        
        query = Doctor.query.filter_by(hospital_id=hospital_id, is_available=True)
        
        if specialty:
            query = query.filter(Doctor.specialty.ilike(f'%{specialty}%'))
        
        doctors = query.all()
        
        return jsonify({
            'doctors': [d.to_dict() for d in doctors],
            'count': len(doctors)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@hospitals_bp.route('/specialties', methods=['GET'])
def get_specialties():
    try:
        # Get all unique specialties from hospitals and doctors
        hospitals = Hospital.query.filter_by(is_active=True).all()
        specialties_set = set()
        
        for hospital in hospitals:
            if hospital.specialties:
                specialties_set.update(json.loads(hospital.specialties))
        
        return jsonify({
            'specialties': sorted(list(specialties_set))
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@hospitals_bp.route('/cities', methods=['GET'])
def get_cities():
    try:
        cities = db.session.query(Hospital.city).filter_by(is_active=True).distinct().all()
        return jsonify({
            'cities': sorted([c[0] for c in cities])
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
