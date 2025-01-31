<template>
  <div class="p-6 min-h-screen">
    <!-- Górna sekcja z nazwą klasy, ID skarbnika i strzałką wyjścia -->
    <div class="flex justify-between items-start mb-6 relative">
      <!-- Strzałka wyjścia -->
      <svg
        @click="moveToHome"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="1.5"
        stroke="currentColor"
        class="absolute top-0 left-0 w-6 h-6 cursor-pointer text-gray-800"
      >
        <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
      </svg>

      <div class="text-left">
        <h1 class="ml-7 text-3xl font-bold ">{{ classItem.name }}</h1>
        <h2 class="text-xl text-gray-600">Skarbnik: {{ classItem.treasurerName }}</h2>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-5 gap-6">
      <div
        class="bg-white p-4 rounded-lg shadow-md col-span-2"
        :style="{ height: `${50 + members.length+1 * 48}px` }"
      >
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold">Uczniowie</h2>
          <button
            @click="AddStudent(classItem.id)"
            class="px-4 py-2 bg-green-500 text-white rounded-lg shadow hover:bg-green-600"
          >
            Dodaj ucznia
          </button>
        </div>
        <ul class="space-y-3">
          <li
            v-for="member in members"
            :key="member.id"
            class="p-1 bg-gray-100 rounded-lg shadow-sm hover:bg-gray-200 flex items-center gap-4"
          >
            <img
              class="w-12 h-12 rounded-full"
              :src="member.avatar"
              alt="Obrazek użytkownika"
            />
            <span>{{ member.name }}</span>
          </li>
        </ul>
      </div>


      <div v-if="showAddForm" class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50">
      <div class="bg-white p-6 rounded-lg shadow-lg w-96">
        <h2 class="text-xl font-semibold mb-4">Dodaj zbiórkę</h2>
        <label class="block mb-2">Tytuł</label>
        <input v-model="newFund.title" type="text" class="w-full p-2 border rounded mb-3">
        
        <label class="block mb-2">Opis</label>
        <textarea v-model="newFund.description" class="w-full p-2 border rounded mb-3"></textarea>
        
        <label class="block mb-2">Data rozpoczęcia</label>
        <input v-model="newFund.startDate" type="date" class="w-full p-2 border rounded mb-3">
        
        <label class="block mb-2">Data zakończenia</label>
        <input v-model="newFund.endDate" type="date" class="w-full p-2 border rounded mb-3">

        <div class="flex justify-end space-x-3 mt-4">
          <button @click="showAddForm = false" class="px-4 py-2 bg-gray-400 text-white rounded">Anuluj</button>
          <button @click="saveFundrise" class="px-4 py-2 bg-green-500 text-white rounded">Zapisz</button>
        </div>
      </div>
    </div>

      <!-- Aktywne zbiórki: zajmuje 3/5 szerokości -->
      <div
        class="bg-white p-4 rounded-lg shadow-md col-span-3"
        :style="{ height: `${50 + filteredCollections.length * 160}px` }"
      >
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold">Aktywne zbiórki</h2>
          <button
            v-if="isTreasurer"
            @click="AddFoundrise(classItem.id)"
            class="px-4 py-2 bg-green-500 text-white rounded-lg shadow hover:bg-green-600"
          >
            Dodaj zbiórkę
          </button>
        </div>
        <label class="flex items-center space-x-2 mb-4">
          <input type="checkbox" v-model="showCompleted" class="form-checkbox h-4 w-4">
          <span class="text-sm text-gray-600">Pokaż zakończone zbiórki</span>
        </label>
        <ul class="space-y-3">
          <li
            v-for="collection in filteredCollections"
            :key="collection.id"
            @click="goToFoundrise(collection)"
            class="p-3 bg-gray-100 rounded-lg shadow-sm hover:bg-gray-200 cursor-pointer"
          >
            <div class="flex gap-4">
              <img
                class="w-24 h-24 rounded-lg"
                :src="collection.image"
                alt="Obrazek zbiórki"
              />
              <div class="flex flex-col">
                <span class="font-semibold">{{ collection.name }}</span>
                <span
                  class="text-sm"
                  :class="{
                    'text-green-500': collection.status === 'Aktywna',
                    'text-red-500': collection.status === 'Zakończona',
                  }"
                >
                  Status: {{ collection.status }}
                </span>
                <span class="text-sm text-gray-500">Rozpoczęcie: {{ collection.startDate }}</span>
                <span class="text-sm text-gray-500">Zakończenie: {{ collection.endDate }}</span>
                <p class="text-sm text-gray-600">{{ collection.description }}</p>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import { getUserId } from "@/api/user";
import { createCollection } from "@/api/foundrises";
import { fetchStudentsInClass } from "@/api/classes";

export default {
  data() {
    return {
      classItem: null, // Inicjalizujemy classItem jako null
      showCompleted: true, // Domyślnie pokazujemy zakończone zbiórki
      showAddForm: false,
      newFund: {
        title: "",
        description: "",
        startDate: "",
        endDate: "",
      },
      collections: [
        {
          id: 1,
          name: "Zbiórka 1",
          goal: 500,
          status: "Aktywna",
          description: "Pomoc dla dzieci.",
          startDate: "2025-01-01",
          endDate: "2025-02-01",
          image:
            "https://www.investopedia.com/thmb/u220LqqeStsaBPgVITIKYKTMOic=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/GettyImages-200275642-001-576a033e5f9b58346aace876.jpg",
        },
        {
          id: 2,
          name: "Zbiórka 2",
          goal: 1000,
          status: "Zakończona",
          description: "Wsparcie dla schroniska.",
          startDate: "2024-12-01",
          endDate: "2025-01-01",
          image: "https://via.placeholder.com/150",
        },
        {
          id: 3,
          name: "Zbiórka 3",
          goal: 800,
          status: "Aktywna",
          description: "Pomoc dla zwierząt.",
          startDate: "2025-01-15",
          endDate: "2025-03-01",
          image: "https://via.placeholder.com/150",
        },
      ],
      members: [], // Lista uczniów będzie ładowana dynamicznie
      userId: null, // Przechowujemy ID użytkownika
    };
  },
  computed: {
    filteredCollections() {
      return this.showCompleted
        ? this.collections
        : this.collections.filter(
            (collection) => collection.status !== "Zakończona"
          );
    },
    isTreasurer() {
      return this.classItem && this.classItem.treasurer_id === this.userId;
    },
  },
  created() {
    const classItemData = this.$route.params.classItem; // Pobieramy dane z URL
    if (classItemData) {
      this.classItem = JSON.parse(classItemData); // Dekodujemy dane JSON
    }

    this.userId = getUserId();

    if (this.classItem) {
      this.loadStudents(); // Pobieramy uczniów danej klasy
    }
  },
  methods: {
    async loadStudents() {
      this.members = await fetchStudentsInClass(this.classItem.id);
    },
    moveToHome() {
      this.$router.push({ name: "Home" });
    },
    AddStudent(classId) {
      console.log(`Dodano członka do klasy o id ${classId}`);
    },
    AddFoundrise() {
      this.showAddForm = true;
    },
    async saveFundrise() {
      try {
        const fundData = {
          ...this.newFund,
          classId: this.classItem.id,
        };

        console.log("Dane do wysłania:", fundData); // Debugging

        const response = await createCollection(fundData);
        console.log("Zbiórka utworzona:", response);

        this.showAddForm = false;
      } catch (error) {
        console.error("Błąd podczas zapisu zbiórki:", error);
      }
    },
    goToFoundrise(collection) {
      this.$router.push({
        name: "FoundRisePage",
        params: { collection: JSON.stringify(collection) },
      });
    },
  },
};
</script>
