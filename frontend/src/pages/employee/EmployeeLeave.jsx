import React, { useState, useEffect } from 'react';
import {
  Calendar,
  Plus,
  CheckCircle,
  Clock,
  Trash2,
  AlertCircle,
  RefreshCw
} from '../../utils/icons';
import { MdCancel as XCircle } from 'react-icons/md';
import api from '../../services/api';

const EmployeeLeave = () => {
  const [activeTab, setActiveTab] = useState('apply');
  const [employeeData, setEmployeeData] = useState(null);
  const [leaveTypes, setLeaveTypes] = useState([]);
  const [leaveBalance, setLeaveBalance] = useState([]);
  const [leaveRequests, setLeaveRequests] = useState([]);
  const [loading, setLoading] = useState(true);

  // Form state
  const [formData, setFormData] = useState({
    leave_type_id: '',
    start_date: '',
    end_date: '',
    reason: ''
  });
  const [submitting, setSubmitting] = useState(false);
  const [showCancelModal, setShowCancelModal] = useState(false);
  const [leaveToCancel, setLeaveToCancel] = useState(null);

  useEffect(() => {
    fetchInitialData();
  }, []);

  const fetchInitialData = async () => {
    try {
      setLoading(true);

      // Fetch employee data
      const employeeResponse = await api.get('/employees/me');
      setEmployeeData(employeeResponse.data);

      const employeeId = employeeResponse.data.id;

      // Fetch leave types
      try {
        const typesResponse = await api.get('/leaves/types');
        setLeaveTypes(typesResponse.data);
      } catch (error) {
        console.log('Leave types not available');
      }

      // Fetch leave balance
      try {
        const balanceResponse = await api.get(`/leaves/balance/${employeeId}`);
        setLeaveBalance(balanceResponse.data);
      } catch (error) {
        console.log('Leave balance not available');
      }

      // Fetch leave requests
      await fetchLeaveRequests(employeeId);

    } catch (error) {
      console.error('Error fetching data:', error);
      alert('Failed to load leave data');
    } finally {
      setLoading(false);
    }
  };

  const fetchLeaveRequests = async (employeeId) => {
    try {
      const response = await api.get('/leaves/requests', {
        params: { employee_id: employeeId }
      });
      setLeaveRequests(response.data || []);
    } catch (error) {
      console.log('Leave requests not available');
      setLeaveRequests([]);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const calculateDays = () => {
    if (formData.start_date && formData.end_date) {
      const start = new Date(formData.start_date);
      const end = new Date(formData.end_date);
      const diffTime = Math.abs(end - start);
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;
      return diffDays;
    }
    return 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.leave_type_id || !formData.start_date || !formData.end_date) {
      alert('Please fill in all required fields');
      return;
    }

    const startDate = new Date(formData.start_date);
    const endDate = new Date(formData.end_date);

    if (endDate < startDate) {
      alert('End date cannot be before start date');
      return;
    }

    try {
      setSubmitting(true);

      await api.post('/leaves/requests', {
        employee_id: employeeData.id,
        leave_type_id: parseInt(formData.leave_type_id),
        start_date: formData.start_date,
        end_date: formData.end_date,
        reason: formData.reason || null
      });

      alert('Leave request submitted successfully!');

      // Reset form
      setFormData({
        leave_type_id: '',
        start_date: '',
        end_date: '',
        reason: ''
      });

      // Refresh data
      await fetchLeaveRequests(employeeData.id);
      const balanceResponse = await api.get(`/leaves/balance/${employeeData.id}`);
      setLeaveBalance(balanceResponse.data);

      setActiveTab('my-leaves');
    } catch (error) {
      console.error('Error submitting leave request:', error);
      alert(error.response?.data?.detail || 'Failed to submit leave request');
    } finally {
      setSubmitting(false);
    }
  };

  const handleCancelLeave = async () => {
    if (!leaveToCancel) return;

    try {
      await api.delete(`/leaves/requests/${leaveToCancel.id}`);
      alert('Leave request cancelled successfully');

      // Refresh data
      await fetchLeaveRequests(employeeData.id);
      const balanceResponse = await api.get(`/leaves/balance/${employeeData.id}`);
      setLeaveBalance(balanceResponse.data);

      setShowCancelModal(false);
      setLeaveToCancel(null);
    } catch (error) {
      console.error('Error cancelling leave:', error);
      alert(error.response?.data?.detail || 'Failed to cancel leave request');
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

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-IN', {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    });
  };

  const getLeaveTypeName = (leaveTypeId) => {
    const leaveType = leaveTypes.find(lt => lt.id === leaveTypeId);
    return leaveType?.name || 'Unknown';
  };

  const getLeaveBalance = (leaveTypeId) => {
    const balance = leaveBalance.find(lb => lb.leave_type_id === leaveTypeId);
    return balance?.balance || 0;
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
          <h1 className="text-2xl font-bold text-gray-900">Leave Management</h1>
          <p className="text-gray-600 mt-1">Apply for leave and track your requests</p>
        </div>
        <Calendar className="w-8 h-8 text-blue-600" />
      </div>

      {/* Leave Balance Summary */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Leave Balance</h2>
        {leaveBalance.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {leaveBalance.map((balance, index) => (
              <div key={index} className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-4 border border-blue-200">
                <p className="text-sm font-medium text-gray-700">{balance.leave_type_name}</p>
                <div className="flex items-baseline mt-2">
                  <p className="text-3xl font-bold text-blue-600">{balance.balance || 0}</p>
                  <p className="text-sm text-gray-600 ml-2">days left</p>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  Used: {balance.used || 0} days
                </p>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500">No leave balance information available</p>
        )}
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow">
        <div className="border-b border-gray-200">
          <nav className="flex -mb-px">
            <button
              onClick={() => setActiveTab('apply')}
              className={`px-6 py-4 text-sm font-medium border-b-2 transition-colors ${
                activeTab === 'apply'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <Plus className="w-4 h-4 inline mr-2" />
              Apply Leave
            </button>
            <button
              onClick={() => setActiveTab('my-leaves')}
              className={`px-6 py-4 text-sm font-medium border-b-2 transition-colors ${
                activeTab === 'my-leaves'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <Calendar className="w-4 h-4 inline mr-2" />
              My Leaves
            </button>
          </nav>
        </div>

        {/* Tab Content */}
        <div className="p-6">
          {activeTab === 'apply' && (
            <div className="max-w-2xl">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Apply for Leave</h3>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Leave Type <span className="text-red-500">*</span>
                  </label>
                  <select
                    name="leave_type_id"
                    value={formData.leave_type_id}
                    onChange={handleInputChange}
                    required
                    className="w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">Select leave type</option>
                    {leaveTypes.map(type => (
                      <option key={type.id} value={type.id}>
                        {type.name} ({getLeaveBalance(type.id)} days available)
                      </option>
                    ))}
                  </select>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Start Date <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="date"
                      name="start_date"
                      value={formData.start_date}
                      onChange={handleInputChange}
                      required
                      min={new Date().toISOString().split('T')[0]}
                      className="w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      End Date <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="date"
                      name="end_date"
                      value={formData.end_date}
                      onChange={handleInputChange}
                      required
                      min={formData.start_date || new Date().toISOString().split('T')[0]}
                      className="w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>

                {formData.start_date && formData.end_date && (
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <p className="text-sm font-medium text-blue-900">
                      Total Days: <span className="text-lg font-bold">{calculateDays()}</span> day(s)
                    </p>
                  </div>
                )}

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Reason (Optional)
                  </label>
                  <textarea
                    name="reason"
                    value={formData.reason}
                    onChange={handleInputChange}
                    rows="4"
                    placeholder="Enter reason for leave..."
                    className="w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div className="flex justify-end space-x-4">
                  <button
                    type="button"
                    onClick={() => {
                      setFormData({
                        leave_type_id: '',
                        start_date: '',
                        end_date: '',
                        reason: ''
                      });
                    }}
                    className="px-6 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
                  >
                    Reset
                  </button>
                  <button
                    type="submit"
                    disabled={submitting}
                    className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {submitting ? (
                      <>
                        <RefreshCw className="w-4 h-4 inline mr-2 animate-spin" />
                        Submitting...
                      </>
                    ) : (
                      <>
                        <Plus className="w-4 h-4 inline mr-2" />
                        Submit Request
                      </>
                    )}
                  </button>
                </div>
              </form>
            </div>
          )}

          {activeTab === 'my-leaves' && (
            <div>
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">My Leave Requests</h3>
                <p className="text-sm text-gray-600">
                  Total: {leaveRequests.length} request(s)
                </p>
              </div>

              {leaveRequests.length > 0 ? (
                <div className="overflow-x-auto">
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
                          Reason
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Status
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Actions
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {leaveRequests.map((leave) => (
                        <tr key={leave.id} className="hover:bg-gray-50">
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                            {leave.leave_type_name || getLeaveTypeName(leave.leave_type_id)}
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
                          <td className="px-6 py-4 text-sm text-gray-600 max-w-xs truncate">
                            {leave.reason || '-'}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            {getStatusBadge(leave.status)}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm">
                            {leave.status === 'Pending' && (
                              <button
                                onClick={() => {
                                  setLeaveToCancel(leave);
                                  setShowCancelModal(true);
                                }}
                                className="text-red-600 hover:text-red-800"
                              >
                                <Trash2 className="w-4 h-4" />
                              </button>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="text-center py-12">
                  <Calendar className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-600 text-lg">No leave requests found</p>
                  <p className="text-gray-500 text-sm mt-2">Click "Apply Leave" to submit a request</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Info Box */}
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
        <div className="flex items-start">
          <AlertCircle className="w-6 h-6 text-yellow-600 flex-shrink-0" />
          <div className="ml-3">
            <h3 className="text-sm font-medium text-yellow-900">Leave Policy Guidelines</h3>
            <div className="mt-2 text-sm text-yellow-700">
              <ul className="list-disc list-inside space-y-1">
                <li>Leave requests should be submitted at least 3 days in advance</li>
                <li>Ensure you have sufficient leave balance before applying</li>
                <li>Emergency leaves can be applied on the same day with proper reason</li>
                <li>You can cancel pending leave requests anytime</li>
                <li>Approved leaves cannot be cancelled through this portal</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Cancel Confirmation Modal */}
      {showCancelModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Cancel Leave Request</h3>
            <p className="text-gray-600 mb-6">
              Are you sure you want to cancel this leave request?
              <br />
              <span className="font-medium text-gray-900">
                {leaveToCancel && `${formatDate(leaveToCancel.start_date)} - ${formatDate(leaveToCancel.end_date)} (${leaveToCancel.days} days)`}
              </span>
            </p>
            <div className="flex justify-end space-x-4">
              <button
                onClick={() => {
                  setShowCancelModal(false);
                  setLeaveToCancel(null);
                }}
                className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
              >
                No, Keep It
              </button>
              <button
                onClick={handleCancelLeave}
                className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
              >
                Yes, Cancel Leave
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default EmployeeLeave;
