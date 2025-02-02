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

export const getClass = async (token, class_id) =>{
  try {
    if (!token) {
      throw new Error('Brak tokenu autoryzacyjnego');
    }

    const response = await axios.get(`${API_URL}/get_class/${class_id}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    console.log('class:', response.data);

    return response.data;
  } catch (error) {
    console.error('Błąd podczas ładowania klas:', error);
    throw error; 
  }
}

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

export const changeClassName = async (token, classId, newName) => {
  try {
    if (!token) {
      throw new Error('Brak tokenu autoryzacyjnego');
    }

    const response = await axios.put(
      `${API_URL}/class/${classId}`,
      { name: newName },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    console.log('response after updating:', response.data);

    return response.data;
  } catch (error) {
    console.error('Błąd podczas zmiany nazwy klasy:', error);
    throw error;
  }
};

export const fetchStudentsInClass = async (classId, token) => {
  try {
    const response = await axios.get(`${API_URL}/get_children_in_class/${classId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    return response.data.map(student => ({
      id: student.id,
      name: `${student.first_name} ${student.last_name}`,
      avatar: student.avatar || "https://static.vecteezy.com/system/resources/previews/009/292/244/non_2x/default-avatar-icon-of-social-media-user-vector.jpg",
    }));
  } catch (error) {
    console.error('Błąd podczas ładowania uczniów:', error);
    return [];
  }
};