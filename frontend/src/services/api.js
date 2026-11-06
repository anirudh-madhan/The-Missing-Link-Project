import axios from 'axios';
import { API_BASE_URL } from '../config';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth APIs
export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  getProfile: () => api.get('/auth/profile'),
  updateProfile: (userData) => api.put('/auth/profile', userData)
};

// Hospital APIs
export const hospitalAPI = {
  getAll: (params) => api.get('/hospitals', { params }),
  getById: (id) => api.get(`/hospitals/${id}`),
  getRecommendations: (preferences) => api.post('/hospitals/recommendations', preferences),
  getDoctors: (hospitalId, specialty) => api.get(`/hospitals/${hospitalId}/doctors`, { params: { specialty } }),
  getSpecialties: () => api.get('/hospitals/specialties'),
  getCities: () => api.get('/hospitals/cities')
};

// Appointment APIs
export const appointmentAPI = {
  getAll: () => api.get('/appointments'),
  getById: (id) => api.get(`/appointments/${id}`),
  book: (appointmentData) => api.post('/appointments', appointmentData),
  update: (id, appointmentData) => api.put(`/appointments/${id}`, appointmentData),
  cancel: (id) => api.delete(`/appointments/${id}`),
  getAvailableSlots: (doctorId, date) => api.get('/appointments/available-slots', { params: { doctor_id: doctorId, date } }),
  getDocumentChecklist: () => api.get('/appointments/documents/checklist')
};

// Admin APIs
export const adminAPI = {
  getStats: () => api.get('/admin/stats'),
  createHospital: (hospitalData) => api.post('/admin/hospitals', hospitalData),
  updateHospital: (id, hospitalData) => api.put(`/admin/hospitals/${id}`, hospitalData),
  deleteHospital: (id) => api.delete(`/admin/hospitals/${id}`),
  createDoctor: (doctorData) => api.post('/admin/doctors', doctorData),
  updateDoctor: (id, doctorData) => api.put(`/admin/doctors/${id}`, doctorData),
  completeAppointment: (id) => api.post(`/admin/appointments/${id}/complete`)
};

// Constraint Lab APIs
export const constraintAPI = {
  getAll: () => api.get('/constraints'),
  getById: (id) => api.get(`/constraints/${id}`),
  runTest: (id, data) => api.post(`/constraints/${id}/test`, data || {}),
  getLogs: (params) => api.get('/constraints/logs', { params }),
  getLog: (id) => api.get(`/constraints/logs/${id}`)
};

export default api;
