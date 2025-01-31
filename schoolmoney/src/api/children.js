import axios from 'axios';

const API_URL = 'http://localhost:8000';

// Fetch children data
export const fetchChildren = async (token) => {
  try {
    if (!token) throw new Error('Brak tokenu');

    const response = await axios.get(`${API_URL}/children/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    console.error('Błąd podczas pobierania listy dzieci:', error);
    throw error;
  }
};

// Add a new child
export const addChild = async (token, firstName, lastName, birthDate, avatar) => {
  const datePattern = /^\d{4}-\d{2}-\d{2}$/;

  if (!firstName.trim() || !lastName.trim()) {
    throw new Error('Wszystkie pola muszą być wypełnione!');
  }

  if (!datePattern.test(birthDate)) {
    throw new Error('Podaj datę w formacie YYYY-MM-DD!');
  }

  try {
    const response = await axios.post(
      `${API_URL}/children/`,
      {
        first_name: firstName,
        last_name: lastName,
        birth_date: birthDate,
        avatar: avatar,
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    return response.data;
  } catch (error) {
    console.error('Błąd:', error);
    if (error.response && error.response.status === 401) {
      throw new Error('Błąd uwierzytelnienia. Upewnij się, że jesteś zalogowany.');
    } else {
      throw new Error('Wystąpił błąd podczas dodawania dziecka.');
    }
  }
};

export const addChildToClass = async (childId, classId, token) => {
  try {
    const response = await axios.post(`${API_URL}/add_child_to_class/`, {
      child_id: childId,
      class_id: classId,
    }, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    console.error("Błąd podczas dodawania dziecka do klasy:", error);
    throw error;
  }
};

