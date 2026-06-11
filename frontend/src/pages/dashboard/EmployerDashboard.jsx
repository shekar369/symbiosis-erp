import { useState, useEffect } from 'react';
import {
  Users,
  Calendar,
  DollarSign,
  TrendingUp,
  Download,
  Upload,
  FileText,
  Mail,
  MapPin,
  Building2,
  AlertCircle,
  CheckCircle2,
  Clock,
} from '../../utils/icons';
import { MdPersonAdd as UserCheck, MdPersonOff as UserX, MdTableChart as FileSpreadsheet } from 'react-icons/md';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import api from '../../services/api';

const EmployerDashboard = () => {
  const [stats, setStats] = useState({
    totalEmployees: 0,
    activeEmployees: 0,
    exitedEmployees: 0,
    presentToday: 0,
    attendancePercentage: 0,
    pendingLeaves: 0,
    currentMonthPayroll: 0,
  });

  const [locations, setLocations] = useState([]);
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [recentActivities, setRecentActivities] = useState([]);

  useEffect(() => {
    fetchDashboardData();
    fetchLocations();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Fetch employee stats
      const employeesRes = await api.get('/employees/');
      const employees = employeesRes.data;

      const active = employees.filter(e => e.status === 'active').length;
      const exited = employees.filter(e => e.status === 'terminated').length;

      setStats(prev => ({
        ...prev,
        totalEmployees: employees.length,
        activeEmployees: active,
        exitedEmployees: exited,
      }));

      // Fetch live attendance stats for today
      const today = new Date();
      const month = today.getMonth() + 1;
      const yearNum = today.getFullYear();
      try {
        const attendanceRes = await api.get(
          `/reports/attendance?month=${month}&year=${yearNum}`
        );
        const records = attendanceRes.data?.records || [];
        const presentToday = records.reduce((sum, r) => sum + (r.present || 0), 0);
        const totalWithRecords = records.filter(r => r.total_recorded > 0).length;
        const pct = totalWithRecords > 0 ? Math.round((presentToday / totalWithRecords) * 100) : 0;
        setStats(prev => ({
          ...prev,
          presentToday,
          attendancePercentage: pct,
        }));
      } catch {
        // Attendance data not yet available for this period — leave defaults
      }

      // Fetch pending leave count
      try {
        const leaveRes = await api.get('/leave/requests?status=pending&limit=1');
        const pendingLeaves = leaveRes.data?.total ?? leaveRes.data?.length ?? 0;
        setStats(prev => ({ ...prev, pendingLeaves }));
      } catch {
        // Leave endpoint may not expose total — skip
      }

    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  };

  const fetchLocations = async () => {
    try {
      const res = await api.get('/locations/');
      setLocations(res.data);
      if (res.data.length > 0) {
        setSelectedLocation(res.data[0].id);
      }
    } catch (error) {
      console.error('Error fetching locations:', error);
    }
  };

  const statCards = [
    {
      title: 'Active Employees',
      value: stats.activeEmployees,
      icon: UserCheck,
      color: 'bg-green-500',
      change: `Total: ${stats.totalEmployees}`,
    },
    {
      title: 'Exited Employees',
      value: stats.exitedEmployees,
      icon: UserX,
      color: 'bg-red-500',
      change: 'This year',
    },
    {
      title: 'Present Today',
      value: stats.presentToday,
      icon: Calendar,
      color: 'bg-blue-500',
      change: `${stats.attendancePercentage}% attendance`,
    },
    {
      title: 'Pending Leaves',
      value: stats.pendingLeaves,
      icon: AlertCircle,
      color: 'bg-orange-500',
      change: 'Awaiting approval',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Employer Dashboard</h1>
          <p className="text-gray-600 mt-1">
            Welcome back! Here's your HR overview
          </p>
        </div>

        {/* Location Selector */}
        {locations.length > 0 && (
          <div className="flex items-center gap-2">
            <MapPin size={20} className="text-gray-500" />
            <select
              value={selectedLocation || ''}
              onChange={(e) => setSelectedLocation(Number(e.target.value))}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="">All Locations</option>
              {locations.map(loc => (
                <option key={loc.id} value={loc.id}>
                  {loc.name} ({loc.city})
                </option>
              ))}
            </select>
          </div>
        )}
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, index) => {
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

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

        {/* Left Column - Employee Database */}
        <div className="lg:col-span-1 space-y-6">
          <Card title="Employee Database">
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <UserCheck className="text-green-600" size={20} />
                  <span className="font-medium text-gray-900">Active Members</span>
                </div>
                <span className="text-2xl font-bold text-green-600">{stats.activeEmployees}</span>
              </div>

              <div className="flex items-center justify-between p-3 bg-red-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <UserX className="text-red-600" size={20} />
                  <span className="font-medium text-gray-900">Exited Employees</span>
                </div>
                <span className="text-2xl font-bold text-red-600">{stats.exitedEmployees}</span>
              </div>

              <div className="pt-4 border-t border-gray-200 space-y-2">
                <Button
                  variant="outline"
                  className="w-full justify-start"
                  icon={<Download size={16} />}
                >
                  Download Excel Template
                </Button>
                <Button
                  variant="outline"
                  className="w-full justify-start"
                  icon={<Upload size={16} />}
                >
                  Upload Employee Data
                </Button>
              </div>
            </div>
          </Card>

          <Card title="Quick Actions">
            <div className="space-y-2">
              <Button
                variant="outline"
                className="w-full justify-start"
                icon={<Mail size={16} />}
              >
                Send Message to All
              </Button>
              <Button
                variant="outline"
                className="w-full justify-start"
                icon={<FileText size={16} />}
              >
                View Reports
              </Button>
              <Button
                variant="outline"
                className="w-full justify-start"
                icon={<Building2 size={16} />}
              >
                Manage Locations
              </Button>
            </div>
          </Card>
        </div>

        {/* Middle Column - Payroll & Attendance */}
        <div className="lg:col-span-1 space-y-6">
          <Card title="Payroll (Monthly)">
            <div className="space-y-3">
              <QuickLink
                icon={FileText}
                label="Attendance Statement"
                href="/attendance"
              />
              <QuickLink
                icon={FileSpreadsheet}
                label="Salary Statement"
                href="/wages"
              />
              <QuickLink
                icon={Download}
                label="Bank Transfer Upload"
                badge="New"
              />
              <QuickLink
                icon={Mail}
                label="Email Payslips"
              />
              <QuickLink
                icon={FileText}
                label="Employee Salary Statement"
                href="/wages"
              />
            </div>
          </Card>

          <Card title="Excel Processing">
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Select Month & Year
                </label>
                <div className="grid grid-cols-2 gap-2">
                  <select className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500">
                    <option>January</option>
                    <option>February</option>
                    <option>March</option>
                    <option>April</option>
                    <option>May</option>
                    <option>June</option>
                    <option>July</option>
                    <option>August</option>
                    <option>September</option>
                    <option>October</option>
                    <option selected>November</option>
                    <option>December</option>
                  </select>
                  <select className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500">
                    <option>2024</option>
                    <option selected>2025</option>
                    <option>2026</option>
                  </select>
                </div>
              </div>

              <Button variant="primary" className="w-full" icon={<Upload size={16} />}>
                Upload & Auto-Process
              </Button>
            </div>
          </Card>
        </div>

        {/* Right Column - Statutory & Reports */}
        <div className="lg:col-span-1 space-y-6">
          <Card title="Statutory Registers">
            <div className="space-y-2">
              <StatutoryLink label="ECR File" />
              <StatutoryLink label="ME Template" />
              <StatutoryLink label="Form V (PT)" />
              <StatutoryLink label="ESI Returns" />
              <StatutoryLink label="TDS Returns" />
              <StatutoryLink label="PF Returns" />
              <StatutoryLink label="Bonus Calculation" />
            </div>
          </Card>

          <Card title="Reports & Analytics">
            <div className="space-y-2">
              <ReportLink label="Wage Register" status="current" />
              <ReportLink label="Payroll Summary" status="current" />
              <ReportLink label="Headcount Abstract" />
              <ReportLink label="HR Analytics" />
              <ReportLink label="Graphs & Charts" />
            </div>
          </Card>

          <Card title="Alerts">
            <div className="space-y-3">
              <AlertItem
                type="warning"
                message="5 leave requests pending approval"
              />
              <AlertItem
                type="info"
                message="Payroll processing due in 3 days"
              />
              <AlertItem
                type="success"
                message="October payroll completed"
              />
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

// Helper Components
const QuickLink = ({ icon: Icon, label, href, badge }) => (
  <a
    href={href || '#'}
    className="flex items-center justify-between p-2 rounded-lg hover:bg-gray-50 transition-colors group"
  >
    <div className="flex items-center gap-2">
      <Icon size={16} className="text-gray-500 group-hover:text-primary-600" />
      <span className="text-sm text-gray-700 group-hover:text-gray-900">{label}</span>
    </div>
    {badge && (
      <span className="px-2 py-0.5 text-xs font-medium bg-primary-100 text-primary-700 rounded-full">
        {badge}
      </span>
    )}
  </a>
);

const StatutoryLink = ({ label }) => (
  <button className="w-full flex items-center justify-between p-2 rounded-lg hover:bg-gray-50 transition-colors text-left">
    <span className="text-sm text-gray-700">{label}</span>
    <Download size={14} className="text-gray-400" />
  </button>
);

const ReportLink = ({ label, status }) => (
  <button className="w-full flex items-center justify-between p-2 rounded-lg hover:bg-gray-50 transition-colors text-left">
    <span className="text-sm text-gray-700">{label}</span>
    {status === 'current' && (
      <span className="px-2 py-0.5 text-xs font-medium bg-green-100 text-green-700 rounded-full">
        Current
      </span>
    )}
  </button>
);

const AlertItem = ({ type, message }) => {
  const config = {
    warning: { bg: 'bg-orange-50', text: 'text-orange-700', icon: AlertCircle, iconColor: 'text-orange-500' },
    info: { bg: 'bg-blue-50', text: 'text-blue-700', icon: Clock, iconColor: 'text-blue-500' },
    success: { bg: 'bg-green-50', text: 'text-green-700', icon: CheckCircle2, iconColor: 'text-green-500' },
  };

  const { bg, text, icon: Icon, iconColor } = config[type] || config.info;

  return (
    <div className={`flex items-start gap-2 p-3 rounded-lg ${bg}`}>
      <Icon size={16} className={`mt-0.5 ${iconColor}`} />
      <p className={`text-sm ${text}`}>{message}</p>
    </div>
  );
};

export default EmployerDashboard;
