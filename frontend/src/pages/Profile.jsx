import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI } from '../services/api';
import './Profile.css';

function Profile({ user, onUpdate, language }) {
  const navigate = useNavigate();
  
  // Calculate age from date_of_birth
  const calculateAge = (dob) => {
    if (!dob) return null;
    const today = new Date();
    const birthDate = new Date(dob);
    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
      age--;
    }
    return age;
  };
  
  const userAge = calculateAge(user?.date_of_birth);
  
  const [formData, setFormData] = useState({
    full_name: user?.full_name || '',
    phone: user?.phone || '',
    date_of_birth: user?.date_of_birth || '',
    language_preference: user?.language_preference || 'en',
    accessibility_needs: user?.accessibility_needs || ''
  });
  const [editing, setEditing] = useState(false);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage('');

    try {
      const response = await authAPI.updateProfile(formData);
      onUpdate(response.data.user);
      setMessage('Profile updated successfully');
      setEditing(false);
    } catch (error) {
      setMessage(error.response?.data?.error || 'Failed to update profile');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="container">
      <div className="profile-page">
        <button 
          onClick={() => navigate('/dashboard')} 
          className="btn btn-outline" 
          style={{ marginBottom: '1rem' }}
        >
          ← Back to Dashboard
        </button>
        
        <h1>My Profile</h1>

        {message && (
          <div className={`alert ${message.includes('success') ? 'alert-success' : 'alert-error'}`}>
            {message}
          </div>
        )}

        <div className="card">
          {!editing ? (
            <div className="profile-view">
              <div className="profile-avatar">
                {(user?.full_name || user?.email || 'U').charAt(0).toUpperCase()}
              </div>
              <div className="profile-info">
                <div className="info-row">
                  <strong>Name:</strong>
                  <span>{user?.full_name || 'Not provided'}</span>
                </div>
                <div className="info-row">
                  <strong>Email:</strong>
                  <span>{user?.email || 'Not provided'}</span>
                </div>
                <div className="info-row">
                  <strong>Phone:</strong>
                  <span>{user?.phone || 'Not provided'}</span>
                </div>
                <div className="info-row">
                  <strong>Age:</strong>
                  <span>{userAge ? `${userAge} years` : 'Not provided'}</span>
                </div>
                <div className="info-row">
                  <strong>Language:</strong>
                  <span>{user?.language_preference === 'ta' ? 'Tamil' : 'English'}</span>
                </div>
                <div className="info-row">
                  <strong>Accessibility Needs:</strong>
                  <span>{user?.accessibility_needs || 'None specified'}</span>
                </div>
                <div className="info-row">
                  <strong>Account Type:</strong>
                  <span className={`badge ${user?.is_admin ? 'badge-error' : 'badge-info'}`}>
                    {user?.is_admin ? 'Administrator' : 'Patient'}
                  </span>
                </div>
              </div>
              <button onClick={() => setEditing(true)} className="btn btn-primary">
                Edit Profile
              </button>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="profile-form">
              <div className="form-group">
                <label className="form-label">Full Name</label>
                <input
                  type="text"
                  name="full_name"
                  className="form-input"
                  value={formData.full_name}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Phone</label>
                <input
                  type="tel"
                  name="phone"
                  className="form-input"
                  value={formData.phone}
                  onChange={handleChange}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Date of Birth</label>
                <input
                  type="date"
                  name="date_of_birth"
                  className="form-input"
                  value={formData.date_of_birth}
                  onChange={handleChange}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Language Preference</label>
                <select
                  name="language_preference"
                  className="form-select"
                  value={formData.language_preference}
                  onChange={handleChange}
                >
                  <option value="en">English</option>
                  <option value="ta">Tamil</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Accessibility Needs</label>
                <textarea
                  name="accessibility_needs"
                  className="form-textarea"
                  value={formData.accessibility_needs}
                  onChange={handleChange}
                />
              </div>

              <div className="profile-actions">
                <button type="submit" className="btn btn-primary" disabled={saving}>
                  {saving ? 'Saving...' : 'Save Changes'}
                </button>
                <button
                  type="button"
                  onClick={() => setEditing(false)}
                  className="btn btn-outline"
                  disabled={saving}
                >
                  Cancel
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}

export default Profile;
