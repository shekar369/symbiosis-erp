import React, { useState, useEffect } from 'react';
import {
  DollarSign,
  Users,
  TrendingUp,
  Calendar,
  CheckCircle,
  Clock,
  AlertCircle,
  Download,
  Mail,
  FileText,
  RefreshCw
} from 'lucide-react';
import api from '../../services/api';

const PayrollDashboard = () => {
  const [selectedMonth, setSelectedMonth] = useState(new Date().getMonth() + 1);
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());
  const [summary, setSummary] = useState(null);
  const [wageStatements, setWageStatements] = useState([]);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [selectedStatements, setSelectedStatements] = useState([]);

  useEffect(() => {
    fetchPayrollData();
  }, [selectedMonth, selectedYear]);

  const fetchPayrollData = async () => {
    try {
      setLoading(true);

      // Fetch summary
      const summaryResponse = await api.get('/payroll/summary', {
        params: { month: selectedMonth, year: selectedYear }
      });
      setSummary(summaryResponse.data);

      // Fetch wage statements
      const statementsResponse = await api.get('/payroll/wage-statements', {
        params: { month: selectedMonth, year: selectedYear }
      });
      setWageStatements(statementsResponse.data);
    } catch (error) {
      console.error('Error fetching payroll data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleProcessBulkPayroll = async () => {
    if (!confirm(`Are you sure you want to process payroll for ${getMonthName(selectedMonth)} ${selectedYear}?`)) {
      return;
    }

    try {
      setProcessing(true);
      const response = await api.post('/payroll/process-bulk', {
        month: selectedMonth,
        year: selectedYear
      });

      alert(`Payroll processed successfully!\nSuccessful: ${response.data.successful}\nFailed: ${response.data.failed}`);
      fetchPayrollData();
    } catch (error) {
      console.error('Error processing payroll:', error);
      alert('Failed to process payroll');
    } finally {
      setProcessing(false);
    }
  };

  const handleApproveSelected = async () => {
    if (selectedStatements.length === 0) {
      alert('Please select at least one payslip to approve');
      return;
    }

    try {
      await api.post('/payroll/approve', {
        wage_statement_ids: selectedStatements
      });
      alert(`${selectedStatements.length} payslip(s) approved successfully`);
      setSelectedStatements([]);
      fetchPayrollData();
    } catch (error) {
      console.error('Error approving payslips:', error);
      alert('Failed to approve payslips');
    }
  };

  const handleMarkPaidSelected = async () => {
    if (selectedStatements.length === 0) {
      alert('Please select at least one payslip to mark as paid');
      return;
    }

    try {
      await api.post('/payroll/mark-paid', {
        wage_statement_ids: selectedStatements
      });
      alert(`${selectedStatements.length} payslip(s) marked as paid successfully`);
      setSelectedStatements([]);
      fetchPayrollData();
    } catch (error) {
      console.error('Error marking payslips as paid:', error);
      alert('Failed to mark payslips as paid');
    }
  };

  const handleSendBulkPayslips = async () => {
    if (!confirm(`Send payslips via email to all employees for ${getMonthName(selectedMonth)} ${selectedYear}?`)) {
      return;
    }

    try {
      const response = await api.post('/payroll/send-bulk-payslips', {
        month: selectedMonth,
        year: selectedYear
      });
      alert(`Bulk email sent!\nEmails sent: ${response.data.summary.emails_sent}\nFailed: ${response.data.summary.emails_failed}\nSkipped: ${response.data.summary.skipped_no_email}`);
    } catch (error) {
      console.error('Error sending bulk payslips:', error);
      alert('Failed to send bulk payslips');
    }
  };

  const handleDownloadSalaryRegister = async () => {
    try {
      const response = await api.get('/payroll/salary-register', {
        params: { month: selectedMonth, year: selectedYear },
        responseType: 'blob'
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `salary_register_${selectedMonth}_${selectedYear}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Error downloading salary register:', error);
      alert('Failed to download salary register');
    }
  };

  const toggleSelectAll = () => {
    if (selectedStatements.length === wageStatements.length) {
      setSelectedStatements([]);
    } else {
      setSelectedStatements(wageStatements.map(s => s.id));
    }
  };

  const toggleSelectStatement = (id) => {
    setSelectedStatements(prev =>
      prev.includes(id) ? prev.filter(sid => sid !== id) : [...prev, id]
    );
  };

  const getMonthName = (month) => {
    const months = ['January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December'];
    return months[month - 1];
  };

  const getStatusBadge = (status) => {
    const badges = {
      draft: 'bg-gray-100 text-gray-800',
      calculated: 'bg-blue-100 text-blue-800',
      approved: 'bg-green-100 text-green-800',
      paid: 'bg-purple-100 text-purple-800'
    };
    return badges[status] || 'bg-gray-100 text-gray-800';
  };

  const getStatusIcon = (status) => {
    switch(status) {
      case 'calculated': return <Clock className="w-4 h-4" />;
      case 'approved': return <CheckCircle className="w-4 h-4" />;
      case 'paid': return <CheckCircle className="w-4 h-4" />;
      default: return <AlertCircle className="w-4 h-4" />;
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount || 0);
  };

  const years = [];
  const currentYear = new Date().getFullYear();
  for (let i = currentYear; i >= currentYear - 3; i--) {
    years.push(i);
  }

  const months = [
    { value: 1, label: 'January' },
    { value: 2, label: 'February' },
    { value: 3, label: 'March' },
    { value: 4, label: 'April' },
    { value: 5, label: 'May' },
    { value: 6, label: 'June' },
    { value: 7, label: 'July' },
    { value: 8, label: 'August' },
    { value: 9, label: 'September' },
    { value: 10, label: 'October' },
    { value: 11, label: 'November' },
    { value: 12, label: 'December' }
  ];

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
          <h1 className="text-2xl font-bold text-gray-900">Payroll Management</h1>
          <p className="text-gray-600 mt-1">Process and manage employee payroll</p>
        </div>
        <button
          onClick={fetchPayrollData}
          className="flex items-center gap-2 px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
        >
          <RefreshCw className="w-4 h-4" />
          Refresh
        </button>
      </div>

      {/* Period Selector */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center gap-4">
          <Calendar className="w-5 h-5 text-gray-400" />
          <div className="flex items-center gap-4">
            <label className="text-sm font-medium text-gray-700">Month:</label>
            <select
              value={selectedMonth}
              onChange={(e) => setSelectedMonth(parseInt(e.target.value))}
              className="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              {months.map(month => (
                <option key={month.value} value={month.value}>{month.label}</option>
              ))}
            </select>

            <label className="text-sm font-medium text-gray-700 ml-4">Year:</label>
            <select
              value={selectedYear}
              onChange={(e) => setSelectedYear(parseInt(e.target.value))}
              className="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              {years.map(year => (
                <option key={year} value={year}>{year}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Summary Cards */}
      {summary && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Employees</p>
                <p className="text-2xl font-bold text-gray-900 mt-2">{summary.summary.total_employees}</p>
              </div>
              <div className="p-3 bg-blue-100 rounded-lg">
                <Users className="w-6 h-6 text-blue-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Gross</p>
                <p className="text-2xl font-bold text-gray-900 mt-2">{formatCurrency(summary.summary.total_gross_salary)}</p>
              </div>
              <div className="p-3 bg-green-100 rounded-lg">
                <TrendingUp className="w-6 h-6 text-green-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Deductions</p>
                <p className="text-2xl font-bold text-gray-900 mt-2">{formatCurrency(summary.summary.total_deductions)}</p>
              </div>
              <div className="p-3 bg-red-100 rounded-lg">
                <DollarSign className="w-6 h-6 text-red-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Net Payable</p>
                <p className="text-2xl font-bold text-gray-900 mt-2">{formatCurrency(summary.summary.total_net_salary)}</p>
              </div>
              <div className="p-3 bg-purple-100 rounded-lg">
                <DollarSign className="w-6 h-6 text-purple-600" />
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Status Overview */}
      {summary && summary.status_breakdown && Object.keys(summary.status_breakdown).length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Status Overview</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(summary.status_breakdown).map(([status, count]) => (
              <div key={status} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                {getStatusIcon(status)}
                <div>
                  <p className="text-sm text-gray-600 capitalize">{status}</p>
                  <p className="text-lg font-semibold text-gray-900">{count}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <button
            onClick={handleProcessBulkPayroll}
            disabled={processing}
            className="flex items-center justify-center gap-2 px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <RefreshCw className={`w-4 h-4 ${processing ? 'animate-spin' : ''}`} />
            {processing ? 'Processing...' : 'Process Payroll'}
          </button>

          <button
            onClick={handleApproveSelected}
            disabled={selectedStatements.length === 0}
            className="flex items-center justify-center gap-2 px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <CheckCircle className="w-4 h-4" />
            Approve Selected
          </button>

          <button
            onClick={handleMarkPaidSelected}
            disabled={selectedStatements.length === 0}
            className="flex items-center justify-center gap-2 px-4 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <DollarSign className="w-4 h-4" />
            Mark as Paid
          </button>

          <button
            onClick={handleSendBulkPayslips}
            className="flex items-center justify-center gap-2 px-4 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
          >
            <Mail className="w-4 h-4" />
            Send Payslips
          </button>
        </div>

        <div className="mt-4 pt-4 border-t border-gray-200">
          <button
            onClick={handleDownloadSalaryRegister}
            className="flex items-center gap-2 px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            <FileText className="w-4 h-4" />
            Download Salary Register
          </button>
        </div>
      </div>

      {/* Employee Payroll Table */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-gray-900">Employee Payroll</h3>
            <span className="text-sm text-gray-600">{selectedStatements.length} selected</span>
          </div>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left">
                  <input
                    type="checkbox"
                    checked={selectedStatements.length === wageStatements.length && wageStatements.length > 0}
                    onChange={toggleSelectAll}
                    className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Employee</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Days</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Gross</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Deductions</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Net Salary</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {wageStatements.map((statement) => (
                <tr key={statement.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <input
                      type="checkbox"
                      checked={selectedStatements.includes(statement.id)}
                      onChange={() => toggleSelectStatement(statement.id)}
                      className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">{statement.employee_name || 'Unknown'}</div>
                    <div className="text-xs text-gray-500">{statement.employee_code || `#${statement.employee_id}`}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    {statement.present_days}/{statement.total_days}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {formatCurrency(statement.total_earnings)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-red-600">
                    {formatCurrency(statement.total_deductions)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-blue-600">
                    {formatCurrency(statement.net_salary)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusBadge(statement.status)}`}>
                      {statement.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {wageStatements.length === 0 && (
            <div className="text-center py-12">
              <FileText className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">No payroll data</h3>
              <p className="mt-1 text-sm text-gray-500">
                Process payroll for this period to see employee data.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PayrollDashboard;
