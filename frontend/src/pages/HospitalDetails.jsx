import { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { hospitalAPI } from '../services/api';
import './HospitalDetails.css';

function HospitalDetails({ language }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [hospital, setHospital] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHospital();
  }, [id]);

  const fetchHospital = async () => {
    try {
      const response = await hospitalAPI.getById(id);
      setHospital(response.data.hospital);
    } catch (error) {
      console.error('Error fetching hospital:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading-container">
          <div className="spinner"></div>
        </div>
      </div>
    );
  }

  if (!hospital) {
    return (
      <div className="container">
        <div className="alert alert-error">Hospital not found</div>
        <button onClick={() => navigate('/hospitals')} className="btn btn-primary">
          ← Back to Hospitals
        </button>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="hospital-details">
        <button onClick={() => navigate('/hospitals')} className="btn btn-outline" style={{ marginBottom: '1rem' }}>
          ← Back to Hospitals
        </button>
        
        <div className="card">
          <div className="hospital-details-header">
            <div>
              <h1>{language === 'ta' && hospital.name_tamil ? hospital.name_tamil : hospital.name}</h1>
              <p>{hospital.address}, {hospital.city}, {hospital.state} - {hospital.pincode}</p>
            </div>
            <div className="hospital-rating-large">⭐ {hospital.rating}</div>
          </div>

          <div className="hospital-details-grid">
            <div className="detail-section">
              <h3>Contact Information</h3>
              <p>📞 {hospital.phone}</p>
              <p>📧 {hospital.email}</p>
            </div>

            <div className="detail-section">
              <h3>Availability</h3>
              <p>🛏️ {hospital.available_beds} of {hospital.total_beds} beds available</p>
              <p>{hospital.emergency_available ? '🚨 Emergency Services Available' : '⚠️ No Emergency Services'}</p>
            </div>
          </div>

          <div className="detail-section">
            <h3>Specialties</h3>
            <div className="specialties-list">
              {hospital.specialties.map((spec) => (
                <span key={spec} className="badge badge-info">{spec}</span>
              ))}
            </div>
          </div>

          <div className="detail-section">
            <h3>Languages Supported</h3>
            <div className="specialties-list">
              {hospital.languages_supported.map((lang) => (
                <span key={lang} className="badge badge-success">{lang}</span>
              ))}
            </div>
          </div>

          {hospital.accessibility_features.length > 0 && (
            <div className="detail-section">
              <h3>Accessibility Features</h3>
              <div className="specialties-list">
                {hospital.accessibility_features.map((feature) => (
                  <span key={feature} className="badge">{feature}</span>
                ))}
              </div>
            </div>
          )}
        </div>

        {hospital.doctors && hospital.doctors.length > 0 && (
          <div className="card">
            <h2>Available Doctors</h2>
            <div className="doctors-grid">
              {hospital.doctors.map((doctor) => (
                <div key={doctor.id} className="doctor-card">
                  <h3>{language === 'ta' && doctor.name_tamil ? doctor.name_tamil : doctor.name}</h3>
                  <p className="doctor-specialty">{doctor.specialty}</p>
                  <p className="doctor-qualification">{doctor.qualification}</p>
                  <p className="doctor-fee">₹{doctor.consultation_fee}</p>
                  <Link 
                    to={`/book-appointment/${hospital.id}/${doctor.id}`}
                    className="btn btn-primary btn-small"
                  >
                    Book Appointment
                  </Link>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default HospitalDetails;
