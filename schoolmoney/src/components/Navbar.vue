<template>
  <div class="navbar">
    <div class="left">SchoolMoney</div>
    <div class="right" v-if="showLogout">
      <div class="profile">
        <span>{{ userName }}</span>

        <svg
          @click="moveToProfile"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="w-6 h-6 profile-icon"
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
        class="w-6 h-6 logout-icon cursor-pointer"
        style="transform: rotate(0deg);"
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
import { getUserFirstName, getUserLastName } from "@/api/user";
import { computed } from "vue";

export default {
  setup() {
    const route = useRoute();
    const router = useRouter();

    const showLogout = computed(() => route.name === "Home");
    const userName = computed(
      () => `${getUserFirstName() || ""} ${getUserLastName() || ""}`.trim()
    );


    const logout = () => {
      router.push("/");
      clearToken();
    };

    const moveToProfile = () => {
      router.push("/profile");
    };

    return {
      showLogout,
      userName,
      logout,
      moveToProfile
    };
  },
};
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #ffffff;
  border-bottom: 1px solid #eaeaea;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.left {
  font-size: 20px;
  font-weight: bold;
}

.right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.profile {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  color: #333333;
}

.profile-icon {
  width: 24px;
  height: 24px;
}

.right button {
  background-color: transparent;
  border: none;
  color: #007bff;
  font-size: 16px;
  cursor: pointer;
}

.right button:hover {
  text-decoration: underline;
}
</style>
