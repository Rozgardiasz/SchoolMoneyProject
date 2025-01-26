import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const login = async (email, password) => {
  try {
    const response = await axios.post(`${API_URL}/login/`, {
        email,
        password,
      });
    
    return response.data;
  } catch (error) {
    if (error.response && error.response.status === 401) {
      throw new Error('Błędny email lub hasło');
    }
    throw new Error('Wystąpił błąd podczas logowania');
  }
};

export const registerUser = async (name, email, password) => {
    try {
      const response = await axios.post(`${API_URL}/register/`, {
        name,
        email,
        password,
      });
      return response.data;
    } catch (error) {
      if (error.response && error.response.status === 400) {
        throw new Error('Rejestracja nie powiodła się. Sprawdź wprowadzone dane.');
      }
      throw new Error('Wystąpił błąd podczas rejestracji.');
    }
  };
  

export const setToken = (token) => {
  localStorage.setItem('access_token', token);
};

export const getToken = () => {
  return localStorage.getItem('access_token');
};

export const clearToken = () => {
  localStorage.removeItem('access_token');
};
