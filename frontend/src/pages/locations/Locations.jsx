import { useState, useEffect } from 'react';
import { Plus, MapPin, Edit2, Trash2, Building2 } from '../../utils/icons';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Modal from '../../components/common/Modal';
import Input from '../../components/common/Input';
import api from '../../services/api';

const Locations = () => {
  const [locations, setLocations] = useState([]);
  const [states, setStates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingLocation, setEditingLocation] = useState(null);

  const [formData, setFormData] = useState({
    name: '',
    city: '',
    state_id: '',
    facility_type: 'regular',
    act_type: 'contract_labour',
    address_line1: '',
    address_line2: '',
    postal_code: '',
    is_active: true,
  });

  useEffect(() => {
    fetchLocations();
    fetchStates();
  }, []);

  const fetchLocations = async () => {
    try {
      setLoading(true);
      const res = await api.get('/locations/');
      setLocations(res.data);
    } catch (error) {
      console.error('Error fetching locations:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchStates = async () => {
    try {
      const res = await api.get('/locations/states');
      setStates(res.data);
    } catch (error) {
      console.error('Error fetching states:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingLocation) {
        await api.put(`/locations/${editingLocation.id}`, formData);
      } else {
        await api.post('/locations/', formData);
      }
      fetchLocations();
      handleCloseModal();
    } catch (error) {
      console.error('Error saving location:', error);
      alert('Error saving location');
    }
  };

  const handleEdit = (location) => {
    setEditingLocation(location);
    setFormData({
      name: location.name,
      city: location.city,
      state_id: location.state_id,
      facility_type: location.facility_type,
      act_type: location.act_type,
      address_line1: location.address_line1 || '',
      address_line2: location.address_line2 || '',
      postal_code: location.postal_code || '',
      is_active: location.is_active,
    });
    setIsModalOpen(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to deactivate this location?')) {
      try {
        await api.delete(`/locations/${id}`);
        fetchLocations();
      } catch (error) {
        console.error('Error deleting location:', error);
        alert('Error deleting location');
      }
    }
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setEditingLocation(null);
    setFormData({
      name: '',
      city: '',
      state_id: '',
      facility_type: 'regular',
      act_type: 'contract_labour',
      address_line1: '',
      address_line2: '',
      postal_code: '',
      is_active: true,
    });
  };

  const facilityTypeLabels = {
    sez: 'SEZ (Special Economic Zone)',
    stp: 'STP (Software Technology Park)',
    asc: 'ASC (Assessment Center)',
    regular: 'Regular',
  };

  const actTypeLabels = {
    contract_labour: 'Contract Labour Act',
    shops_establishment: 'Shops & Establishment Act',
    factories: 'Factories Act',
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Locations</h1>
          <p className="text-gray-600 mt-1">Manage your organization locations</p>
        </div>
        <Button
          onClick={() => setIsModalOpen(true)}
          icon={<Plus size={20} />}
        >
          Add Location
        </Button>
      </div>

      {loading ? (
        <div className="text-center py-8">Loading...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {locations.map((location) => (
            <Card key={location.id}>
              <div className="space-y-4">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-primary-100 rounded-lg">
                      <Building2 className="text-primary-600" size={24} />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">{location.name}</h3>
                      <p className="text-sm text-gray-600 flex items-center gap-1">
                        <MapPin size={14} />
                        {location.city}
                      </p>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleEdit(location)}
                      className="p-1 text-gray-600 hover:text-primary-600"
                    >
                      <Edit2 size={16} />
                    </button>
                    <button
                      onClick={() => handleDelete(location.id)}
                      className="p-1 text-gray-600 hover:text-red-600"
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                </div>

                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Facility Type:</span>
                    <span className="font-medium text-gray-900">
                      {facilityTypeLabels[location.facility_type]}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Act Type:</span>
                    <span className="font-medium text-gray-900">
                      {actTypeLabels[location.act_type]}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Status:</span>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      location.is_active
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {location.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </div>
                </div>

                {location.address_line1 && (
                  <div className="pt-3 border-t border-gray-200">
                    <p className="text-xs text-gray-600">
                      {location.address_line1}
                      {location.address_line2 && `, ${location.address_line2}`}
                      {location.postal_code && ` - ${location.postal_code}`}
                    </p>
                  </div>
                )}
              </div>
            </Card>
          ))}
        </div>
      )}

      <Modal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        title={editingLocation ? 'Edit Location' : 'Add New Location'}
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Location Name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            required
          />

          <Input
            label="City"
            value={formData.city}
            onChange={(e) => setFormData({ ...formData, city: e.target.value })}
            required
          />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              State
            </label>
            <select
              value={formData.state_id}
              onChange={(e) => setFormData({ ...formData, state_id: parseInt(e.target.value) })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              required
            >
              <option value="">Select State</option>
              {states.map((state) => (
                <option key={state.id} value={state.id}>
                  {state.name} ({state.code})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Facility Type
            </label>
            <select
              value={formData.facility_type}
              onChange={(e) => setFormData({ ...formData, facility_type: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              required
            >
              {Object.entries(facilityTypeLabels).map(([value, label]) => (
                <option key={value} value={value}>{label}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Act Type
            </label>
            <select
              value={formData.act_type}
              onChange={(e) => setFormData({ ...formData, act_type: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              required
            >
              {Object.entries(actTypeLabels).map(([value, label]) => (
                <option key={value} value={value}>{label}</option>
              ))}
            </select>
          </div>

          <Input
            label="Address Line 1"
            value={formData.address_line1}
            onChange={(e) => setFormData({ ...formData, address_line1: e.target.value })}
          />

          <Input
            label="Address Line 2"
            value={formData.address_line2}
            onChange={(e) => setFormData({ ...formData, address_line2: e.target.value })}
          />

          <Input
            label="Postal Code"
            value={formData.postal_code}
            onChange={(e) => setFormData({ ...formData, postal_code: e.target.value })}
          />

          <div className="flex gap-3 pt-4">
            <Button type="submit" className="flex-1">
              {editingLocation ? 'Update' : 'Create'}
            </Button>
            <Button type="button" variant="outline" onClick={handleCloseModal} className="flex-1">
              Cancel
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default Locations;
