import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  MdBusiness, MdPeople, MdPendingActions, MdCheckCircle,
  MdCancel, MdAttachMoney, MdOpenInNew,
} from 'react-icons/md';
import api from '../../api/axios';

const StatCard = ({ icon: Icon, label, value, sub, color }) => (
  <div className="bg-white rounded-xl shadow p-5 flex items-start gap-4">
    <div className={`p-3 rounded-lg ${color}`}>
      <Icon size={24} className="text-white" />
    </div>
    <div>
      <p className="text-sm text-gray-500">{label}</p>
      <p className="text-2xl font-bold text-gray-800">{value ?? '—'}</p>
      {sub && <p className="text-xs text-gray-400 mt-0.5">{sub}</p>}
    </div>
  </div>
);

const StatusBadge = ({ status }) => {
  const map = {
    pending:   'bg-yellow-100 text-yellow-800',
    approved:  'bg-green-100  text-green-800',
    rejected:  'bg-red-100    text-red-800',
    suspended: 'bg-gray-100   text-gray-600',
  };
  return (
    <span className={`px-2 py-0.5 rounded-full text-xs font-semibold capitalize ${map[status] ?? 'bg-gray-100 text-gray-600'}`}>
      {status}
    </span>
  );
};

export default function SaasAdminDashboard() {
  const [data, setData]       = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError]     = useState(null);

  useEffect(() => {
    api.get('/admin/saas-admin/dashboard')
      .then(r => { setData(r.data); setLoading(false); })
      .catch(e => { setError(e.response?.data?.detail || e.message); setLoading(false); });
  }, []);

  if (loading) return (
    <div className="flex items-center justify-center h-64">
      <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600" />
    </div>
  );

  if (error) return (
    <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4 m-6">
      Failed to load dashboard: {error}
    </div>
  );

  const dd   = data?.dashboard_data ?? {};
  const ts   = dd.tenant_stats     ?? {};
  const us   = dd.user_stats       ?? {};
  const rs   = dd.registration_stats ?? { pending: 0, approved: 0, rejected: 0 };
  const regs = dd.recent_registrations ?? [];

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">SaaS Admin Dashboard</h1>
          <p className="text-sm text-gray-500 mt-1">System-wide overview</p>
        </div>
        <Link
          to="/admin/registrations"
          className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
        >
          <MdPendingActions size={18} />
          Manage Registrations
          {rs.pending > 0 && (
            <span className="bg-yellow-400 text-yellow-900 text-xs font-bold px-1.5 py-0.5 rounded-full">
              {rs.pending}
            </span>
          )}
        </Link>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard icon={MdBusiness}       label="Total Tenants"    value={ts.total}              sub={`${ts.active ?? 0} active`}       color="bg-blue-500" />
        <StatCard icon={MdPeople}         label="Total Users"      value={us.total_users}         sub={`${us.by_role?.employee ?? 0} employees`} color="bg-indigo-500" />
        <StatCard icon={MdPendingActions} label="Pending Reg."     value={rs.pending}             sub="awaiting review"                  color="bg-yellow-500" />
        <StatCard icon={MdCheckCircle}    label="Approved Orgs"    value={rs.approved}            sub={`${rs.rejected ?? 0} rejected`}   color="bg-green-500" />
      </div>

      {/* Registration stats bar */}
      <div className="bg-white rounded-xl shadow p-5">
        <h2 className="text-sm font-semibold text-gray-600 uppercase tracking-wide mb-3">Registration Pipeline</h2>
        <div className="flex gap-6">
          {[
            { label: 'Pending',  value: rs.pending,  color: 'bg-yellow-400' },
            { label: 'Approved', value: rs.approved, color: 'bg-green-400' },
            { label: 'Rejected', value: rs.rejected, color: 'bg-red-400' },
          ].map(item => (
            <div key={item.label} className="flex items-center gap-2">
              <div className={`w-3 h-3 rounded-full ${item.color}`} />
              <span className="text-sm text-gray-600">{item.label}:</span>
              <span className="text-sm font-bold text-gray-800">{item.value ?? 0}</span>
            </div>
          ))}
        </div>
        {/* progress bar */}
        {(() => {
          const total = (rs.pending ?? 0) + (rs.approved ?? 0) + (rs.rejected ?? 0);
          if (!total) return null;
          return (
            <div className="mt-3 h-2 bg-gray-100 rounded-full flex overflow-hidden">
              <div className="bg-yellow-400" style={{ width: `${(rs.pending / total) * 100}%` }} />
              <div className="bg-green-400"  style={{ width: `${(rs.approved / total) * 100}%` }} />
              <div className="bg-red-400"    style={{ width: `${(rs.rejected / total) * 100}%` }} />
            </div>
          );
        })()}
      </div>

      {/* Recent Registrations */}
      <div className="bg-white rounded-xl shadow">
        <div className="flex items-center justify-between px-5 py-4 border-b border-gray-100">
          <h2 className="font-semibold text-gray-800">Recent Registrations</h2>
          <Link to="/admin/registrations" className="text-sm text-blue-600 hover:underline flex items-center gap-1">
            View all <MdOpenInNew size={14} />
          </Link>
        </div>
        {regs.length === 0 ? (
          <div className="p-8 text-center text-gray-400 text-sm">No registrations yet.</div>
        ) : (
          <div className="divide-y divide-gray-50">
            {regs.map(reg => (
              <div key={reg.id} className="px-5 py-3 flex items-center justify-between hover:bg-gray-50">
                <div>
                  <p className="font-medium text-gray-800 text-sm">{reg.name || reg.username}</p>
                  <p className="text-xs text-gray-400">{reg.email}</p>
                </div>
                <div className="flex items-center gap-3">
                  <StatusBadge status={reg.status ?? 'pending'} />
                  <Link to="/admin/registrations" className="text-xs text-blue-600 hover:underline">Review</Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* User breakdown */}
      <div className="bg-white rounded-xl shadow p-5">
        <h2 className="text-sm font-semibold text-gray-600 uppercase tracking-wide mb-4">User Breakdown by Role</h2>
        <div className="grid grid-cols-3 gap-4">
          {[
            { label: 'Employers',  value: us.by_role?.employer_admin, color: 'text-blue-600' },
            { label: 'Employees',  value: us.by_role?.employee,       color: 'text-green-600' },
            { label: 'Auditors',   value: us.by_role?.auditor,        color: 'text-orange-600' },
          ].map(item => (
            <div key={item.label} className="text-center">
              <p className={`text-3xl font-bold ${item.color}`}>{item.value ?? 0}</p>
              <p className="text-xs text-gray-500 mt-1">{item.label}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
