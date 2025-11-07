import { useState } from 'react';
import { Users, Calendar, DollarSign, TrendingUp, Download } from '../../utils/icons';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Modal from '../../components/common/Modal';
import { attendanceAPI } from '../../api/attendance';
import { employeesAPI } from '../../api/employees';

const Dashboard = () => {
  const [isAttendanceModalOpen, setIsAttendanceModalOpen] = useState(false);
  const currentDate = new Date();
  const [templateMonth, setTemplateMonth] = useState(currentDate.getMonth() + 1);
  const [templateYear, setTemplateYear] = useState(currentDate.getFullYear());

  const handleAttendanceTemplateDownload = async (e) => {
    e.preventDefault();
    try {
      await attendanceAPI.downloadTemplate(templateMonth, templateYear);
      setIsAttendanceModalOpen(false);
      alert('Attendance template downloaded successfully');
    } catch (error) {
      console.error('Failed to download attendance template:', error);
      alert('Failed to download attendance template. Please try again.');
    }
  };

  const handleEmployeeTemplateDownload = async () => {
    try {
      await employeesAPI.downloadTemplate();
      alert('Employee template downloaded successfully');
    } catch (error) {
      console.error('Failed to download employee template:', error);
      alert('Failed to download employee template. Please try again.');
    }
  };

  const stats = [
    {
      title: 'Total Employees',
      value: '150',
      icon: Users,
      color: 'bg-blue-500',
      change: '+5 this month',
    },
    {
      title: 'Present Today',
      value: '142',
      icon: Calendar,
      color: 'bg-green-500',
      change: '94.7% attendance',
    },
    {
      title: 'Payroll This Month',
      value: '$125,000',
      icon: DollarSign,
      color: 'bg-purple-500',
      change: '+8% from last month',
    },
    {
      title: 'Leave Requests',
      value: '12',
      icon: TrendingUp,
      color: 'bg-orange-500',
      change: '5 pending approval',
    },
  ];

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <Card key={index}>
              <div className="flex items-center">
                <div className={`${stat.color} p-3 rounded-lg`}>
                  <Icon size={24} className="text-white" />
                </div>
                <div className="ml-4 flex-1">
                  <p className="text-sm text-gray-600">{stat.title}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                  <p className="text-xs text-gray-500 mt-1">{stat.change}</p>
                </div>
              </div>
            </Card>
          );
        })}
      </div>

      <Card title="Download Templates" className="mb-6">
        <p className="text-sm text-gray-600 mb-4">
          Download templates to bulk upload employee and attendance data
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="border border-gray-200 rounded-lg p-4">
            <h3 className="font-semibold text-gray-900 mb-2">Employee Template</h3>
            <p className="text-sm text-gray-600 mb-3">
              Download Excel template for bulk employee data upload. Includes all required fields.
            </p>
            <Button
              variant="outline"
              onClick={handleEmployeeTemplateDownload}
              className="w-full"
            >
              <Download size={18} className="inline mr-2" />
              Download Employee Template
            </Button>
          </div>

          <div className="border border-gray-200 rounded-lg p-4">
            <h3 className="font-semibold text-gray-900 mb-2">Attendance Template</h3>
            <p className="text-sm text-gray-600 mb-3">
              Download Excel template for monthly attendance data. Pre-filled with employee list.
            </p>
            <Button
              variant="outline"
              onClick={() => setIsAttendanceModalOpen(true)}
              className="w-full"
            >
              <Download size={18} className="inline mr-2" />
              Download Attendance Template
            </Button>
          </div>
        </div>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card title="Recent Activity">
          <div className="space-y-4">
            <ActivityItem
              title="New employee onboarded"
              description="John Doe joined as Software Engineer"
              time="2 hours ago"
            />
            <ActivityItem
              title="Payroll processed"
              description="Monthly payroll for October completed"
              time="1 day ago"
            />
            <ActivityItem
              title="Leave approved"
              description="Sarah Smith's leave request approved"
              time="2 days ago"
            />
          </div>
        </Card>

        <Card title="Upcoming Events">
          <div className="space-y-4">
            <EventItem
              title="Holiday - Diwali"
              date="Nov 1, 2025"
              type="holiday"
            />
            <EventItem
              title="Payroll Processing"
              date="Nov 30, 2025"
              type="payroll"
            />
            <EventItem
              title="Performance Reviews"
              date="Dec 15, 2025"
              type="review"
            />
          </div>
        </Card>
      </div>

      <Modal
        isOpen={isAttendanceModalOpen}
        onClose={() => setIsAttendanceModalOpen(false)}
        title="Download Attendance Template"
        size="sm"
      >
        <form onSubmit={handleAttendanceTemplateDownload}>
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

          <div className="flex gap-3 mt-6">
            <Button type="submit" className="flex-1">
              <Download size={18} className="inline mr-2" />
              Download
            </Button>
            <Button
              type="button"
              variant="secondary"
              onClick={() => setIsAttendanceModalOpen(false)}
            >
              Cancel
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

const ActivityItem = ({ title, description, time }) => (
  <div className="flex items-start gap-3 pb-3 border-b border-gray-100 last:border-0">
    <div className="w-2 h-2 bg-primary-600 rounded-full mt-2"></div>
    <div className="flex-1">
      <p className="font-medium text-gray-900">{title}</p>
      <p className="text-sm text-gray-600">{description}</p>
      <p className="text-xs text-gray-400 mt-1">{time}</p>
    </div>
  </div>
);

const EventItem = ({ title, date, type }) => {
  const colors = {
    holiday: 'bg-red-100 text-red-800',
    payroll: 'bg-green-100 text-green-800',
    review: 'bg-blue-100 text-blue-800',
  };

  return (
    <div className="flex items-center justify-between pb-3 border-b border-gray-100 last:border-0">
      <div>
        <p className="font-medium text-gray-900">{title}</p>
        <p className="text-sm text-gray-600">{date}</p>
      </div>
      <span className={`px-3 py-1 rounded-full text-xs font-medium ${colors[type]}`}>
        {type}
      </span>
    </div>
  );
};

export default Dashboard;
