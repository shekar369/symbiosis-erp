import { useState } from 'react';
import { Download, Building2, FileText, AlertCircle } from '../../utils/icons';
import api from '../../services/api';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';

const BankTransfer = () => {
  const [selectedMonth, setSelectedMonth] = useState(new Date().getMonth() + 1);
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());
  const [selectedFormat, setSelectedFormat] = useState('csv');
  const [downloading, setDownloading] = useState(false);

  const months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  const years = Array.from({ length: 5 }, (_, i) => new Date().getFullYear() - i);

  const bankFormats = [
    {
      id: 'csv',
      name: 'Standard CSV',
      description: 'Universal format compatible with any bank',
      icon: '📊',
      color: 'blue'
    },
    {
      id: 'neft',
      name: 'NEFT Format',
      description: 'Fixed-width text file for NEFT transfer',
      icon: '🏦',
      color: 'green'
    },
    {
      id: 'hdfc',
      name: 'HDFC Bank',
      description: 'HDFC Bank specific CSV format',
      icon: '🏛️',
      color: 'red'
    },
    {
      id: 'icici',
      name: 'ICICI Bank',
      description: 'ICICI Bank specific CSV format',
      icon: '🏛️',
      color: 'orange'
    },
    {
      id: 'sbi',
      name: 'SBI Bank',
      description: 'State Bank of India CSV format',
      icon: '🏛️',
      color: 'indigo'
    }
  ];

  const handleDownloadBankFile = async () => {
    try {
      setDownloading(true);

      const response = await api.get('/payroll/bank-transfer-file', {
        params: {
          month: selectedMonth,
          year: selectedYear,
          format: selectedFormat
        },
        responseType: 'blob'
      });

      const extension = selectedFormat === 'neft' ? 'txt' : 'csv';
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `salary_transfer_${selectedFormat}_${selectedMonth}_${selectedYear}.${extension}`);
      document.body.appendChild(link);
      link.click();
      link.remove();

      alert('Bank transfer file downloaded successfully!');
    } catch (error) {
      console.error('Error downloading bank file:', error);
      alert('Failed to download bank file: ' + (error.response?.data?.detail || error.message));
    } finally {
      setDownloading(false);
    }
  };

  const handleDownloadPaymentSummary = async () => {
    try {
      setDownloading(true);

      const response = await api.get('/payroll/payment-summary', {
        params: {
          month: selectedMonth,
          year: selectedYear
        },
        responseType: 'blob'
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `payment_summary_${selectedMonth}_${selectedYear}.txt`);
      document.body.appendChild(link);
      link.click();
      link.remove();

      alert('Payment summary downloaded successfully!');
    } catch (error) {
      console.error('Error downloading payment summary:', error);
      alert('Failed to download payment summary');
    } finally {
      setDownloading(false);
    }
  };

  const getColorClasses = (color) => {
    const colors = {
      blue: 'border-blue-500 hover:bg-blue-50',
      green: 'border-green-500 hover:bg-green-50',
      red: 'border-red-500 hover:bg-red-50',
      orange: 'border-orange-500 hover:bg-orange-50',
      indigo: 'border-indigo-500 hover:bg-indigo-50'
    };
    return colors[color] || colors.blue;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Bank Transfer Files</h1>
          <p className="text-gray-600">Generate bank files for salary payment</p>
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
            <h3 className="font-medium text-blue-900 mb-1">Important</h3>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>• Only approved and paid wage statements are included</li>
              <li>• Verify all bank account details before upload</li>
              <li>• Choose the format matching your bank's requirement</li>
              <li>• Download payment summary for reconciliation</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Bank Format Selection */}
      <div>
        <h2 className="text-lg font-semibold mb-4">Select Bank Format</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {bankFormats.map(format => (
            <button
              key={format.id}
              onClick={() => setSelectedFormat(format.id)}
              className={`p-4 border-2 rounded-lg transition-all ${
                selectedFormat === format.id
                  ? `${getColorClasses(format.color)} border-opacity-100`
                  : 'border-gray-200 hover:border-gray-300'
              }`}
            >
              <div className="flex items-start">
                <span className="text-3xl mr-3">{format.icon}</span>
                <div className="text-left">
                  <h3 className="font-semibold">{format.name}</h3>
                  <p className="text-sm text-gray-600">{format.description}</p>
                </div>
              </div>
              {selectedFormat === format.id && (
                <div className="mt-3 flex justify-end">
                  <span className="text-sm px-2 py-1 bg-blue-100 text-blue-800 rounded-full">
                    Selected
                  </span>
                </div>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Download Actions */}
      <div className="grid grid-cols-2 gap-6">
        {/* Bank File Card */}
        <Card>
          <div className="p-6">
            <div className="flex items-center mb-4">
              <Building2 className="w-6 h-6 text-blue-600 mr-3" />
              <h3 className="font-semibold text-lg">Bank Transfer File</h3>
            </div>

            <p className="text-sm text-gray-600 mb-6">
              Download salary transfer file in {bankFormats.find(f => f.id === selectedFormat)?.name} format
            </p>

            <div className="space-y-3">
              <div className="bg-gray-50 p-3 rounded-lg text-sm">
                <div className="flex justify-between mb-1">
                  <span className="text-gray-600">Period:</span>
                  <span className="font-medium">{months[selectedMonth - 1]} {selectedYear}</span>
                </div>
                <div className="flex justify-between mb-1">
                  <span className="text-gray-600">Format:</span>
                  <span className="font-medium">{bankFormats.find(f => f.id === selectedFormat)?.name}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Type:</span>
                  <span className="font-medium">{selectedFormat === 'neft' ? 'TXT' : 'CSV'}</span>
                </div>
              </div>

              <Button
                onClick={handleDownloadBankFile}
                disabled={downloading}
                className="w-full"
              >
                {downloading ? (
                  <>
                    <span className="animate-spin mr-2">⏳</span>
                    Downloading...
                  </>
                ) : (
                  <>
                    <Download className="w-4 h-4 mr-2" />
                    Download Bank File
                  </>
                )}
              </Button>
            </div>
          </div>
        </Card>

        {/* Payment Summary Card */}
        <Card>
          <div className="p-6">
            <div className="flex items-center mb-4">
              <FileText className="w-6 h-6 text-green-600 mr-3" />
              <h3 className="font-semibold text-lg">Payment Summary</h3>
            </div>

            <p className="text-sm text-gray-600 mb-6">
              Download detailed payment summary with bank-wise breakdown
            </p>

            <div className="space-y-3">
              <div className="bg-gray-50 p-3 rounded-lg text-sm">
                <p className="font-medium mb-2">Summary includes:</p>
                <ul className="space-y-1 text-gray-600">
                  <li>• Total employees and amount</li>
                  <li>• Bank-wise breakdown</li>
                  <li>• Employee-wise listing</li>
                  <li>• Authorized signatory section</li>
                </ul>
              </div>

              <Button
                onClick={handleDownloadPaymentSummary}
                disabled={downloading}
                className="w-full"
                variant="outline"
              >
                {downloading ? (
                  <>
                    <span className="animate-spin mr-2">⏳</span>
                    Downloading...
                  </>
                ) : (
                  <>
                    <Download className="w-4 h-4 mr-2" />
                    Download Summary
                  </>
                )}
              </Button>
            </div>
          </div>
        </Card>
      </div>

      {/* Instructions */}
      <Card>
        <div className="p-6">
          <h3 className="font-semibold text-lg mb-4">Bank Upload Instructions</h3>

          <div className="space-y-4">
            <div>
              <h4 className="font-medium mb-2">Standard CSV Format</h4>
              <p className="text-sm text-gray-600">
                Universal format with columns: Employee Code, Name, Account Number, IFSC, Amount.
                Can be used for manual verification or bank portals accepting standard format.
              </p>
            </div>

            <div>
              <h4 className="font-medium mb-2">NEFT Format</h4>
              <p className="text-sm text-gray-600">
                Fixed-width text file with Header, Detail, and Trailer records.
                Upload to NEFT-enabled bank portals for direct processing.
              </p>
            </div>

            <div>
              <h4 className="font-medium mb-2">Bank-Specific Formats</h4>
              <p className="text-sm text-gray-600">
                Pre-formatted files matching HDFC, ICICI, and SBI requirements.
                Upload directly to respective bank salary payment portals.
              </p>
            </div>
          </div>
        </div>
      </Card>

      {/* Workflow Steps */}
      <Card>
        <div className="p-6 bg-gray-50">
          <h3 className="font-semibold text-lg mb-4">Payment Workflow</h3>

          <div className="space-y-3">
            <div className="flex items-center">
              <span className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center mr-3 font-semibold">
                1
              </span>
              <p className="text-sm">Download bank file in your bank's format</p>
            </div>

            <div className="flex items-center">
              <span className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center mr-3 font-semibold">
                2
              </span>
              <p className="text-sm">Verify data and amounts in the file</p>
            </div>

            <div className="flex items-center">
              <span className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center mr-3 font-semibold">
                3
              </span>
              <p className="text-sm">Log in to your bank's salary payment portal</p>
            </div>

            <div className="flex items-center">
              <span className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center mr-3 font-semibold">
                4
              </span>
              <p className="text-sm">Upload the file and process payment</p>
            </div>

            <div className="flex items-center">
              <span className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center mr-3 font-semibold">
                5
              </span>
              <p className="text-sm">Download payment summary for records</p>
            </div>

            <div className="flex items-center">
              <span className="w-8 h-8 bg-green-600 text-white rounded-full flex items-center justify-center mr-3 font-semibold">
                6
              </span>
              <p className="text-sm">Mark wage statements as "Paid" in Payroll section</p>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default BankTransfer;
