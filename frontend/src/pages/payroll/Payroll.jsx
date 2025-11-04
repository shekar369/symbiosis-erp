import { useState, useEffect } from 'react';
import { Download, Mail, Send, CheckCircle, Clock, AlertCircle } from '../../utils/icons';
import api from '../../services/api';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Modal from '../../components/common/Modal';

const Payroll = () => {
  const [activeTab, setActiveTab] = useState('process');
  const [wageStatements, setWageStatements] = useState([]);
  const [selectedMonth, setSelectedMonth] = useState(new Date().getMonth() + 1);
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());
  const [loading, setLoading] = useState(false);
  const [processingStatus, setProcessingStatus] = useState(null);
  const [selectedStatements, setSelectedStatements] = useState([]);
  const [showEmailModal, setShowEmailModal] = useState(false);
  const [emailStatus, setEmailStatus] = useState(null);

  const months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  const years = Array.from({ length: 5 }, (_, i) => new Date().getFullYear() - i);

  // Fetch wage statements
  const fetchWageStatements = async () => {
    try {
      setLoading(true);
      const response = await api.get('/payroll/wage-statements', {
        params: {
          month: selectedMonth,
          year: selectedYear
        }
      });
      setWageStatements(response.data);
    } catch (error) {
      console.error('Error fetching wage statements:', error);
      alert('Failed to fetch wage statements');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (activeTab === 'review') {
      fetchWageStatements();
    }
  }, [selectedMonth, selectedYear, activeTab]);

  // Process bulk payroll
  const handleProcessPayroll = async () => {
    if (!confirm(`Process payroll for ${months[selectedMonth - 1]} ${selectedYear}?`)) {
      return;
    }

    try {
      setLoading(true);
      setProcessingStatus(null);

      const response = await api.post('/payroll/process-bulk', {
        month: selectedMonth,
        year: selectedYear
      });

      setProcessingStatus({
        success: true,
        message: response.data.message,
        summary: response.data.summary
      });

      // Switch to review tab
      setTimeout(() => {
        setActiveTab('review');
        fetchWageStatements();
      }, 2000);
    } catch (error) {
      setProcessingStatus({
        success: false,
        message: error.response?.data?.detail || 'Failed to process payroll'
      });
    } finally {
      setLoading(false);
    }
  };

  // Approve wage statements
  const handleApprove = async () => {
    if (selectedStatements.length === 0) {
      alert('Please select statements to approve');
      return;
    }

    if (!confirm(`Approve ${selectedStatements.length} wage statements?`)) {
      return;
    }

    try {
      setLoading(true);
      const response = await api.post('/payroll/approve', {
        wage_statement_ids: selectedStatements
      });

      alert(response.data.message);
      setSelectedStatements([]);
      fetchWageStatements();
    } catch (error) {
      alert('Failed to approve statements: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  // Mark as paid
  const handleMarkPaid = async () => {
    if (selectedStatements.length === 0) {
      alert('Please select statements to mark as paid');
      return;
    }

    if (!confirm(`Mark ${selectedStatements.length} statements as paid?`)) {
      return;
    }

    try {
      setLoading(true);
      const response = await api.post('/payroll/mark-paid', {
        wage_statement_ids: selectedStatements
      });

      alert(response.data.message);
      setSelectedStatements([]);
      fetchWageStatements();
    } catch (error) {
      alert('Failed to mark as paid: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  // Download salary register
  const handleDownloadRegister = async () => {
    try {
      setLoading(true);
      const response = await api.get('/payroll/salary-register', {
        params: {
          month: selectedMonth,
          year: selectedYear
        },
        responseType: 'blob'
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `salary_register_${selectedMonth}_${selectedYear}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();

      alert('Salary register downloaded successfully!');
    } catch (error) {
      alert('Failed to download salary register');
    } finally {
      setLoading(false);
    }
  };

  // Download individual payslip
  const handleDownloadPayslip = async (employeeId, employeeCode) => {
    try {
      const response = await api.get(`/payroll/payslip/${employeeId}`, {
        params: {
          month: selectedMonth,
          year: selectedYear
        },
        responseType: 'blob'
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `payslip_${employeeCode}_${selectedMonth}_${selectedYear}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      alert('Failed to download payslip');
    }
  };

  // Send bulk emails
  const handleSendBulkEmails = async () => {
    if (!confirm('Send payslips to all approved employees via email?')) {
      return;
    }

    try {
      setLoading(true);
      setEmailStatus(null);

      const response = await api.post('/payroll/send-bulk-payslips', null, {
        params: {
          month: selectedMonth,
          year: selectedYear
        }
      });

      setEmailStatus({
        success: true,
        message: response.data.message,
        summary: response.data.summary
      });

      setShowEmailModal(false);
    } catch (error) {
      setEmailStatus({
        success: false,
        message: error.response?.data?.detail || 'Failed to send emails'
      });
    } finally {
      setLoading(false);
    }
  };

  // Send individual email
  const handleSendEmail = async (employeeId, employeeName) => {
    if (!confirm(`Send payslip to ${employeeName} via email?`)) {
      return;
    }

    try {
      const response = await api.post(`/payroll/send-payslip-email/${employeeId}`, null, {
        params: {
          month: selectedMonth,
          year: selectedYear
        }
      });

      alert(response.data.message);
    } catch (error) {
      alert('Failed to send email: ' + (error.response?.data?.detail || error.message));
    }
  };

  // Toggle statement selection
  const toggleStatementSelection = (id) => {
    setSelectedStatements(prev =>
      prev.includes(id) ? prev.filter(s => s !== id) : [...prev, id]
    );
  };

  // Select all statements
  const handleSelectAll = () => {
    if (selectedStatements.length === wageStatements.length) {
      setSelectedStatements([]);
    } else {
      setSelectedStatements(wageStatements.map(ws => ws.id));
    }
  };

  const getStatusBadge = (status) => {
    const styles = {
      draft: 'bg-gray-100 text-gray-800',
      calculated: 'bg-blue-100 text-blue-800',
      approved: 'bg-green-100 text-green-800',
      paid: 'bg-purple-100 text-purple-800'
    };

    return (
      <span className={`px-2 py-1 text-xs font-semibold rounded-full ${styles[status] || styles.draft}`}>
        {status?.toUpperCase()}
      </span>
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Payroll Management</h1>
          <p className="text-gray-600">Process and manage monthly payroll</p>
        </div>

        {/* Month/Year Selector */}
        <div className="flex gap-3">
          <select
            value={selectedMonth}
            onChange={(e) => setSelectedMonth(parseInt(e.target.value))}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            {months.map((month, index) => (
              <option key={index} value={index + 1}>{month}</option>
            ))}
          </select>

          <select
            value={selectedYear}
            onChange={(e) => setSelectedYear(parseInt(e.target.value))}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            {years.map(year => (
              <option key={year} value={year}>{year}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('process')}
            className={`py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'process'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Process Payroll
          </button>
          <button
            onClick={() => setActiveTab('review')}
            className={`py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'review'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Review & Approve
          </button>
          <button
            onClick={() => setActiveTab('distribute')}
            className={`py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'distribute'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Distribute Payslips
          </button>
        </nav>
      </div>

      {/* Tab Content */}
      <div className="mt-6">
        {/* Process Payroll Tab */}
        {activeTab === 'process' && (
          <div className="space-y-6">
            <Card>
              <div className="p-6">
                <h2 className="text-lg font-semibold mb-4">Process Bulk Payroll</h2>
                <p className="text-gray-600 mb-6">
                  Calculate salaries for all active employees for {months[selectedMonth - 1]} {selectedYear}
                </p>

                <div className="space-y-4">
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <h3 className="font-medium text-blue-900 mb-2">What happens when you process?</h3>
                    <ul className="list-disc list-inside space-y-1 text-sm text-blue-800">
                      <li>Fetches attendance data for all active employees</li>
                      <li>Calculates pro-rata salary based on days worked</li>
                      <li>Applies all earnings and deductions</li>
                      <li>Creates wage statements for review</li>
                    </ul>
                  </div>

                  <Button
                    onClick={handleProcessPayroll}
                    disabled={loading}
                    className="w-full"
                  >
                    {loading ? 'Processing...' : 'Process Payroll'}
                  </Button>
                </div>

                {/* Processing Status */}
                {processingStatus && (
                  <div className={`mt-4 p-4 rounded-lg ${
                    processingStatus.success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
                  }`}>
                    <div className="flex items-start">
                      {processingStatus.success ? (
                        <CheckCircle className="w-5 h-5 text-green-600 mr-2 mt-0.5" />
                      ) : (
                        <AlertCircle className="w-5 h-5 text-red-600 mr-2 mt-0.5" />
                      )}
                      <div>
                        <p className={`font-medium ${processingStatus.success ? 'text-green-900' : 'text-red-900'}`}>
                          {processingStatus.message}
                        </p>
                        {processingStatus.summary && (
                          <div className="mt-2 space-y-1 text-sm">
                            <p>Total Employees: {processingStatus.summary.total_employees}</p>
                            <p>Successful: {processingStatus.summary.successful}</p>
                            <p>Failed: {processingStatus.summary.failed}</p>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </Card>
          </div>
        )}

        {/* Review & Approve Tab */}
        {activeTab === 'review' && (
          <div className="space-y-6">
            {/* Actions Bar */}
            <div className="flex justify-between items-center">
              <div className="flex items-center gap-4">
                <input
                  type="checkbox"
                  checked={selectedStatements.length === wageStatements.length && wageStatements.length > 0}
                  onChange={handleSelectAll}
                  className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                />
                <span className="text-sm text-gray-600">
                  {selectedStatements.length} of {wageStatements.length} selected
                </span>
              </div>

              <div className="flex gap-3">
                <Button onClick={handleApprove} disabled={loading || selectedStatements.length === 0}>
                  Approve Selected
                </Button>
                <Button onClick={handleMarkPaid} disabled={loading || selectedStatements.length === 0} variant="secondary">
                  Mark as Paid
                </Button>
                <Button onClick={handleDownloadRegister} disabled={loading} variant="outline">
                  <Download className="w-4 h-4 mr-2" />
                  Download Register
                </Button>
              </div>
            </div>

            {/* Wage Statements Table */}
            <Card>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left">
                        <input
                          type="checkbox"
                          checked={selectedStatements.length === wageStatements.length && wageStatements.length > 0}
                          onChange={handleSelectAll}
                          className="w-4 h-4 text-blue-600 rounded"
                        />
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Employee</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Days</th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Gross</th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Deductions</th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Net Salary</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {loading ? (
                      <tr>
                        <td colSpan="8" className="px-6 py-4 text-center text-gray-500">
                          Loading...
                        </td>
                      </tr>
                    ) : wageStatements.length === 0 ? (
                      <tr>
                        <td colSpan="8" className="px-6 py-4 text-center text-gray-500">
                          No wage statements found for this period
                        </td>
                      </tr>
                    ) : (
                      wageStatements.map((ws) => (
                        <tr key={ws.id} className="hover:bg-gray-50">
                          <td className="px-6 py-4">
                            <input
                              type="checkbox"
                              checked={selectedStatements.includes(ws.id)}
                              onChange={() => toggleStatementSelection(ws.id)}
                              className="w-4 h-4 text-blue-600 rounded"
                            />
                          </td>
                          <td className="px-6 py-4 text-sm text-gray-900">
                            Employee ID: {ws.employee_id}
                          </td>
                          <td className="px-6 py-4 text-sm text-gray-900">
                            {ws.effective_days?.toFixed(1) || ws.days_worked}
                          </td>
                          <td className="px-6 py-4 text-sm text-right text-gray-900">
                            ₹{ws.gross_salary?.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                          </td>
                          <td className="px-6 py-4 text-sm text-right text-gray-900">
                            ₹{ws.total_deductions?.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                          </td>
                          <td className="px-6 py-4 text-sm text-right font-medium text-gray-900">
                            ₹{ws.net_salary?.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                          </td>
                          <td className="px-6 py-4">
                            {getStatusBadge(ws.status)}
                          </td>
                          <td className="px-6 py-4 text-right text-sm">
                            <button
                              onClick={() => handleDownloadPayslip(ws.employee_id, `EMP${ws.employee_id}`)}
                              className="text-blue-600 hover:text-blue-900 mr-3"
                              title="Download PDF"
                            >
                              <Download className="w-4 h-4" />
                            </button>
                            <button
                              onClick={() => handleSendEmail(ws.employee_id, `Employee ${ws.employee_id}`)}
                              className="text-green-600 hover:text-green-900"
                              title="Send Email"
                            >
                              <Mail className="w-4 h-4" />
                            </button>
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </Card>
          </div>
        )}

        {/* Distribute Payslips Tab */}
        {activeTab === 'distribute' && (
          <div className="space-y-6">
            <Card>
              <div className="p-6">
                <h2 className="text-lg font-semibold mb-4">Distribute Payslips</h2>

                <div className="grid grid-cols-2 gap-6">
                  {/* Download Options */}
                  <div className="space-y-4">
                    <h3 className="font-medium text-gray-900">Download PDFs</h3>
                    <p className="text-sm text-gray-600 mb-4">
                      Download payslips as PDF files
                    </p>

                    <div className="space-y-3">
                      <Button onClick={handleDownloadRegister} className="w-full" variant="outline">
                        <Download className="w-4 h-4 mr-2" />
                        Download Salary Register
                      </Button>

                      <div className="text-sm text-gray-500">
                        For individual payslips, use the download button in the Review tab
                      </div>
                    </div>
                  </div>

                  {/* Email Options */}
                  <div className="space-y-4">
                    <h3 className="font-medium text-gray-900">Send via Email</h3>
                    <p className="text-sm text-gray-600 mb-4">
                      Email payslips to all employees
                    </p>

                    <Button onClick={() => setShowEmailModal(true)} className="w-full">
                      <Mail className="w-4 h-4 mr-2" />
                      Send Bulk Emails
                    </Button>

                    {emailStatus && (
                      <div className={`mt-4 p-4 rounded-lg ${
                        emailStatus.success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
                      }`}>
                        <p className={`font-medium ${emailStatus.success ? 'text-green-900' : 'text-red-900'}`}>
                          {emailStatus.message}
                        </p>
                        {emailStatus.summary && (
                          <div className="mt-2 space-y-1 text-sm">
                            <p>Emails Sent: {emailStatus.summary.emails_sent}</p>
                            <p>Failed: {emailStatus.summary.emails_failed}</p>
                            <p>Skipped (no email): {emailStatus.summary.skipped_no_email}</p>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </Card>
          </div>
        )}
      </div>

      {/* Email Confirmation Modal */}
      <Modal
        isOpen={showEmailModal}
        onClose={() => setShowEmailModal(false)}
        title="Send Bulk Payslip Emails"
      >
        <div className="space-y-4">
          <p className="text-gray-600">
            This will send payslip emails to all approved employees for {months[selectedMonth - 1]} {selectedYear}.
          </p>

          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <p className="text-sm text-yellow-800">
              <strong>Note:</strong> Make sure SMTP is configured in your environment variables.
              Employees without email addresses will be skipped.
            </p>
          </div>

          <div className="flex gap-3 justify-end">
            <Button onClick={() => setShowEmailModal(false)} variant="outline">
              Cancel
            </Button>
            <Button onClick={handleSendBulkEmails} disabled={loading}>
              {loading ? 'Sending...' : 'Send Emails'}
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default Payroll;
