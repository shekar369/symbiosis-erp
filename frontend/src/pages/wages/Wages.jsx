import { useState, useEffect } from 'react';
import { Search, FileText, Download } from '../../utils/icons';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Table from '../../components/common/Table';
import { wagesAPI } from '../../api/wages';

const Wages = () => {
  const [wages, setWages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    employeeId: '',
    month: new Date().getMonth() + 1,
    year: new Date().getFullYear(),
  });

  useEffect(() => {
    fetchWages();
  }, [filters]);

  const fetchWages = async () => {
    try {
      setLoading(true);
      const data = await wagesAPI.getAll(0, 20, filters);
      setWages(data);
    } catch (error) {
      console.error('Failed to fetch wages:', error);
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    { key: 'employee_id', label: 'Employee ID' },
    {
      key: 'month',
      label: 'Month',
      render: (month, row) => `${getMonthName(month)} ${row.year}`,
    },
    {
      key: 'basic_salary',
      label: 'Basic Salary',
      render: (value) => `$${parseFloat(value || 0).toFixed(2)}`,
    },
    {
      key: 'total_earnings',
      label: 'Total Earnings',
      render: (value) => `$${parseFloat(value || 0).toFixed(2)}`,
    },
    {
      key: 'total_deductions',
      label: 'Total Deductions',
      render: (value) => `$${parseFloat(value || 0).toFixed(2)}`,
    },
    {
      key: 'net_salary',
      label: 'Net Salary',
      render: (value) => (
        <span className="font-semibold text-green-600">
          ${parseFloat(value || 0).toFixed(2)}
        </span>
      ),
    },
    {
      key: 'status',
      label: 'Status',
      render: (status) => {
        const colors = {
          DRAFT: 'bg-gray-100 text-gray-800',
          CALCULATED: 'bg-blue-100 text-blue-800',
          APPROVED: 'bg-green-100 text-green-800',
          PAID: 'bg-purple-100 text-purple-800',
        };
        return (
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${colors[status]}`}>
            {status}
          </span>
        );
      },
    },
    {
      key: 'actions',
      label: 'Actions',
      render: (_, wage) => (
        <div className="flex gap-2">
          <button className="text-blue-600 hover:text-blue-800" title="View Payslip">
            <FileText size={18} />
          </button>
          <button className="text-green-600 hover:text-green-800" title="Download">
            <Download size={18} />
          </button>
        </div>
      ),
    },
  ];

  const getMonthName = (month) => {
    const months = [
      'January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December'
    ];
    return months[month - 1];
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Wage Statements</h1>
      </div>

      <Card className="mb-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Employee ID
            </label>
            <input
              type="number"
              placeholder="Filter by Employee ID"
              value={filters.employeeId}
              onChange={(e) => setFilters({ ...filters, employeeId: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Month
            </label>
            <select
              value={filters.month}
              onChange={(e) => setFilters({ ...filters, month: parseInt(e.target.value) })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              {Array.from({ length: 12 }, (_, i) => i + 1).map((month) => (
                <option key={month} value={month}>
                  {getMonthName(month)}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Year
            </label>
            <select
              value={filters.year}
              onChange={(e) => setFilters({ ...filters, year: parseInt(e.target.value) })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              {Array.from({ length: 5 }, (_, i) => new Date().getFullYear() - i).map((year) => (
                <option key={year} value={year}>
                  {year}
                </option>
              ))}
            </select>
          </div>
        </div>
      </Card>

      <Card>
        <Table columns={columns} data={wages} loading={loading} />
      </Card>
    </div>
  );
};

export default Wages;
