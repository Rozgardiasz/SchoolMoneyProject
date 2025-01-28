<template>
  <div class="flex justify-between items-center px-5 py-3 bg-white border-b shadow">
    <div class="flex items-center gap-2 cursor-pointer" @click="moveToHome">
      <img
        :src="logo"
        alt="SchoolMoney Logo"
        class="w-8 h-8 object-contain"
      />
      <div class="text-lg font-bold text-gray-800">SchoolMoney</div>
    </div>
    <div class="flex items-center gap-3" v-if="showLogout">
      <div class="flex items-center gap-2 text-gray-800">
        <span>{{ userName }}</span>
        <svg
          @click="moveToProfile"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="w-6 h-6 cursor-pointer"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M15.75 9A3.75 3.75 0 1112 5.25 3.75 3.75 0 0115.75 9zM19.5 20.25A6.75 6.75 0 006.75 20.25v-.375a4.125 4.125 0 014.125-4.125h4.25a4.125 4.125 0 014.125 4.125v.375z"
          />
        </svg>
      </div>
      <svg
        @click="logout"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="1.5"
        stroke="currentColor"
        class="w-6 h-6 cursor-pointer"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M15.75 9V5.25a2.25 2.25 0 10-4.5 0V9m4.5 0h2.25a2.25 2.25 0 012.25 2.25v4.5a2.25 2.25 0 01-2.25 2.25H6.75a2.25 2.25 0 01-2.25-2.25v-4.5A2.25 2.25 0 016.75 9h2.25m4.5 0v6"
        />
      </svg>
    </div>
  </div>
</template>

<script>
import { useRoute, useRouter } from "vue-router";
import { clearToken } from "@/api/auth";
import { clearUserData, getUserFirstName, getUserLastName } from "@/api/user";
import { computed } from "vue";
import logoPng from "../assets/Logo_png.png"; 

export default {
  setup() {
    const route = useRoute();
    const router = useRouter();

    const showLogout = computed(() => route.name === "Home" || route.name === "Profile" || route.name === "ClassPage");
    const userName = computed(
      () => `${getUserFirstName() || ""} ${getUserLastName() || ""}`.trim()
    );

    const logout = () => {
      router.push("/");
      clearToken();
      clearUserData(); // Fixed function call
    };

    const moveToProfile = () => {
      router.push("/profile");
    };

    const moveToHome = () => {
      router.push("/Home");
    };

    return {
      logo: logoPng, // Add logo to the returned setup object
      showLogout,
      userName,
      logout,
      moveToProfile,
      moveToHome,
    };
  },
};
</script>
