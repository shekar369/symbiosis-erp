import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from '@/contexts/auth'

export default function PrivateRoute({ allowedRoles }) {
  const { user, loading } = useAuth()

  if (loading) {
    return <div>Loading...</div>
  }

  if (!user) {
    return <Navigate to="/login" replace />
  }

  if (allowedRoles && !allowedRoles.includes(user.role)) {
    // Redirect to appropriate dashboard based on role
    switch (user.role) {
      case 'saas_admin':
        return <Navigate to="/saas-admin/dashboard" replace />
      case 'employer_admin':
        return <Navigate to="/employer/dashboard" replace />
      case 'employee':
        return <Navigate to="/employee/dashboard" replace />
      case 'auditor':
        return <Navigate to="/auditor/dashboard" replace />
      default:
        return <Navigate to="/login" replace />
    }
  }

  return <Outlet />
}