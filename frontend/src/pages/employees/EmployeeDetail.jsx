import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Save } from '../../utils/icons';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';
import { employeesAPI } from '../../api/employees';

const EmployeeDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('basic');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [employee, setEmployee] = useState(null);

  // Form data for different sections
  const [basicInfo, setBasicInfo] = useState({
    employee_code: '',
    first_name: '',
    last_name: '',
    middle_name: '',
    date_of_birth: '',
    gender: '',
    marital_status: '',
    father_husband_name: '',
    blood_group: '',
  });

  const [contactInfo, setContactInfo] = useState({
    email: '',
    phone: '',
    alternate_phone: '',
    emergency_contact_name: '',
    emergency_contact_number: '',
    emergency_contact_relation: '',
  });

  const [employmentInfo, setEmploymentInfo] = useState({
    date_of_joining: '',
    date_of_leaving: '',
    employment_type: 'permanent',
    probation_period_months: '',
    confirmation_date: '',
    notice_period_days: '',
    department_id: '',
    designation_id: '',
    grade_id: '',
    reporting_manager_id: '',
    status: 'active',
  });

  const [bankInfo, setBankInfo] = useState({
    account_holder_name: '',
    account_number: '',
    bank_name: '',
    branch_name: '',
    ifsc_code: '',
    account_type: 'savings',
    pan_number: '',
  });

  const [salaryInfo, setSalaryInfo] = useState({
    basic_salary: '0',
    hra: '0',
    conveyance_allowance: '0',
    medical_allowance: '0',
    special_allowance: '0',
    other_allowance: '0',
    gross_salary: '0',
    pf_employee: '0',
    pf_employer: '0',
    esic_employee: '0',
    esic_employer: '0',
    professional_tax: '0',
    tds: '0',
    total_deductions: '0',
    net_salary: '0',
    ctc: '0',
  });

  const [statutoryInfo, setStatutoryInfo] = useState({
    pan_number: '',
    aadhaar_number: '',
    uan_number: '',
    esic_number: '',
    pf_applicable: true,
    esic_applicable: true,
    lwf_applicable: false,
    pt_applicable: true,
    previous_employer_pf_number: '',
    date_of_exit_from_previous_pf: '',
  });

  useEffect(() => {
    if (id) {
      fetchEmployee();
    }
  }, [id]);

  const fetchEmployee = async () => {
    try {
      setLoading(true);
      const data = await employeesAPI.getById(id);
      setEmployee(data);
      populateFormData(data);
    } catch (error) {
      console.error('Failed to fetch employee:', error);
      alert('Failed to load employee data');
    } finally {
      setLoading(false);
    }
  };

  const populateFormData = (data) => {
    // Basic Info
    setBasicInfo({
      employee_code: data.employee_code || '',
      first_name: data.first_name || '',
      last_name: data.last_name || '',
      middle_name: data.middle_name || '',
      date_of_birth: data.date_of_birth || '',
      gender: data.gender || '',
      marital_status: data.marital_status || '',
      father_husband_name: data.father_husband_name || '',
      blood_group: data.blood_group || '',
    });

    // Contact Info
    setContactInfo({
      email: data.email || '',
      phone: data.phone || '',
      alternate_phone: data.alternate_phone || '',
      emergency_contact_name: data.emergency_contact_name || '',
      emergency_contact_number: data.emergency_contact_number || '',
      emergency_contact_relation: data.emergency_contact_relation || '',
    });

    // Employment Info
    setEmploymentInfo({
      date_of_joining: data.date_of_joining || '',
      date_of_leaving: data.date_of_leaving || '',
      employment_type: data.employment_type || 'permanent',
      probation_period_months: data.probation_period_months || '',
      confirmation_date: data.confirmation_date || '',
      notice_period_days: data.notice_period_days || '',
      department_id: data.department_id || '',
      designation_id: data.designation_id || '',
      grade_id: data.grade_id || '',
      reporting_manager_id: data.reporting_manager_id || '',
      status: data.status || 'active',
    });

    // Bank Info - TODO: fetch from bank_details relationship
    // Salary Info - TODO: fetch from salary_details relationship
    // Statutory Info - TODO: fetch from statutory_details relationship
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      const updateData = {
        ...basicInfo,
        ...contactInfo,
        ...employmentInfo,
      };
      await employeesAPI.update(id, updateData);
      alert('Employee updated successfully');
      fetchEmployee();
    } catch (error) {
      console.error('Failed to update employee:', error);
      alert('Failed to update employee. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  const tabs = [
    { id: 'basic', label: 'Basic Information' },
    { id: 'contact', label: 'Contact Information' },
    { id: 'employment', label: 'Employment Details' },
    { id: 'bank', label: 'Bank Account Details' },
    { id: 'salary', label: 'Salary Information' },
    { id: 'statutory', label: 'Statutory Information' },
  ];

  if (loading) {
    return <div className="flex justify-center items-center h-64">Loading...</div>;
  }

  return (
    <div>
      <div className="flex items-center gap-4 mb-6">
        <button
          onClick={() => navigate('/employees')}
          className="text-gray-600 hover:text-gray-900"
        >
          <ArrowLeft size={24} />
        </button>
        <div className="flex-1">
          <h1 className="text-3xl font-bold text-gray-900">
            {employee?.first_name} {employee?.last_name}
          </h1>
          <p className="text-gray-600">{employee?.employee_code}</p>
        </div>
        <Button onClick={handleSave} disabled={saving}>
          <Save size={20} className="inline mr-2" />
          {saving ? 'Saving...' : 'Save Changes'}
        </Button>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`
                whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm
                ${
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }
              `}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="space-y-6">
        {activeTab === 'basic' && (
          <Card title="Basic Information">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input
                label="Employee Code"
                value={basicInfo.employee_code}
                onChange={(e) => setBasicInfo({ ...basicInfo, employee_code: e.target.value })}
                required
              />
              <Input
                label="First Name"
                value={basicInfo.first_name}
                onChange={(e) => setBasicInfo({ ...basicInfo, first_name: e.target.value })}
                required
              />
              <Input
                label="Middle Name"
                value={basicInfo.middle_name}
                onChange={(e) => setBasicInfo({ ...basicInfo, middle_name: e.target.value })}
              />
              <Input
                label="Last Name"
                value={basicInfo.last_name}
                onChange={(e) => setBasicInfo({ ...basicInfo, last_name: e.target.value })}
                required
              />
              <Input
                label="Date of Birth"
                type="date"
                value={basicInfo.date_of_birth}
                onChange={(e) => setBasicInfo({ ...basicInfo, date_of_birth: e.target.value })}
              />
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Gender</label>
                <select
                  value={basicInfo.gender}
                  onChange={(e) => setBasicInfo({ ...basicInfo, gender: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  <option value="">Select Gender</option>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Marital Status</label>
                <select
                  value={basicInfo.marital_status}
                  onChange={(e) => setBasicInfo({ ...basicInfo, marital_status: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  <option value="">Select Status</option>
                  <option value="single">Single</option>
                  <option value="married">Married</option>
                  <option value="divorced">Divorced</option>
                  <option value="widowed">Widowed</option>
                </select>
              </div>
              <Input
                label="Father/Husband Name"
                value={basicInfo.father_husband_name}
                onChange={(e) => setBasicInfo({ ...basicInfo, father_husband_name: e.target.value })}
              />
              <Input
                label="Blood Group"
                value={basicInfo.blood_group}
                onChange={(e) => setBasicInfo({ ...basicInfo, blood_group: e.target.value })}
                placeholder="e.g., A+, O-, AB+"
              />
            </div>
          </Card>
        )}

        {activeTab === 'contact' && (
          <Card title="Contact Information">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input
                label="Email"
                type="email"
                value={contactInfo.email}
                onChange={(e) => setContactInfo({ ...contactInfo, email: e.target.value })}
                required
              />
              <Input
                label="Phone"
                value={contactInfo.phone}
                onChange={(e) => setContactInfo({ ...contactInfo, phone: e.target.value })}
              />
              <Input
                label="Alternate Phone"
                value={contactInfo.alternate_phone}
                onChange={(e) => setContactInfo({ ...contactInfo, alternate_phone: e.target.value })}
              />
              <div className="md:col-span-2">
                <h3 className="font-semibold text-gray-900 mb-3 mt-4">Emergency Contact</h3>
              </div>
              <Input
                label="Emergency Contact Name"
                value={contactInfo.emergency_contact_name}
                onChange={(e) => setContactInfo({ ...contactInfo, emergency_contact_name: e.target.value })}
              />
              <Input
                label="Emergency Contact Number"
                value={contactInfo.emergency_contact_number}
                onChange={(e) => setContactInfo({ ...contactInfo, emergency_contact_number: e.target.value })}
              />
              <Input
                label="Relationship"
                value={contactInfo.emergency_contact_relation}
                onChange={(e) => setContactInfo({ ...contactInfo, emergency_contact_relation: e.target.value })}
                placeholder="e.g., Father, Spouse, Sibling"
              />
            </div>
          </Card>
        )}

        {activeTab === 'employment' && (
          <Card title="Employment Details">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input
                label="Date of Joining"
                type="date"
                value={employmentInfo.date_of_joining}
                onChange={(e) => setEmploymentInfo({ ...employmentInfo, date_of_joining: e.target.value })}
                required
              />
              <Input
                label="Date of Leaving"
                type="date"
                value={employmentInfo.date_of_leaving}
                onChange={(e) => setEmploymentInfo({ ...employmentInfo, date_of_leaving: e.target.value })}
              />
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Employment Type</label>
                <select
                  value={employmentInfo.employment_type}
                  onChange={(e) => setEmploymentInfo({ ...employmentInfo, employment_type: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  <option value="permanent">Permanent</option>
                  <option value="contract">Contract</option>
                  <option value="temporary">Temporary</option>
                  <option value="intern">Intern</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
                <select
                  value={employmentInfo.status}
                  onChange={(e) => setEmploymentInfo({ ...employmentInfo, status: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  <option value="active">Active</option>
                  <option value="inactive">Inactive</option>
                  <option value="terminated">Terminated</option>
                </select>
              </div>
              <Input
                label="Probation Period (Months)"
                type="number"
                value={employmentInfo.probation_period_months}
                onChange={(e) => setEmploymentInfo({ ...employmentInfo, probation_period_months: e.target.value })}
              />
              <Input
                label="Confirmation Date"
                type="date"
                value={employmentInfo.confirmation_date}
                onChange={(e) => setEmploymentInfo({ ...employmentInfo, confirmation_date: e.target.value })}
              />
              <Input
                label="Notice Period (Days)"
                type="number"
                value={employmentInfo.notice_period_days}
                onChange={(e) => setEmploymentInfo({ ...employmentInfo, notice_period_days: e.target.value })}
              />
            </div>
          </Card>
        )}

        {activeTab === 'bank' && (
          <Card title="Bank Account Details">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input
                label="Account Holder Name"
                value={bankInfo.account_holder_name}
                onChange={(e) => setBankInfo({ ...bankInfo, account_holder_name: e.target.value })}
              />
              <Input
                label="Account Number"
                value={bankInfo.account_number}
                onChange={(e) => setBankInfo({ ...bankInfo, account_number: e.target.value })}
              />
              <Input
                label="Bank Name"
                value={bankInfo.bank_name}
                onChange={(e) => setBankInfo({ ...bankInfo, bank_name: e.target.value })}
              />
              <Input
                label="Branch Name"
                value={bankInfo.branch_name}
                onChange={(e) => setBankInfo({ ...bankInfo, branch_name: e.target.value })}
              />
              <Input
                label="IFSC Code"
                value={bankInfo.ifsc_code}
                onChange={(e) => setBankInfo({ ...bankInfo, ifsc_code: e.target.value })}
              />
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Account Type</label>
                <select
                  value={bankInfo.account_type}
                  onChange={(e) => setBankInfo({ ...bankInfo, account_type: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  <option value="savings">Savings</option>
                  <option value="current">Current</option>
                </select>
              </div>
              <Input
                label="PAN Number"
                value={bankInfo.pan_number}
                onChange={(e) => setBankInfo({ ...bankInfo, pan_number: e.target.value })}
              />
            </div>
          </Card>
        )}

        {activeTab === 'salary' && (
          <Card title="Salary Information">
            <div className="space-y-6">
              <div>
                <h3 className="font-semibold text-gray-900 mb-3">Earnings</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <Input
                    label="Basic Salary"
                    type="number"
                    value={salaryInfo.basic_salary}
                    onChange={(e) => setSalaryInfo({ ...salaryInfo, basic_salary: e.target.value })}
                  />
                  <Input
                    label="HRA"
                    type="number"
                    value={salaryInfo.hra}
                    onChange={(e) => setSalaryInfo({ ...salaryInfo, hra: e.target.value })}
                  />
                  <Input
                    label="Conveyance Allowance"
                    type="number"
                    value={salaryInfo.conveyance_allowance}
                    onChange={(e) => setSalaryInfo({ ...salaryInfo, conveyance_allowance: e.target.value })}
                  />
                  <Input
                    label="Medical Allowance"
                    type="number"
                    value={salaryInfo.medical_allowance}
                    onChange={(e) => setSalaryInfo({ ...salaryInfo, medical_allowance: e.target.value })}
                  />
                  <Input
                    label="Special Allowance"
                    type="number"
                    value={salaryInfo.special_allowance}
                    onChange={(e) => setSalaryInfo({ ...salaryInfo, special_allowance: e.target.value })}
                  />
                  <Input
                    label="Other Allowance"
                    type="number"
                    value={salaryInfo.other_allowance}
                    onChange={(e) => setSalaryInfo({ ...salaryInfo, other_allowance: e.target.value })}
                  />
                </div>
              </div>

              <div>
                <h3 className="font-semibold text-gray-900 mb-3">Deductions</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <Input
                    label="PF Employee"
                    type="number"
                    value={salaryInfo.pf_employee}
                    onChange={(e) => setSalaryInfo({ ...salaryInfo, pf_employee: e.target.value })}
                  />
                  <Input
                    label="PF Employer"
                    type="number"
                    value={salaryInfo.pf_employer}
                    onChange={(e) => setSalaryInfo({ ...salaryInfo, pf_employer: e.target.value })}
                  />
                  <Input
                    label="ESIC Employee"
                    type="number"
                    value={salaryInfo.esic_employee}
                    onChange={(e) => setSalaryInfo({ ...salaryInfo, esic_employee: e.target.value })}
                  />
                  <Input
                    label="ESIC Employer"
                    type="number"
                    value={salaryInfo.esic_employer}
                    onChange={(e) => setSalaryInfo({ ...salaryInfo, esic_employer: e.target.value })}
                  />
                  <Input
                    label="Professional Tax"
                    type="number"
                    value={salaryInfo.professional_tax}
                    onChange={(e) => setSalaryInfo({ ...salaryInfo, professional_tax: e.target.value })}
                  />
                  <Input
                    label="TDS"
                    type="number"
                    value={salaryInfo.tds}
                    onChange={(e) => setSalaryInfo({ ...salaryInfo, tds: e.target.value })}
                  />
                </div>
              </div>

              <div>
                <h3 className="font-semibold text-gray-900 mb-3">Summary</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <Input
                    label="Gross Salary"
                    type="number"
                    value={salaryInfo.gross_salary}
                    onChange={(e) => setSalaryInfo({ ...salaryInfo, gross_salary: e.target.value })}
                    disabled
                  />
                  <Input
                    label="Total Deductions"
                    type="number"
                    value={salaryInfo.total_deductions}
                    onChange={(e) => setSalaryInfo({ ...salaryInfo, total_deductions: e.target.value })}
                    disabled
                  />
                  <Input
                    label="Net Salary"
                    type="number"
                    value={salaryInfo.net_salary}
                    onChange={(e) => setSalaryInfo({ ...salaryInfo, net_salary: e.target.value })}
                    disabled
                  />
                  <Input
                    label="CTC"
                    type="number"
                    value={salaryInfo.ctc}
                    onChange={(e) => setSalaryInfo({ ...salaryInfo, ctc: e.target.value })}
                    disabled
                  />
                </div>
              </div>
            </div>
          </Card>
        )}

        {activeTab === 'statutory' && (
          <Card title="Statutory Information">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input
                label="PAN Number"
                value={statutoryInfo.pan_number}
                onChange={(e) => setStatutoryInfo({ ...statutoryInfo, pan_number: e.target.value })}
              />
              <Input
                label="Aadhaar Number"
                value={statutoryInfo.aadhaar_number}
                onChange={(e) => setStatutoryInfo({ ...statutoryInfo, aadhaar_number: e.target.value })}
              />
              <Input
                label="UAN Number"
                value={statutoryInfo.uan_number}
                onChange={(e) => setStatutoryInfo({ ...statutoryInfo, uan_number: e.target.value })}
              />
              <Input
                label="ESIC Number"
                value={statutoryInfo.esic_number}
                onChange={(e) => setStatutoryInfo({ ...statutoryInfo, esic_number: e.target.value })}
              />
              <div className="md:col-span-2">
                <h3 className="font-semibold text-gray-900 mb-3 mt-4">Applicability</h3>
              </div>
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="pf_applicable"
                  checked={statutoryInfo.pf_applicable}
                  onChange={(e) => setStatutoryInfo({ ...statutoryInfo, pf_applicable: e.target.checked })}
                  className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
                <label htmlFor="pf_applicable" className="ml-2 block text-sm text-gray-900">
                  PF Applicable
                </label>
              </div>
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="esic_applicable"
                  checked={statutoryInfo.esic_applicable}
                  onChange={(e) => setStatutoryInfo({ ...statutoryInfo, esic_applicable: e.target.checked })}
                  className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
                <label htmlFor="esic_applicable" className="ml-2 block text-sm text-gray-900">
                  ESIC Applicable
                </label>
              </div>
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="lwf_applicable"
                  checked={statutoryInfo.lwf_applicable}
                  onChange={(e) => setStatutoryInfo({ ...statutoryInfo, lwf_applicable: e.target.checked })}
                  className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
                <label htmlFor="lwf_applicable" className="ml-2 block text-sm text-gray-900">
                  LWF Applicable
                </label>
              </div>
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="pt_applicable"
                  checked={statutoryInfo.pt_applicable}
                  onChange={(e) => setStatutoryInfo({ ...statutoryInfo, pt_applicable: e.target.checked })}
                  className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
                <label htmlFor="pt_applicable" className="ml-2 block text-sm text-gray-900">
                  PT Applicable
                </label>
              </div>
              <div className="md:col-span-2">
                <h3 className="font-semibold text-gray-900 mb-3 mt-4">Previous Employer Details</h3>
              </div>
              <Input
                label="Previous Employer PF Number"
                value={statutoryInfo.previous_employer_pf_number}
                onChange={(e) => setStatutoryInfo({ ...statutoryInfo, previous_employer_pf_number: e.target.value })}
              />
              <Input
                label="Date of Exit from Previous PF"
                type="date"
                value={statutoryInfo.date_of_exit_from_previous_pf}
                onChange={(e) => setStatutoryInfo({ ...statutoryInfo, date_of_exit_from_previous_pf: e.target.value })}
              />
            </div>
          </Card>
        )}
      </div>
    </div>
  );
};

export default EmployeeDetail;
