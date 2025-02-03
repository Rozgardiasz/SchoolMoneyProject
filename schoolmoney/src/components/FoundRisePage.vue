<template>
    <div class="p-6 min-h-screen">
      <!-- Górna sekcja -->
      <div class="flex justify-between items-start mb-6 relative">
        <!-- Strzałka wyjścia -->
        <svg
          @click="goBack"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="absolute top-0 left-0 w-6 h-6 cursor-pointer text-gray-800"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
        </svg>
      </div>



  
      <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-3 gap-6">
        <!-- Informacje o zbiórce -->
        <div class="bg-white p-6 rounded-lg shadow-md md:col-span-2">
          <img class="w-full h-64 object-cover rounded-lg" :src="parsedCollection.image" alt="Obrazek zbiórki" />
            
          <div class="mt-6 flex space-x-4">
          <button @click="openEditForm" class="px-4 py-2 bg-blue-500 text-white rounded-lg shadow hover:bg-blue-600 flex items-center">
            <svg class="w-5 h-5 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19h2M4 10l5.5 5.5L20 5" />
            </svg>
            Edytuj zbiórkę
          </button>
  
            <button @click="endFoundRise" class="px-4 py-2 bg-red-500 text-white rounded-lg shadow hover:bg-red-600 flex items-center">
              <svg class="w-5 h-5 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
              Zakończ zbiórkę
            </button>
          </div>

          <h1 class="text-3xl font-bold mt-4">{{ parsedCollection.name }}</h1>
          <p class="text-gray-600 mt-2">Cel: {{ parsedCollection.goal }} zł</p>
  
          <!-- Daty z ikonkami -->
          <div class="mt-2 flex items-center text-gray-500">
            <svg class="w-5 h-5 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3M16 7V3M3 11h18M5 21h14a2 2 0 002-2V9H3v10a2 2 0 002 2z" />
            </svg>
            <p>Rozpoczęcie: {{ parsedCollection.startDate }}</p>
          </div>
  
          <div class="text-gray-500 flex items-center">
            <svg class="w-5 h-5 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3M16 7V3M3 11h18M5 21h14a2 2 0 002-2V9H3v10a2 2 0 002 2z" />
            </svg>
            <p>Zakończenie: {{ parsedCollection.endDate }}</p>
          </div>
  
          <!-- Status -->
          <p class="mt-4">
            Status: <span :class="statusClass">{{ parsedCollection.status }}</span>
          </p>
  
          <p class="mt-4 text-gray-700">{{ parsedCollection.description }}</p>
  
        </div>
  
        <!-- Komponent z listą członków klasy -->
        <div class="bg-white p-6 rounded-lg shadow-md md:col-span-1">
          <h2 class="text-xl font-semibold mb-4">Lista członków</h2>
          <ul class="space-y-3">
            <li v-for="member in members" :key="member.id" class="p-2 bg-gray-100 rounded-lg shadow-sm flex items-center gap-4">
              <img class="w-10 h-10 rounded-full" :src="member.avatar" alt="Avatar" />
              <span>{{ member.name }}</span>
            </li>
          </ul>
        </div>

      </div>

    <!-- Historia transakcji jako graf -->
    <div class="bg-white p-6 mt-6 rounded-lg shadow-md overflow-x-auto max-w-full md:col-span-2">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold">Historia transakcji</h2>

        <!-- Przycisk po prawej stronie -->
        <div class="flex space-x-4">
          <button @click="openPaymentModal" class="px-4 py-2 bg-green-500 text-white rounded-lg shadow hover:bg-green-600">
            Wpłać
          </button>
          <button class="px-4 py-2 bg-blue-500 text-white rounded-lg shadow hover:bg-blue-600">
            Wygeneruj raport
          </button>
        </div>
      </div>

  <div class="relative border-t-4 border-orange-500 pt-6 flex space-x-6">
    <div
      v-for="(transaction, index) in transactions"
      :key="transaction.id"
      class="relative flex flex-col items-center"
    >
      <div
        class="w-6 h-6 rounded-full flex items-center justify-center"
        :class="transaction.type === 'zamknięcie' ? 'bg-blue-500' : 'bg-orange-500'"
      ></div>
      <div class="text-center mt-2">
        <p class="font-semibold" :class="transaction.type === 'zamknięcie' ? 'text-blue-600' : 'text-gray-800'">
          {{ transaction.name }}
        </p>
        <p class="text-sm text-gray-500">{{ transaction.date }}</p>
        <p class="text-md text-gray-700 font-bold">{{ transaction.amount }} zł</p>
      </div>
    </div>
  </div>
</div>



          <!-- Formularz edycji zbiórki -->
          <div v-if="showEditForm" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div class="bg-white p-6 rounded-lg shadow-md w-96">
        <h2 class="text-2xl font-bold mb-4">Edytuj zbiórkę</h2>
        <label class="block text-gray-700">Tytuł</label>
        <input v-model="editFund.title" class="w-full p-2 border rounded-lg mb-3" type="text" />

        <label class="block text-gray-700">Opis</label>
        <textarea v-model="editFund.description" class="w-full p-2 border rounded-lg mb-3"></textarea>

        <label class="block text-gray-700">Cel (zł)</label>
        <input v-model="editFund.goal" class="w-full p-2 border rounded-lg mb-3" type="number" />

        <label class="block text-gray-700">Data rozpoczęcia</label>
        <input v-model="editFund.startDate" class="w-full p-2 border rounded-lg mb-3" type="date" />

        <label class="block text-gray-700">Data zakończenia</label>
        <input v-model="editFund.endDate" class="w-full p-2 border rounded-lg mb-3" type="date" />

        <div class="flex justify-between mt-4">
          <button @click="logEditData" class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600">Zapisz zmiany</button>
          <button @click="showEditForm = false" class="px-4 py-2 bg-gray-400 text-white rounded-lg hover:bg-gray-500">Anuluj</button>
        </div>
      </div>
    </div>
    <!-- Modal: Wpłata -->
    <div v-if="showPaymentModal" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div class="bg-white p-6 rounded-lg shadow-md w-96">
        <h2 class="text-xl font-semibold mb-4">Wpisz kwotę wpłaty</h2>
        <input v-model="paymentAmount" class="w-full p-2 border rounded-lg mb-3" type="number" placeholder="Kwota w zł" />

        <div class="flex justify-between mt-4">
          <button @click="confirmPayment" class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600">Wpłać</button>
          <button @click="closePaymentModal" class="px-4 py-2 bg-gray-400 text-white rounded-lg hover:bg-gray-500">Zamknij</button>
        </div>
      </div>
    </div>

    <!-- Modal: Potwierdzenie wpłaty -->
    <div v-if="showConfirmationModal" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div class="bg-white p-6 rounded-lg shadow-md w-96">
        <h2 class="text-xl font-semibold mb-4">Potwierdzenie wpłaty</h2>
        <p class="text-lg">Czy na pewno chcesz przelać {{ paymentAmount }} zł?</p>

        <div class="flex justify-between mt-4">
          <button @click="finalizePayment" class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600">Wpłać</button>
          <button @click="closeConfirmationModal" class="px-4 py-2 bg-gray-400 text-white rounded-lg hover:bg-gray-500">Anuluj</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { fetchStudentsInClass } from "@/api/classes";
import { getToken } from '@/api/auth'; // Pobieramy token z auth.js

export default {
  props: ["collection"],
  data() {
    return {
      showEditForm: false,
      showPaymentModal: false,
      showConfirmationModal: false,
      parsedCollection: null,
      members: [],
      transactions: [
        { id: 1, name: "Zamknięcie zbiórki", amount: 2500.0, date: "23.01.2025", type: "zamknięcie" },
        { id: 2, name: "Amelka Rogala", amount: 312.5, date: "23.01.2025", type: "wpłata" },
        { id: 3, name: "Justyna Rogala", amount: 312.5, date: "23.01.2025", type: "wpłata" },
        { id: 4, name: "Krystian Marciniak", amount: 312.5, date: "23.01.2025", type: "wpłata" },
        { id: 4, name: "Krystian Marciniak", amount: 312.5, date: "23.01.2025", type: "wpłata" },

        { id: 4, name: "Krystian Marciniak", amount: 312.5, date: "23.01.2025", type: "wpłata" },

        { id: 4, name: "Krystian Marciniak", amount: 312.5, date: "23.01.2025", type: "wpłata" },

        { id: 4, name: "Krystian Marciniak", amount: 312.5, date: "23.01.2025", type: "wpłata" },

        { id: 4, name: "Krystian Marciniak", amount: 312.5, date: "23.01.2025", type: "wpłata" },


        { id: 4, name: "Krystian Marciniak", amount: 312.5, date: "23.01.2025", type: "wpłata" },
        { id: 4, name: "Krystian Marciniak", amount: 312.5, date: "23.01.2025", type: "wpłata" },

        { id: 4, name: "Krystian Marciniak", amount: 312.5, date: "23.01.2025", type: "wpłata" },

        { id: 4, name: "Krystian Marciniak", amount: 312.5, date: "23.01.2025", type: "wpłata" },

        { id: 4, name: "Krystian Marciniak", amount: 312.5, date: "23.01.2025", type: "wpłata" },

        { id: 4, name: "Krystian Marciniak", amount: 312.5, date: "23.01.2025", type: "wpłata" },

      ],
    };
  },
  computed: {
    statusClass() {
      return this.parsedCollection?.status === "Aktywna" ? "text-green-500 font-semibold" : "font-semibold";
    },
  },
  async created() {
    if (this.collection) {
      try {
        this.parsedCollection = JSON.parse(this.collection);
        await this.loadClassMembers(); // Pobierz listę uczniów
      } catch (error) {
        console.error("Błąd parsowania collection:", error);
      }
    }
  },
  methods: {
    async loadClassMembers() {
      try {
        const { class_id } = this.parsedCollection || {};
        const token = getToken(); // Pobieramy token z localStorage
        if (!class_id || !token) {
          console.error("Brak class_id lub tokena");
          return;
        }
        this.members = await fetchStudentsInClass(class_id, token);
      } catch (error) {
        console.error("Błąd podczas pobierania uczniów:", error);
      }
    },
    goBack() {
      this.$router.go(-1);
    },
    openEditForm() {
      this.showEditForm = true;
      this.editFund = {
        title: this.parsedCollection.name,
        description: this.parsedCollection.description,
        goal: this.parsedCollection.goal,
        startDate: this.parsedCollection.startDate,
        endDate: this.parsedCollection.endDate,
      };
    },
    logEditData() {
      console.log("Nowe dane zbiórki:", this.editFund);
      this.showEditForm = false;
    },
    endFoundRise() {
      console.log("Zbiórka zakończona.");
    },
    openPaymentModal() {
      this.showPaymentModal = true;
    },
    closePaymentModal() {
      this.showPaymentModal = false;
    },
    confirmPayment() {
      if (this.paymentAmount && this.paymentAmount > 0) {
        this.showPaymentModal = false;
        this.showConfirmationModal = true;
      }
    },
    closeConfirmationModal() {
      this.showConfirmationModal = false;
      this.showPaymentModal = true;
    },
    finalizePayment() {
      // Finalizowanie wpłaty, możesz dodać logikę zapisu transakcji
      console.log(`Wpłacono: ${this.paymentAmount} zł`);
      this.showConfirmationModal = false;
      this.paymentAmount = null;
    }
  },
};
</script>
