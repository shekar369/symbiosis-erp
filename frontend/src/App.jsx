import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { ConfigProvider } from './contexts/config';
import ProtectedRoute from './components/common/ProtectedRoute';
import Layout from './components/layout/Layout';
import Login from './pages/auth/Login';
import Dashboard from './pages/dashboard/Dashboard';
import EmployerDashboard from './pages/dashboard/EmployerDashboard';
import Employees from './pages/employees/Employees';
import EmployeeDetail from './pages/employees/EmployeeDetail';
import Attendance from './pages/attendance/Attendance';
import Wages from './pages/wages/Wages';
import Leaves from './pages/leaves/Leaves';
import Reports from './pages/reports/Reports';
import Locations from './pages/locations/Locations';
import Payroll from './pages/payroll/Payroll';
import Statutory from './pages/statutory/Statutory';
import BankTransfer from './pages/bank/BankTransfer';
import SystemConfig from './pages/admin/SystemConfig';
import EmployeeDashboard from './pages/employee/EmployeeDashboard';
import EmployeePayslips from './pages/employee/EmployeePayslips';
import EmployeeLeave from './pages/employee/EmployeeLeave';
import EmployeeProfile from './pages/employee/EmployeeProfile';

function App() {
  return (
    <AuthProvider>
      <ConfigProvider>
        <Routes>
            <Route path="/login" element={<Login />} />
            
            <Route
              path="/*"
              element={
                <ProtectedRoute>
                  <Layout />
                </ProtectedRoute>
              }
            >
              <Route index element={<Navigate to="dashboard" replace />} />
              <Route path="dashboard" element={<EmployerDashboard />} />
            <Route path="dashboard-old" element={<Dashboard />} />
            <Route path="employees" element={<Employees />} />
            <Route path="employees/:id" element={<EmployeeDetail />} />
            <Route path="locations" element={<Locations />} />
            <Route path="attendance" element={<Attendance />} />
            <Route path="payroll" element={<Payroll />} />
            <Route path="statutory" element={<Statutory />} />
            <Route path="bank-transfer" element={<BankTransfer />} />
            <Route path="wages" element={<Wages />} />
            <Route path="leaves" element={<Leaves />} />
            <Route path="reports" element={<Reports />} />

            {/* Admin Routes */}
            <Route path="admin/config" element={<SystemConfig />} />

            {/* Employee Routes */}
            <Route path="employee/dashboard" element={<EmployeeDashboard />} />
            <Route path="employee/payslips" element={<EmployeePayslips />} />
            <Route path="employee/leave" element={<EmployeeLeave />} />
            <Route path="employee/profile" element={<EmployeeProfile />} />
          </Route>

          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </ConfigProvider>
    </AuthProvider>
  );
}

export default App;
