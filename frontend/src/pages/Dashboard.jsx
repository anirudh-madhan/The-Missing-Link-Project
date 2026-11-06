import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { appointmentAPI, hospitalAPI } from '../services/api';
import { TRANSLATIONS } from '../config';
import './Dashboard.css';

function Dashboard({ user, language }) {
  const [appointments, setAppointments] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const t = TRANSLATIONS[language];

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Check if token exists
      const token = localStorage.getItem('token');
      if (!token) {
        console.warn('No authentication token found');
        setLoading(false);
        return;
      }

      const [appointmentsRes] = await Promise.all([
        appointmentAPI.getAll()
      ]);
      
      const allAppointments = appointmentsRes.data.appointments || [];
      setAppointments(allAppointments.slice(0, 5)); // Latest 5
      
      // Calculate stats
      const upcoming = allAppointments.filter(apt => 
        apt.status === 'scheduled' && new Date(apt.appointment_date) >= new Date()
      ).length;
      
      const completed = allAppointments.filter(apt => apt.status === 'completed').length;
      
      setStats({
        totalAppointments: allAppointments.length,
        upcoming,
        completed
      });
      
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      // Handle empty appointments gracefully
      setAppointments([]);
      setStats({
        totalAppointments: 0,
        upcoming: 0,
        completed: 0
      });
    } finally {
      setLoading(false);
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
          <p>{t.loading}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="dashboard">
        <div className="dashboard-header">
          <h1>{t.welcome}, {user?.full_name || user?.email || 'User'}!</h1>
          <p>Manage your healthcare journey efficiently</p>
        </div>

        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon">📅</div>
            <div className="stat-content">
              <h3>{stats?.totalAppointments || 0}</h3>
              <p>Total Appointments</p>
            </div>
          </div>
          
          <div className="stat-card">
            <div className="stat-icon">🕐</div>
            <div className="stat-content">
              <h3>{stats?.upcoming || 0}</h3>
              <p>Upcoming</p>
            </div>
          </div>
          
          <div className="stat-card">
            <div className="stat-icon">✓</div>
            <div className="stat-content">
              <h3>{stats?.completed || 0}</h3>
              <p>Completed</p>
            </div>
          </div>
        </div>

        <div className="quick-actions">
          <h2>Quick Actions</h2>
          <div className="action-grid">
            <Link to="/hospitals" className="action-card">
              <div className="action-icon">🏥</div>
              <h3>{t.hospitals}</h3>
              <p>Search for hospitals and services</p>
            </Link>

            <Link to="/recommendations" className="action-card">
              <div className="action-icon">⭐</div>
              <h3>{t.recommendations}</h3>
              <p>Get personalized hospital suggestions</p>
            </Link>

            <Link to="/appointments" className="action-card">
              <div className="action-icon">📋</div>
              <h3>{t.appointments}</h3>
              <p>View and manage your appointments</p>
            </Link>

            <Link to="/past-records" className="action-card">
              <div className="action-icon">🗂️</div>
              <h3>Past Records</h3>
              <p>Review completed and cancelled visits</p>
            </Link>

            <Link to="/constraint-lab" className="action-card">
              <div className="action-icon">🔬</div>
              <h3>{t.constraintLab}</h3>
              <p>Test system resilience scenarios</p>
            </Link>
          </div>
        </div>

        {appointments.length > 0 && (
          <div className="recent-appointments">
            <div className="flex-between mb-3">
              <h2>Recent Appointments</h2>
              <Link to="/appointments" className="btn btn-outline btn-small">View All</Link>
            </div>

            <div className="card">
              <table className="table">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Time</th>
                    <th>Hospital</th>
                    <th>Doctor</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {appointments.map((apt) => (
                    <tr key={apt.id}>
                      <td>{new Date(apt.appointment_date).toLocaleDateString()}</td>
                      <td>{apt.appointment_time}</td>
                      <td>{apt.hospital_name}</td>
                      <td>{apt.doctor_name}</td>
                      <td>
                        <span className={`badge ${getStatusBadge(apt.status)}`}>
                          {apt.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
