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
  const [bankDetails, setBankDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [editingBank, setEditingBank] = useState(false);
  const [saving, setSaving] = useState(false);
  const [savingBank, setSavingBank] = useState(false);
  const [formData, setFormData] = useState({});
  const [bankFormData, setBankFormData] = useState({});

  useEffect(() => {
    fetchEmployeeData();
    fetchBankDetails();
  }, []);

  const fetchEmployeeData = async () => {
    try {
      setLoading(true);
      const response = await api.get('/employees/me');
      setEmployeeData(response.data);
      setFormData({
        first_name: response.data.first_name || '',
        last_name: response.data.last_name || '',
        phone: response.data.phone || '',
        date_of_birth: response.data.date_of_birth || ''
      });
    } catch (error) {
      console.error('Error fetching employee data:', error);
      alert('Failed to load employee data');
    } finally {
      setLoading(false);
    }
  };

  const fetchBankDetails = async () => {
    try {
      const response = await api.get('/bank/my-bank-details');
      setBankDetails(response.data);
      setBankFormData({
        account_holder_name: response.data.account_holder_name || '',
        account_number: response.data.account_number || '',
        bank_name: response.data.bank_name || '',
        branch_name: response.data.branch_name || '',
        ifsc_code: response.data.ifsc_code || '',
        account_type: response.data.account_type || '',
        pan_number: response.data.pan_number || ''
      });
    } catch (error) {
      console.error('Error fetching bank details:', error);
      // It's okay if bank details don't exist yet
      setBankDetails(null);
      setBankFormData({
        account_holder_name: '',
        account_number: '',
        bank_name: '',
        branch_name: '',
        ifsc_code: '',
        account_type: 'savings',
        pan_number: ''
      });
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleBankInputChange = (e) => {
    const { name, value } = e.target;
    setBankFormData({ ...bankFormData, [name]: value });
  };

  const handleSave = async () => {
    try {
      setSaving(true);

      await api.put('/employees/me/profile', formData);

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

  const handleSaveBank = async () => {
    try {
      setSavingBank(true);

      if (bankDetails) {
        // Update existing bank details
        await api.put('/bank/my-bank-details', bankFormData);
      } else {
        // Create new bank details
        await api.post('/bank/my-bank-details', bankFormData);
      }

      alert('Bank details updated successfully!');
      await fetchBankDetails();
      setEditingBank(false);
    } catch (error) {
      console.error('Error updating bank details:', error);
      alert(error.response?.data?.detail || 'Failed to update bank details');
    } finally {
      setSavingBank(false);
    }
  };

  const handleCancel = () => {
    setFormData({
      first_name: employeeData.first_name || '',
      last_name: employeeData.last_name || '',
      phone: employeeData.phone || '',
      date_of_birth: employeeData.date_of_birth || ''
    });
    setEditing(false);
  };

  const handleCancelBank = () => {
    if (bankDetails) {
      setBankFormData({
        account_holder_name: bankDetails.account_holder_name || '',
        account_number: bankDetails.account_number || '',
        bank_name: bankDetails.bank_name || '',
        branch_name: bankDetails.branch_name || '',
        ifsc_code: bankDetails.ifsc_code || '',
        account_type: bankDetails.account_type || '',
        pan_number: bankDetails.pan_number || ''
      });
    }
    setEditingBank(false);
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
                  {editing ? (
                    <input
                      type="text"
                      name="first_name"
                      value={formData.first_name}
                      onChange={handleInputChange}
                      className="mt-1 w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  ) : (
                    <p className="mt-1 text-gray-900 font-medium">{employeeData?.first_name}</p>
                  )}
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600 flex items-center">
                    <User className="w-4 h-4 mr-2" />
                    Last Name
                  </label>
                  {editing ? (
                    <input
                      type="text"
                      name="last_name"
                      value={formData.last_name}
                      onChange={handleInputChange}
                      className="mt-1 w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  ) : (
                    <p className="mt-1 text-gray-900 font-medium">{employeeData?.last_name}</p>
                  )}
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600 flex items-center">
                    <Calendar className="w-4 h-4 mr-2" />
                    Date of Birth
                  </label>
                  {editing ? (
                    <input
                      type="date"
                      name="date_of_birth"
                      value={formData.date_of_birth}
                      onChange={handleInputChange}
                      className="mt-1 w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  ) : (
                    <p className="mt-1 text-gray-900 font-medium">{formatDate(employeeData?.date_of_birth)}</p>
                  )}
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
                <p className="mt-1 text-gray-900 font-medium">{employeeData?.email || '-'}</p>
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
            </div>
          </div>

          {/* Bank Details */}
          <div className="bg-white rounded-lg shadow">
            <div className="p-6 border-b border-gray-200 flex justify-between items-center">
              <h3 className="text-lg font-semibold text-gray-900">Bank Account Details</h3>
              {!editingBank && !editing ? (
                <button
                  onClick={() => setEditingBank(true)}
                  className="flex items-center px-3 py-1.5 bg-blue-600 text-white rounded-md hover:bg-blue-700 text-sm"
                >
                  <Edit className="w-3 h-3 mr-1.5" />
                  {bankDetails ? 'Edit' : 'Add'}
                </button>
              ) : editingBank ? (
                <div className="flex space-x-2">
                  <button
                    onClick={handleCancelBank}
                    className="flex items-center px-3 py-1.5 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 text-sm"
                  >
                    <X className="w-3 h-3 mr-1.5" />
                    Cancel
                  </button>
                  <button
                    onClick={handleSaveBank}
                    disabled={savingBank}
                    className="flex items-center px-3 py-1.5 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 text-sm"
                  >
                    {savingBank ? (
                      <>
                        <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-white mr-1.5"></div>
                        Saving...
                      </>
                    ) : (
                      <>
                        <Save className="w-3 h-3 mr-1.5" />
                        Save
                      </>
                    )}
                  </button>
                </div>
              ) : null}
            </div>
            <div className="p-6 space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="text-sm font-medium text-gray-600 flex items-center">
                    <User className="w-4 h-4 mr-2" />
                    Account Holder Name
                  </label>
                  {editingBank ? (
                    <input
                      type="text"
                      name="account_holder_name"
                      value={bankFormData.account_holder_name}
                      onChange={handleBankInputChange}
                      className="mt-1 w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  ) : (
                    <p className="mt-1 text-gray-900 font-medium">{bankDetails?.account_holder_name || '-'}</p>
                  )}
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600 flex items-center">
                    <CreditCard className="w-4 h-4 mr-2" />
                    Account Number
                  </label>
                  {editingBank ? (
                    <input
                      type="text"
                      name="account_number"
                      value={bankFormData.account_number}
                      onChange={handleBankInputChange}
                      className="mt-1 w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  ) : (
                    <p className="mt-1 text-gray-900 font-medium font-mono">
                      {bankDetails?.account_number ?
                        `XXXX${bankDetails.account_number.slice(-4)}` : '-'}
                    </p>
                  )}
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600 flex items-center">
                    <Building className="w-4 h-4 mr-2" />
                    Bank Name
                  </label>
                  {editingBank ? (
                    <input
                      type="text"
                      name="bank_name"
                      value={bankFormData.bank_name}
                      onChange={handleBankInputChange}
                      className="mt-1 w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  ) : (
                    <p className="mt-1 text-gray-900 font-medium">{bankDetails?.bank_name || '-'}</p>
                  )}
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600 flex items-center">
                    <Building className="w-4 h-4 mr-2" />
                    Branch Name
                  </label>
                  {editingBank ? (
                    <input
                      type="text"
                      name="branch_name"
                      value={bankFormData.branch_name}
                      onChange={handleBankInputChange}
                      className="mt-1 w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  ) : (
                    <p className="mt-1 text-gray-900 font-medium">{bankDetails?.branch_name || '-'}</p>
                  )}
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600 flex items-center">
                    <Building className="w-4 h-4 mr-2" />
                    IFSC Code
                  </label>
                  {editingBank ? (
                    <input
                      type="text"
                      name="ifsc_code"
                      value={bankFormData.ifsc_code}
                      onChange={handleBankInputChange}
                      className="mt-1 w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  ) : (
                    <p className="mt-1 text-gray-900 font-medium font-mono">{bankDetails?.ifsc_code || '-'}</p>
                  )}
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600 flex items-center">
                    <CreditCard className="w-4 h-4 mr-2" />
                    Account Type
                  </label>
                  {editingBank ? (
                    <select
                      name="account_type"
                      value={bankFormData.account_type}
                      onChange={handleBankInputChange}
                      className="mt-1 w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="savings">Savings</option>
                      <option value="current">Current</option>
                    </select>
                  ) : (
                    <p className="mt-1 text-gray-900 font-medium capitalize">{bankDetails?.account_type || '-'}</p>
                  )}
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600 flex items-center">
                    <CreditCard className="w-4 h-4 mr-2" />
                    PAN Number
                  </label>
                  {editingBank ? (
                    <input
                      type="text"
                      name="pan_number"
                      value={bankFormData.pan_number}
                      onChange={handleBankInputChange}
                      className="mt-1 w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Optional"
                    />
                  ) : (
                    <p className="mt-1 text-gray-900 font-medium font-mono">{bankDetails?.pan_number || '-'}</p>
                  )}
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
      {!editing && !editingBank && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p className="text-sm text-blue-900">
            <strong>Note:</strong> You can edit your basic information (name, phone, date of birth) and bank details.
            For changes to employment details or salary information, please contact HR department.
          </p>
        </div>
      )}
    </div>
  );
};

export default EmployeeProfile;
