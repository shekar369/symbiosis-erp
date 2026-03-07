import { Link, useLocation } from 'react-router-dom';
import {
  MdDashboard as LayoutDashboard,
  MdPeople as Users,
  MdCalendarToday as Calendar,
  MdAttachMoney as DollarSign,
  MdDescription as FileText,
  MdBeachAccess as Umbrella,
  MdSettings as Settings,
  MdLogout as LogOut,
  MdLocationOn as MapPin,
  MdCalculate as Calculator,
  MdBusiness as Building2,
  MdFactCheck as FileCheck,
  MdPerson as User,
  MdReceipt as Receipt,
  MdDateRange as CalendarDays,
  MdAccountCircle as UserCircle,
  MdSettings as Cog,
  MdAdminPanelSettings as ShieldCheck,
  MdAppRegistration as ClipboardList,
} from 'react-icons/md';
import { useAuth } from '../../contexts/AuthContext';

const Sidebar = () => {
  const location = useLocation();
  const { logout, user } = useAuth();

  const employerMenuItems = [
    { path: '/dashboard',          icon: LayoutDashboard, label: 'Dashboard' },
    { path: '/employees',          icon: Users,           label: 'Employees' },
    { path: '/locations',          icon: MapPin,          label: 'Locations' },
    { path: '/attendance',         icon: Calendar,        label: 'Attendance' },
    { path: '/holidays',           icon: CalendarDays,    label: 'Holiday Calendar' },
    { path: '/payroll',            icon: Calculator,      label: 'Payroll' },
    { path: '/bank-transfer',      icon: Building2,       label: 'Bank Transfer' },
    { path: '/statutory',          icon: FileCheck,       label: 'Statutory' },
    { path: '/wages',              icon: DollarSign,      label: 'Wages' },
    { path: '/leaves',             icon: Umbrella,        label: 'Leaves' },
    { path: '/reports',            icon: FileText,        label: 'Reports' },
  ];

  const employeeMenuItems = [
    { path: '/employee/dashboard', icon: User,            label: 'My Dashboard' },
    { path: '/employee/payslips',  icon: Receipt,         label: 'My Payslips' },
    { path: '/employee/leave',     icon: CalendarDays,    label: 'My Leaves' },
    { path: '/employee/profile',   icon: UserCircle,      label: 'My Profile' },
  ];

  const saasAdminMenuItems = [
    { path: '/admin/dashboard',      icon: ShieldCheck,   label: 'Admin Dashboard' },
    { path: '/admin/registrations',  icon: ClipboardList, label: 'Registrations' },
    { path: '/admin/config',         icon: Cog,           label: 'System Config' },
  ];

  const isActive = (path) => location.pathname === path;

  const NavItem = ({ item }) => {
    const Icon = item.icon;
    return (
      <li>
        <Link
          to={item.path}
          className={`
            flex items-center gap-3 px-4 py-3 rounded-lg transition-colors
            ${isActive(item.path)
              ? 'bg-blue-600 text-white'
              : 'text-gray-300 hover:bg-gray-800 hover:text-white'
            }
          `}
        >
          <Icon size={20} />
          <span>{item.label}</span>
        </Link>
      </li>
    );
  };

  const isSaasAdmin = user?.role === 'admin' || user?.role === 'saas_admin';
  const isEmployer  = user?.role === 'employer' || user?.role === 'employer_admin' || user?.role === 'hr_manager';
  const isEmployee  = user?.role === 'employee';

  return (
    <div className="h-screen w-64 bg-gray-900 text-white fixed left-0 top-0 flex flex-col">
      <div className="p-6 border-b border-gray-700">
        <h1 className="text-xl font-bold">HR Payroll</h1>
        <p className="text-xs text-gray-400 mt-1">
          {isSaasAdmin ? 'System Administration' : isEmployee ? 'Employee Portal' : 'Management System'}
        </p>
      </div>

      <nav className="flex-1 px-4 py-6 overflow-y-auto">

        {/* SaaS Admin Section */}
        {isSaasAdmin && (
          <div className="mb-6">
            <h3 className="text-xs font-semibold text-gray-400 uppercase mb-2 px-4">SaaS Admin</h3>
            <ul className="space-y-1">
              {saasAdminMenuItems.map(item => <NavItem key={item.path} item={item} />)}
            </ul>
            <div className="border-t border-gray-700 mt-4 pt-4">
              <h3 className="text-xs font-semibold text-gray-400 uppercase mb-2 px-4">Employer View</h3>
              <ul className="space-y-1">
                {employerMenuItems.map(item => <NavItem key={item.path} item={item} />)}
              </ul>
            </div>
          </div>
        )}

        {/* Employer / HR Section */}
        {isEmployer && (
          <div className="mb-6">
            <h3 className="text-xs font-semibold text-gray-400 uppercase mb-2 px-4">
              {user?.role === 'hr_manager' ? 'HR Management' : 'Employer'}
            </h3>
            <ul className="space-y-1">
              {employerMenuItems.map(item => <NavItem key={item.path} item={item} />)}
            </ul>
          </div>
        )}

        {/* Employee Section */}
        {isEmployee && (
          <div>
            <h3 className="text-xs font-semibold text-gray-400 uppercase mb-2 px-4">Employee Self-Service</h3>
            <ul className="space-y-1">
              {employeeMenuItems.map(item => <NavItem key={item.path} item={item} />)}
            </ul>
          </div>
        )}
      </nav>

      <div className="p-4 border-t border-gray-700">
        <div className="px-4 mb-3">
          <p className="text-xs text-gray-500">Logged in as</p>
          <p className="text-sm font-medium text-gray-200">{user?.username}</p>
          <p className="text-xs text-gray-500 capitalize">{user?.role}</p>
        </div>
        <button
          onClick={logout}
          className="flex items-center gap-3 px-4 py-3 w-full rounded-lg text-gray-300 hover:bg-gray-800 hover:text-white transition-colors"
        >
          <LogOut size={20} />
          <span>Logout</span>
        </button>
      </div>
    </div>
  );
};

export default Sidebar;
