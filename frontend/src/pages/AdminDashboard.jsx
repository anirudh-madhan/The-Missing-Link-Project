import { useState, useEffect } from 'react';
import { adminAPI, appointmentAPI } from '../services/api';
import './AdminDashboard.css';

function AdminDashboard({ language }) {
  const [stats, setStats] = useState(null);
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [statsRes, appointmentsRes] = await Promise.all([
        adminAPI.getStats(),
        appointmentAPI.getAll()
      ]);
      
      setStats(statsRes.data);
      setAppointments(appointmentsRes.data.appointments);
    } catch (error) {
      console.error('Error fetching admin data:', error);
    } finally {
      setLoading(false);
    }
  };

  const completeAppointment = async (id) => {
    if (!window.confirm('Mark this appointment as completed?')) return;

    try {
      await adminAPI.completeAppointment(id);
      fetchData();
      alert('Appointment marked as completed');
    } catch (error) {
      alert('Failed to update appointment');
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
      <div className="admin-dashboard">
        <h1>Admin Dashboard</h1>

        <div className="admin-stats-grid">
          <div className="stat-card">
            <div className="stat-icon">🏥</div>
            <div className="stat-content">
              <h3>{stats.hospitals}</h3>
              <p>Hospitals</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">👨‍⚕️</div>
            <div className="stat-content">
              <h3>{stats.doctors}</h3>
              <p>Doctors</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">👥</div>
            <div className="stat-content">
              <h3>{stats.patients}</h3>
              <p>Patients</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">📅</div>
            <div className="stat-content">
              <h3>{stats.appointments?.total || 0}</h3>
              <p>Total Appointments</p>
            </div>
          </div>
        </div>

        <div className="card mt-4">
          <h2>Bed Availability</h2>
          <div className="bed-stats">
            <div className="bed-stat">
              <strong>Total Beds:</strong>
              <span>{stats.beds?.total || 0}</span>
            </div>
            <div className="bed-stat">
              <strong>Available:</strong>
              <span className="text-success">{stats.beds?.available || 0}</span>
            </div>
            <div className="bed-stat">
              <strong>Occupancy:</strong>
              <span className="text-warning">{stats.beds?.occupancy_rate || 0}%</span>
            </div>
          </div>
        </div>

        <div className="card mt-4">
          <h2>All Appointments</h2>
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Time</th>
                  <th>Patient</th>
                  <th>Hospital</th>
                  <th>Doctor</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {appointments.map((apt) => (
                  <tr key={apt.id}>
                    <td>{new Date(apt.appointment_date).toLocaleDateString()}</td>
                    <td>{apt.appointment_time}</td>
                    <td>{apt.patient_name}</td>
                    <td>{apt.hospital_name}</td>
                    <td>{apt.doctor_name}</td>
                    <td>
                      <span className={`badge ${getStatusBadge(apt.status)}`}>
                        {apt.status}
                      </span>
                    </td>
                    <td>
                      {apt.status === 'scheduled' && (
                        <button
                          onClick={() => completeAppointment(apt.id)}
                          className="btn btn-success btn-small"
                        >
                          Complete
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AdminDashboard;
