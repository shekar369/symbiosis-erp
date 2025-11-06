import React, { useState, useEffect } from 'react';
import {
  User,
  Calendar,
  DollarSign,
  FileText,
  Clock,
  CheckCircle,
  AlertCircle,
  Download,
  TrendingUp
} from '../../utils/icons';
import { MdCancel as XCircle } from 'react-icons/md';
import api from '../../services/api';

const EmployeeDashboard = () => {
  const [employeeData, setEmployeeData] = useState(null);
  const [currentMonthPayslip, setCurrentMonthPayslip] = useState(null);
  const [leaveBalance, setLeaveBalance] = useState([]);
  const [recentLeaves, setRecentLeaves] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);

      // Fetch employee profile
      const profileResponse = await api.get('/employees/me');
      setEmployeeData(profileResponse.data);

      const employeeId = profileResponse.data.id;
      const currentMonth = new Date().getMonth() + 1;
      const currentYear = new Date().getFullYear();

      // Fetch current month payslip
      try {
        const payslipResponse = await api.get(`/payroll/wage-statements`, {
          params: {
            month: currentMonth,
            year: currentYear,
            employee_id: employeeId
          }
        });
        if (payslipResponse.data.length > 0) {
          setCurrentMonthPayslip(payslipResponse.data[0]);
        }
      } catch (error) {
        console.log('No payslip for current month');
      }

      // Fetch leave balance
      try {
        const leaveBalanceResponse = await api.get(`/leaves/balance/${employeeId}`);
        setLeaveBalance(leaveBalanceResponse.data);
      } catch (error) {
        console.log('Leave balance not available');
      }

      // Fetch recent leave requests
      try {
        const leavesResponse = await api.get(`/leaves/requests`, {
          params: { employee_id: employeeId }
        });
        setRecentLeaves(leavesResponse.data.slice(0, 5));
      } catch (error) {
        console.log('Leave requests not available');
      }

    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      alert('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPayslip = async () => {
    try {
      const currentMonth = new Date().getMonth() + 1;
      const currentYear = new Date().getFullYear();

      const response = await api.get(`/payroll/payslip/${employeeData.id}`, {
        params: { month: currentMonth, year: currentYear },
        responseType: 'blob'
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `Payslip_${employeeData.employee_code}_${currentMonth}_${currentYear}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Error downloading payslip:', error);
      alert('Failed to download payslip');
    }
  };

  const getStatusBadge = (status) => {
    const statusConfig = {
      approved: { color: 'bg-green-100 text-green-800', icon: CheckCircle },
      pending: { color: 'bg-yellow-100 text-yellow-800', icon: Clock },
      rejected: { color: 'bg-red-100 text-red-800', icon: XCircle }
    };

    const config = statusConfig[status?.toLowerCase()] || statusConfig.pending;
    const Icon = config.icon;

    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${config.color}`}>
        <Icon className="w-3 h-3 mr-1" />
        {status}
      </span>
    );
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(amount || 0);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-IN', {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Employee Dashboard</h1>
          <p className="text-gray-600 mt-1">Welcome back, {employeeData?.first_name}!</p>
        </div>
        <div className="text-sm text-gray-500">
          {new Date().toLocaleDateString('en-IN', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
          })}
        </div>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Employee Info Card */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Employee Code</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">{employeeData?.employee_code}</p>
            </div>
            <div className="bg-blue-100 rounded-full p-3">
              <User className="w-6 h-6 text-blue-600" />
            </div>
          </div>
          <p className="text-xs text-gray-500 mt-2">{employeeData?.designation}</p>
        </div>

        {/* Current Salary Card */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Current Month</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">
                {currentMonthPayslip ? formatCurrency(currentMonthPayslip.net_pay) : 'N/A'}
              </p>
            </div>
            <div className="bg-green-100 rounded-full p-3">
              <DollarSign className="w-6 h-6 text-green-600" />
            </div>
          </div>
          <p className="text-xs text-gray-500 mt-2">
            {currentMonthPayslip ? getStatusBadge(currentMonthPayslip.status) : 'Not processed'}
          </p>
        </div>

        {/* Leave Balance Card */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Leave Balance</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">
                {leaveBalance.reduce((sum, leave) => sum + (leave.balance || 0), 0)} days
              </p>
            </div>
            <div className="bg-purple-100 rounded-full p-3">
              <Calendar className="w-6 h-6 text-purple-600" />
            </div>
          </div>
          <p className="text-xs text-gray-500 mt-2">
            {leaveBalance.length} leave types available
          </p>
        </div>

        {/* Pending Requests Card */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Pending Requests</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">
                {recentLeaves.filter(l => l.status === 'Pending').length}
              </p>
            </div>
            <div className="bg-yellow-100 rounded-full p-3">
              <Clock className="w-6 h-6 text-yellow-600" />
            </div>
          </div>
          <p className="text-xs text-gray-500 mt-2">Leave requests awaiting approval</p>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Current Month Payslip */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold text-gray-900">Current Month Salary</h2>
              <FileText className="w-5 h-5 text-gray-400" />
            </div>
          </div>
          <div className="p-6">
            {currentMonthPayslip ? (
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-600">Gross Pay</p>
                    <p className="text-xl font-bold text-gray-900">
                      {formatCurrency(currentMonthPayslip.gross_pay)}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Deductions</p>
                    <p className="text-xl font-bold text-red-600">
                      {formatCurrency(currentMonthPayslip.total_deductions)}
                    </p>
                  </div>
                </div>

                <div className="border-t border-gray-200 pt-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Net Pay</p>
                      <p className="text-2xl font-bold text-green-600">
                        {formatCurrency(currentMonthPayslip.net_pay)}
                      </p>
                    </div>
                    <div>
                      {getStatusBadge(currentMonthPayslip.status)}
                    </div>
                  </div>
                </div>

                <div className="border-t border-gray-200 pt-4">
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <p className="text-gray-600">Days Worked</p>
                      <p className="font-semibold text-gray-900">
                        {currentMonthPayslip.days_worked || 0}
                      </p>
                    </div>
                    <div>
                      <p className="text-gray-600">Days in Month</p>
                      <p className="font-semibold text-gray-900">
                        {currentMonthPayslip.total_days || 0}
                      </p>
                    </div>
                  </div>
                </div>

                {currentMonthPayslip.status === 'Approved' && (
                  <button
                    onClick={handleDownloadPayslip}
                    className="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
                  >
                    <Download className="w-4 h-4 mr-2" />
                    Download Payslip
                  </button>
                )}
              </div>
            ) : (
              <div className="text-center py-8">
                <AlertCircle className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                <p className="text-gray-600">No payslip available for current month</p>
                <p className="text-sm text-gray-500 mt-1">Payslip will be available after payroll processing</p>
              </div>
            )}
          </div>
        </div>

        {/* Leave Balance Details */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold text-gray-900">Leave Balance</h2>
              <Calendar className="w-5 h-5 text-gray-400" />
            </div>
          </div>
          <div className="p-6">
            {leaveBalance.length > 0 ? (
              <div className="space-y-4">
                {leaveBalance.map((leave, index) => (
                  <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div>
                      <p className="font-semibold text-gray-900">{leave.leave_type_name}</p>
                      <p className="text-sm text-gray-600 mt-1">
                        Used: {leave.used || 0} days
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-2xl font-bold text-blue-600">{leave.balance || 0}</p>
                      <p className="text-xs text-gray-500">days left</p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <Calendar className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                <p className="text-gray-600">No leave balance information</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Recent Leave Requests */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900">Recent Leave Requests</h2>
            <TrendingUp className="w-5 h-5 text-gray-400" />
          </div>
        </div>
        <div className="overflow-x-auto">
          {recentLeaves.length > 0 ? (
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Leave Type
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    From Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    To Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Days
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {recentLeaves.map((leave) => (
                  <tr key={leave.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {leave.leave_type_name}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      {formatDate(leave.start_date)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      {formatDate(leave.end_date)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      {leave.days}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {getStatusBadge(leave.status)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className="text-center py-8">
              <FileText className="w-12 h-12 text-gray-400 mx-auto mb-3" />
              <p className="text-gray-600">No leave requests found</p>
            </div>
          )}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <a
            href="/employee/payslips"
            className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <FileText className="w-8 h-8 text-blue-600 mr-3" />
            <div>
              <p className="font-semibold text-gray-900">View Payslips</p>
              <p className="text-sm text-gray-600">Download past payslips</p>
            </div>
          </a>

          <a
            href="/employee/leave"
            className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <Calendar className="w-8 h-8 text-purple-600 mr-3" />
            <div>
              <p className="font-semibold text-gray-900">Apply Leave</p>
              <p className="text-sm text-gray-600">Request time off</p>
            </div>
          </a>

          <a
            href="/employee/profile"
            className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <User className="w-8 h-8 text-green-600 mr-3" />
            <div>
              <p className="font-semibold text-gray-900">My Profile</p>
              <p className="text-sm text-gray-600">Update information</p>
            </div>
          </a>
        </div>
      </div>
    </div>
  );
};

export default EmployeeDashboard;
