<template>
  <div class="flex h-screen items-center justify-center relative">
    <div class="w-11/12 md:w-11/12 lg:w-8/12 bg-white shadow-lg rounded-2xl p-6">
      <div class="top-1 right-1 flex gap-4">
        <button
          class="px-4 py-2 bg-blue-500 text-white rounded-xl shadow hover:bg-blue-600"
          @click="showModal = true"
        >
          Dodaj klasę
        </button>
        <button class="px-4 py-2 bg-green-500 text-white rounded-xl shadow hover:bg-green-600">
          Dodaj dziecko do klasy
        </button>
      </div>
      <h1 class="text-xl font-semibold text-center mb-4">Lista klas</h1>

      <!-- Lista klas -->
      <div v-if="classes.length > 0">
        <ul class="space-y-3">
          <li
            v-for="(classItem, index) in classes"
            :key="index"
            @click="goToClassPage(classItem)"
            class="p-3 bg-gray-50 rounded-lg shadow-sm hover:bg-gray-100 flex justify-between items-center"
          >
            <span>{{ classItem.name }}</span>
            <!-- Ikony akcji, widoczne tylko dla skarbnika -->
            <div class="flex gap-2">
              <svg
                v-if="classItem.treasurer_id === userId"
                @click.stop="editClass(classItem)"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                class="w-6 h-6 text-blue-500 cursor-pointer hover:text-blue-700"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M16.862 3.487a2.25 2.25 0 1 1 3.182 3.182L7.697 18.015a4.5 4.5 0 0 1-1.591 1.045l-4.233 1.693c-.47.188-.906-.248-.718-.719l1.694-4.233a4.5 4.5 0 0 1 1.044-1.591l12.348-12.348z"
                />
              </svg>
              <svg
                v-if="classItem.treasurer_id === userId"
                @click.stop="deleteClass(classItem.id)"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                class="w-6 h-6 text-red-500 cursor-pointer hover:text-red-700"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M6 7h12M9 7v12m6-12v12M4 7h16M10 11v6m4-6v6M5 7l1-3h12l1 3"
                />
              </svg>
            </div>
          </li>
        </ul>
      </div>
      <!-- Brak klas -->
      <p v-else class="text-center text-gray-600">Twoje dzieci nie są przypisane do żadnej klasy.</p>

      <!-- Modal -->
      <div
        v-if="showModal"
        class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
      >
        <div class="bg-white p-6 rounded-lg shadow-lg w-10/12 md:w-6/12 lg:w-4/12">
          <h2 class="text-lg font-semibold mb-4">{{ isEditing ? 'Zmień Nazwę' : 'Dodaj nową klasę' }}</h2>
          <input
            v-model="className"
            type="text"
            placeholder="Nazwa klasy"
            class="w-full p-2 border rounded-lg focus:outline-none"
            :class="{ 'border-red-500': errorMessage }"
          />
          <p v-if="errorMessage" class="text-red-500 text-sm mt-2">{{ errorMessage }}</p>
          <div class="mt-4 flex justify-end gap-2">
            <button
              class="px-4 py-2 bg-gray-300 rounded-lg hover:bg-gray-400"
              @click="closeModal"
            >
              Anuluj
            </button>
            <button
              class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
              @click="isEditing ? handleEditClass() : handleAddClass()"
            >
              Zatwierdź
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { fetchClasses, createClass, changeClassName } from "@/api/classes";
import { getToken } from "@/api/auth";
import { getUserId } from "@/api/user";

export default {
  name: "Home",
  data() {
    return {
      classes: [],
      showModal: false,
      className: "",
      errorMessage: "",
      userId: null, // ID aktualnego użytkownika
      isEditing: false,
      currentClassId: null, // ID klasy, która jest edytowana
    };
  },
  async created() {
    this.userId = getUserId(); // Pobierz ID użytkownika
    await this.loadClasses(); // Załaduj listę klas
  },
  methods: {
    async loadClasses() {
      try {
        const token = getToken();
        if (!token) {
          throw new Error("Brak tokenu autoryzacyjnego");
        }

        const classesData = await fetchClasses(token);
        this.classes = classesData;
      } catch (error) {
        console.error("Błąd podczas ładowania klas:", error);
      }
    },
    async handleAddClass() {
      if (!this.className.trim()) {
        this.errorMessage = "Podaj nazwę klasy";
        return;
      }

      try {
        const token = getToken();
        if (!token) {
          throw new Error("Brak tokenu autoryzacyjnego");
        }

        const newClass = await createClass(token, this.className.trim());
        await this.loadClasses(); // Odśwież listę klas
        console.log("Nowa klasa została dodana:", newClass);

        this.closeModal();
      } catch (error) {
        console.error("Błąd podczas dodawania klasy:", error);
      }
    },
    async handleEditClass() {
      if (!this.className.trim()) {
        this.errorMessage = "Podaj nazwę klasy";
        return;
      }

      try {
        const token = getToken();
        if (!token) {
          throw new Error("Brak tokenu autoryzacyjnego");
        }

        const updatedClass = await changeClassName(
          token,
          this.currentClassId,
          this.className.trim()
        );
        await this.loadClasses();
        this.closeModal();
      } catch (error) {
        console.error("Błąd podczas zmiany nazwy klasy:", error);
      }

      this.closeModal();
    },
    editClass(classItem) {
      this.isEditing = true;
      this.currentClassId = classItem.id;
      this.className = classItem.name; 
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.className = "";
      this.errorMessage = "";
      this.isEditing = false;
      this.currentClassId = null;
    },
    deleteClass(classId) {
      console.log(`Usunięto item (${classId})`);
      // Tutaj można dodać wywołanie API do usunięcia klasy, jeśli będzie wymagane
    },

    goToClassPage(classItem) {
      this.$router.push({
        name: "ClassPage",
        params: { classItem: JSON.stringify(classItem) },
      });
    },
  },
};
</script>
