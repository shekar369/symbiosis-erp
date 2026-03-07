import React, { useState, useEffect } from 'react';
import { FileText, Download, Calendar, DollarSign } from '../../utils/icons';
import { MdFilterAlt as Filter, MdSearch as Search, MdClose as Close, MdVisibility as Eye } from 'react-icons/md';
import api from '../../services/api';

const EmployeePayslips = () => {
  const [payslips, setPayslips] = useState([]);
  const [employeeData, setEmployeeData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());
  const [searchTerm, setSearchTerm] = useState('');
  const [downloading, setDownloading] = useState({});
  const [selectedPayslip, setSelectedPayslip] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [loadingDetail, setLoadingDetail] = useState(false);

  useEffect(() => {
    fetchEmployeeData();
  }, []);

  useEffect(() => {
    if (employeeData) {
      fetchPayslips();
    }
  }, [employeeData, selectedYear]);

  const fetchEmployeeData = async () => {
    try {
      const response = await api.get('/employees/me');
      setEmployeeData(response.data);
    } catch (error) {
      console.error('Error fetching employee data:', error);
      alert('Failed to load employee data');
    }
  };

  const fetchPayslips = async () => {
    try {
      setLoading(true);
      const response = await api.get('/payroll/wage-statements', {
        params: {
          employee_id: employeeData.id,
          year: selectedYear
        }
      });
      setPayslips(response.data || []);
    } catch (error) {
      console.error('Error fetching payslips:', error);
      setPayslips([]);
    } finally {
      setLoading(false);
    }
  };

  const handleViewPayslip = async (month, year) => {
    try {
      setLoadingDetail(true);
      setShowModal(true);

      const response = await api.get(`/payroll/wage-statement/${employeeData.id}`, {
        params: { month, year }
      });

      setSelectedPayslip(response.data);
    } catch (error) {
      console.error('Error fetching payslip details:', error);
      alert('Failed to load payslip details');
      setShowModal(false);
    } finally {
      setLoadingDetail(false);
    }
  };

  const handleDownloadPayslip = async (month, year, employeeCode) => {
    try {
      setDownloading({ ...downloading, [`${month}-${year}`]: true });

      const response = await api.get(`/payroll/payslip/${employeeData.id}`, {
        params: { month, year },
        responseType: 'blob'
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `Payslip_${employeeCode}_${month}_${year}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();

      setDownloading({ ...downloading, [`${month}-${year}`]: false });
    } catch (error) {
      console.error('Error downloading payslip:', error);
      alert('Failed to download payslip');
      setDownloading({ ...downloading, [`${month}-${year}`]: false });
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(amount || 0);
  };

  const numberToWords = (num) => {
    const ones = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
      'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen'];
    const tens = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety'];
    if (!num || num === 0) return 'Zero Rupees Only';
    const convertLessThanThousand = (n) => {
      if (n < 20) return ones[n];
      if (n < 100) return tens[Math.floor(n / 10)] + (n % 10 ? '-' + ones[n % 10] : '');
      return ones[Math.floor(n / 100)] + ' Hundred' + (n % 100 ? ' ' + convertLessThanThousand(n % 100) : '');
    };
    const convertIndian = (n) => {
      if (n < 1000) return convertLessThanThousand(n);
      if (n < 100000) return convertLessThanThousand(Math.floor(n / 1000)) + ' Thousand' + (n % 1000 ? ' ' + convertLessThanThousand(n % 1000) : '');
      if (n < 10000000) return convertLessThanThousand(Math.floor(n / 100000)) + ' Lakh' + (n % 100000 ? ' ' + convertIndian(n % 100000) : '');
      return convertLessThanThousand(Math.floor(n / 10000000)) + ' Crore' + (n % 10000000 ? ' ' + convertIndian(n % 10000000) : '');
    };
    const rupees = Math.floor(num);
    const paise = Math.round((num - rupees) * 100);
    let result = convertIndian(rupees) + ' Rupees';
    if (paise > 0) result += ' and ' + convertIndian(paise) + ' Paise';
    return result + ' Only';
  };

  const getMonthName = (month) => {
    const months = [
      'January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December'
    ];
    return months[month - 1];
  };

  const getStatusBadge = (status) => {
    const colors = {
      approved: 'bg-green-100 text-green-800',
      pending: 'bg-yellow-100 text-yellow-800',
      draft: 'bg-gray-100 text-gray-800',
      paid: 'bg-blue-100 text-blue-800'
    };
    return colors[status?.toLowerCase()] || colors.draft;
  };

  const filteredPayslips = payslips.filter(payslip => {
    const monthName = getMonthName(payslip.month).toLowerCase();
    return monthName.includes(searchTerm.toLowerCase());
  });

  const years = [];
  const currentYear = new Date().getFullYear();
  for (let i = currentYear; i >= currentYear - 5; i--) {
    years.push(i);
  }

  const totalEarnings = filteredPayslips.reduce((sum, p) => sum + (p.total_earnings || 0), 0);
  const totalDeductions = filteredPayslips.reduce((sum, p) => sum + (p.total_deductions || 0), 0);
  const totalNetPay = filteredPayslips.reduce((sum, p) => sum + (p.net_salary || 0), 0);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">My Payslips</h1>
          <p className="text-gray-600 mt-1">View and download your salary slips</p>
        </div>
        <div className="flex items-center space-x-3">
          <FileText className="w-8 h-8 text-blue-600" />
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Earnings</p>
              <p className="text-2xl font-bold text-green-600 mt-1">
                {formatCurrency(totalEarnings)}
              </p>
            </div>
            <div className="bg-green-100 rounded-full p-3">
              <DollarSign className="w-6 h-6 text-green-600" />
            </div>
          </div>
          <p className="text-xs text-gray-500 mt-2">For {selectedYear}</p>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Deductions</p>
              <p className="text-2xl font-bold text-red-600 mt-1">
                {formatCurrency(totalDeductions)}
              </p>
            </div>
            <div className="bg-red-100 rounded-full p-3">
              <DollarSign className="w-6 h-6 text-red-600" />
            </div>
          </div>
          <p className="text-xs text-gray-500 mt-2">For {selectedYear}</p>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Net Pay</p>
              <p className="text-2xl font-bold text-blue-600 mt-1">
                {formatCurrency(totalNetPay)}
              </p>
            </div>
            <div className="bg-blue-100 rounded-full p-3">
              <DollarSign className="w-6 h-6 text-blue-600" />
            </div>
          </div>
          <p className="text-xs text-gray-500 mt-2">For {selectedYear}</p>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <Calendar className="w-5 h-5 text-gray-400" />
              <label className="text-sm font-medium text-gray-700">Year:</label>
              <select
                value={selectedYear}
                onChange={(e) => setSelectedYear(parseInt(e.target.value))}
                className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {years.map(year => (
                  <option key={year} value={year}>{year}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search by month..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      </div>

      {/* Payslips List */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">
            Payslips for {selectedYear}
          </h2>
          <p className="text-sm text-gray-600 mt-1">
            {filteredPayslips.length} payslip(s) found
          </p>
        </div>

        {loading ? (
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : filteredPayslips.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Month
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Days Worked
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Gross Pay
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Deductions
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Net Pay
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
                {filteredPayslips.map((payslip) => (
                  <tr key={payslip.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <Calendar className="w-5 h-5 text-gray-400 mr-2" />
                        <div>
                          <div className="text-sm font-medium text-gray-900">
                            {getMonthName(payslip.month)} {payslip.year}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      {payslip.present_days || 0} / {payslip.total_days || 0}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-green-600">
                      {formatCurrency(payslip.total_earnings)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-red-600">
                      {formatCurrency(payslip.total_deductions)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-blue-600">
                      {formatCurrency(payslip.net_salary)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusBadge(payslip.status)}`}>
                        {payslip.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      {payslip.status === 'approved' || payslip.status === 'calculated' || payslip.status === 'paid' ? (
                        <div className="flex space-x-2">
                          <button
                            onClick={() => handleViewPayslip(payslip.month, payslip.year)}
                            className="inline-flex items-center px-3 py-1.5 border border-blue-600 text-xs font-medium rounded text-blue-600 bg-white hover:bg-blue-50"
                          >
                            <Eye className="w-3 h-3 mr-1" />
                            View
                          </button>
                          <button
                            onClick={() => handleDownloadPayslip(payslip.month, payslip.year, employeeData.employee_code)}
                            disabled={downloading[`${payslip.month}-${payslip.year}`]}
                            className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                          >
                            {downloading[`${payslip.month}-${payslip.year}`] ? (
                              <>
                                <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-white mr-2"></div>
                                Downloading...
                              </>
                            ) : (
                              <>
                                <Download className="w-3 h-3 mr-1" />
                                Download
                              </>
                            )}
                          </button>
                        </div>
                      ) : (
                        <span className="text-gray-400 text-xs">Not available</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-center py-12">
            <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600 text-lg">No payslips found</p>
            <p className="text-gray-500 text-sm mt-2">
              {searchTerm ? 'Try adjusting your search' : `No payslips available for ${selectedYear}`}
            </p>
          </div>
        )}
      </div>

      {/* Info Section */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <div className="flex items-start">
          <div className="flex-shrink-0">
            <FileText className="w-6 h-6 text-blue-600" />
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-blue-900">About Your Payslips</h3>
            <div className="mt-2 text-sm text-blue-700">
              <ul className="list-disc list-inside space-y-1">
                <li>Payslips are available for download once approved by your employer</li>
                <li>You can download payslips for up to 5 years</li>
                <li>Each payslip includes detailed breakdown of earnings and deductions</li>
                <li>Keep your payslips safe for tax filing and loan applications</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Payslip Detail Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
          <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            {/* Background overlay */}
            <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" onClick={() => setShowModal(false)}></div>

            {/* Modal panel */}
            <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full">
              {loadingDetail ? (
                <div className="flex items-center justify-center h-64">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                </div>
              ) : selectedPayslip ? (
                <>
                  {/* Modal Header */}
                  <div className="flex items-center justify-between px-6 py-3 border-b border-gray-200 bg-gray-50">
                    <h3 className="text-base font-bold text-gray-900">
                      Salary Slip — {getMonthName(selectedPayslip.period.month)} {selectedPayslip.period.year}
                    </h3>
                    <button onClick={() => setShowModal(false)} className="text-gray-500 hover:text-gray-700">
                      <Close className="w-5 h-5" />
                    </button>
                  </div>

                  {/* Content — mirrors PDF layout exactly */}
                  <div className="px-6 py-4 max-h-[80vh] overflow-y-auto font-sans">

                    {/* Payslip Title Bar */}
                    <div className="bg-gray-100 border border-gray-300 text-center font-bold text-sm py-2 mb-0">
                      Payslip For the Month of {getMonthName(selectedPayslip.period.month)} {selectedPayslip.period.year}
                    </div>

                    {/* Employee Info Table — 6 rows × 4 cols matching PDF */}
                    <table className="w-full border-collapse text-xs">
                      <tbody>
                        <tr>
                          <td className="bg-gray-100 font-bold border border-gray-300 px-2 py-1.5 w-[22%]">Employee ID</td>
                          <td className="bg-white border border-gray-300 px-2 py-1.5 w-[28%]">{selectedPayslip.employee.code}</td>
                          <td className="bg-gray-100 font-bold border border-gray-300 px-2 py-1.5 w-[22%]">Bank Name</td>
                          <td className="bg-white border border-gray-300 px-2 py-1.5 w-[28%]">{selectedPayslip.employee.bank_name || 'N/A'}</td>
                        </tr>
                        <tr>
                          <td className="bg-gray-100 font-bold border border-gray-300 px-2 py-1.5">Employee Name</td>
                          <td className="bg-white border border-gray-300 px-2 py-1.5">{selectedPayslip.employee.name}</td>
                          <td className="bg-gray-100 font-bold border border-gray-300 px-2 py-1.5">Account No.</td>
                          <td className="bg-white border border-gray-300 px-2 py-1.5">{selectedPayslip.employee.bank_account || 'N/A'}</td>
                        </tr>
                        <tr>
                          <td className="bg-gray-100 font-bold border border-gray-300 px-2 py-1.5">Department</td>
                          <td className="bg-white border border-gray-300 px-2 py-1.5">{selectedPayslip.employee.department || 'N/A'}</td>
                          <td className="bg-gray-100 font-bold border border-gray-300 px-2 py-1.5">PAN Card No.</td>
                          <td className="bg-white border border-gray-300 px-2 py-1.5">{selectedPayslip.employee.pan || 'N/A'}</td>
                        </tr>
                        <tr>
                          <td className="bg-gray-100 font-bold border border-gray-300 px-2 py-1.5">Designation</td>
                          <td className="bg-white border border-gray-300 px-2 py-1.5">{selectedPayslip.employee.designation || 'N/A'}</td>
                          <td className="bg-gray-100 font-bold border border-gray-300 px-2 py-1.5">UAN No.</td>
                          <td className="bg-white border border-gray-300 px-2 py-1.5">{selectedPayslip.employee.uan_number || 'N/A'}</td>
                        </tr>
                        <tr>
                          <td className="bg-gray-100 font-bold border border-gray-300 px-2 py-1.5">Days in Month</td>
                          <td className="bg-white border border-gray-300 px-2 py-1.5">{selectedPayslip.attendance.days_in_month}</td>
                          <td className="bg-gray-100 font-bold border border-gray-300 px-2 py-1.5">ESI No.</td>
                          <td className="bg-white border border-gray-300 px-2 py-1.5">{selectedPayslip.employee.esi_number || 'N/A'}</td>
                        </tr>
                        <tr>
                          <td className="bg-gray-100 font-bold border border-gray-300 px-2 py-1.5">Days Payable</td>
                          <td className="bg-white border border-gray-300 px-2 py-1.5">{selectedPayslip.attendance.days_payable}</td>
                          <td className="bg-gray-100 font-bold border border-gray-300 px-2 py-1.5">CTC per Month</td>
                          <td className="bg-white border border-gray-300 px-2 py-1.5">
                            Rs. {new Intl.NumberFormat('en-IN').format(Math.round(selectedPayslip.employee.ctc || 0))}
                          </td>
                        </tr>
                      </tbody>
                    </table>

                    {/* Leave Row — 3 cells matching PDF */}
                    <table className="w-full border-collapse text-xs">
                      <tbody>
                        <tr>
                          <td className="bg-gray-100 font-bold border border-gray-300 px-2 py-1.5 text-center w-1/3">
                            Total Leaves Accumulated: {selectedPayslip.leave_details?.total_accumulated ?? 'N/A'}
                          </td>
                          <td className="bg-gray-100 font-bold border border-gray-300 px-2 py-1.5 text-center w-1/3">
                            Leaves Availed: {selectedPayslip.leave_details?.leaves_availed ?? 'N/A'}
                          </td>
                          <td className="bg-gray-100 font-bold border border-gray-300 px-2 py-1.5 text-center w-1/3">
                            Balance Leaves: {selectedPayslip.leave_details?.balance_leaves ?? 'N/A'}
                          </td>
                        </tr>
                      </tbody>
                    </table>

                    {/* Earnings & Deductions — 5-column table matching PDF */}
                    {(() => {
                      const actual = selectedPayslip.earnings.actual || {};
                      const earned = selectedPayslip.earnings.earned || {};
                      const deductionsBreakdown = selectedPayslip.deductions.breakdown || {};

                      const fmt = (v) => v > 0 ? new Intl.NumberFormat('en-IN').format(Math.round(v)) : '—';

                      const earningRows = [
                        { label: 'Basic Salary', key: 'basic_salary' },
                        { label: 'HRA', key: 'hra' },
                        { label: 'Conveyance Allowance', key: 'conveyance_allowance' },
                        { label: 'Medical Allowance', key: 'medical_allowance' },
                        { label: 'Special Allowance', key: 'special_allowance' },
                        { label: 'Other Allowance', key: 'other_allowance' },
                      ];

                      const deductionRows = [
                        { label: 'EPF Contribution', key: 'pf_employee' },
                        { label: 'ESI Contribution', key: 'esi_employee' },
                        { label: 'Professional Tax', key: 'professional_tax' },
                        { label: 'TDS', key: 'tds' },
                        { label: 'Advance', key: 'advance_deduction' },
                        { label: 'Other Deductions', key: 'other_deductions' },
                      ];

                      const grossActual = earningRows.reduce((s, r) => s + (actual[r.key] || 0), 0);
                      const grossEarned = earningRows.reduce((s, r) => s + (earned[r.key] || 0), 0);
                      const totalDeductions = deductionRows.reduce((s, r) => s + (deductionsBreakdown[r.key] || 0), 0);

                      return (
                        <table className="w-full border-collapse text-xs">
                          <thead>
                            <tr>
                              <th className="bg-gray-100 font-bold border border-gray-300 px-2 py-1.5 text-left w-[28%]">EARNINGS</th>
                              <th className="bg-gray-100 font-bold border border-gray-300 px-2 py-1.5 text-right w-[15%]">Actual (Rs.)</th>
                              <th className="bg-gray-100 font-bold border border-gray-300 px-2 py-1.5 text-right w-[15%]">Earned (Rs.)</th>
                              <th className="bg-gray-100 font-bold border border-gray-300 px-2 py-1.5 text-left w-[27%]">DEDUCTIONS</th>
                              <th className="bg-gray-100 font-bold border border-gray-300 px-2 py-1.5 text-right w-[15%]">Amount (Rs.)</th>
                            </tr>
                          </thead>
                          <tbody>
                            {earningRows.map((er, i) => {
                              const dr = deductionRows[i];
                              return (
                                <tr key={i}>
                                  <td className="bg-gray-50 border border-gray-300 px-2 py-1.5">{er.label}</td>
                                  <td className="bg-white border border-gray-300 px-2 py-1.5 text-right">{fmt(actual[er.key] || 0)}</td>
                                  <td className="bg-white border border-gray-300 px-2 py-1.5 text-right">{fmt(earned[er.key] || 0)}</td>
                                  <td className="bg-gray-50 border border-gray-300 px-2 py-1.5">{dr.label}</td>
                                  <td className="bg-white border border-gray-300 px-2 py-1.5 text-right">{fmt(deductionsBreakdown[dr.key] || 0)}</td>
                                </tr>
                              );
                            })}
                            <tr>
                              <td className="bg-gray-100 font-bold border border-gray-300 px-2 py-1.5">Gross Salary</td>
                              <td className="bg-gray-100 font-bold border border-gray-300 px-2 py-1.5 text-right">{fmt(grossActual)}</td>
                              <td className="bg-gray-100 font-bold border border-gray-300 px-2 py-1.5 text-right">{fmt(grossEarned)}</td>
                              <td className="bg-gray-100 font-bold border border-gray-300 px-2 py-1.5">Total Deductions</td>
                              <td className="bg-gray-100 font-bold border border-gray-300 px-2 py-1.5 text-right">{fmt(totalDeductions)}</td>
                            </tr>
                          </tbody>
                        </table>
                      );
                    })()}

                    {/* Net Salary + In Words — connected 2-row table matching PDF */}
                    <table className="w-full border-collapse text-xs">
                      <tbody>
                        <tr>
                          <td className="bg-gray-100 font-bold border border-gray-300 px-2 py-2 w-[27%]">Net Salary</td>
                          <td className="bg-white font-bold border border-gray-300 px-2 py-2 text-right text-sm">
                            Rs. {new Intl.NumberFormat('en-IN', { minimumFractionDigits: 2 }).format(selectedPayslip.net_salary)}
                          </td>
                        </tr>
                        <tr>
                          <td className="bg-gray-100 font-bold border border-gray-300 px-2 py-2 whitespace-nowrap">Net Salary in Words</td>
                          <td className="bg-white border border-gray-300 px-2 py-2 italic">
                            {numberToWords(selectedPayslip.net_salary)}
                          </td>
                        </tr>
                      </tbody>
                    </table>

                    <p className="text-gray-400 text-xs italic mt-2">
                      This is a computer generated document, no signature required.
                    </p>
                  </div>

                  {/* Footer */}
                  <div className="bg-gray-50 px-6 py-4 flex justify-end space-x-3">
                    <button
                      onClick={() => setShowModal(false)}
                      className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
                    >
                      Close
                    </button>
                    <button
                      onClick={() => {
                        handleDownloadPayslip(selectedPayslip.period.month, selectedPayslip.period.year, selectedPayslip.employee.code);
                      }}
                      className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
                    >
                      <Download className="w-4 h-4 inline mr-2" />
                      Download PDF
                    </button>
                  </div>
                </>
              ) : null}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default EmployeePayslips;
