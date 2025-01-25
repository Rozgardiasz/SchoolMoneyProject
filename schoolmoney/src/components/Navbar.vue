<template>
    <div class="navbar">
      <div class="left">SchoolMoney</div>
      <div class="right" v-if="showLogout">
        <button @click="logout">Wyloguj</button>
      </div>
    </div>
  </template>
  
  <script>
  import { useRoute, useRouter } from 'vue-router';
  
  export default {
    setup() {
      const route = useRoute();
      const router = useRouter();
  
      const showLogout = route.name === 'Home';
  
      const logout = () => {
        router.push('/');
      };
  
      return {
        showLogout,
        logout,
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