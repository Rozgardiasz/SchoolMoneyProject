<template>
  <div class="flex h-screen items-center justify-center bg-gray-100 relative">
    <div class="w-11/12 md:w-11/12 lg:w-8/12 bg-white shadow-lg rounded-2xl p-6">
      <div class="top-1 right-1 flex gap-4">
        <button
          class="px-4 py-2 bg-blue-500 text-white rounded-xl shadow hover:bg-blue-600"
          @click="addClass"
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

    async addClass() {
      try {
        const token = getToken();
        if (!token) {
          throw new Error('Brak tokenu autoryzacyjnego');
        }

        const newClass = await createClass(token, "III C", 6);

        this.loadClasses();
        console.log('Nowa klasa została dodana:', newClass);
      } catch (error) {
        console.error('Błąd podczas dodawania klasy:', error);
      }
    },
  },
};
</script>
