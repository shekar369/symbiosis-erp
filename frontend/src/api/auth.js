import axios from './axios';

export const authAPI = {
  login: async (username, password) => {
    // Use URLSearchParams for x-www-form-urlencoded format
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const response = await axios.post('/auth/login', formData.toString(), {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  },

  getCurrentUser: async () => {
    const response = await axios.get('/auth/me');
    return response.data;
  },
};
