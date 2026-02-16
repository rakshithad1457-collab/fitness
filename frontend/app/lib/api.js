import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000'; 

const api = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' },
});

// Auto-attach token to every request
api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

export const authAPI = {
  login: async (email, password) => {
    const response = await api.post('/api/auth/login', { email, password });
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },
  getCurrentUser: () => {
    if (typeof window !== 'undefined') {
      const user = localStorage.getItem('user');
      return user ? JSON.parse(user) : null;
    }
    return null;
  },
  // ADDED: This fixes the crash when clicking Logout in your Navbar
  logout: () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    }
  }
};

export const nutritionAPI = {
  getRecipes: async (goal, restrictions = []) => {
    const response = await api.get('/api/nutrition/recipes', {
      params: { 
        goal: goal, 
        restrictions: restrictions.length > 0 ? restrictions.join(',') : "" 
      }
    });
    return response.data;
  },
  getMealPlan: async (goal, restrictions = [], days = 7) => {
    // FIXED LINE 51: Removed 'var' so the build error goes away
    const response = await api.get('/api/nutrition/meal-plan', {
      params: { 
        goal: goal, 
        restrictions: restrictions.length > 0 ? restrictions.join(',') : "", 
        days 
      }
    });
    return response.data;
  },
  getHealthySwaps: async (craving) => {
    const response = await api.get('/api/nutrition/healthy-swaps', {
      params: { craving }
    });
    return response.data;
  }
};

export default api;