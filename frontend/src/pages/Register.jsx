import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authAPI } from '../services/api';
import { TRANSLATIONS, LANGUAGES } from '../config';
import './Auth.css';

function Register({ onLogin, language }) {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    full_name: '',
    phone: '',
    age: '',
    language_preference: 'en',
    accessibility_needs: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const t = TRANSLATIONS[language];

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await authAPI.register(formData);
      localStorage.setItem('token', response.data.access_token);
      onLogin(response.data.user);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.error || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <button 
          onClick={() => navigate('/')} 
          className="btn btn-outline btn-small" 
          style={{ marginBottom: '1rem', width: 'auto' }}
        >
          ← Back to Home
        </button>
        
        <div className="auth-header">
          <h1>{t.appName}</h1>
          <p className="auth-tagline">{t.tagline}</p>
        </div>

        <h2 className="auth-title">{t.register}</h2>

        {error && <div className="alert alert-error">{error}</div>}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label className="form-label">{t.fullName} *</label>
            <input
              type="text"
              name="full_name"
              className="form-input"
              value={formData.full_name}
              onChange={handleChange}
              required
              placeholder="John Doe"
            />
          </div>

          <div className="form-group">
            <label className="form-label">{t.email} *</label>
            <input
              type="email"
              name="email"
              className="form-input"
              value={formData.email}
              onChange={handleChange}
              required
              placeholder="john.doe@email.com"
            />
          </div>

          <div className="form-group">
            <label className="form-label">{t.password} *</label>
            <input
              type="password"
              name="password"
              className="form-input"
              value={formData.password}
              onChange={handleChange}
              required
              minLength="6"
              placeholder="••••••••"
            />
          </div>

          <div className="form-group">
            <label className="form-label">{t.phone}</label>
            <input
              type="tel"
              name="phone"
              className="form-input"
              value={formData.phone}
              onChange={handleChange}
              placeholder="+91-9876543210"
            />
          </div>

          <div className="form-group">
            <label className="form-label">Age</label>
            <input
              type="number"
              name="age"
              className="form-input"
              value={formData.age}
              onChange={handleChange}
              min="1"
              max="120"
              placeholder="Enter your age"
            />
          </div>

          <div className="form-group">
            <label className="form-label">{t.languagePreference}</label>
            <select
              name="language_preference"
              className="form-select"
              value={formData.language_preference}
              onChange={handleChange}
            >
              {Object.entries(LANGUAGES).map(([code, name]) => (
                <option key={code} value={code}>
                  {name}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Accessibility Needs</label>
            <textarea
              name="accessibility_needs"
              className="form-textarea"
              value={formData.accessibility_needs}
              onChange={handleChange}
              placeholder="Please describe any accessibility requirements (wheelchair access, hearing assistance, etc.)"
            />
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? t.loading : t.register}
          </button>
        </form>

        <div className="auth-footer">
          <p>
            Already have an account? <Link to="/login">{t.login}</Link>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Register;
