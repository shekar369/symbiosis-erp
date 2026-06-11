import { useState, useEffect } from 'react';
import { Download, FileText, Users, DollarSign, Calendar } from '../../utils/icons';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import api from '../../services/api';

const MONTHS = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December',
];

const currentDate = new Date();
const YEARS = Array.from({ length: 5 }, (_, i) => currentDate.getFullYear() - i);

const Reports = () => {
  const [activeTab, setActiveTab] = useState('attendance');
  const [month, setMonth] = useState(currentDate.getMonth() + 1);
  const [year, setYear] = useState(currentDate.getFullYear());
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState(null);
  const [error, setError] = useState('');

  const fetchReport = async () => {
    setLoading(true);
    setError('');
    setReport(null);
    try {
      const endpoint = activeTab === 'attendance'
        ? `/reports/attendance?month=${month}&year=${year}`
        : `/reports/payroll?month=${month}&year=${year}`;
      const res = await api.get(endpoint);
      setReport(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load report');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setReport(null);
  }, [activeTab]);

  const exportCSV = () => {
    if (!report) return;
    const rows = report.records || [];
    if (!rows.length) return;
    const headers = Object.keys(rows[0]).join(',');
    const lines = rows.map(r => Object.values(r).join(','));
    const csv = [headers, ...lines].join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${activeTab}_report_${MONTHS[month - 1]}_${year}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Reports</h1>
        {report && (
          <Button variant="outline" icon={<Download size={16} />} onClick={exportCSV}>
            Export CSV
          </Button>
        )}
      </div>

      {/* Tab selector */}
      <div className="flex gap-2 border-b border-gray-200">
        {[
          { key: 'attendance', label: 'Attendance Report', icon: Calendar },
          { key: 'payroll', label: 'Payroll Report', icon: DollarSign },
          { key: 'salary', label: 'Salary Register', icon: FileText },
        ].map(({ key, label, icon: Icon }) => (
          <button
            key={key}
            onClick={() => setActiveTab(key)}
            className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
              activeTab === key
                ? 'border-primary-600 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            <Icon size={16} />
            {label}
          </button>
        ))}
      </div>

      {/* Filters */}
      <Card>
        <div className="flex flex-wrap gap-4 items-end">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Month</label>
            <select
              value={month}
              onChange={e => setMonth(Number(e.target.value))}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              {MONTHS.map((m, i) => (
                <option key={i + 1} value={i + 1}>{m}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Year</label>
            <select
              value={year}
              onChange={e => setYear(Number(e.target.value))}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              {YEARS.map(y => (
                <option key={y} value={y}>{y}</option>
              ))}
            </select>
          </div>
          <Button variant="primary" onClick={fetchReport} disabled={loading}>
            {loading ? 'Loading…' : 'Generate Report'}
          </Button>
        </div>
      </Card>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
          {error}
        </div>
      )}

      {/* Results */}
      {report && activeTab === 'attendance' && <AttendanceTable data={report} />}
      {report && activeTab === 'payroll' && <PayrollTable data={report} />}
      {report && activeTab === 'salary' && <SalaryRegisterTable data={report} />}
    </div>
  );
};

// ─── Sub-tables ──────────────────────────────────────────────────────────────

const AttendanceTable = ({ data }) => (
  <Card title={`Attendance — ${MONTHS[data.month - 1]} ${data.year}`}>
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200 text-sm">
        <thead className="bg-gray-50">
          <tr>
            {['Code', 'Name', 'Present', 'Absent', 'Half Day', 'Leave', 'Weekly Off', 'Holiday', 'Total Recorded'].map(h => (
              <th key={h} className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{h}</th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-100">
          {data.records.length === 0 && (
            <tr><td colSpan={9} className="px-4 py-6 text-center text-gray-400">No records found</td></tr>
          )}
          {data.records.map(r => (
            <tr key={r.employee_id} className="hover:bg-gray-50">
              <td className="px-4 py-2 font-mono text-xs">{r.employee_code}</td>
              <td className="px-4 py-2 font-medium">{r.name}</td>
              <td className="px-4 py-2 text-green-700 font-semibold">{r.present}</td>
              <td className="px-4 py-2 text-red-600">{r.absent}</td>
              <td className="px-4 py-2 text-yellow-600">{r.half_day}</td>
              <td className="px-4 py-2 text-blue-600">{r.leave}</td>
              <td className="px-4 py-2 text-gray-500">{r.weekly_off}</td>
              <td className="px-4 py-2 text-purple-600">{r.holiday}</td>
              <td className="px-4 py-2 text-gray-700">{r.total_recorded}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </Card>
);

const PayrollTable = ({ data }) => (
  <Card title={`Payroll Summary — ${MONTHS[data.month - 1]} ${data.year}`}>
    {/* Summary bar */}
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      {[
        { label: 'Employees', value: data.summary.total_employees },
        { label: 'Total Gross', value: `₹${Number(data.summary.total_gross).toLocaleString('en-IN')}` },
        { label: 'Total Deductions', value: `₹${Number(data.summary.total_deductions).toLocaleString('en-IN')}` },
        { label: 'Total Net', value: `₹${Number(data.summary.total_net).toLocaleString('en-IN')}`, highlight: true },
      ].map(s => (
        <div key={s.label} className={`p-3 rounded-lg ${s.highlight ? 'bg-green-50' : 'bg-gray-50'}`}>
          <p className="text-xs text-gray-500">{s.label}</p>
          <p className={`text-lg font-bold ${s.highlight ? 'text-green-700' : 'text-gray-800'}`}>{s.value}</p>
        </div>
      ))}
    </div>
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200 text-sm">
        <thead className="bg-gray-50">
          <tr>
            {['Code', 'Name', 'Present', 'Absent', 'Basic', 'Gross', 'Deductions', 'Net Salary', 'Status'].map(h => (
              <th key={h} className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{h}</th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-100">
          {data.records.length === 0 && (
            <tr><td colSpan={9} className="px-4 py-6 text-center text-gray-400">No records found</td></tr>
          )}
          {data.records.map(r => (
            <tr key={r.employee_id} className="hover:bg-gray-50">
              <td className="px-4 py-2 font-mono text-xs">{r.employee_code}</td>
              <td className="px-4 py-2 font-medium">{r.name}</td>
              <td className="px-4 py-2">{r.present_days}</td>
              <td className="px-4 py-2 text-red-600">{r.absent_days}</td>
              <td className="px-4 py-2">₹{Number(r.basic_salary).toLocaleString('en-IN')}</td>
              <td className="px-4 py-2">₹{Number(r.total_earnings).toLocaleString('en-IN')}</td>
              <td className="px-4 py-2 text-red-600">₹{Number(r.total_deductions).toLocaleString('en-IN')}</td>
              <td className="px-4 py-2 font-bold text-green-700">₹{Number(r.net_salary).toLocaleString('en-IN')}</td>
              <td className="px-4 py-2">
                <StatusBadge status={r.status} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </Card>
);

const SalaryRegisterTable = ({ data }) => (
  <Card title={`Salary Register — ${data.month}/${data.year}`}>
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200 text-sm">
        <thead className="bg-gray-50">
          <tr>
            {['Code', 'Name', 'Basic', 'HRA', 'Conveyance', 'Medical', 'Special', 'PF', 'ESI', 'PT', 'Net Salary', 'Status'].map(h => (
              <th key={h} className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{h}</th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-100">
          {(data.records || []).length === 0 && (
            <tr><td colSpan={12} className="px-4 py-6 text-center text-gray-400">No records found</td></tr>
          )}
          {(data.records || []).map(r => {
            const e = r.earnings || {};
            const d = r.deductions || {};
            return (
              <tr key={r.employee_id} className="hover:bg-gray-50">
                <td className="px-4 py-2 font-mono text-xs">{r.employee_code}</td>
                <td className="px-4 py-2 font-medium">{r.name}</td>
                <td className="px-4 py-2">₹{Number(e.basic_salary || 0).toLocaleString('en-IN')}</td>
                <td className="px-4 py-2">₹{Number(e.hra || 0).toLocaleString('en-IN')}</td>
                <td className="px-4 py-2">₹{Number(e.conveyance_allowance || 0).toLocaleString('en-IN')}</td>
                <td className="px-4 py-2">₹{Number(e.medical_allowance || 0).toLocaleString('en-IN')}</td>
                <td className="px-4 py-2">₹{Number(e.special_allowance || 0).toLocaleString('en-IN')}</td>
                <td className="px-4 py-2 text-red-600">₹{Number(d.pf_employee || 0).toLocaleString('en-IN')}</td>
                <td className="px-4 py-2 text-red-600">₹{Number(d.esi_employee || 0).toLocaleString('en-IN')}</td>
                <td className="px-4 py-2 text-red-600">₹{Number(d.professional_tax || 0).toLocaleString('en-IN')}</td>
                <td className="px-4 py-2 font-bold text-green-700">₹{Number(r.net_salary || 0).toLocaleString('en-IN')}</td>
                <td className="px-4 py-2"><StatusBadge status={r.status} /></td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  </Card>
);

const STATUS_COLORS = {
  calculated: 'bg-blue-100 text-blue-700',
  approved:   'bg-green-100 text-green-700',
  paid:       'bg-emerald-100 text-emerald-700',
  draft:      'bg-gray-100 text-gray-600',
};

const StatusBadge = ({ status }) => (
  <span className={`px-2 py-0.5 rounded-full text-xs font-medium capitalize ${STATUS_COLORS[status] || 'bg-gray-100 text-gray-600'}`}>
    {status}
  </span>
);

export default Reports;
