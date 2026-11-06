import { Link } from 'react-router-dom';
import { TRANSLATIONS } from '../config';
import './Navbar.css';

function Navbar({ user, onLogout, language, onLanguageChange }) {
  const t = TRANSLATIONS[language];

  // Safely get user display name and initial
  const userName = user?.full_name || user?.email || 'User';
  const userInitial = userName.charAt(0).toUpperCase();

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/dashboard" className="navbar-brand">
          <h1>{t.appName}</h1>
          <span className="navbar-tagline">{t.tagline}</span>
        </Link>

        <div className="navbar-menu">
          <Link to="/dashboard" className="nav-link">
            {t.dashboard}
          </Link>
          <Link to="/hospitals" className="nav-link">
            {t.hospitals}
          </Link>
          <Link to="/recommendations" className="nav-link">
            {t.recommendations}
          </Link>
          <Link to="/appointments" className="nav-link">
            {t.appointments}
          </Link>
          <Link to="/past-records" className="nav-link">
            Past Records
          </Link>
          <Link to="/constraint-lab" className="nav-link">
            {t.constraintLab}
          </Link>
          {user?.is_admin && (
            <Link to="/admin" className="nav-link nav-link-admin">
              {t.admin}
            </Link>
          )}
        </div>

        <div className="navbar-actions">
          <div className="language-toggle">
            <button
              className={`lang-btn ${language === 'en' ? 'active' : ''}`}
              onClick={() => onLanguageChange('en')}
            >
              EN
            </button>
            <button
              className={`lang-btn ${language === 'ta' ? 'active' : ''}`}
              onClick={() => onLanguageChange('ta')}
            >
              தமிழ்
            </button>
          </div>

          <Link to="/profile" className="user-profile">
            <span className="user-avatar">{userInitial}</span>
            <span className="user-name">{userName}</span>
          </Link>

          <button onClick={onLogout} className="btn btn-outline btn-small">
            {t.logout}
          </button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
