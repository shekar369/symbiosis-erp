import { useState, useEffect } from 'react';
import { Plus, Upload, Calendar, Download } from '../../utils/icons';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';
import Table from '../../components/common/Table';
import Modal from '../../components/common/Modal';
import { attendanceAPI } from '../../api/attendance';

const Attendance = () => {
  const [attendance, setAttendance] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
  const [isDownloadModalOpen, setIsDownloadModalOpen] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);

  const [formData, setFormData] = useState({
    employee_id: '',
    date: new Date().toISOString().split('T')[0],
    check_in: '',
    check_out: '',
    status: 'PRESENT',
  });

  const currentDate = new Date();
  const [templateMonth, setTemplateMonth] = useState(currentDate.getMonth() + 1);
  const [templateYear, setTemplateYear] = useState(currentDate.getFullYear());

  useEffect(() => {
    fetchAttendance();
  }, []);

  const fetchAttendance = async () => {
    try {
      setLoading(true);
      const data = await attendanceAPI.getAll();
      setAttendance(data);
    } catch (error) {
      console.error('Failed to fetch attendance:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await attendanceAPI.create(formData);
      setIsModalOpen(false);
      resetForm();
      fetchAttendance();
    } catch (error) {
      console.error('Failed to create attendance:', error);
      alert('Failed to create attendance record. Please try again.');
    }
  };

  const handleFileUpload = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      alert('Please select a file to upload');
      return;
    }

    try {
      await attendanceAPI.uploadFile(selectedFile);
      setIsUploadModalOpen(false);
      setSelectedFile(null);
      fetchAttendance();
      alert('Attendance file uploaded successfully');
    } catch (error) {
      console.error('Failed to upload file:', error);
      alert('Failed to upload file. Please try again.');
    }
  };

  const handleTemplateDownload = async (e) => {
    e.preventDefault();
    try {
      await attendanceAPI.downloadTemplate(templateMonth, templateYear);
      setIsDownloadModalOpen(false);
      alert('Template downloaded successfully');
    } catch (error) {
      console.error('Failed to download template:', error);
      alert('Failed to download template. Please try again.');
    }
  };

  const resetForm = () => {
    setFormData({
      employee_id: '',
      date: new Date().toISOString().split('T')[0],
      check_in: '',
      check_out: '',
      status: 'PRESENT',
    });
  };

  const columns = [
    { key: 'employee_id', label: 'Employee ID' },
    {
      key: 'date',
      label: 'Date',
      render: (date) => new Date(date).toLocaleDateString(),
    },
    { key: 'check_in', label: 'Check In' },
    { key: 'check_out', label: 'Check Out' },
    {
      key: 'status',
      label: 'Status',
      render: (status) => {
        const colors = {
          PRESENT: 'bg-green-100 text-green-800',
          ABSENT: 'bg-red-100 text-red-800',
          HALF_DAY: 'bg-yellow-100 text-yellow-800',
          LEAVE: 'bg-blue-100 text-blue-800',
        };
        return (
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${colors[status]}`}>
            {status}
          </span>
        );
      },
    },
  ];

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Attendance</h1>
        <div className="flex gap-3">
          <Button variant="outline" onClick={() => setIsDownloadModalOpen(true)}>
            <Download size={20} className="inline mr-2" />
            Download Template
          </Button>
          <Button variant="outline" onClick={() => setIsUploadModalOpen(true)}>
            <Upload size={20} className="inline mr-2" />
            Upload Excel
          </Button>
          <Button onClick={() => setIsModalOpen(true)}>
            <Plus size={20} className="inline mr-2" />
            Add Record
          </Button>
        </div>
      </div>

      <Card>
        <Table columns={columns} data={attendance} loading={loading} />
      </Card>

      <Modal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          resetForm();
        }}
        title="Add Attendance Record"
      >
        <form onSubmit={handleSubmit}>
          <Input
            label="Employee ID"
            type="number"
            name="employee_id"
            value={formData.employee_id}
            onChange={(e) => setFormData({ ...formData, employee_id: e.target.value })}
            required
          />
          <Input
            label="Date"
            type="date"
            name="date"
            value={formData.date}
            onChange={(e) => setFormData({ ...formData, date: e.target.value })}
            required
          />
          <Input
            label="Check In"
            type="time"
            name="check_in"
            value={formData.check_in}
            onChange={(e) => setFormData({ ...formData, check_in: e.target.value })}
          />
          <Input
            label="Check Out"
            type="time"
            name="check_out"
            value={formData.check_out}
            onChange={(e) => setFormData({ ...formData, check_out: e.target.value })}
          />

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Status <span className="text-red-500">*</span>
            </label>
            <select
              value={formData.status}
              onChange={(e) => setFormData({ ...formData, status: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              required
            >
              <option value="PRESENT">Present</option>
              <option value="ABSENT">Absent</option>
              <option value="HALF_DAY">Half Day</option>
              <option value="LEAVE">Leave</option>
            </select>
          </div>

          <div className="flex gap-3 mt-6">
            <Button type="submit" className="flex-1">
              Create Record
            </Button>
            <Button
              type="button"
              variant="secondary"
              onClick={() => {
                setIsModalOpen(false);
                resetForm();
              }}
            >
              Cancel
            </Button>
          </div>
        </form>
      </Modal>

      <Modal
        isOpen={isUploadModalOpen}
        onClose={() => {
          setIsUploadModalOpen(false);
          setSelectedFile(null);
        }}
        title="Upload Attendance File"
        size="sm"
      >
        <form onSubmit={handleFileUpload}>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Excel/CSV File
            </label>
            <input
              type="file"
              accept=".xlsx,.xls,.csv"
              onChange={(e) => setSelectedFile(e.target.files[0])}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
            {selectedFile && (
              <p className="mt-2 text-sm text-gray-600">
                Selected: {selectedFile.name}
              </p>
            )}
          </div>

          <div className="flex gap-3 mt-6">
            <Button type="submit" className="flex-1">
              Upload
            </Button>
            <Button
              type="button"
              variant="secondary"
              onClick={() => {
                setIsUploadModalOpen(false);
                setSelectedFile(null);
              }}
            >
              Cancel
            </Button>
          </div>
        </form>
      </Modal>

      <Modal
        isOpen={isDownloadModalOpen}
        onClose={() => setIsDownloadModalOpen(false)}
        title="Download Attendance Template"
        size="sm"
      >
        <form onSubmit={handleTemplateDownload}>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Month <span className="text-red-500">*</span>
            </label>
            <select
              value={templateMonth}
              onChange={(e) => setTemplateMonth(parseInt(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              required
            >
              <option value={1}>January</option>
              <option value={2}>February</option>
              <option value={3}>March</option>
              <option value={4}>April</option>
              <option value={5}>May</option>
              <option value={6}>June</option>
              <option value={7}>July</option>
              <option value={8}>August</option>
              <option value={9}>September</option>
              <option value={10}>October</option>
              <option value={11}>November</option>
              <option value={12}>December</option>
            </select>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Year <span className="text-red-500">*</span>
            </label>
            <input
              type="number"
              value={templateYear}
              onChange={(e) => setTemplateYear(parseInt(e.target.value))}
              min="2020"
              max="2030"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              required
            />
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-4">
            <p className="text-sm text-blue-800">
              This will download an Excel template with all employee data pre-filled for the selected month.
              Fill in the attendance codes (P, A, L, WO, H, HD) and upload it back.
            </p>
          </div>

          <div className="flex gap-3 mt-6">
            <Button type="submit" className="flex-1">
              <Download size={20} className="inline mr-2" />
              Download
            </Button>
            <Button
              type="button"
              variant="secondary"
              onClick={() => setIsDownloadModalOpen(false)}
            >
              Cancel
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default Attendance;
