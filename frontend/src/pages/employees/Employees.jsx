import { useState, useEffect } from 'react';
import { Plus, Search, Edit, Trash2 } from "../../utils/icons";
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';
import Table from '../../components/common/Table';
import Modal from '../../components/common/Modal';
import { employeesAPI } from '../../api/employees';

const Employees = () => {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingEmployee, setEditingEmployee] = useState(null);

  const [formData, setFormData] = useState({
    employee_code: '',
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    date_of_joining: new Date().toISOString().split('T')[0], // Today's date in YYYY-MM-DD format
    status: 'ACTIVE',
  });

  useEffect(() => {
    fetchEmployees();
  }, []);

  const fetchEmployees = async () => {
    try {
      setLoading(true);
      const data = await employeesAPI.getAll();
      setEmployees(data);
    } catch (error) {
      console.error('Failed to fetch employees:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingEmployee) {
        await employeesAPI.update(editingEmployee.id, formData);
      } else {
        await employeesAPI.create(formData);
      }
      setIsModalOpen(false);
      resetForm();
      fetchEmployees();
    } catch (error) {
      console.error('Failed to save employee:', error);
      alert('Failed to save employee. Please try again.');
    }
  };

  const handleEdit = (employee) => {
    setEditingEmployee(employee);
    setFormData({
      employee_code: employee.employee_code,
      first_name: employee.first_name,
      last_name: employee.last_name,
      email: employee.email,
      phone: employee.phone || '',
      date_of_joining: employee.date_of_joining || new Date().toISOString().split('T')[0],
      status: employee.status,
    });
    setIsModalOpen(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this employee?')) {
      try {
        await employeesAPI.delete(id);
        fetchEmployees();
      } catch (error) {
        console.error('Failed to delete employee:', error);
        alert('Failed to delete employee. Please try again.');
      }
    }
  };

  const resetForm = () => {
    setFormData({
      employee_code: '',
      first_name: '',
      last_name: '',
      email: '',
      phone: '',
      date_of_joining: new Date().toISOString().split('T')[0],
      status: 'ACTIVE',
    });
    setEditingEmployee(null);
  };

  const columns = [
    { key: 'employee_code', label: 'Code' },
    { key: 'first_name', label: 'First Name' },
    { key: 'last_name', label: 'Last Name' },
    { key: 'email', label: 'Email' },
    { key: 'phone', label: 'Phone' },
    {
      key: 'status',
      label: 'Status',
      render: (status) => (
        <span
          className={`px-2 py-1 rounded-full text-xs font-medium ${
            status === 'ACTIVE'
              ? 'bg-green-100 text-green-800'
              : 'bg-red-100 text-red-800'
          }`}
        >
          {status}
        </span>
      ),
    },
    {
      key: 'actions',
      label: 'Actions',
      render: (_, employee) => (
        <div className="flex gap-2">
          <button
            onClick={(e) => {
              e.stopPropagation();
              handleEdit(employee);
            }}
            className="text-blue-600 hover:text-blue-800"
          >
            <Edit size={18} />
          </button>
          <button
            onClick={(e) => {
              e.stopPropagation();
              handleDelete(employee.id);
            }}
            className="text-red-600 hover:text-red-800"
          >
            <Trash2 size={18} />
          </button>
        </div>
      ),
    },
  ];

  const filteredEmployees = employees.filter((emp) =>
    `${emp.first_name} ${emp.last_name} ${emp.employee_code} ${emp.email}`
      .toLowerCase()
      .includes(searchTerm.toLowerCase())
  );

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Employees</h1>
        <Button
          onClick={() => {
            resetForm();
            setIsModalOpen(true);
          }}
        >
          <Plus size={20} className="inline mr-2" />
          Add Employee
        </Button>
      </div>

      <Card>
        <div className="mb-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
            <input
              type="text"
              placeholder="Search employees..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 pr-4 py-2 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
        </div>

        <Table columns={columns} data={filteredEmployees} loading={loading} />
      </Card>

      <Modal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          resetForm();
        }}
        title={editingEmployee ? 'Edit Employee' : 'Add New Employee'}
      >
        <form onSubmit={handleSubmit}>
          <Input
            label="Employee Code"
            name="employee_code"
            value={formData.employee_code}
            onChange={(e) => setFormData({ ...formData, employee_code: e.target.value })}
            required
          />
          <Input
            label="First Name"
            name="first_name"
            value={formData.first_name}
            onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
            required
          />
          <Input
            label="Last Name"
            name="last_name"
            value={formData.last_name}
            onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
            required
          />
          <Input
            label="Email"
            type="email"
            name="email"
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            required
          />
          <Input
            label="Phone"
            name="phone"
            value={formData.phone}
            onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
          />

          <Input
            label="Date of Joining"
            name="date_of_joining"
            type="date"
            value={formData.date_of_joining}
            onChange={(e) => setFormData({ ...formData, date_of_joining: e.target.value })}
            required
          />

          <div className="flex gap-3 mt-6">
            <Button type="submit" className="flex-1">
              {editingEmployee ? 'Update' : 'Create'} Employee
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
    </div>
  );
};

export default Employees;
