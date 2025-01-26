<template>
  <div class="flex h-screen items-center justify-center bg-gray-100 relative">
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
      <ul class="space-y-3">
        <li
          v-for="(classItem, index) in classes"
          :key="index"
          class="p-3 bg-gray-50 rounded-lg shadow-sm hover:bg-gray-100"
        >
          {{ classItem.name }}
        </li>
      </ul>

      <!-- Modal -->
      <div
        v-if="showModal"
        class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
      >
        <div class="bg-white p-6 rounded-lg shadow-lg w-10/12 md:w-6/12 lg:w-4/12">
          <h2 class="text-lg font-semibold mb-4">Dodaj nową klasę</h2>
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
              @click="handleAddClass"
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
import { fetchClasses, createClass } from '@/api/classes';
import { getToken } from '@/api/auth';

export default {
  name: 'Home',
  data() {
    return {
      classes: [],
      showModal: false,
      className: '',
      errorMessage: '',
    };
  },
  created() {
    this.loadClasses();
  },
  methods: {
    async loadClasses() {
      try {
        const token = getToken();
        if (!token) {
          throw new Error('Brak tokenu autoryzacyjnego');
        }

        const classesData = await fetchClasses(token);
        this.classes = classesData;
      } catch (error) {
        console.error('Błąd podczas ładowania klas:', error);
      }
    },
    async handleAddClass() {
      if (!this.className.trim()) {
        this.errorMessage = 'Podaj nazwę klasy';
        return;
      }

      try {
        const token = getToken();
        if (!token) {
          throw new Error('Brak tokenu autoryzacyjnego');
        }

        const newClass = await createClass(token, this.className.trim());
        this.loadClasses();
        console.log('Nowa klasa została dodana:', newClass);

        this.closeModal();
      } catch (error) {
        console.error('Błąd podczas dodawania klasy:', error);
      }
    },
    closeModal() {
      this.showModal = false;
      this.className = '';
      this.errorMessage = '';
    },
  },
};
</script>

<style scoped>
.border-red-500 {
  border-color: red;
}
</style>
