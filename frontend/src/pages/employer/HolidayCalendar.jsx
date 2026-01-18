import { useState, useEffect } from 'react';
import { Calendar, Plus, Edit2, Trash2, Check, X, Settings } from 'lucide-react';
import api from '../../services/api';

const HolidayCalendar = () => {
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());
  const [selectedMonth, setSelectedMonth] = useState(new Date().getMonth());
  const [holidays, setHolidays] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showAddModal, setShowAddModal] = useState(false);
  const [showWeeklyOffModal, setShowWeeklyOffModal] = useState(false);
  const [editingHoliday, setEditingHoliday] = useState(null);
  const [selectedDate, setSelectedDate] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    date: '',
    is_mandatory: true,
    description: ''
  });

  const [workingCalendar, setWorkingCalendar] = useState({
    monday: true,
    tuesday: true,
    wednesday: true,
    thursday: true,
    friday: true,
    saturday: false,
    sunday: false
  });

  const [stats, setStats] = useState({
    total_holidays: 0,
    mandatory_holidays: 0,
    optional_holidays: 0
  });

  const months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  useEffect(() => {
    fetchHolidays();
    fetchWorkingCalendar();
  }, [selectedYear]);

  const fetchHolidays = async () => {
    try {
      setLoading(true);
      const response = await api.get(`/holidays/`, {
        params: { year: selectedYear }
      });
      setHolidays(response.data || []);

      // Calculate stats
      const mandatory = (response.data || []).filter(h => h.is_mandatory).length;
      const optional = (response.data || []).filter(h => !h.is_mandatory).length;

      setStats({
        total_holidays: (response.data || []).length,
        mandatory_holidays: mandatory,
        optional_holidays: optional
      });
    } catch (error) {
      console.error('Error fetching holidays:', error);
      // Don't show alert for initial load, just log the error
      setHolidays([]);
      setStats({
        total_holidays: 0,
        mandatory_holidays: 0,
        optional_holidays: 0
      });
    } finally {
      setLoading(false);
    }
  };

  const fetchWorkingCalendar = async () => {
    try {
      const response = await api.get('/working-calendar/');
      if (response.data) {
        setWorkingCalendar({
          monday: response.data.monday ?? true,
          tuesday: response.data.tuesday ?? true,
          wednesday: response.data.wednesday ?? true,
          thursday: response.data.thursday ?? true,
          friday: response.data.friday ?? true,
          saturday: response.data.saturday ?? false,
          sunday: response.data.sunday ?? false
        });
      }
    } catch (error) {
      console.error('Error fetching working calendar:', error);
      // Keep default working calendar (Mon-Fri working, Sat-Sun off)
    }
  };

  const handleSaveWorkingCalendar = async () => {
    try {
      await api.post('/working-calendar/', workingCalendar);
      alert('Weekly off days updated successfully!');
      setShowWeeklyOffModal(false);
    } catch (error) {
      console.error('Error saving working calendar:', error);
      alert(error.response?.data?.detail || 'Failed to update weekly off days');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      if (editingHoliday) {
        // Update
        await api.put(`/holidays/${editingHoliday.id}`, formData);
        alert('Holiday updated successfully!');
      } else {
        // Create
        await api.post('/holidays/', formData);
        alert('Holiday added successfully!');
      }

      setShowAddModal(false);
      setEditingHoliday(null);
      resetForm();
      fetchHolidays();
    } catch (error) {
      console.error('Error saving holiday:', error);
      alert(error.response?.data?.detail || 'Failed to save holiday');
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this holiday?')) return;

    try {
      await api.delete(`/holidays/${id}`);
      alert('Holiday deleted successfully!');
      fetchHolidays();
    } catch (error) {
      console.error('Error deleting holiday:', error);
      alert('Failed to delete holiday');
    }
  };

  const handleEdit = (holiday) => {
    setEditingHoliday(holiday);
    setFormData({
      name: holiday.name,
      date: holiday.date,
      is_mandatory: holiday.is_mandatory,
      description: holiday.description || ''
    });
    setShowAddModal(true);
  };

  const resetForm = () => {
    setFormData({
      name: '',
      date: '',
      is_mandatory: true,
      description: ''
    });
    setSelectedDate(null);
  };

  const handleCloseModal = () => {
    setShowAddModal(false);
    setEditingHoliday(null);
    resetForm();
  };

  const handleDateClick = (date) => {
    const dateStr = `${selectedYear}-${String(selectedMonth + 1).padStart(2, '0')}-${String(date).padStart(2, '0')}`;

    // Check if holiday exists on this date
    const existingHoliday = holidays.find(h => h.date === dateStr);

    if (existingHoliday) {
      handleEdit(existingHoliday);
    } else {
      setSelectedDate(date);
      setFormData({
        name: '',
        date: dateStr,
        is_mandatory: true,
        description: ''
      });
      setShowAddModal(true);
    }
  };

  const getHolidayForDate = (date) => {
    const dateStr = `${selectedYear}-${String(selectedMonth + 1).padStart(2, '0')}-${String(date).padStart(2, '0')}`;
    return holidays.find(h => h.date === dateStr);
  };

  const isWeekend = (dayOfWeek) => {
    const dayMap = {
      0: 'sunday',
      1: 'monday',
      2: 'tuesday',
      3: 'wednesday',
      4: 'thursday',
      5: 'friday',
      6: 'saturday'
    };
    return !workingCalendar[dayMap[dayOfWeek]];
  };

  const getDaysInMonth = (month, year) => {
    return new Date(year, month + 1, 0).getDate();
  };

  const getFirstDayOfMonth = (month, year) => {
    return new Date(year, month, 1).getDay();
  };

  const renderCalendar = () => {
    const daysInMonth = getDaysInMonth(selectedMonth, selectedYear);
    const firstDay = getFirstDayOfMonth(selectedMonth, selectedYear);
    const days = [];

    // Empty cells for days before the first day of month
    for (let i = 0; i < firstDay; i++) {
      days.push(<div key={`empty-${i}`} className="h-24 bg-gray-50"></div>);
    }

    // Days of the month
    for (let date = 1; date <= daysInMonth; date++) {
      const dayOfWeek = new Date(selectedYear, selectedMonth, date).getDay();
      const holiday = getHolidayForDate(date);
      const isWeekendDay = isWeekend(dayOfWeek);

      days.push(
        <div
          key={date}
          onClick={() => handleDateClick(date)}
          className={`h-24 border border-gray-200 p-2 cursor-pointer transition-all hover:shadow-lg ${
            holiday
              ? holiday.is_mandatory
                ? 'bg-yellow-50 hover:bg-yellow-100'
                : 'bg-green-50 hover:bg-green-100'
              : isWeekendDay
              ? 'bg-red-50 hover:bg-red-100'
              : 'bg-white hover:bg-gray-50'
          }`}
        >
          <div className="flex justify-between items-start">
            <span className={`text-sm font-semibold ${
              holiday ? 'text-gray-900' : isWeekendDay ? 'text-red-600' : 'text-gray-600'
            }`}>
              {date}
            </span>
            {isWeekendDay && !holiday && (
              <span className="text-xs text-red-600 font-medium">WO</span>
            )}
          </div>
          {holiday && (
            <div className="mt-1">
              <p className="text-xs font-medium text-gray-900 line-clamp-2">
                {holiday.name}
              </p>
              <span className={`inline-block mt-1 px-1.5 py-0.5 text-xs rounded ${
                holiday.is_mandatory
                  ? 'bg-yellow-200 text-yellow-800'
                  : 'bg-green-200 text-green-800'
              }`}>
                {holiday.is_mandatory ? 'Mandatory' : 'Optional'}
              </span>
            </div>
          )}
        </div>
      );
    }

    return days;
  };

  return (
    <div className="p-6">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Holiday Calendar</h1>
          <p className="text-sm text-gray-600 mt-1">
            Click on any date to add a holiday or configure weekly offs
          </p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={() => setShowWeeklyOffModal(true)}
            className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
          >
            <Settings className="w-4 h-4 mr-2" />
            Configure Weekly Offs
          </button>
          <button
            onClick={() => {
              resetForm();
              setShowAddModal(true);
            }}
            className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
          >
            <Plus className="w-4 h-4 mr-2" />
            Add Holiday
          </button>
        </div>
      </div>

      {/* Stats & Controls */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-6">
            <div>
              <label className="text-sm font-medium text-gray-700 mr-2">Year:</label>
              <select
                value={selectedYear}
                onChange={(e) => setSelectedYear(parseInt(e.target.value))}
                className="rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              >
                {[...Array(5)].map((_, i) => {
                  const year = new Date().getFullYear() - 1 + i;
                  return (
                    <option key={year} value={year}>{year}</option>
                  );
                })}
              </select>
            </div>

            <div>
              <label className="text-sm font-medium text-gray-700 mr-2">Month:</label>
              <select
                value={selectedMonth}
                onChange={(e) => setSelectedMonth(parseInt(e.target.value))}
                className="rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              >
                {months.map((month, index) => (
                  <option key={index} value={index}>{month}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="flex space-x-6">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">{stats.total_holidays}</div>
              <div className="text-xs text-gray-600">Total Holidays</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-yellow-600">{stats.mandatory_holidays}</div>
              <div className="text-xs text-gray-600">Mandatory</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">{stats.optional_holidays}</div>
              <div className="text-xs text-gray-600">Optional</div>
            </div>
          </div>
        </div>

        {/* Legend */}
        <div className="mt-4 pt-4 border-t border-gray-200">
          <div className="flex items-center space-x-6 text-sm">
            <div className="flex items-center">
              <div className="w-4 h-4 bg-yellow-100 border border-yellow-300 rounded mr-2"></div>
              <span className="text-gray-700">Mandatory Holiday</span>
            </div>
            <div className="flex items-center">
              <div className="w-4 h-4 bg-green-100 border border-green-300 rounded mr-2"></div>
              <span className="text-gray-700">Optional Holiday</span>
            </div>
            <div className="flex items-center">
              <div className="w-4 h-4 bg-red-50 border border-red-300 rounded mr-2"></div>
              <span className="text-gray-700">Weekly Off</span>
            </div>
          </div>
        </div>
      </div>

      {/* Calendar Grid */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          {months[selectedMonth]} {selectedYear}
        </h2>

        {/* Day headers */}
        <div className="grid grid-cols-7 gap-0 mb-2">
          {daysOfWeek.map((day) => (
            <div key={day} className="text-center py-2 font-semibold text-gray-700 text-sm">
              {day}
            </div>
          ))}
        </div>

        {/* Calendar days */}
        <div className="grid grid-cols-7 gap-0 border-t border-l border-gray-200">
          {renderCalendar()}
        </div>
      </div>

      {/* Add/Edit Holiday Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-full max-w-md shadow-lg rounded-md bg-white">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold text-gray-900">
                {editingHoliday ? 'Edit Holiday' : 'Add New Holiday'}
              </h3>
              <button
                onClick={handleCloseModal}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Holiday Name*
                </label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                  placeholder="e.g., Independence Day"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Date*
                </label>
                <input
                  type="date"
                  required
                  value={formData.date}
                  onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Type*
                </label>
                <select
                  value={formData.is_mandatory}
                  onChange={(e) => setFormData({ ...formData, is_mandatory: e.target.value === 'true' })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                >
                  <option value="true">Mandatory (Paid)</option>
                  <option value="false">Optional</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Description
                </label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  rows="3"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                  placeholder="Optional description..."
                />
              </div>

              <div className="flex justify-between items-center mt-6">
                {editingHoliday && (
                  <button
                    type="button"
                    onClick={() => {
                      handleDelete(editingHoliday.id);
                      handleCloseModal();
                    }}
                    className="px-4 py-2 border border-red-300 rounded-md text-sm font-medium text-red-700 hover:bg-red-50"
                  >
                    Delete
                  </button>
                )}
                <div className="flex space-x-3 ml-auto">
                  <button
                    type="button"
                    onClick={handleCloseModal}
                    className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
                  >
                    {editingHoliday ? 'Update' : 'Add'} Holiday
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Weekly Off Configuration Modal */}
      {showWeeklyOffModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-full max-w-md shadow-lg rounded-md bg-white">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold text-gray-900">
                Configure Weekly Off Days
              </h3>
              <button
                onClick={() => setShowWeeklyOffModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3">
              <p className="text-sm text-gray-600 mb-4">
                Select which days are working days for your company. Unchecked days will be marked as weekly offs.
              </p>

              {Object.keys(workingCalendar).map((day) => (
                <label key={day} className="flex items-center justify-between p-3 bg-gray-50 rounded-md hover:bg-gray-100 cursor-pointer">
                  <span className="text-sm font-medium text-gray-700 capitalize">
                    {day}
                  </span>
                  <input
                    type="checkbox"
                    checked={workingCalendar[day]}
                    onChange={(e) => setWorkingCalendar({
                      ...workingCalendar,
                      [day]: e.target.checked
                    })}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                </label>
              ))}
            </div>

            <div className="flex justify-end space-x-3 mt-6">
              <button
                type="button"
                onClick={() => setShowWeeklyOffModal(false)}
                className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                onClick={handleSaveWorkingCalendar}
                className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
              >
                Save Configuration
              </button>
            </div>
          </div>
        </div>
      )}

      {loading && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-4 rounded-lg shadow-lg">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        </div>
      )}
    </div>
  );
};

export default HolidayCalendar;
