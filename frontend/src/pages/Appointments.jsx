import { useState, useEffect } from 'react';
import { appointmentAPI } from '../services/api';
import './Appointments.css';

function Appointments({ language }) {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedApt, setSelectedApt] = useState(null);

  useEffect(() => {
    fetchAppointments();
  }, []);

  const fetchAppointments = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        console.warn('No authentication token found');
        setLoading(false);
        return;
      }

      const response = await appointmentAPI.getAll();
      setAppointments(response.data.appointments || []);
    } catch (error) {
      console.error('Error fetching appointments:', error);
      // Handle gracefully - show empty state
      setAppointments([]);
    } finally {
      setLoading(false);
    }
  };

  const cancelAppointment = async (id) => {
    if (!window.confirm('Are you sure you want to cancel this appointment?')) return;
    
    try {
      await appointmentAPI.cancel(id);
      fetchAppointments();
      alert('Appointment cancelled successfully');
    } catch (error) {
      alert(error.response?.data?.error || 'Failed to cancel appointment');
    }
  };

  const getStatusBadge = (status) => {
    const statusMap = {
      scheduled: 'badge-info',
      completed: 'badge-success',
      cancelled: 'badge-error',
      rescheduled: 'badge-warning'
    };
    return statusMap[status] || 'badge-info';
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

  return (
    <div className="container">
      <div className="appointments-page">
        <h1>My Appointments</h1>

        {appointments.length === 0 ? (
          <div className="card">
            <p className="text-center">No appointments found</p>
          </div>
        ) : (
          <div className="card">
            <table className="table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Time</th>
                  <th>Hospital</th>
                  <th>Doctor</th>
                  <th>Specialty</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {appointments.map((apt) => (
                  <tr key={apt.id}>
                    <td>{new Date(apt.appointment_date).toLocaleDateString()}</td>
                    <td>{apt.appointment_time}</td>
                    <td>{apt.hospital_name}</td>
                    <td>{apt.doctor_name}</td>
                    <td>{apt.doctor_specialty}</td>
                    <td>
                      <span className={`badge ${getStatusBadge(apt.status)}`}>
                        {apt.status}
                      </span>
                    </td>
                    <td>
                      {apt.status === 'scheduled' && (
                        <button
                          onClick={() => cancelAppointment(apt.id)}
                          className="btn btn-error btn-small"
                        >
                          Cancel
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default Appointments;
