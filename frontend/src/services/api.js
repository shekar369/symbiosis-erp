import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken'); // Fixed: was 'token', should be 'accessToken'
    console.log('[API Service] Token from localStorage:', token ? 'Token exists' : 'No token');
    console.log('[API Service] Request URL:', config.url);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
      console.log('[API Service] Authorization header set');
    }
    return config;
  },
  (error) => {
    console.error('[API Service] Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => {
    console.log('[API Service] Response received:', response.config.url, response.status);
    return response;
  },
  (error) => {
    console.error('[API Service] Response error:', error.config?.url, error.response?.status);
    if (error.response?.status === 401) {
      console.log('[API Service] 401 detected, clearing auth and redirecting to login');
      // Token expired or invalid
      localStorage.removeItem('accessToken'); // Fixed: was 'token', should be 'accessToken'
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
