import axios from 'axios';

const API_URL = 'http://localhost:8000';

// Fetch children data
export const fetchChildren = async (token) => {
  try {
    if (!token) throw new Error('Brak tokenu');
    const response = await axios.get(`${API_URL}/children/`, {
      headers: { Authorization: `Bearer ${token}` },
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
      { first_name: firstName, last_name: lastName, birth_date: birthDate, avatar: avatar },
      { headers: { Authorization: `Bearer ${token}` } }
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
// Update an existing child
export const updateChild = async (token, childId, firstName, lastName, birthDate) => {
  try {
    const response = await axios.put(
      `${API_URL}/children/${childId}`,
      { first_name: firstName, last_name: lastName, birth_date: birthDate },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    return response.data;
  } catch (error) {
    console.error('Błąd aktualizacji dziecka:', error);
    throw error;
  }
};
// Delete a child – złapujemy błąd walidacji odpowiedzi i zwracamy pusty obiekt
export const deleteChildApi = async (token, childId) => {
  try {
    const response = await axios.delete(`${API_URL}/children/${childId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    // Jeśli backend zwróci pustą odpowiedź, zwracamy pusty obiekt
    return {};
  } catch (error) {
    // Jeśli błąd dotyczy walidacji odpowiedzi, traktujemy to jako sukces
    if (
      error.response &&
      error.response.status === 500 &&
      typeof error.response.data === 'string' &&
      error.response.data.includes('model_attributes_type')
    ) {
      return {};
    }
    console.error('Błąd usuwania dziecka:', error);
    throw error;
  }
};

