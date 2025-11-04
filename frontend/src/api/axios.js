import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1';

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    console.log('[Axios Interceptor] Token from localStorage:', token ? 'Token exists' : 'No token');
    console.log('[Axios Interceptor] Request URL:', config.url);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
      console.log('[Axios Interceptor] Authorization header set');
    }
    return config;
  },
  (error) => {
    console.error('[Axios Interceptor] Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
axiosInstance.interceptors.response.use(
  (response) => {
    console.log('[Axios Interceptor] Response received:', response.config.url, response.status);
    return response;
  },
  (error) => {
    console.error('[Axios Interceptor] Response error:', error.config?.url, error.response?.status);
    if (error.response?.status === 401) {
      console.log('[Axios Interceptor] 401 detected, clearing auth and redirecting to login');
      localStorage.removeItem('accessToken');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;
 
