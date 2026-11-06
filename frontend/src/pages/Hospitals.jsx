import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { hospitalAPI } from '../services/api';
import { TRANSLATIONS } from '../config';
import './Hospitals.css';

function Hospitals({ language }) {
  const [hospitals, setHospitals] = useState([]);
  const [specialties, setSpecialties] = useState([]);
  const [cities, setCities] = useState([]);
  const [filters, setFilters] = useState({
    specialty: '',
    city: '',
    emergency: false
  });
  const [loading, setLoading] = useState(true);
  const t = TRANSLATIONS[language];

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    searchHospitals();
  }, [filters]);

  const fetchData = async () => {
    try {
      const [hospitalsRes, specialtiesRes, citiesRes] = await Promise.all([
        hospitalAPI.getAll(),
        hospitalAPI.getSpecialties(),
        hospitalAPI.getCities()
      ]);
      
      setHospitals(hospitalsRes.data.hospitals);
      setSpecialties(specialtiesRes.data.specialties);
      setCities(citiesRes.data.cities);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const searchHospitals = async () => {
    try {
      const response = await hospitalAPI.getAll(filters);
      setHospitals(response.data.hospitals);
    } catch (error) {
      console.error('Error searching hospitals:', error);
    }
  };

  const handleFilterChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFilters({
      ...filters,
      [name]: type === 'checkbox' ? checked : value
    });
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
      <div className="hospitals-page">
        <h1>{t.hospitals}</h1>
        
        <div className="filters-card">
          <div className="filters-grid">
            <div className="form-group">
              <label className="form-label">Specialty</label>
              <select
                name="specialty"
                className="form-select"
                value={filters.specialty}
                onChange={handleFilterChange}
              >
                <option value="">All Specialties</option>
                {specialties.map((specialty) => (
                  <option key={specialty} value={specialty}>{specialty}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">City</label>
              <select
                name="city"
                className="form-select"
                value={filters.city}
                onChange={handleFilterChange}
              >
                <option value="">All Cities</option>
                {cities.map((city) => (
                  <option key={city} value={city}>{city}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="emergency"
                  checked={filters.emergency}
                  onChange={handleFilterChange}
                />
                <span>Emergency Services Only</span>
              </label>
            </div>
          </div>
        </div>

        <div className="results-count">
          <p>{hospitals.length} hospital{hospitals.length !== 1 ? 's' : ''} found</p>
        </div>

        <div className="hospitals-grid">
          {hospitals.map((hospital) => (
            <div key={hospital.id} className="hospital-card">
              <div className="hospital-header">
                <h3>{language === 'ta' && hospital.name_tamil ? hospital.name_tamil : hospital.name}</h3>
                <div className="hospital-rating">⭐ {hospital.rating}</div>
              </div>
              
              <p className="hospital-address">{hospital.address}, {hospital.city}</p>
              
              <div className="hospital-info">
                <div className="info-item">
                  <span>📞</span>
                  <span>{hospital.phone}</span>
                </div>
                <div className="info-item">
                  <span>🛏️</span>
                  <span>{hospital.available_beds}/{hospital.total_beds} beds available</span>
                </div>
              </div>

              {hospital.specialties.length > 0 && (
                <div className="hospital-specialties">
                  {hospital.specialties.slice(0, 3).map((spec) => (
                    <span key={spec} className="badge badge-info">{spec}</span>
                  ))}
                  {hospital.specialties.length > 3 && (
                    <span className="badge">+{hospital.specialties.length - 3} more</span>
                  )}
                </div>
              )}

              <div className="hospital-actions">
                <Link to={`/hospitals/${hospital.id}`} className="btn btn-primary btn-small">
                  {t.viewDetails}
                </Link>
              </div>
            </div>
          ))}
        </div>

        {hospitals.length === 0 && (
          <div className="no-results">
            <p>{t.noResults}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Hospitals;
