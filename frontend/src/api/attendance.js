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

  getTemplateInfo: async (month, year) => {
    const response = await axios.get(`/attendance/template/info?month=${month}&year=${year}`);
    return response.data;
  },

  downloadTemplate: async (month, year) => {
    const response = await axios.get(`/attendance/template/download?month=${month}&year=${year}`, {
      responseType: 'blob',
    });

    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `attendance_template_${year}_${month.toString().padStart(2, '0')}.xlsx`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  },
};
