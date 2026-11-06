import { Link } from 'react-router-dom';
import { TRANSLATIONS } from '../config';
import './Landing.css';

function Landing({ language = 'en' }) {
  const t = TRANSLATIONS[language];

  return (
    <div className="landing-container">
      <nav className="landing-nav">
        <div className="nav-brand">
          <h2>{t.appName}</h2>
        </div>
        <div className="nav-actions">
          <Link to="/login" className="nav-link">
            {t.login}
          </Link>
          <Link to="/register" className="btn btn-primary">
            {t.register}
          </Link>
        </div>
      </nav>

      <section className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">
            Your Healthcare
            <span className="highlight"> Access Navigator</span>
          </h1>
          <p className="hero-subtitle">
            Bridging the gap between patients and quality healthcare.
            Find hospitals, book appointments, and manage your health records all in one place.
          </p>
          <div className="hero-actions">
            <Link to="/register" className="btn btn-primary btn-large">
              Get Started
            </Link>
            <Link to="/login" className="btn btn-secondary btn-large">
              Sign In
            </Link>
          </div>
        </div>
        <div className="hero-graphic">
          <div className="graphic-card">
            <div className="card-icon">🏥</div>
            <h3>Find Hospitals</h3>
            <p>Search and discover healthcare facilities near you</p>
          </div>
          <div className="graphic-card">
            <div className="card-icon">📅</div>
            <h3>Book Appointments</h3>
            <p>Schedule appointments with top doctors instantly</p>
          </div>
          <div className="graphic-card">
            <div className="card-icon">🌐</div>
            <h3>Multilingual Support</h3>
            <p>Access services in English and Tamil</p>
          </div>
        </div>
      </section>

      <section className="features-section">
        <h2 className="section-title">Why Choose The Missing Link?</h2>
        <div className="features-grid">
          <div className="feature-item">
            <div className="feature-icon">🔍</div>
            <h3>Smart Recommendations</h3>
            <p>Get personalized hospital recommendations based on your needs, location, and preferences</p>
          </div>
          <div className="feature-item">
            <div className="feature-icon">♿</div>
            <h3>Accessibility First</h3>
            <p>Comprehensive accessibility information for wheelchair users and special needs</p>
          </div>
          <div className="feature-item">
            <div className="feature-icon">📱</div>
            <h3>Real-time Updates</h3>
            <p>Check hospital availability, bed status, and emergency services in real-time</p>
          </div>
          <div className="feature-item">
            <div className="feature-icon">🔒</div>
            <h3>Secure & Private</h3>
            <p>Your health data is encrypted and protected with industry-standard security</p>
          </div>
          <div className="feature-item">
            <div className="feature-icon">🌍</div>
            <h3>Language Support</h3>
            <p>Navigate the platform in your preferred language - English or Tamil</p>
          </div>
          <div className="feature-item">
            <div className="feature-icon">⚡</div>
            <h3>Quick Booking</h3>
            <p>Book appointments in seconds with our streamlined booking process</p>
          </div>
        </div>
      </section>

      <section className="demo-section">
        <div className="demo-card">
          <h2>Try Our Demo</h2>
          <p>Experience the platform with our demo accounts</p>
          <div className="demo-credentials-grid">
            <div className="demo-box">
              <h3>Patient Account</h3>
              <p><strong>Email:</strong> john.doe@email.com</p>
              <p><strong>Password:</strong> patient123</p>
              <Link to="/login" className="btn btn-outline">
                Try Patient Login
              </Link>
            </div>
            <div className="demo-box">
              <h3>Admin Account</h3>
              <p><strong>Email:</strong> admin@hospital.com</p>
              <p><strong>Password:</strong> admin123</p>
              <Link to="/login" className="btn btn-outline">
                Try Admin Login
              </Link>
            </div>
          </div>
        </div>
      </section>

      <section className="cta-section">
        <div className="cta-content">
          <h2>Ready to Get Started?</h2>
          <p>Join thousands of users who trust The Missing Link for their healthcare needs</p>
          <Link to="/register" className="btn btn-primary btn-large">
            Create Your Account
          </Link>
        </div>
      </section>

      <footer className="landing-footer">
        <div className="footer-content">
          <div className="footer-brand">
            <h3>{t.appName}</h3>
            <p>{t.tagline}</p>
          </div>
          <div className="footer-links">
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </div>
        </div>
        <div className="footer-bottom">
          <p>&copy; 2024 The Missing Link. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

export default Landing;
