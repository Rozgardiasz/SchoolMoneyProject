
<template>
  <div class="profile-page">
    <div class="profile-header">
      <h1>Profil użytkownika</h1>
    </div>
    <div class="profile-info">
      <div class="info-item">
        <span class="label">Imię:</span>
        <span class="value">{{ firstName }}</span>
      </div>
      <div class="info-item">
        <span class="label">Nazwisko:</span>
        <span class="value">{{ lastName }}</span>
      </div>
      <div class="info-item">
        <span class="label">Email:</span>
        <span class="value">{{ email }}</span>
      </div>
    </div>
    <div class="add-child">
      <button @click="showAddChildModal = true">Dodaj dziecko</button>
    </div>

    <div class="children-list">
      <h2>Dzieci</h2>
      <div v-if="children.length > 0">
        <div v-for="child in children" :key="child.id" class="child-item">
          <img :src="child.avatar || 'https://via.placeholder.com/50'" alt="Avatar" class="avatar" />
          <div class="child-info">
            <p><strong>Imię:</strong> {{ child.first_name }}</p>
            <p><strong>Nazwisko:</strong> {{ child.last_name }}</p>
            <p><strong>Data urodzenia:</strong> {{ child.birth_date }}</p>
          </div>
        </div>
      </div>
      <p v-else>Brak dzieci w systemie.</p>
    </div>

    <div v-if="showAddChildModal" class="modal-overlay">
      <div class="modal">
        <div class="form-group">
          <label for="firstName">Imię</label>
          <input v-model="firstNameField" id="firstName" type="text" />
        </div>
        <div class="form-group">
          <label for="lastName">Nazwisko</label>
          <input v-model="lastNameField" id="lastName" type="text" />
        </div>
        <div class="form-group">
          <label for="birthDate">Data urodzenia (YYYY-MM-DD)</label>
          <input v-model="birthDateField" id="birthDate" type="date" required />
        </div>
        <div class="form-group">
          <label for="avatar">URL awatara</label>
          <input v-model="avatarField" id="avatar" type="text" />
        </div>
        <div class="modal-actions">
          <button @click="addChild">Dodaj</button>
          <button @click="showAddChildModal = false">Anuluj</button>
        </div>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";
import { getUserFirstName, getUserLastName, getUserEmail } from "@/api/user";
import { getToken } from "@/api/auth";

export default {
  setup() {
    const firstName = ref(getUserFirstName());
    const lastName = ref(getUserLastName());
    const email = ref(getUserEmail());

    const children = ref([]);
    const showAddChildModal = ref(false);

    const firstNameField = ref("");
    const lastNameField = ref("");
    const birthDateField = ref("");
    const avatarField = ref("");

    const errorMessage = ref("");

    const fetchChildren = async () => {
      try {
        const token = getToken();
        if (!token) throw new Error("Brak tokenu");

        const response = await axios.get("http://localhost:8000/children/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        children.value = response.data;
      } catch (error) {
        console.error("Błąd podczas pobierania listy dzieci:", error);
      }
    };

    const addChild = async () => {
      const datePattern = /^\d{4}-\d{2}-\d{2}$/;

      if (!firstNameField.value.trim() || !lastNameField.value.trim()) {
        errorMessage.value = "Wszystkie pola muszą być wypełnione!";
        return;
      }

      if (!datePattern.test(birthDateField.value)) {
        errorMessage.value = "Podaj datę w formacie YYYY-MM-DD!";
        return;
      }

      errorMessage.value = ""; // Resetowanie wiadomości o błędzie
      try {
        const token = getToken();
        const response = await axios.post(
          "http://localhost:8000/children/",
          {
            first_name: firstNameField.value,
            last_name: lastNameField.value,
            birth_date: birthDateField.value,
            avatar: avatarField.value || "https://i1.sndcdn.com/artworks-000675384715-epwfpn-t500x500.jpg",
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        children.value.push(response.data);
        resetForm();
        showAddChildModal.value = false;
      } catch (error) {
        console.error("Błąd:", error);
        if (error.response && error.response.status === 401) {
          errorMessage.value =
            "Błąd uwierzytelnienia. Upewnij się, że jesteś zalogowany.";
        } else {
          errorMessage.value = "Wystąpił błąd podczas dodawania dziecka.";
        }
      }
    };

    const resetForm = () => {
      firstNameField.value = "";
      lastNameField.value = "";
      birthDateField.value = "";
      avatarField.value = "";
    };

    onMounted(() => {
      fetchChildren();
    });

    return {
      firstName,
      lastName,
      email,
      children,
      showAddChildModal,
      firstNameField,
      lastNameField,
      birthDateField,
      avatarField,
      errorMessage,
      addChild,
    };
  },
};
</script>

<style scoped>
.profile-page {
  padding: 20px;
  max-width: 600px;
  margin: 0 auto;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.profile-header {
  text-align: center;
  margin-bottom: 20px;
}

.profile-header h1 {
  font-size: 24px;
  font-weight: bold;
  color: #333333;
}

.profile-info {
  margin-bottom: 20px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #eaeaea;
}

.label {
  font-weight: bold;
  color: #555555;
}

.value {
  color: #333333;
}

.add-child {
  text-align: center;
  margin-bottom: 20px;
}

.add-child button {
  background-color: #007bff;
  color: #ffffff;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.add-child button:hover {
  background-color: #0056b3;
}

.children-list {
  margin-top: 20px;
  background-color: #ffffff;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.child-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 10px 0;
  border-bottom: 1px solid #eaeaea;
}

.child-item:last-child {
  border-bottom: none;
}

.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
}

.child-info p {
  margin: 0;
  font-size: 14px;
  color: #333333;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 400px;
  max-width: 90%;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #555555;
}

.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #eaeaea;
  border-radius: 4px;
  font-size: 14px;
  color: #333333;
  box-sizing: border-box;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.modal-actions button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 15px;
  font-size: 14px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.modal-actions button:hover {
  background-color: #0056b3;
}

.modal-actions button:nth-child(2) {
  background-color: #dc3545;
}

.modal-actions button:nth-child(2):hover {
  background-color: #a71d2a;
}

.error {
  color: #dc3545;
  margin-top: 10px;
  font-size: 14px;
  text-align: center;
}
</style>
