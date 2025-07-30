import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API_BASE = `${BACKEND_URL}/api`;

// Create axios instance with base configuration
const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Services API
export const servicesAPI = {
  getAll: async () => {
    const response = await api.get('/services');
    return response.data;
  },
  
  create: async (service) => {
    const response = await api.post('/services', service);
    return response.data;
  },
  
  update: async (id, service) => {
    const response = await api.put(`/services/${id}`, service);
    return response.data;
  },
  
  delete: async (id) => {
    const response = await api.delete(`/services/${id}`);
    return response.data;
  }
};

// Portfolio API
export const portfolioAPI = {
  getAll: async () => {
    const response = await api.get('/portfolio');
    return response.data;
  },
  
  create: async (portfolioItem) => {
    const response = await api.post('/portfolio', portfolioItem);
    return response.data;
  },
  
  update: async (id, portfolioItem) => {
    const response = await api.put(`/portfolio/${id}`, portfolioItem);
    return response.data;
  },
  
  delete: async (id) => {
    const response = await api.delete(`/portfolio/${id}`);
    return response.data;
  }
};

// Contacts API
export const contactsAPI = {
  get: async () => {
    const response = await api.get('/contacts');
    return response.data;
  },
  
  update: async (contacts) => {
    const response = await api.put('/contacts', contacts);
    return response.data;
  }
};

// Admin API
export const adminAPI = {
  login: async (credentials) => {
    const response = await api.post('/admin/login', credentials);
    return response.data;
  }
};

// Images API
export const imagesAPI = {
  upload: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await axios.post(`${API_BASE}/upload-image`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
  
  getAll: async () => {
    const response = await api.get('/uploaded-images');
    return response.data;
  },
  
  delete: async (id) => {
    const response = await api.delete(`/uploaded-images/${id}`);
    return response.data;
  }
};

// Error handler wrapper
export const handleAPIError = (error) => {
  if (error.response) {
    // Server responded with error status
    return {
      message: error.response.data.detail || 'Произошла ошибка на сервере',
      status: error.response.status
    };
  } else if (error.request) {
    // Request was made but no response
    return {
      message: 'Сервер не отвечает. Проверьте подключение к интернету.',
      status: 0
    };
  } else {
    // Something else happened
    return {
      message: 'Произошла неожиданная ошибка',
      status: -1
    };
  }
};