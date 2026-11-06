import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import './App.css';
import './theme-fixes.css';

// Pages
import Landing from './pages/Landing';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Hospitals from './pages/Hospitals';
import HospitalDetails from './pages/HospitalDetails';
import Recommendations from './pages/Recommendations';
import Appointments from './pages/Appointments';
import PastRecords from './pages/PastRecords';
import BookAppointment from './pages/BookAppointment';
import ConstraintLab from './pages/ConstraintLab';
import AdminDashboard from './pages/AdminDashboard';
import Profile from './pages/Profile';

// Components
import Navbar from './components/Navbar';

function App() {
  const [user, setUser] = useState(null);
  const [language, setLanguage] = useState('en');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Load user from localStorage
    const storedUser = localStorage.getItem('user');
    const storedLanguage = localStorage.getItem('language');
    
    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser));
      } catch (e) {
        localStorage.removeItem('user');
      }
    }
    
    if (storedLanguage) {
      setLanguage(storedLanguage);
    }
    
    setLoading(false);
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));
    if (userData.language_preference) {
      setLanguage(userData.language_preference);
      localStorage.setItem('language', userData.language_preference);
    }
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('user');
    localStorage.removeItem('token');
  };

  const changeLanguage = (lang) => {
    setLanguage(lang);
    localStorage.setItem('language', lang);
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <BrowserRouter>
      <div className="app">
        {user && <Navbar user={user} onLogout={handleLogout} language={language} onLanguageChange={changeLanguage} />}
        
        <Routes>
          {/* Landing Page */}
          <Route 
            path="/" 
            element={user ? <Navigate to="/dashboard" /> : <Landing language={language} />} 
          />

          {/* Public Routes */}
          <Route 
            path="/login" 
            element={user ? <Navigate to="/dashboard" /> : <Login onLogin={handleLogin} language={language} />} 
          />
          <Route 
            path="/register" 
            element={user ? <Navigate to="/dashboard" /> : <Register onLogin={handleLogin} language={language} />} 
          />

          {/* Protected Routes */}
          <Route
            path="/dashboard"
            element={user ? <Dashboard user={user} language={language} /> : <Navigate to="/login" />}
          />
          <Route
            path="/hospitals"
            element={user ? <Hospitals language={language} /> : <Navigate to="/login" />}
          />
          <Route
            path="/hospitals/:id"
            element={user ? <HospitalDetails language={language} /> : <Navigate to="/login" />}
          />
          <Route
            path="/recommendations"
            element={user ? <Recommendations language={language} /> : <Navigate to="/login" />}
          />
          <Route
            path="/appointments"
            element={user ? <Appointments language={language} /> : <Navigate to="/login" />}
          />
          <Route
            path="/past-records"
            element={user ? <PastRecords /> : <Navigate to="/login" />}
          />
          <Route
            path="/book-appointment/:hospitalId/:doctorId"
            element={user ? <BookAppointment language={language} /> : <Navigate to="/login" />}
          />
          <Route
            path="/constraint-lab"
            element={user ? <ConstraintLab language={language} /> : <Navigate to="/login" />}
          />
          <Route
            path="/profile"
            element={user ? <Profile user={user} onUpdate={handleLogin} language={language} /> : <Navigate to="/login" />}
          />

          {/* Admin Routes */}
          <Route
            path="/admin"
            element={user?.is_admin ? <AdminDashboard language={language} /> : <Navigate to="/dashboard" />}
          />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
