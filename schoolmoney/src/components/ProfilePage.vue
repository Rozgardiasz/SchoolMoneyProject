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
      <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
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

    <div class="profile-account mb-5">
      <div class="info-item flex justify-between py-2 border-b border-gray-300">
        <span class="label font-semibold text-gray-600">Numer konta:</span>
        <span class="value text-gray-800">{{ accountNumber }}</span>
      </div>
      <div class="info-item flex justify-between py-2 border-b border-gray-300">
        <span class="label font-semibold text-gray-600">Saldo:</span>
        <span class="value text-gray-800">{{ accountBalance + " zł" }}</span>
      </div>
    </div>

    <!-- Przycisk edytowania profilu -->
    <div class="edit-profile text-center mb-5">
      <button @click="showEditProfileModal = true" class="bg-green-500 text-white px-6 py-3 rounded-md text-lg hover:bg-green-600 transition">
        Edytuj profil
      </button>
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
        <div
          v-for="(child, index) in children"
          :key="child.id"
          class="child-item flex items-center gap-4 py-2 border-b border-gray-300"
        >
          <img
            :src="child.avatar || 'https://static.vecteezy.com/system/resources/previews/009/292/244/non_2x/default-avatar-icon-of-social-media-user-vector.jpg'"
            alt="Avatar"
            class="avatar w-12 h-12 rounded-full object-cover"
          />
          <div class="child-info flex-1">
            <p class="text-sm text-gray-800"><strong>Imię:</strong> {{ child.first_name }}</p>
            <p class="text-sm text-gray-800"><strong>Nazwisko:</strong> {{ child.last_name }}</p>
            <p class="text-sm text-gray-800"><strong>Data urodzenia:</strong> {{ child.birth_date }}</p>
          </div>
          <div class="child-actions flex gap-2">
            <!-- Ikonka edycji -->
            <button @click="openEditChildModal(child, index)" title="Edytuj dziecko">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-500 hover:text-blue-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5M16.5 3.5a2.121 2.121 0 113 3L12 15l-4 1 1-4 7.5-7.5z"
                />
              </svg>
            </button>
            <!-- Ikonka usuwania -->
            <button @click="handleDeleteChild(child.id, index)" title="Usuń dziecko">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-red-500 hover:text-red-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6M1 7h22M8 7V4a2 2 0 012-2h4a2 2 0 012 2v3"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>
      <p v-else class="text-center text-gray-600">Brak dzieci w systemie.</p>
    </div>

    <!-- Modal dodawania dziecka -->
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

    <!-- Modal edycji profilu -->
    <div v-if="showEditProfileModal" class="modal-overlay fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
      <div class="modal bg-white p-6 rounded-lg shadow-lg w-full max-w-md">
        <h2 class="text-xl font-bold mb-4 text-center">Edytuj profil</h2>
        <div class="form-group mb-4">
          <label for="editFirstName" class="block text-gray-700 font-semibold mb-2">Nowe imię</label>
          <input v-model="editFirstName" id="editFirstName" type="text" class="w-full p-2 border border-gray-300 rounded-md text-gray-800" />
        </div>
        <div class="form-group mb-4">
          <label for="editLastName" class="block text-gray-700 font-semibold mb-2">Nowe nazwisko</label>
          <input v-model="editLastName" id="editLastName" type="text" class="w-full p-2 border border-gray-300 rounded-md text-gray-800" />
        </div>
        <div class="form-group mb-4">
          <label for="editEmail" class="block text-gray-700 font-semibold mb-2">Nowy email</label>
          <input v-model="editEmail" id="editEmail" type="email" class="w-full p-2 border border-gray-300 rounded-md text-gray-800" />
        </div>
        <div class="modal-actions flex justify-between mt-6">
          <button @click="confirmEditProfile" class="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600 transition">Potwierdź</button>
          <button @click="showEditProfileModal = false" class="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600 transition">Anuluj</button>
        </div>
      </div>
    </div>

    <!-- Modal edycji dziecka -->
    <div v-if="showEditChildModal" class="modal-overlay fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
      <div class="modal bg-white p-6 rounded-lg shadow-lg w-full max-w-md">
        <h2 class="text-xl font-bold mb-4 text-center">Edytuj dziecko</h2>
        <div class="form-group mb-4">
          <label for="editChildFirstName" class="block text-gray-700 font-semibold mb-2">Nowe imię</label>
          <input v-model="editChildFirstName" id="editChildFirstName" type="text" class="w-full p-2 border border-gray-300 rounded-md text-gray-800" />
        </div>
        <div class="form-group mb-4">
          <label for="editChildLastName" class="block text-gray-700 font-semibold mb-2">Nowe nazwisko</label>
          <input v-model="editChildLastName" id="editChildLastName" type="text" class="w-full p-2 border border-gray-300 rounded-md text-gray-800" />
        </div>
        <div class="modal-actions flex justify-between mt-6">
          <button @click="confirmEditChild" class="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600 transition">Potwierdź</button>
          <button @click="showEditChildModal = false" class="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600 transition">Anuluj</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from "vue-router";
import { ref, onMounted } from "vue";
import { fetchChildren, addChild, updateChild, deleteChildApi } from "@/api/children";
import { getToken } from "@/api/auth";
import {
  getUserFirstName,
  getUserLastName,
  getUserEmail,
  getAccountNumber,
  getAccountBalance
} from "@/api/user";

export default {
  setup() {
    const router = useRouter();
    const token = getToken();

    const firstName = ref(getUserFirstName());
    const lastName = ref(getUserLastName());
    const email = ref(getUserEmail());
    const accountNumber = ref(getAccountNumber());
    const accountBalance = ref(getAccountBalance());

    const children = ref([]);
    const showAddChildModal = ref(false);
    const showEditProfileModal = ref(false);
    const showEditChildModal = ref(false);

    const firstNameField = ref('');
    const lastNameField = ref('');
    const birthDateField = ref('');
    const avatarField = ref('');
    const errorMessage = ref('');

    // Pola dla edycji profilu
    const editFirstName = ref(firstName.value);
    const editLastName = ref(lastName.value);
    const editEmail = ref(email.value);

    // Pola dla edycji dziecka
    const childToEditIndex = ref(null);
    const childToEditId = ref(null);
    const editChildFirstName = ref('');
    const editChildLastName = ref('');
    const editChildBirthDate = ref(''); // dodajemy pole na datę urodzenia

    const fetchChildrenData = async () => {
      try {
        children.value = await fetchChildren(token);
      } catch (error) {
        // Obsługa błędu w razie potrzeby
      }
    };

    const addNewChild = async () => {
      try {
        const newChild = await addChild(token, firstNameField.value, lastNameField.value, birthDateField.value, avatarField.value);
        children.value.push(newChild);
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

    const confirmEditProfile = () => {
      // Logika wysyłania zmian profilu
      showEditProfileModal.value = false;
    };

    // Otwieranie modalu edycji dziecka i inicjalizacja pól
    const openEditChildModal = (child, index) => {
      childToEditIndex.value = index;
      childToEditId.value = child.id;
      editChildFirstName.value = child.first_name;
      editChildLastName.value = child.last_name;
      editChildBirthDate.value = child.birth_date; // zapisujemy oryginalną datę urodzenia
      showEditChildModal.value = true;
    };

    // Potwierdzanie edycji dziecka poprzez wysłanie żądania update
    const confirmEditChild = async () => {
      try {
        await updateChild(token, childToEditId.value, editChildFirstName.value, editChildLastName.value, editChildBirthDate.value);
        if (childToEditIndex.value !== null) {
          children.value[childToEditIndex.value].first_name = editChildFirstName.value;
          children.value[childToEditIndex.value].last_name = editChildLastName.value;
          // zachowujemy oryginalną datę urodzenia
        }
        childToEditIndex.value = null;
        childToEditId.value = null;
        showEditChildModal.value = false;
      } catch (error) {
        // Obsługa błędu w razie potrzeby
      }
    };

    // Usuwanie dziecka poprzez wysłanie żądania DELETE
    const handleDeleteChild = async (childId, index) => {
      try {
        await deleteChildApi(token, childId);
        children.value.splice(index, 1);
      } catch (error) {
        // Obsługa błędu w razie potrzeby
      }
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
      accountNumber,
      accountBalance,
      children,
      showAddChildModal,
      showEditProfileModal,
      showEditChildModal,
      firstNameField,
      lastNameField,
      birthDateField,
      avatarField,
      errorMessage,
      editFirstName,
      editLastName,
      editEmail,
      editChildFirstName,
      editChildLastName,
      addNewChild,
      confirmEditProfile,
      openEditChildModal,
      confirmEditChild,
      handleDeleteChild,
      moveToHome,
    };
  },
};
</script>
