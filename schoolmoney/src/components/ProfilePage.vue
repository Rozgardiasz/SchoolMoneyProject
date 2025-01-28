<template>
  <div class="profile-page mt-6 p-5 max-w-3xl mx-auto bg-gray-100 rounded-xl shadow-lg relative">
    <svg
      @click="moveToHome"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="absolute top-4 left-4 w-6 h-6 cursor-pointer text-gray-800"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M15.75 19.5L8.25 12l7.5-7.5"
      />
    </svg>
    
    <div class="profile-header text-center mb-5">
      <h1 class="text-2xl font-bold text-gray-800">Profil użytkownika</h1>
      <div class="profile-picture mt-4 mb-5">
        <img 
          src="https://static.vecteezy.com/system/resources/previews/009/292/244/non_2x/default-avatar-icon-of-social-media-user-vector.jpg" 
          alt="Avatar"
          class="w-24 h-24 rounded-full object-cover mx-auto"
        />
      </div>
    </div>
    <div class="profile-info mb-5">
      <div class="info-item flex justify-between py-2 border-b border-gray-300">
        <span class="label font-semibold text-gray-600">Imię:</span>
        <span class="value text-gray-800">{{ firstName }}</span>
      </div>
      <div class="info-item flex justify-between py-2 border-b border-gray-300">
        <span class="label font-semibold text-gray-600">Nazwisko:</span>
        <span class="value text-gray-800">{{ lastName }}</span>
      </div>
      <div class="info-item flex justify-between py-2 border-b border-gray-300">
        <span class="label font-semibold text-gray-600">Email:</span>
        <span class="value text-gray-800">{{ email }}</span>
      </div>
    </div>
    <div class="add-child text-center mb-5">
      <button @click="showAddChildModal = true" class="bg-blue-500 text-white px-6 py-3 rounded-md text-lg hover:bg-blue-600 transition">
        Dodaj dziecko
      </button>
    </div>
  
    <div class="profile-header text-center mb-5">
      <h1 class="text-2xl font-bold text-gray-800">Dzieci</h1>
    </div>
  
    <div class="children-list mt-5 bg-white p-4 rounded-lg shadow-sm">
      <div v-if="children.length > 0">
        <div v-for="child in children" :key="child.id" class="child-item flex items-center gap-4 py-2 border-b border-gray-300">
          <img :src="child.avatar || 'https://static.vecteezy.com/system/resources/previews/009/292/244/non_2x/default-avatar-icon-of-social-media-user-vector.jpg'" alt="Avatar" class="avatar w-12 h-12 rounded-full object-cover" />
          <div class="child-info">
            <p class="text-sm text-gray-800"><strong>Imię:</strong> {{ child.first_name }}</p>
            <p class="text-sm text-gray-800"><strong>Nazwisko:</strong> {{ child.last_name }}</p>
            <p class="text-sm text-gray-800"><strong>Data urodzenia:</strong> {{ child.birth_date }}</p>
          </div>
        </div>
      </div>
      <p v-else class="text-center text-gray-600">Brak dzieci w systemie.</p>
    </div>
  
    <div v-if="showAddChildModal" class="modal-overlay fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
      <div class="modal bg-white p-6 rounded-lg shadow-lg w-full max-w-md">
        <div class="form-group mb-4">
          <label for="firstName" class="block text-gray-700 font-semibold mb-2">Imię</label>
          <input v-model="firstNameField" id="firstName" type="text" class="w-full p-2 border border-gray-300 rounded-md text-gray-800" />
        </div>
        <div class="form-group mb-4">
          <label for="lastName" class="block text-gray-700 font-semibold mb-2">Nazwisko</label>
          <input v-model="lastNameField" id="lastName" type="text" class="w-full p-2 border border-gray-300 rounded-md text-gray-800" />
        </div>
        <div class="form-group mb-4">
          <label for="birthDate" class="block text-gray-700 font-semibold mb-2">Data urodzenia (YYYY-MM-DD)</label>
          <input v-model="birthDateField" id="birthDate" type="date" required class="w-full p-2 border border-gray-300 rounded-md text-gray-800" />
        </div>
        <div class="modal-actions flex justify-between mt-6">
          <button @click="addNewChild" class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition">Dodaj</button>
          <button @click="showAddChildModal = false" class="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600 transition">Anuluj</button>
        </div>
        <p v-if="errorMessage" class="error text-red-500 text-center mt-3">{{ errorMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from "vue-router";
import { ref, onMounted } from "vue";
import { fetchChildren, addChild } from "@/api/profile";  
import { getToken } from "@/api/auth";
import { getUserFirstName, getUserLastName, getUserEmail } from "@/api/user";

export default {
setup() {
  const router = useRouter();
  const firstName = ref(getUserFirstName());
  const lastName = ref(getUserLastName());
  const email = ref(getUserEmail());

  const children = ref([]);
  const showAddChildModal = ref(false);

  const firstNameField = ref('');
  const lastNameField = ref('');
  const birthDateField = ref('');
  const avatarField = ref('');

  const errorMessage = ref('');

  const fetchChildrenData = async () => {
    const token = getToken();
    try {
      children.value = await fetchChildren(token);  
    } catch (error) {
      console.error('Błąd:', error);
    }
  };

  const addNewChild = async () => {
    const token = getToken();
    try {
      await addChild(token, firstNameField.value, lastNameField.value, birthDateField.value, avatarField.value);  
      children.value.push({
        first_name: firstNameField.value,
        last_name: lastNameField.value,
        birth_date: birthDateField.value,
        avatar: avatarField.value,
      });
      resetForm();
      showAddChildModal.value = false;
    } catch (error) {
      errorMessage.value = error.message;
    }
  };

  const resetForm = () => {
    firstNameField.value = '';
    lastNameField.value = '';
    birthDateField.value = '';
    avatarField.value = '';
  };

  const moveToHome = () => {
    router.push("/Home");
  };

  onMounted(() => {
    fetchChildrenData();
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
    addNewChild,
    moveToHome,
  };
},
};
</script>
