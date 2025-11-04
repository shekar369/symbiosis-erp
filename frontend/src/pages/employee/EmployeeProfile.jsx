import React, { useState, useEffect } from 'react';
import {
  User,
  Mail,
  Phone,
  MapPin,
  Calendar,
  CreditCard,
  Save,
  Edit,
  CheckCircle,
  Building
} from '../../utils/icons';
import { MdWork as Briefcase, MdClose as X } from 'react-icons/md';
import api from '../../services/api';

const EmployeeProfile = () => {
  const [employeeData, setEmployeeData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [saving, setSaving] = useState(false);
  const [formData, setFormData] = useState({});

  useEffect(() => {
    fetchEmployeeData();
  }, []);

  const fetchEmployeeData = async () => {
    try {
      setLoading(true);
      const response = await api.get('/employees/me');
      setEmployeeData(response.data);
      setFormData({
        email: response.data.email || '',
        phone: response.data.phone || '',
        address: response.data.address || '',
        city: response.data.city || '',
        state: response.data.state || '',
        pincode: response.data.pincode || ''
      });
    } catch (error) {
      console.error('Error fetching employee data:', error);
      alert('Failed to load employee data');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSave = async () => {
    try {
      setSaving(true);

      await api.put(`/employees/${employeeData.id}`, formData);

      alert('Profile updated successfully!');
      await fetchEmployeeData();
      setEditing(false);
    } catch (error) {
      console.error('Error updating profile:', error);
      alert(error.response?.data?.detail || 'Failed to update profile');
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    setFormData({
      email: employeeData.email || '',
      phone: employeeData.phone || '',
      address: employeeData.address || '',
      city: employeeData.city || '',
      state: employeeData.state || '',
      pincode: employeeData.pincode || ''
    });
    setEditing(false);
  };

  const formatDate = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString('en-IN', {
      day: '2-digit',
      month: 'long',
      year: 'numeric'
    });
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(amount || 0);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">My Profile</h1>
          <p className="text-gray-600 mt-1">View and manage your personal information</p>
        </div>
        {!editing ? (
          <button
            onClick={() => setEditing(true)}
            className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            <Edit className="w-4 h-4 mr-2" />
            Edit Profile
          </button>
        ) : (
          <div className="flex space-x-2">
            <button
              onClick={handleCancel}
              className="flex items-center px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
            >
              <X className="w-4 h-4 mr-2" />
              Cancel
            </button>
            <button
              onClick={handleSave}
              disabled={saving}
              className="flex items-center px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50"
            >
              {saving ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Saving...
                </>
              ) : (
                <>
                  <Save className="w-4 h-4 mr-2" />
                  Save Changes
                </>
              )}
            </button>
          </div>
        )}
      </div>

      {/* Profile Header Card */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 rounded-lg shadow-lg p-8 text-white">
        <div className="flex items-center space-x-6">
          <div className="bg-white rounded-full p-4">
            <User className="w-16 h-16 text-blue-600" />
          </div>
          <div>
            <h2 className="text-3xl font-bold">
              {employeeData?.first_name} {employeeData?.middle_name || ''} {employeeData?.last_name}
            </h2>
            <p className="text-blue-100 text-lg mt-1">{employeeData?.designation}</p>
            <div className="flex items-center space-x-4 mt-3">
              <span className="bg-blue-500 px-3 py-1 rounded-full text-sm">
                {employeeData?.employee_code}
              </span>
              <span className="bg-blue-500 px-3 py-1 rounded-full text-sm">
                {employeeData?.department}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Personal Information */}
        <div className="lg:col-span-2 space-y-6">
          {/* Basic Information */}
          <div className="bg-white rounded-lg shadow">
            <div className="p-6 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">Basic Information</h3>
            </div>
            <div className="p-6 space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="text-sm font-medium text-gray-600 flex items-center">
                    <User className="w-4 h-4 mr-2" />
                    First Name
                  </label>
                  <p className="mt-1 text-gray-900 font-medium">{employeeData?.first_name}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600 flex items-center">
                    <User className="w-4 h-4 mr-2" />
                    Last Name
                  </label>
                  <p className="mt-1 text-gray-900 font-medium">{employeeData?.last_name}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600 flex items-center">
                    <Calendar className="w-4 h-4 mr-2" />
                    Date of Birth
                  </label>
                  <p className="mt-1 text-gray-900 font-medium">{formatDate(employeeData?.date_of_birth)}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600 flex items-center">
                    <User className="w-4 h-4 mr-2" />
                    Gender
                  </label>
                  <p className="mt-1 text-gray-900 font-medium">{employeeData?.gender || '-'}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Contact Information */}
          <div className="bg-white rounded-lg shadow">
            <div className="p-6 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">Contact Information</h3>
            </div>
            <div className="p-6 space-y-4">
              <div>
                <label className="text-sm font-medium text-gray-600 flex items-center">
                  <Mail className="w-4 h-4 mr-2" />
                  Email Address
                </label>
                {editing ? (
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    className="mt-1 w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                ) : (
                  <p className="mt-1 text-gray-900 font-medium">{employeeData?.email || '-'}</p>
                )}
              </div>

              <div>
                <label className="text-sm font-medium text-gray-600 flex items-center">
                  <Phone className="w-4 h-4 mr-2" />
                  Phone Number
                </label>
                {editing ? (
                  <input
                    type="tel"
                    name="phone"
                    value={formData.phone}
                    onChange={handleInputChange}
                    className="mt-1 w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                ) : (
                  <p className="mt-1 text-gray-900 font-medium">{employeeData?.phone || '-'}</p>
                )}
              </div>

              <div>
                <label className="text-sm font-medium text-gray-600 flex items-center">
                  <MapPin className="w-4 h-4 mr-2" />
                  Address
                </label>
                {editing ? (
                  <textarea
                    name="address"
                    value={formData.address}
                    onChange={handleInputChange}
                    rows="3"
                    className="mt-1 w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                ) : (
                  <p className="mt-1 text-gray-900 font-medium">{employeeData?.address || '-'}</p>
                )}
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="text-sm font-medium text-gray-600">City</label>
                  {editing ? (
                    <input
                      type="text"
                      name="city"
                      value={formData.city}
                      onChange={handleInputChange}
                      className="mt-1 w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  ) : (
                    <p className="mt-1 text-gray-900 font-medium">{employeeData?.city || '-'}</p>
                  )}
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600">State</label>
                  {editing ? (
                    <input
                      type="text"
                      name="state"
                      value={formData.state}
                      onChange={handleInputChange}
                      className="mt-1 w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  ) : (
                    <p className="mt-1 text-gray-900 font-medium">{employeeData?.state || '-'}</p>
                  )}
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600">Pincode</label>
                  {editing ? (
                    <input
                      type="text"
                      name="pincode"
                      value={formData.pincode}
                      onChange={handleInputChange}
                      className="mt-1 w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  ) : (
                    <p className="mt-1 text-gray-900 font-medium">{employeeData?.pincode || '-'}</p>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Bank Details */}
          <div className="bg-white rounded-lg shadow">
            <div className="p-6 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">Bank Account Details</h3>
            </div>
            <div className="p-6 space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="text-sm font-medium text-gray-600 flex items-center">
                    <CreditCard className="w-4 h-4 mr-2" />
                    Account Number
                  </label>
                  <p className="mt-1 text-gray-900 font-medium font-mono">
                    {employeeData?.bank_account_number ?
                      `XXXX${employeeData.bank_account_number.slice(-4)}` : '-'}
                  </p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600 flex items-center">
                    <Building className="w-4 h-4 mr-2" />
                    IFSC Code
                  </label>
                  <p className="mt-1 text-gray-900 font-medium font-mono">{employeeData?.ifsc_code || '-'}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600 flex items-center">
                    <Building className="w-4 h-4 mr-2" />
                    Bank Name
                  </label>
                  <p className="mt-1 text-gray-900 font-medium">{employeeData?.bank_name || '-'}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600 flex items-center">
                    <Building className="w-4 h-4 mr-2" />
                    Branch
                  </label>
                  <p className="mt-1 text-gray-900 font-medium">{employeeData?.bank_branch || '-'}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column */}
        <div className="space-y-6">
          {/* Employment Details */}
          <div className="bg-white rounded-lg shadow">
            <div className="p-6 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">Employment Details</h3>
            </div>
            <div className="p-6 space-y-4">
              <div>
                <label className="text-sm font-medium text-gray-600 flex items-center">
                  <Briefcase className="w-4 h-4 mr-2" />
                  Employee Code
                </label>
                <p className="mt-1 text-gray-900 font-bold">{employeeData?.employee_code}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-600 flex items-center">
                  <Calendar className="w-4 h-4 mr-2" />
                  Date of Joining
                </label>
                <p className="mt-1 text-gray-900 font-medium">{formatDate(employeeData?.date_of_joining)}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-600 flex items-center">
                  <Briefcase className="w-4 h-4 mr-2" />
                  Department
                </label>
                <p className="mt-1 text-gray-900 font-medium">{employeeData?.department}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-600 flex items-center">
                  <Briefcase className="w-4 h-4 mr-2" />
                  Designation
                </label>
                <p className="mt-1 text-gray-900 font-medium">{employeeData?.designation}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-600 flex items-center">
                  <CheckCircle className="w-4 h-4 mr-2" />
                  Status
                </label>
                <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium mt-1 ${
                  employeeData?.status === 'Active'
                    ? 'bg-green-100 text-green-800'
                    : 'bg-gray-100 text-gray-800'
                }`}>
                  {employeeData?.status}
                </span>
              </div>
            </div>
          </div>

          {/* Salary Information */}
          <div className="bg-white rounded-lg shadow">
            <div className="p-6 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">Salary Information</h3>
            </div>
            <div className="p-6 space-y-4">
              <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-lg p-4 border border-green-200">
                <label className="text-sm font-medium text-gray-600">Basic Salary</label>
                <p className="text-2xl font-bold text-green-600 mt-1">
                  {formatCurrency(employeeData?.basic_salary)}
                </p>
                <p className="text-xs text-gray-600 mt-1">Per month</p>
              </div>

              <div>
                <label className="text-sm font-medium text-gray-600">HRA</label>
                <p className="mt-1 text-gray-900 font-medium">{formatCurrency(employeeData?.hra)}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-600">Other Allowances</label>
                <p className="mt-1 text-gray-900 font-medium">{formatCurrency(employeeData?.other_allowances)}</p>
              </div>
            </div>
          </div>

          {/* Statutory Details */}
          <div className="bg-white rounded-lg shadow">
            <div className="p-6 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">Statutory Information</h3>
            </div>
            <div className="p-6 space-y-4">
              <div>
                <label className="text-sm font-medium text-gray-600">PAN Number</label>
                <p className="mt-1 text-gray-900 font-medium font-mono">{employeeData?.pan_number || '-'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-600">Aadhaar Number</label>
                <p className="mt-1 text-gray-900 font-medium font-mono">
                  {employeeData?.aadhaar_number ?
                    `XXXX XXXX ${employeeData.aadhaar_number.slice(-4)}` : '-'}
                </p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-600">UAN (PF)</label>
                <p className="mt-1 text-gray-900 font-medium font-mono">{employeeData?.uan_number || '-'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-600">ESI Number</label>
                <p className="mt-1 text-gray-900 font-medium font-mono">{employeeData?.esi_number || '-'}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Note */}
      {!editing && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p className="text-sm text-blue-900">
            <strong>Note:</strong> You can only edit your contact information. For changes to employment details,
            salary, or bank information, please contact HR department.
          </p>
        </div>
      )}
    </div>
  );
};

export default EmployeeProfile;
