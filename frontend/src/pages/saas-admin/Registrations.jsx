import { useState, useEffect, useCallback } from 'react';
import {
  MdSearch, MdFilterList, MdRefresh, MdCheckCircle, MdCancel,
  MdBusiness, MdPerson, MdPhone, MdEmail, MdLocationOn,
  MdPeople, MdWeb, MdNotes, MdClose, MdHourglassEmpty,
  MdBlock,
} from 'react-icons/md';
import api from '../../api/axios';

/* ── helpers ──────────────────────────────────────────────────────────────── */
const STATUS_OPTIONS = ['all', 'pending', 'approved', 'rejected', 'suspended'];

const StatusBadge = ({ status }) => {
  const map = {
    pending:   { cls: 'bg-yellow-100 text-yellow-800', icon: MdHourglassEmpty },
    approved:  { cls: 'bg-green-100  text-green-800',  icon: MdCheckCircle },
    rejected:  { cls: 'bg-red-100    text-red-800',    icon: MdCancel },
    suspended: { cls: 'bg-gray-200   text-gray-700',   icon: MdBlock },
  };
  const { cls, icon: Icon } = map[status] ?? { cls: 'bg-gray-100 text-gray-600', icon: MdBusiness };
  return (
    <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold capitalize ${cls}`}>
      <Icon size={12} />
      {status}
    </span>
  );
};

const Field = ({ icon: Icon, label, value }) => (
  <div className="flex items-start gap-2">
    <Icon size={16} className="text-gray-400 mt-0.5 shrink-0" />
    <div>
      <p className="text-xs text-gray-400">{label}</p>
      <p className="text-sm text-gray-800 font-medium">{value || '—'}</p>
    </div>
  </div>
);

/* ── Detail Modal ─────────────────────────────────────────────────────────── */
function RegistrationModal({ reg, onClose, onReviewed }) {
  const [reviewNotes, setReviewNotes] = useState('');
  const [loading, setLoading]         = useState(false);
  const [error, setError]             = useState(null);

  const submit = async (status) => {
    setLoading(true);
    setError(null);
    try {
      await api.put(`/registration/registrations/${reg.id}/review`, {
        status,
        review_notes: reviewNotes || `${status.charAt(0).toUpperCase() + status.slice(1)} by SaaS Admin`,
      });
      onReviewed(reg.id, status);
      onClose();
    } catch (e) {
      setError(e.response?.data?.detail || 'Action failed');
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100">
          <div>
            <h2 className="text-lg font-bold text-gray-900">{reg.name}</h2>
            <p className="text-xs text-gray-400">Registration #{reg.id} · submitted {new Date(reg.created_at).toLocaleDateString()}</p>
          </div>
          <div className="flex items-center gap-3">
            <StatusBadge status={reg.status} />
            <button onClick={onClose} className="text-gray-400 hover:text-gray-700">
              <MdClose size={22} />
            </button>
          </div>
        </div>

        {/* Body */}
        <div className="p-6 grid grid-cols-2 gap-5">
          <Field icon={MdBusiness}  label="Organisation Name"    value={reg.name} />
          <Field icon={MdBusiness}  label="Business Type"        value={reg.business_type} />
          <Field icon={MdPerson}    label="Contact Person"       value={reg.contact_person} />
          <Field icon={MdEmail}     label="Email"                value={reg.email} />
          <Field icon={MdPhone}     label="Phone"                value={reg.phone} />
          <Field icon={MdPeople}    label="Employee Count"       value={reg.employee_count} />
          <Field icon={MdBusiness}  label="Registration Number"  value={reg.registration_number} />
          <Field icon={MdBusiness}  label="Tax ID / GST"         value={reg.tax_id} />
          <div className="col-span-2">
            <Field icon={MdLocationOn} label="Address" value={reg.address} />
          </div>
          {reg.website && (
            <div className="col-span-2">
              <Field icon={MdWeb} label="Website" value={reg.website} />
            </div>
          )}
          {reg.notes && (
            <div className="col-span-2">
              <Field icon={MdNotes} label="Applicant Notes" value={reg.notes} />
            </div>
          )}
        </div>

        {/* Review history */}
        {reg.reviewed_at && (
          <div className="mx-6 mb-4 bg-gray-50 rounded-lg p-4 text-sm space-y-1">
            <p className="font-semibold text-gray-600 text-xs uppercase tracking-wide">Review Record</p>
            <p className="text-gray-700">Reviewed: {new Date(reg.reviewed_at).toLocaleString()}</p>
            {reg.review_notes && <p className="text-gray-500 italic">"{reg.review_notes}"</p>}
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="mx-6 mb-4 bg-red-50 border border-red-200 text-red-700 rounded-lg p-3 text-sm">
            {error}
          </div>
        )}

        {/* Action footer — only for pending */}
        {reg.status === 'pending' && (
          <div className="px-6 pb-6">
            <label className="block text-sm font-medium text-gray-700 mb-1">Review Notes (optional)</label>
            <textarea
              value={reviewNotes}
              onChange={e => setReviewNotes(e.target.value)}
              rows={3}
              placeholder="Add notes for this decision..."
              className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            />
            <div className="flex gap-3 mt-4 justify-end">
              <button
                onClick={() => submit('rejected')}
                disabled={loading}
                className="flex items-center gap-2 px-5 py-2 rounded-lg border border-red-300 text-red-600 hover:bg-red-50 text-sm font-medium transition-colors disabled:opacity-50"
              >
                <MdCancel size={18} />
                Reject
              </button>
              <button
                onClick={() => submit('approved')}
                disabled={loading}
                className="flex items-center gap-2 px-5 py-2 rounded-lg bg-green-600 hover:bg-green-700 text-white text-sm font-medium transition-colors disabled:opacity-50"
              >
                <MdCheckCircle size={18} />
                {loading ? 'Processing…' : 'Approve'}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

/* ── Main Page ────────────────────────────────────────────────────────────── */
export default function Registrations() {
  const [registrations, setRegistrations] = useState([]);
  const [stats, setStats]                 = useState(null);
  const [loading, setLoading]             = useState(true);
  const [error, setError]                 = useState(null);
  const [filterStatus, setFilterStatus]   = useState('all');
  const [search, setSearch]               = useState('');
  const [selected, setSelected]           = useState(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [regsRes, statsRes] = await Promise.all([
        api.get('/registration/registrations', { params: { limit: 100 } }),
        api.get('/registration/registrations/stats'),
      ]);
      setRegistrations(regsRes.data);
      setStats(statsRes.data?.counts ?? null);
    } catch (e) {
      setError(e.response?.data?.detail || e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchData(); }, [fetchData]);

  const handleReviewed = (id, newStatus) => {
    setRegistrations(prev =>
      prev.map(r => r.id === id ? { ...r, status: newStatus, reviewed_at: new Date().toISOString() } : r)
    );
  };

  /* filter + search */
  const displayed = registrations.filter(r => {
    const matchStatus = filterStatus === 'all' || r.status === filterStatus;
    const q = search.toLowerCase();
    const matchSearch = !q ||
      r.name?.toLowerCase().includes(q) ||
      r.email?.toLowerCase().includes(q) ||
      r.contact_person?.toLowerCase().includes(q) ||
      r.business_type?.toLowerCase().includes(q);
    return matchStatus && matchSearch;
  });

  const statCards = [
    { label: 'Total',     key: 'pending',   extra: true,  color: 'bg-gray-100 text-gray-700' },
    { label: 'Pending',   key: 'pending',                 color: 'bg-yellow-100 text-yellow-700' },
    { label: 'Approved',  key: 'approved',                color: 'bg-green-100 text-green-700' },
    { label: 'Rejected',  key: 'rejected',                color: 'bg-red-100 text-red-700' },
  ];

  const totalCount = stats
    ? Object.values(stats).reduce((a, b) => a + b, 0)
    : registrations.length;

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Organisation Registrations</h1>
          <p className="text-sm text-gray-500 mt-1">Review and approve new organisation registration requests</p>
        </div>
        <button
          onClick={fetchData}
          className="flex items-center gap-2 border border-gray-200 text-gray-600 hover:bg-gray-50 px-3 py-2 rounded-lg text-sm transition-colors"
        >
          <MdRefresh size={18} /> Refresh
        </button>
      </div>

      {/* Stats strip */}
      {stats && (
        <div className="grid grid-cols-4 gap-3">
          <div className="bg-white rounded-xl shadow p-4 text-center">
            <p className="text-2xl font-bold text-gray-800">{totalCount}</p>
            <p className="text-xs text-gray-400 mt-1">Total</p>
          </div>
          {[
            { label: 'Pending',   val: stats.pending,   color: 'text-yellow-600' },
            { label: 'Approved',  val: stats.approved,  color: 'text-green-600' },
            { label: 'Rejected',  val: stats.rejected,  color: 'text-red-600' },
          ].map(s => (
            <div key={s.label} className="bg-white rounded-xl shadow p-4 text-center cursor-pointer hover:ring-2 hover:ring-blue-200 transition"
              onClick={() => setFilterStatus(s.label.toLowerCase())}>
              <p className={`text-2xl font-bold ${s.color}`}>{s.val ?? 0}</p>
              <p className="text-xs text-gray-400 mt-1">{s.label}</p>
            </div>
          ))}
        </div>
      )}

      {/* Filters */}
      <div className="bg-white rounded-xl shadow p-4 flex flex-col sm:flex-row gap-3">
        <div className="relative flex-1">
          <MdSearch size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            placeholder="Search by name, email, contact person…"
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="w-full pl-9 pr-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div className="flex items-center gap-2">
          <MdFilterList size={18} className="text-gray-400" />
          <div className="flex gap-1">
            {STATUS_OPTIONS.map(s => (
              <button
                key={s}
                onClick={() => setFilterStatus(s)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium capitalize transition-colors ${
                  filterStatus === s
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {s}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4 text-sm">{error}</div>
      )}

      {/* Table */}
      {loading ? (
        <div className="flex items-center justify-center h-48">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600" />
        </div>
      ) : displayed.length === 0 ? (
        <div className="bg-white rounded-xl shadow p-12 text-center text-gray-400">
          <MdBusiness size={40} className="mx-auto mb-3 opacity-30" />
          <p className="text-sm">No registrations found{search ? ` for "${search}"` : ''}.</p>
        </div>
      ) : (
        <div className="bg-white rounded-xl shadow overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-gray-50 border-b border-gray-100">
                  <th className="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase">#</th>
                  <th className="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Organisation</th>
                  <th className="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Contact</th>
                  <th className="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Business Type</th>
                  <th className="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Employees</th>
                  <th className="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Submitted</th>
                  <th className="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Status</th>
                  <th className="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {displayed.map(reg => (
                  <tr key={reg.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-5 py-3 text-gray-400 text-xs">{reg.id}</td>
                    <td className="px-5 py-3">
                      <p className="font-semibold text-gray-800">{reg.name}</p>
                      <p className="text-xs text-gray-400">{reg.email}</p>
                    </td>
                    <td className="px-5 py-3">
                      <p className="text-gray-700">{reg.contact_person}</p>
                      <p className="text-xs text-gray-400">{reg.phone}</p>
                    </td>
                    <td className="px-5 py-3 text-gray-600">{reg.business_type}</td>
                    <td className="px-5 py-3 text-gray-600 text-center">{reg.employee_count}</td>
                    <td className="px-5 py-3 text-gray-400 text-xs whitespace-nowrap">
                      {new Date(reg.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-5 py-3"><StatusBadge status={reg.status} /></td>
                    <td className="px-5 py-3">
                      {reg.status === 'pending' ? (
                        <button
                          onClick={() => setSelected(reg)}
                          className="text-xs bg-blue-600 hover:bg-blue-700 text-white px-3 py-1.5 rounded-lg font-medium transition-colors"
                        >
                          Review
                        </button>
                      ) : (
                        <button
                          onClick={() => setSelected(reg)}
                          className="text-xs border border-gray-200 hover:bg-gray-50 text-gray-600 px-3 py-1.5 rounded-lg transition-colors"
                        >
                          View
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="px-5 py-3 bg-gray-50 border-t border-gray-100 text-xs text-gray-400">
            Showing {displayed.length} of {registrations.length} registrations
          </div>
        </div>
      )}

      {/* Detail modal */}
      {selected && (
        <RegistrationModal
          reg={selected}
          onClose={() => setSelected(null)}
          onReviewed={handleReviewed}
        />
      )}
    </div>
  );
}
