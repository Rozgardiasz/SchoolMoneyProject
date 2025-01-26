import axios from 'axios';
import { setUserId, setUserName, setUserEmail } from './user';

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

export const fetchUserDetails = async (token) => {
  try {
    const userResponse = await axios.get(`${API_URL}/me/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    const { id, first_name, last_name, email: userEmail } = userResponse.data;

    setUserId(id);
    setUserName(first_name, last_name);
    setUserEmail(userEmail);

    return userResponse.data;
  } catch (error) {
    throw new Error('Wystąpił błąd podczas pobierania danych użytkownika');
  }
};


export const registerUser = async (first_name, last_name, email, password) => {
    try {
      const response = await axios.post(`${API_URL}/register/`, {
        first_name,
        last_name,
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
