import { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../api/auth';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      setLoading(true);
      try {
        const token = localStorage.getItem('accessToken');
        const savedUser = localStorage.getItem('user');

        if (token && savedUser) {
          try {
            const userData = JSON.parse(savedUser);
            setUser(userData);
          } catch (error) {
            console.error('Failed to parse saved user:', error);
            localStorage.removeItem('accessToken');
            localStorage.removeItem('user');
          }
        }
      } finally {
        setLoading(false);
      }
    };

    initAuth();
  }, []);

  const login = async (username, password) => {
    try {
      console.log('[AuthContext] Login attempt for user:', username);
      const response = await authAPI.login(username, password);
      console.log('[AuthContext] Login response:', response);
      const { access_token, user: userData } = response;

      console.log('[AuthContext] Saving token to localStorage');
      localStorage.setItem('accessToken', access_token);
      localStorage.setItem('user', JSON.stringify(userData));
      setUser(userData);

      console.log('[AuthContext] Token saved, verifying:', localStorage.getItem('accessToken') ? 'Token exists' : 'Token missing');
      console.log('[AuthContext] User state updated:', userData);

      return { success: true };
    } catch (error) {
      console.error('[AuthContext] Login error:', error);
      return {
        success: false,
        error: error.response?.data?.detail || 'Login failed'
      };
    }
  };

  const logout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('user');
    setUser(null);
  };

  const contextValue = {
    user,
    loading,
    login,
    logout,
    isAuthenticated: !!user
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {typeof children === 'function' ? children(contextValue) : children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
