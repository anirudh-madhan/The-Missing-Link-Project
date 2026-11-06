import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authAPI } from '../services/api';
import { TRANSLATIONS } from '../config';
import './Auth.css';

function Login({ onLogin, language }) {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
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
      const response = await authAPI.login(formData);
      localStorage.setItem('token', response.data.access_token);
      onLogin(response.data.user);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.error || 'Login failed. Please try again.');
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

        <h2 className="auth-title">{t.login}</h2>

        {error && <div className="alert alert-error">{error}</div>}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label className="form-label">{t.email}</label>
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
            <label className="form-label">{t.password}</label>
            <input
              type="password"
              name="password"
              className="form-input"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="••••••••"
            />
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? t.loading : t.login}
          </button>
        </form>

        <div className="auth-footer">
          <p>
            Don't have an account? <Link to="/register">{t.register}</Link>
          </p>
        </div>

        <div className="auth-demo">
          <h3>Demo Credentials:</h3>
          <div className="demo-credentials">
            <div>
              <strong>Patient:</strong>
              <p>Email: john.doe@email.com</p>
              <p>Password: patient123</p>
            </div>
            <div>
              <strong>Admin:</strong>
              <p>Email: admin@hospital.com</p>
              <p>Password: admin123</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
