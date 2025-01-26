import axios from 'axios';

const API_URL = 'http://localhost:8000';


export const fetchClasses = async (token) => {
  try {
    if (!token) {
      throw new Error('Brak tokenu autoryzacyjnego');
    }

    const response = await axios.get(`${API_URL}/user_classes/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    console.log('classes:', response.data);

    return response.data;
  } catch (error) {
    console.error('Błąd podczas ładowania klas:', error);
    throw error; 
  }
};


export const createClass = async (token, class_name) => {
  try {
    if (!token) {
      throw new Error('Brak tokenu autoryzacyjnego');
    }

    const newClass = {
      id: 0,  
      name: class_name,  
      treasurer_id: 0, 
    };

    const response = await axios.post(`${API_URL}/class/`, newClass, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    console.log('response after creating:', response.data);

    return response.data; 
  } catch (error) {
    console.error('Błąd podczas tworzenia klasy:', error);
    throw error;
  }
};
