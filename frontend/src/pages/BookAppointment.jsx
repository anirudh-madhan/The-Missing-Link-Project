import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { hospitalAPI, appointmentAPI } from '../services/api';
import './BookAppointment.css';

function BookAppointment({ language }) {
  const { hospitalId, doctorId } = useParams();
  const navigate = useNavigate();
  const [hospital, setHospital] = useState(null);
  const [doctor, setDoctor] = useState(null);
  const [formData, setFormData] = useState({
    appointment_date: '',
    appointment_time: '',
    reason: '',
    notes: ''
  });
  const [availableSlots, setAvailableSlots] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    if (formData.appointment_date && doctorId) {
      fetchAvailableSlots();
    }
  }, [formData.appointment_date]);

  const fetchData = async () => {
    try {
      const response = await hospitalAPI.getById(hospitalId);
      const hospitalData = response.data.hospital;
      setHospital(hospitalData);
      
      const foundDoctor = hospitalData.doctors.find(d => d.id === parseInt(doctorId));
      setDoctor(foundDoctor);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchAvailableSlots = async () => {
    try {
      const response = await appointmentAPI.getAvailableSlots(doctorId, formData.appointment_date);
      setAvailableSlots(response.data.available_slots);
    } catch (error) {
      console.error('Error fetching slots:', error);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSubmitting(true);

    try {
      await appointmentAPI.book({
        hospital_id: parseInt(hospitalId),
        doctor_id: parseInt(doctorId),
        ...formData
      });
      
      alert('Appointment booked successfully!');
      navigate('/appointments');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to book appointment');
    } finally {
      setSubmitting(false);
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

  if (!hospital || !doctor) {
    return (
      <div className="container">
        <div className="alert alert-error">Hospital or Doctor not found</div>
      </div>
    );
  }

  const minDate = new Date().toISOString().split('T')[0];

  return (
    <div className="container">
      <div className="book-appointment">
        <button 
          onClick={() => navigate(`/hospitals/${hospitalId}`)} 
          className="btn btn-outline" 
          style={{ marginBottom: '1rem' }}
        >
          ← Back to Hospital Details
        </button>
        
        <h1>Book Appointment</h1>

        <div className="booking-info card">
          <h2>{hospital.name}</h2>
          <h3>{doctor.name} - {doctor.specialty}</h3>
          <p>Consultation Fee: ₹{doctor.consultation_fee}</p>
        </div>

        {error && <div className="alert alert-error">{error}</div>}

        <form onSubmit={handleSubmit} className="card booking-form">
          <div className="form-group">
            <label className="form-label">Appointment Date *</label>
            <input
              type="date"
              name="appointment_date"
              className="form-input"
              value={formData.appointment_date}
              onChange={handleChange}
              min={minDate}
              required
            />
          </div>

          {availableSlots.length > 0 && (
            <div className="form-group">
              <label className="form-label">Available Time Slots *</label>
              <select
                name="appointment_time"
                className="form-select"
                value={formData.appointment_time}
                onChange={handleChange}
                required
              >
                <option value="">Select a time slot</option>
                {availableSlots.map((slot) => (
                  <option key={slot} value={slot}>{slot}</option>
                ))}
              </select>
            </div>
          )}

          {formData.appointment_date && availableSlots.length === 0 && (
            <div className="alert alert-warning">No available slots for this date</div>
          )}

          <div className="form-group">
            <label className="form-label">Reason for Visit *</label>
            <textarea
              name="reason"
              className="form-textarea"
              value={formData.reason}
              onChange={handleChange}
              required
              placeholder="Brief description of your health concern"
            />
          </div>

          <div className="form-group">
            <label className="form-label">Additional Notes</label>
            <textarea
              name="notes"
              className="form-textarea"
              value={formData.notes}
              onChange={handleChange}
              placeholder="Any additional information for the doctor"
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            disabled={submitting || availableSlots.length === 0}
          >
            {submitting ? 'Booking...' : 'Book Appointment'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default BookAppointment;
