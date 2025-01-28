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
        <h1 class="text-3xl font-bold ">{{ classItem.name }}</h1>
        <h2 class="text-xl text-gray-600">Skarbnik: {{ classItem.treasurer_id }}</h2>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-5 gap-6">
      <div
        class="bg-white p-4 rounded-lg shadow-md col-span-2"
        :style="{ height: `${50 + members.length * 88}px` }"
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

      <!-- Aktywne zbiórki: zajmuje 3/5 szerokości -->
      <div
        class="bg-white p-4 rounded-lg shadow-md col-span-3"
        :style="{ height: `${50 + filteredCollections.length * 160}px` }"
      >
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold">Aktywne zbiórki</h2>
          <button
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
            class="p-3 bg-gray-100 rounded-lg shadow-sm hover:bg-gray-200"
          >
            <div class="flex gap-4">
              <img
                class="w-24 h-24 rounded-lg"
                :src="collection.image"
                alt="Obrazek zbiórki"
              />
              <div class="flex flex-col">
                <span class="font-semibold">{{ collection.name }}</span>
                <span class="text-sm text-gray-500">Cel: {{ collection.goal }} zł</span>
                <span class="text-sm text-gray-500">Status: {{ collection.status }}</span>
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
export default {
  data() {
    return {
      classItem: null, // Inicjalizujemy classItem jako null
      showCompleted: true, // Domyślnie pokazujemy zakończone zbiórki
      collections: [
        {
          id: 1,
          name: "Zbiórka 1",
          goal: 500,
          status: "Aktywna",
          description: "Pomoc dla dzieci.",
          image:
            "https://www.investopedia.com/thmb/u220LqqeStsaBPgVITIKYKTMOic=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/GettyImages-200275642-001-576a033e5f9b58346aace876.jpg",
        },
        {
          id: 2,
          name: "Zbiórka 2",
          goal: 1000,
          status: "Zakończona",
          description: "Wsparcie dla schroniska.",
          image: "https://via.placeholder.com/150",
        },
        {
          id: 3,
          name: "Zbiórka 3",
          goal: 800,
          status: "Aktywna",
          description: "Pomoc dla zwierząt.",
          image: "https://via.placeholder.com/150",
        },
      ],
      members: [
        {
          id: 1,
          name: "Jan Kowalski",
          avatar:
            "https://static.vecteezy.com/system/resources/previews/009/292/244/non_2x/default-avatar-icon-of-social-media-user-vector.jpg",
        },
        {
          id: 2,
          name: "Agnieszka Nowak",
          avatar:
            "https://static.vecteezy.com/system/resources/previews/009/292/244/non_2x/default-avatar-icon-of-social-media-user-vector.jpg",
        },
        {
          id: 3,
          name: "Kamil Zieliński",
          avatar:
            "https://static.vecteezy.com/system/resources/previews/009/292/244/non_2x/default-avatar-icon-of-social-media-user-vector.jpg",
        },
      ],
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
  },
  created() {
    const classItemData = this.$route.params.classItem; // Pobieramy dane z URL
    if (classItemData) {
      this.classItem = JSON.parse(classItemData); // Dekodujemy dane JSON
    }
  },
  methods: {
    moveToHome() {
      this.$router.push({ name: "home" });
    },
    AddStudent(classId) {
      console.log(`Dodano członka do klasy o id ${classId}`);
    },
    AddFoundrise(classId) {
      console.log(`Dodano zbiórkę do klasy o id ${classId}`);
    },
  },
};
</script>
