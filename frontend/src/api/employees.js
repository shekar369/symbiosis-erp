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

  // Bank Details
  getBankDetails: async (employeeId) => {
    try {
      const response = await axios.get(`/employees/${employeeId}/bank-details`);
      return response.data;
    } catch (error) {
      if (error.response?.status === 404) {
        return null;
      }
      throw error;
    }
  },

  createBankDetails: async (employeeId, data) => {
    const response = await axios.post(`/employees/${employeeId}/bank-details`, data);
    return response.data;
  },

  updateBankDetails: async (employeeId, data) => {
    const response = await axios.put(`/employees/${employeeId}/bank-details`, data);
    return response.data;
  },

  // Salary Details
  getSalaryDetails: async (employeeId) => {
    try {
      const response = await axios.get(`/employees/${employeeId}/salary-details`);
      return response.data;
    } catch (error) {
      if (error.response?.status === 404) {
        return null;
      }
      throw error;
    }
  },

  createSalaryDetails: async (employeeId, data) => {
    const response = await axios.post(`/employees/${employeeId}/salary-details`, data);
    return response.data;
  },

  updateSalaryDetails: async (employeeId, data) => {
    const response = await axios.put(`/employees/${employeeId}/salary-details`, data);
    return response.data;
  },

  // Statutory Details
  getStatutoryDetails: async (employeeId) => {
    try {
      const response = await axios.get(`/employees/${employeeId}/statutory-details`);
      return response.data;
    } catch (error) {
      if (error.response?.status === 404) {
        return null;
      }
      throw error;
    }
  },

  createStatutoryDetails: async (employeeId, data) => {
    const response = await axios.post(`/employees/${employeeId}/statutory-details`, data);
    return response.data;
  },

  updateStatutoryDetails: async (employeeId, data) => {
    const response = await axios.put(`/employees/${employeeId}/statutory-details`, data);
    return response.data;
  },
};
