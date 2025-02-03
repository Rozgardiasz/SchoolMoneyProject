<template>
  <div class="p-6 min-h-screen">
    <div class="flex justify-between items-start mb-6 relative">
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

      <div v-if="classItem" class="text-left">
        <h1 class="ml-7 text-3xl font-bold ">{{ classItem.name }}</h1>
        <h2 class="text-xl text-gray-600">Skarbnik: {{ classItem.treasurerName }}</h2>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-5 gap-6">
      <div
        class="bg-white p-4 rounded-lg shadow-md col-span-2"
        :style="{ height: `${50 + (members.length+1) * 58}px` }"
      >
        <div v-if="classItem" class="flex justify-between items-center mb-4">
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
  
        <!-- Formularz zaproszenia -->
        <div v-if="showInviteForm" class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50">
          <div class="bg-white p-6 rounded-lg shadow-lg w-96">
            <h2 class="text-xl font-semibold mb-4">Dodaj ucznia</h2>
            
            <label class="block mb-2">Kod zaproszenia</label>
            <input v-model="inviteCode" type="text" class="w-full p-2 border rounded mb-3" disabled />
  
            <label class="block mb-2">Wybierz dziecko</label>
            <select v-model="selectedChild" class="w-full p-2 border rounded mb-3">
              <option v-for="child in childrenList" :key="child.id" :value="child.id">
                {{ child.first_name }} {{ child.last_name }}
              </option>
            </select>
  
            <div class="flex justify-end space-x-3 mt-4">
              <button @click="showInviteForm = false" class="px-4 py-2 bg-gray-400 text-white rounded">Anuluj</button>
              <button @click="submitInviteForm" class="px-4 py-2 bg-green-500 text-white rounded">Dodaj</button>
            </div>
          </div>
        </div>
  
        <!-- Formularz dodawania zbiórki -->
        <div v-if="showAddForm" class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50">
          <div class="bg-white p-6 rounded-lg shadow-lg w-96">
            <h2 class="text-xl font-semibold mb-4">Dodaj zbiórkę</h2>
            <label class="block mb-2">Tytuł</label>
            <input v-model="title" type="text" class="w-full p-2 border rounded mb-3">
            
            <label class="block mb-2">Opis</label>
            <textarea v-model="description" class="w-full p-2 border rounded mb-3"></textarea>
            
            <label class="block mb-2">Data rozpoczęcia</label>
            <input v-model="startDate" type="date" class="w-full p-2 border rounded mb-3">

            <label class="block mb-2">Data zakończenia</label>
            <input v-model="endDate" type="date" class="w-full p-2 border rounded mb-3">
  
            <div class="flex justify-end space-x-3 mt-4">
              <button @click="showAddForm = false" class="px-4 py-2 bg-gray-400 text-white rounded">Anuluj</button>
              <button @click="saveFundrise" class="px-4 py-2 bg-green-500 text-white rounded">Zapisz</button>
            </div>
          </div>
        </div>
  
        <!-- Lista aktywnych zbiórek -->
        <div
          class="bg-white p-4 rounded-lg shadow-md col-span-3"
          :style="{ height: `${50 + (filteredCollections.length+1) * 160}px` }"
        >
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-xl font-semibold">Aktywne zbiórki</h2>
            <button
              v-if="isTreasurer"
              @click="AddFoundrise"
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
              v-for="fundrise in filteredCollections"
              :key="fundrise.id"
              @click="goToFundrise(fundrise)"
              class="p-3 bg-gray-100 rounded-lg shadow-sm hover:bg-gray-200 cursor-pointer"
            >
              <div class="flex gap-4">
                <img
                  class="w-24 h-24 rounded-lg"
                  :src="fundrise.image"
                  alt="Obrazek zbiórki"
                />
                <div class="flex flex-col">
                  <!-- Używamy właściwego pola title -->
                  <span class="font-semibold">{{ fundrise.title }}</span>
                  <p
                    class="text-sm"
                    :class="{
                      'text-green-500': fundrise.status === 'Aktywna',
                      'text-red-500': fundrise.status === 'Zakończona',
                    }"
                  >
                    Status: {{ fundrise.status }}
                  </p>
                  <!-- Wyświetlamy daty korzystając z poprawnych nazw pól -->
                  <p class="text-sm text-gray-500">Rozpoczęcie: {{ fundrise.start_date.split('T')[0] }}</p>
                  <p class="text-sm text-gray-500">Zakończenie: {{ fundrise.end_date.split('T')[0] }}</p>
                  <p class="text-sm text-gray-600">{{ fundrise.description }}</p>
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
import { createCollection, fetchCollectionsInClass } from "@/api/foundrises";
import { fetchStudentsInClass } from "@/api/classes";
import { fetchChildren, addChildToClass } from "@/api/children";
import { getToken } from "@/api/auth";
import { jwtDecode } from "jwt-decode";
import { getClass } from "@/api/classes";
export default {
  data() {
    return {
      classItem: null,
      showCompleted: true,
      showAddForm: false,
      showInviteForm: false,
      inviteCode: "",
      selectedChild: null,
      childrenList: [],
      title: "",
      description: "",
      startDate: "",
      endDate: "",
      collections: [],
      members: [],
      userId: null,
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
    const classItemData = this.$route.params.classItem;
    const inviteToken = this.$route.query.token;

    if (inviteToken) {
      this.showInviteForm = true;
      this.inviteCode = inviteToken;

      // Decode the JWT token to extract classId
      try {
        const decodedToken = jwtDecode(inviteToken);
        const classIdFromToken = decodedToken.class_id; // assuming classId is stored in the token payload
        this.loadClassFromId(classIdFromToken);

      } catch (error) {
        console.error("Invalid token:", error);
      }
    } else if (classItemData) {
      this.classItem = JSON.parse(classItemData); // Normal class URL
      this.loadStudents();
      this.loadCollections();
    }

    this.userId = getUserId();
  },
  methods: {
    // Assuming you have a method to fetch all classes (replace with your actual method)


    async loadClassFromId(classId) {
      try {

        const token = getToken();
        if (!token) {
          throw new Error("Brak tokenu autoryzacyjnego");
        }
        const classItem = await getClass(token,classId); // Get all classes (or from a local store)

        if (classItem) {
          this.classItem = classItem;
          this.loadStudents();
          this.loadCollections();
        } else {
          console.error("Class not found for ID:", classId);
        }

        this.childrenList = await fetchChildren(token);

      } catch (error) {
        console.error("Error fetching class from ID:", error);
      }
    },

    async loadStudents() {
      if (!this.classItem) return;
      const token = getToken();
      try {
        this.members = await fetchStudentsInClass(this.classItem.id, token);
      } catch (error) {
        console.error("Błąd podczas ładowania studentów:", error);
      }
    },

    async loadCollections() {
      if (!this.classItem) return;
      try {
        this.collections = await fetchCollectionsInClass(this.classItem.id);
      } catch (error) {
        console.error("Błąd podczas ładowania zbiórek:", error);
      }
    },

    moveToHome() {
      this.$router.push({ name: "Home" });
    },

    async AddStudent() {
      this.showInviteForm = true;
      try {
        const token = getToken();
        this.childrenList = await fetchChildren(token);
      } catch (error) {
        console.error("Błąd podczas pobierania listy dzieci:", error);
      }
    },

    async submitInviteForm() {
      if (!this.selectedChild) return;
        const token = getToken();
        await addChildToClass(this.selectedChild, this.classItem.id, token);
        this.showInviteForm = false;
        this.loadStudents();
        this.loadCollections();
    },

    AddFoundrise() {
      this.showAddForm = true;
    },

    async saveFundrise() {
  if (!this.title || !this.startDate || !this.endDate) {
    console.error("Wszystkie pola muszą być wypełnione!");
    return;
  }

  try {
    // Tworzymy obiekt zbiórki z poprawnymi wartościami
    const fundData = {
      title: this.title,
      goal: 0, // Możesz dodać pole celu w formularzu
      description: this.description,
      startDate: new Date(this.startDate).toISOString(),
      endDate: new Date(this.endDate).toISOString(),
      classId: this.classItem.id
    };

    // Wywołujemy funkcję API do stworzenia zbiórki
    await createCollection(fundData);

    // Resetujemy formularz i zamykamy okno
    this.showAddForm = false;
    this.title = "";
    this.description = "";
    this.startDate = "";
    this.endDate = "";

    // Ponownie ładujemy listę zbiórek
    this.loadCollections();
  } catch (error) {
    console.error("Błąd podczas zapisywania zbiórki:", error);
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

