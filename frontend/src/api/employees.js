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
};
