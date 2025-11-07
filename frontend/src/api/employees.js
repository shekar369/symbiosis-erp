import axios from './axios';

export const employeesAPI = {
  getAll: async (skip = 0, limit = 20) => {
    const response = await axios.get(`/employees?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  getById: async (id) => {
    const response = await axios.get(`/employees/${id}`);
    return response.data;
  },

  create: async (data) => {
    const response = await axios.post('/employees', data);
    return response.data;
  },

  update: async (id, data) => {
    const response = await axios.put(`/employees/${id}`, data);
    return response.data;
  },

  delete: async (id) => {
    const response = await axios.delete(`/employees/${id}`);
    return response.data;
  },

  getTemplateInfo: async () => {
    const response = await axios.get('/employees/template/info');
    return response.data;
  },

  downloadTemplate: async () => {
    const response = await axios.get('/employees/template/download', {
      responseType: 'blob',
    });

    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    const timestamp = new Date().toISOString().slice(0, 10).replace(/-/g, '');
    link.setAttribute('download', `employee_template_${timestamp}.xlsx`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  },
};
