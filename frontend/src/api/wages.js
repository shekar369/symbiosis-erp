import axios from './axios';

export const wagesAPI = {
  getAll: async (skip = 0, limit = 20, filters = {}) => {
    let url = `/wage?skip=${skip}&limit=${limit}`;
    if (filters.employeeId) url += `&employee_id=${filters.employeeId}`;
    if (filters.month) url += `&month=${filters.month}`;
    if (filters.year) url += `&year=${filters.year}`;
    const response = await axios.get(url);
    return response.data;
  },

  getById: async (id) => {
    const response = await axios.get(`/wage/${id}`);
    return response.data;
  },
};
