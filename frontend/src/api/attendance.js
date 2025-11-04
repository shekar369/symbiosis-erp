import axios from './axios';

export const attendanceAPI = {
  getAll: async (skip = 0, limit = 20, employeeId = null) => {
    let url = `/attendance?skip=${skip}&limit=${limit}`;
    if (employeeId) {
      url += `&employee_id=${employeeId}`;
    }
    const response = await axios.get(url);
    return response.data;
  },

  create: async (data) => {
    const response = await axios.post('/attendance', data);
    return response.data;
  },

  uploadFile: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await axios.post('/attendance/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};
