import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { hospitalAPI } from '../services/api';
import './Recommendations.css';

function Recommendations({ language }) {
  const navigate = useNavigate();
  const [preferences, setPreferences] = useState({
    latitude: '',
    longitude: '',
    specialty: '',
    language: '',
    accessibility: ''
  });
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const handleChange = (e) => {
    setPreferences({
      ...preferences,
      [e.target.name]: e.target.value
    });
  };

  const getLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setPreferences({
            ...preferences,
            latitude: position.coords.latitude.toString(),
            longitude: position.coords.longitude.toString()
          });
        },
        (error) => {
          alert('Unable to get your location. Please enter manually.');
        }
      );
    } else {
      alert('Geolocation is not supported by your browser');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSearched(true);

    try {
      const response = await hospitalAPI.getRecommendations(preferences);
      setRecommendations(response.data.recommendations);
    } catch (error) {
      console.error('Error getting recommendations:', error);
      alert('Failed to get recommendations');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="recommendations-page">
        <button 
          onClick={() => navigate('/dashboard')} 
          className="btn btn-outline" 
          style={{ marginBottom: '1rem' }}
        >
          ← Back to Dashboard
        </button>
        
        <h1>Smart Hospital Recommendations</h1>
        <p className="page-subtitle">Get personalized hospital suggestions based on your needs</p>

        <form onSubmit={handleSubmit} className="card recommendations-form">
          <div className="form-grid">
            <div className="form-group">
              <label className="form-label">Latitude</label>
              <input
                type="number"
                step="any"
                name="latitude"
                className="form-input"
                value={preferences.latitude}
                onChange={handleChange}
                placeholder="13.0827"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Longitude</label>
              <input
                type="number"
                step="any"
                name="longitude"
                className="form-input"
                value={preferences.longitude}
                onChange={handleChange}
                placeholder="80.2707"
              />
            </div>
          </div>

          <button type="button" onClick={getLocation} className="btn btn-outline btn-small mb-3">
            📍 Use My Current Location
          </button>

          <div className="form-group">
            <label className="form-label">Preferred Specialty</label>
            <input
              type="text"
              name="specialty"
              className="form-input"
              value={preferences.specialty}
              onChange={handleChange}
              placeholder="e.g., Cardiology, Orthopedics"
            />
          </div>

          <div className="form-group">
            <label className="form-label">Preferred Language</label>
            <select
              name="language"
              className="form-select"
              value={preferences.language}
              onChange={handleChange}
            >
              <option value="">Any Language</option>
              <option value="English">English</option>
              <option value="Tamil">Tamil</option>
              <option value="Hindi">Hindi</option>
              <option value="Kannada">Kannada</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Accessibility Requirements</label>
            <input
              type="text"
              name="accessibility"
              className="form-input"
              value={preferences.accessibility}
              onChange={handleChange}
              placeholder="e.g., Wheelchair Access"
            />
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Finding Recommendations...' : 'Get Recommendations'}
          </button>
        </form>

        {searched && recommendations.length > 0 && (
          <div className="recommendations-results">
            <h2>{recommendations.length} Recommended Hospitals</h2>
            <div className="recommendations-grid">
              {recommendations.map((hospital, index) => (
                <div key={hospital.id} className="recommendation-card">
                  <div className="recommendation-rank">#{index + 1}</div>
                  <h3>{hospital.name}</h3>
                  <div className="recommendation-score">
                    Match Score: {hospital.recommendation_score}/100
                  </div>
                  
                  {hospital.distance_km && (
                    <p className="distance">📍 {hospital.distance_km} km away</p>
                  )}

                  {hospital.recommendation_reasons.length > 0 && (
                    <div className="reasons">
                      {hospital.recommendation_reasons.map((reason, idx) => (
                        <div key={idx} className="reason">✓ {reason}</div>
                      ))}
                    </div>
                  )}

                  <div className="hospital-quick-info">
                    <span>⭐ {hospital.rating}</span>
                    <span>🛏️ {hospital.available_beds} beds</span>
                  </div>

                  <Link to={`/hospitals/${hospital.id}`} className="btn btn-primary btn-small">
                    View Details
                  </Link>
                </div>
              ))}
            </div>
          </div>
        )}

        {searched && recommendations.length === 0 && !loading && (
          <div className="card">
            <p className="text-center">No recommendations found. Try adjusting your preferences.</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Recommendations;
