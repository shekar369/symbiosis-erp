import { useState } from 'react';
import { Download, FileText, AlertCircle } from '../../utils/icons';
import api from '../../services/api';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';

const Statutory = () => {
  const [selectedMonth, setSelectedMonth] = useState(new Date().getMonth() + 1);
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());
  const [selectedState, setSelectedState] = useState('Maharashtra');
  const [downloading, setDownloading] = useState({});

  const months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  const years = Array.from({ length: 5 }, (_, i) => new Date().getFullYear() - i);

  const indianStates = [
    'Andhra Pradesh', 'Telangana', 'Karnataka', 'Tamil Nadu', 'Kerala',
    'Maharashtra', 'Gujarat', 'Rajasthan', 'Madhya Pradesh', 'Uttar Pradesh',
    'West Bengal', 'Bihar', 'Odisha', 'Punjab', 'Haryana'
  ];

  const statutoryForms = [
    {
      id: 'epf-ecr',
      title: 'EPF-ECR',
      description: 'Electronic Challan Cum Return for EPF',
      endpoint: '/statutory/epf-ecr',
      format: 'CSV',
      deadline: '15th of next month',
      icon: '🏦',
      color: 'blue'
    },
    {
      id: 'esi-return',
      title: 'ESI Return',
      description: 'Employee State Insurance monthly return',
      endpoint: '/statutory/esi-return',
      format: 'CSV',
      deadline: '10th of next month',
      icon: '🏥',
      color: 'green'
    },
    {
      id: 'pt-form-v',
      title: 'PT Form V',
      description: 'Professional Tax return form',
      endpoint: '/statutory/pt-form-v',
      format: 'PDF',
      deadline: 'As per state',
      icon: '📋',
      color: 'purple',
      requiresState: true
    },
    {
      id: 'form-xiii',
      title: 'Form-XIII',
      description: 'Workmen Register under Contract Labour Act',
      endpoint: '/statutory/form-xiii',
      format: 'PDF',
      deadline: 'For records',
      icon: '📝',
      color: 'yellow'
    },
    {
      id: 'pf-challan',
      title: 'PF Challan Summary',
      description: 'Monthly PF payment summary',
      endpoint: '/statutory/pf-challan-summary',
      format: 'PDF',
      deadline: '15th of next month',
      icon: '💰',
      color: 'indigo'
    }
  ];

  const handleDownload = async (form) => {
    try {
      setDownloading(prev => ({ ...prev, [form.id]: true }));

      const params = {
        month: selectedMonth,
        year: selectedYear
      };

      if (form.requiresState) {
        params.state = selectedState;
      }

      const response = await api.get(form.endpoint, {
        params,
        responseType: 'blob'
      });

      const extension = form.format.toLowerCase();
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${form.id}_${selectedMonth}_${selectedYear}.${extension}`);
      document.body.appendChild(link);
      link.click();
      link.remove();

      alert(`${form.title} downloaded successfully!`);
    } catch (error) {
      console.error(`Error downloading ${form.title}:`, error);
      alert(`Failed to download ${form.title}: ${error.response?.data?.detail || error.message}`);
    } finally {
      setDownloading(prev => ({ ...prev, [form.id]: false }));
    }
  };

  const getColorClasses = (color) => {
    const colors = {
      blue: 'bg-blue-50 border-blue-200 text-blue-900',
      green: 'bg-green-50 border-green-200 text-green-900',
      purple: 'bg-purple-50 border-purple-200 text-purple-900',
      yellow: 'bg-yellow-50 border-yellow-200 text-yellow-900',
      indigo: 'bg-indigo-50 border-indigo-200 text-indigo-900'
    };
    return colors[color] || colors.blue;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Statutory Compliance</h1>
          <p className="text-gray-600">Generate and download statutory forms</p>
        </div>

        {/* Period Selector */}
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

      {/* Info Banner */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-start">
          <AlertCircle className="w-5 h-5 text-blue-600 mr-3 mt-0.5" />
          <div>
            <h3 className="font-medium text-blue-900 mb-1">Important Information</h3>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>• Ensure payroll is processed and approved before downloading forms</li>
              <li>• EPF-ECR and ESI returns must be filed before their respective deadlines</li>
              <li>• Keep Form-XIII for labour department inspection</li>
              <li>• State-specific forms require state selection</li>
            </ul>
          </div>
        </div>
      </div>

      {/* State Selector for PT Form */}
      <Card>
        <div className="p-6">
          <h3 className="font-medium text-gray-900 mb-3">State Selection (for PT Form V)</h3>
          <select
            value={selectedState}
            onChange={(e) => setSelectedState(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            {indianStates.map(state => (
              <option key={state} value={state}>{state}</option>
            ))}
          </select>
        </div>
      </Card>

      {/* Statutory Forms Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {statutoryForms.map(form => (
          <Card key={form.id}>
            <div className={`p-6 border-l-4 ${getColorClasses(form.color)}`}>
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center">
                  <span className="text-3xl mr-3">{form.icon}</span>
                  <div>
                    <h3 className="font-semibold text-lg">{form.title}</h3>
                    <span className="text-xs px-2 py-1 bg-white rounded-full">
                      {form.format}
                    </span>
                  </div>
                </div>
              </div>

              <p className="text-sm mb-4">
                {form.description}
              </p>

              <div className="space-y-2 text-sm mb-4">
                <div className="flex justify-between">
                  <span className="text-gray-600">Deadline:</span>
                  <span className="font-medium">{form.deadline}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Period:</span>
                  <span className="font-medium">
                    {months[selectedMonth - 1]} {selectedYear}
                  </span>
                </div>
              </div>

              <Button
                onClick={() => handleDownload(form)}
                disabled={downloading[form.id]}
                className="w-full"
                variant="outline"
              >
                {downloading[form.id] ? (
                  <>
                    <span className="animate-spin mr-2">⏳</span>
                    Downloading...
                  </>
                ) : (
                  <>
                    <Download className="w-4 h-4 mr-2" />
                    Download {form.format}
                  </>
                )}
              </Button>
            </div>
          </Card>
        ))}
      </div>

      {/* Compliance Checklist */}
      <Card>
        <div className="p-6">
          <h3 className="font-semibold text-lg mb-4">Monthly Compliance Checklist</h3>

          <div className="space-y-3">
            <div className="flex items-center p-3 bg-gray-50 rounded-lg">
              <input type="checkbox" className="w-4 h-4 text-blue-600 rounded mr-3" />
              <div>
                <p className="font-medium">Process Monthly Payroll</p>
                <p className="text-sm text-gray-600">By 7th of next month</p>
              </div>
            </div>

            <div className="flex items-center p-3 bg-gray-50 rounded-lg">
              <input type="checkbox" className="w-4 h-4 text-blue-600 rounded mr-3" />
              <div>
                <p className="font-medium">Generate and Upload ESI Return</p>
                <p className="text-sm text-gray-600">By 10th of next month</p>
              </div>
            </div>

            <div className="flex items-center p-3 bg-gray-50 rounded-lg">
              <input type="checkbox" className="w-4 h-4 text-blue-600 rounded mr-3" />
              <div>
                <p className="font-medium">Generate and Upload EPF-ECR</p>
                <p className="text-sm text-gray-600">By 15th of next month</p>
              </div>
            </div>

            <div className="flex items-center p-3 bg-gray-50 rounded-lg">
              <input type="checkbox" className="w-4 h-4 text-blue-600 rounded mr-3" />
              <div>
                <p className="font-medium">Pay Professional Tax</p>
                <p className="text-sm text-gray-600">As per state rules</p>
              </div>
            </div>

            <div className="flex items-center p-3 bg-gray-50 rounded-lg">
              <input type="checkbox" className="w-4 h-4 text-blue-600 rounded mr-3" />
              <div>
                <p className="font-medium">Maintain Form-XIII Records</p>
                <p className="text-sm text-gray-600">For labour inspection</p>
              </div>
            </div>
          </div>
        </div>
      </Card>

      {/* Help Section */}
      <Card>
        <div className="p-6 bg-gray-50">
          <h3 className="font-semibold text-lg mb-3">Need Help?</h3>
          <div className="space-y-2 text-sm text-gray-700">
            <p><strong>EPF-ECR:</strong> Upload the CSV file to the EPFO portal (unifiedportal-mem.epfindia.gov.in)</p>
            <p><strong>ESI Return:</strong> Upload the CSV file to the ESIC portal (esic.nic.in)</p>
            <p><strong>PT Form V:</strong> File with your state's Professional Tax department</p>
            <p><strong>Form-XIII:</strong> Keep for records and labour department inspection</p>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default Statutory;
