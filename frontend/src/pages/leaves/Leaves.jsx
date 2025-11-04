import React, { useState, useEffect } from 'react';
import {
  Calendar,
  CheckCircle,
  Clock,
  User,
  FileText,
  RefreshCw,
  Search
} from '../../utils/icons';
import { MdCancel as XCircle } from 'react-icons/md';
import api from '../../services/api';

const Leaves = () => {
  const [activeTab, setActiveTab] = useState('pending');
  const [leaveRequests, setLeaveRequests] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [leaveTypes, setLeaveTypes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterStatus, setFilterStatus] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedRequest, setSelectedRequest] = useState(null);
  const [showApprovalModal, setShowApprovalModal] = useState(false);
  const [showRejectionModal, setShowRejectionModal] = useState(false);
  const [remarks, setRemarks] = useState('');
  const [processing, setProcessing] = useState(false);

  useEffect(() => {
    fetchInitialData();
  }, []);

  const fetchInitialData = async () => {
    try {
      setLoading(true);
      const requestsResponse = await api.get('/leaves/requests');
      setLeaveRequests(requestsResponse.data || []);

      try {
        const employeesResponse = await api.get('/employees');
        setEmployees(employeesResponse.data || []);
      } catch (error) {
        console.log('Employees not available');
      }

      try {
        const typesResponse = await api.get('/leaves/types');
        setLeaveTypes(typesResponse.data || []);
      } catch (error) {
        console.log('Leave types not available');
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getEmployeeName = (employeeId) => {
    const employee = employees.find(emp => emp.id === employeeId);
    return employee ? employee.full_name : `Employee #${employeeId}`;
  };

  const getLeaveTypeName = (leaveTypeId) => {
    const leaveType = leaveTypes.find(lt => lt.id === leaveTypeId);
    return leaveType?.name || 'Unknown';
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

  const handleApprove = async () => {
    if (!selectedRequest) return;

    try {
      setProcessing(true);
      await api.put(`/leaves/requests/${selectedRequest.id}/approve`, null, {
        params: { remarks: remarks || undefined }
      });

      alert('Leave request approved successfully');
      await fetchInitialData();
      setShowApprovalModal(false);
      setSelectedRequest(null);
      setRemarks('');
    } catch (error) {
      console.error('Error approving leave:', error);
      alert(error.response?.data?.detail || 'Failed to approve leave request');
    } finally {
      setProcessing(false);
    }
  };

  const handleReject = async () => {
    if (!selectedRequest) return;

    if (!remarks.trim()) {
      alert('Please provide a reason for rejection');
      return;
    }

    try {
      setProcessing(true);
      await api.put(`/leaves/requests/${selectedRequest.id}/reject`, null, {
        params: { remarks: remarks }
      });

      alert('Leave request rejected');
      await fetchInitialData();
      setShowRejectionModal(false);
      setSelectedRequest(null);
      setRemarks('');
    } catch (error) {
      console.error('Error rejecting leave:', error);
      alert(error.response?.data?.detail || 'Failed to reject leave request');
    } finally {
      setProcessing(false);
    }
  };

  const filteredRequests = leaveRequests.filter(request => {
    if (activeTab === 'pending' && request.status !== 'pending') return false;
    if (activeTab === 'approved' && request.status !== 'approved') return false;
    if (activeTab === 'rejected' && request.status !== 'rejected') return false;
    if (activeTab === 'all' && filterStatus !== 'all' && request.status !== filterStatus) return false;

    if (searchTerm) {
      const employeeName = getEmployeeName(request.employee_id).toLowerCase();
      const leaveType = getLeaveTypeName(request.leave_type_id).toLowerCase();
      const search = searchTerm.toLowerCase();
      return employeeName.includes(search) || leaveType.includes(search);
    }

    return true;
  });

  const getStatistics = () => {
    return {
      total: leaveRequests.length,
      pending: leaveRequests.filter(r => r.status === 'pending').length,
      approved: leaveRequests.filter(r => r.status === 'approved').length,
      rejected: leaveRequests.filter(r => r.status === 'rejected').length,
    };
  };

  const stats = getStatistics();

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Leave Management</h1>
          <p className="text-gray-600 mt-1">Review and manage employee leave requests</p>
        </div>
        <button onClick={fetchInitialData} className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
          <RefreshCw className="w-4 h-4 mr-2" />
          Refresh
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Requests</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">{stats.total}</p>
            </div>
            <FileText className="w-10 h-10 text-gray-400" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Pending</p>
              <p className="text-2xl font-bold text-yellow-600 mt-1">{stats.pending}</p>
            </div>
            <Clock className="w-10 h-10 text-yellow-400" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Approved</p>
              <p className="text-2xl font-bold text-green-600 mt-1">{stats.approved}</p>
            </div>
            <CheckCircle className="w-10 h-10 text-green-400" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Rejected</p>
              <p className="text-2xl font-bold text-red-600 mt-1">{stats.rejected}</p>
            </div>
            <XCircle className="w-10 h-10 text-red-400" />
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-4">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Search by employee name or leave type..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          {activeTab === 'all' && (
            <div className="w-full md:w-48">
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">All Status</option>
                <option value="pending">Pending</option>
                <option value="approved">Approved</option>
                <option value="rejected">Rejected</option>
              </select>
            </div>
          )}
        </div>
      </div>

      <div className="bg-white rounded-lg shadow">
        <div className="border-b border-gray-200">
          <nav className="flex -mb-px">
            <button onClick={() => setActiveTab('pending')} className={`px-6 py-4 text-sm font-medium border-b-2 transition-colors ${activeTab === 'pending' ? 'border-yellow-500 text-yellow-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}>
              <Clock className="w-4 h-4 inline mr-2" />
              Pending ({stats.pending})
            </button>
            <button onClick={() => setActiveTab('approved')} className={`px-6 py-4 text-sm font-medium border-b-2 transition-colors ${activeTab === 'approved' ? 'border-green-500 text-green-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}>
              <CheckCircle className="w-4 h-4 inline mr-2" />
              Approved ({stats.approved})
            </button>
            <button onClick={() => setActiveTab('rejected')} className={`px-6 py-4 text-sm font-medium border-b-2 transition-colors ${activeTab === 'rejected' ? 'border-red-500 text-red-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}>
              <XCircle className="w-4 h-4 inline mr-2" />
              Rejected ({stats.rejected})
            </button>
            <button onClick={() => setActiveTab('all')} className={`px-6 py-4 text-sm font-medium border-b-2 transition-colors ${activeTab === 'all' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}>
              <FileText className="w-4 h-4 inline mr-2" />
              All ({stats.total})
            </button>
          </nav>
        </div>

        <div className="p-6">
          {filteredRequests.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Employee</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Leave Type</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">From Date</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">To Date</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Days</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Reason</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {filteredRequests.map((request) => (
                    <tr key={request.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <User className="w-5 h-5 text-gray-400 mr-2" />
                          <span className="text-sm font-medium text-gray-900">{getEmployeeName(request.employee_id)}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{getLeaveTypeName(request.leave_type_id)}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{formatDate(request.start_date)}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{formatDate(request.end_date)}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{request.days}</td>
                      <td className="px-6 py-4 text-sm text-gray-600 max-w-xs truncate">{request.reason || '-'}</td>
                      <td className="px-6 py-4 whitespace-nowrap">{getStatusBadge(request.status)}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm space-x-2">
                        {request.status === 'pending' && (
                          <>
                            <button onClick={() => { setSelectedRequest(request); setShowApprovalModal(true); }} className="inline-flex items-center px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700">
                              <CheckCircle className="w-4 h-4 mr-1" />
                              Approve
                            </button>
                            <button onClick={() => { setSelectedRequest(request); setShowRejectionModal(true); }} className="inline-flex items-center px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700">
                              <XCircle className="w-4 h-4 mr-1" />
                              Reject
                            </button>
                          </>
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
              <p className="text-gray-500 text-sm mt-2">
                {activeTab === 'pending' ? 'No pending requests at the moment' :
                 activeTab === 'approved' ? 'No approved requests' :
                 activeTab === 'rejected' ? 'No rejected requests' :
                 'No leave requests in the system'}
              </p>
            </div>
          )}
        </div>
      </div>

      {showApprovalModal && selectedRequest && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Approve Leave Request</h3>
            <div className="space-y-4">
              <div className="bg-gray-50 rounded-lg p-4">
                <p className="text-sm text-gray-600">Employee</p>
                <p className="font-medium text-gray-900">{getEmployeeName(selectedRequest.employee_id)}</p>
              </div>
              <div className="bg-gray-50 rounded-lg p-4">
                <p className="text-sm text-gray-600">Leave Period</p>
                <p className="font-medium text-gray-900">{formatDate(selectedRequest.start_date)} - {formatDate(selectedRequest.end_date)}</p>
                <p className="text-sm text-gray-600 mt-1">{selectedRequest.days} day(s)</p>
              </div>
              <div className="bg-gray-50 rounded-lg p-4">
                <p className="text-sm text-gray-600">Reason</p>
                <p className="font-medium text-gray-900">{selectedRequest.reason || 'No reason provided'}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Remarks (Optional)</label>
                <textarea value={remarks} onChange={(e) => setRemarks(e.target.value)} rows="3" placeholder="Add any remarks..." className="w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
              </div>
            </div>
            <div className="flex justify-end space-x-4 mt-6">
              <button onClick={() => { setShowApprovalModal(false); setSelectedRequest(null); setRemarks(''); }} disabled={processing} className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 disabled:opacity-50">
                Cancel
              </button>
              <button onClick={handleApprove} disabled={processing} className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50">
                {processing ? 'Approving...' : 'Approve'}
              </button>
            </div>
          </div>
        </div>
      )}

      {showRejectionModal && selectedRequest && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Reject Leave Request</h3>
            <div className="space-y-4">
              <div className="bg-gray-50 rounded-lg p-4">
                <p className="text-sm text-gray-600">Employee</p>
                <p className="font-medium text-gray-900">{getEmployeeName(selectedRequest.employee_id)}</p>
              </div>
              <div className="bg-gray-50 rounded-lg p-4">
                <p className="text-sm text-gray-600">Leave Period</p>
                <p className="font-medium text-gray-900">{formatDate(selectedRequest.start_date)} - {formatDate(selectedRequest.end_date)}</p>
                <p className="text-sm text-gray-600 mt-1">{selectedRequest.days} day(s)</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Reason for Rejection <span className="text-red-500">*</span></label>
                <textarea value={remarks} onChange={(e) => setRemarks(e.target.value)} rows="4" required placeholder="Please provide a reason for rejection..." className="w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
              </div>
            </div>
            <div className="flex justify-end space-x-4 mt-6">
              <button onClick={() => { setShowRejectionModal(false); setSelectedRequest(null); setRemarks(''); }} disabled={processing} className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 disabled:opacity-50">
                Cancel
              </button>
              <button onClick={handleReject} disabled={processing || !remarks.trim()} className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 disabled:opacity-50">
                {processing ? 'Rejecting...' : 'Reject'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Leaves;
