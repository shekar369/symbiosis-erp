import { Users, Calendar, DollarSign, TrendingUp } from '../../utils/icons';
import Card from '../../components/common/Card';

const Dashboard = () => {
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
