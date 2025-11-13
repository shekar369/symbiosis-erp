import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { MdLogin as LogIn } from 'react-icons/md';
import { useAuth } from '../../contexts/AuthContext';
import Input from '../../components/common/Input';
import Button from '../../components/common/Button';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const { login, isAuthenticated, user } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    // If already authenticated, redirect to appropriate dashboard based on role
    if (isAuthenticated && user) {
      let defaultPath = '/dashboard';
      if (user.role === 'employee') {
        defaultPath = '/employee/dashboard';
      }
      const from = location.state?.from?.pathname || defaultPath;
      navigate(from, { replace: true });
    }
  }, [isAuthenticated, user, navigate, location]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const result = await login(username, password);
      if (result.success) {
        // Get user from localStorage to determine role
        const userData = JSON.parse(localStorage.getItem('user'));
        const userRole = userData?.role;

        // Navigate based on user role
        if (userRole === 'employee') {
          navigate('/employee/dashboard');
        } else {
          // employer, hr_manager, admin go to main dashboard
          navigate('/dashboard');
        }
      } else {
        setError(result.error || 'Login failed');
      }
    } catch (err) {
      setError('An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-500 to-primary-700">
      <div className="bg-white p-8 rounded-lg shadow-2xl w-full max-w-md">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 rounded-full mb-4">
            <LogIn size={32} className="text-primary-600" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900">HR Payroll System</h1>
          <p className="text-gray-600 mt-2">Sign in to your account</p>
        </div>

        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-800 text-sm">{error}</p>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <Input
            label="Username"
            type="text"
            name="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Enter your username"
            required
          />

          <Input
            label="Password"
            type="password"
            name="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter your password"
            required
          />

          <Button
            type="submit"
            disabled={loading}
            className="w-full mt-6"
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </Button>
        </form>

        <div className="mt-6 text-center text-sm text-gray-600">
          <p>Demo credentials:</p>
          <p className="font-mono mt-1">Username: admin | Password: admin123</p>
        </div>
      </div>
    </div>
  );
};

export default Login;
