import { useState } from 'react';
import Modal from '../../components/common/Modal';
import FileUpload from '../../components/common/FileUpload';
import Button from '../../components/common/Button';
import { Download } from '../../utils/icons';
import api from '../../services/api';

const UploadModal = ({ isOpen, onClose, uploadType, onSuccess }) => {
  const [downloading, setDownloading] = useState(false);

  const getConfig = () => {
    switch (uploadType) {
      case 'employees':
        return {
          title: 'Upload Employee Data',
          endpoint: '/uploads/employees',
          templateEndpoint: '/templates/employee-database?act_type=contract_labour',
          instructions: [
            'Download the Excel template using the button below',
            'Fill in employee details following the sample data format',
            'All fields marked with * are mandatory',
            'Use DD/MM/YYYY format for dates',
            'Upload the completed file',
          ],
        };
      case 'attendance':
        return {
          title: 'Upload Attendance Data',
          endpoint: '/uploads/attendance',
          templateEndpoint: `/templates/attendance?month=11&year=2025`,
          instructions: [
            'Download the attendance template',
            'Fill in attendance records for each employee',
            'Use DD/MM/YYYY format for dates',
            'Use HH:MM format for check-in and check-out times',
            'Upload the completed file',
          ],
        };
      default:
        return null;
    }
  };

  const config = getConfig();
  if (!config) return null;

  const handleDownloadTemplate = async () => {
    try {
      setDownloading(true);
      const response = await api.get(config.templateEndpoint, {
        responseType: 'blob',
      });

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute(
        'download',
        `${uploadType}_template_${new Date().toISOString().split('T')[0]}.xlsx`
      );
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error downloading template:', error);
      alert('Error downloading template');
    } finally {
      setDownloading(false);
    }
  };

  const handleUploadSuccess = (result) => {
    if (onSuccess) {
      onSuccess(result);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={config.title} size="lg">
      <div className="space-y-6">
        {/* Instructions */}
        <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
          <p className="font-medium text-blue-900 mb-2">Instructions:</p>
          <ol className="list-decimal list-inside space-y-1 text-sm text-blue-800">
            {config.instructions.map((instruction, idx) => (
              <li key={idx}>{instruction}</li>
            ))}
          </ol>
        </div>

        {/* Download Template Button */}
        <div>
          <Button
            variant="outline"
            onClick={handleDownloadTemplate}
            disabled={downloading}
            icon={<Download size={16} />}
            className="w-full"
          >
            {downloading ? 'Downloading...' : 'Download Excel Template'}
          </Button>
        </div>

        {/* File Upload Component */}
        <div>
          <FileUpload
            endpoint={config.endpoint}
            acceptedFormats=".xlsx,.xls"
            onSuccess={handleUploadSuccess}
          />
        </div>

        {/* Close Button */}
        <div className="flex justify-end pt-4 border-t border-gray-200">
          <Button variant="outline" onClick={onClose}>
            Close
          </Button>
        </div>
      </div>
    </Modal>
  );
};

export default UploadModal;
