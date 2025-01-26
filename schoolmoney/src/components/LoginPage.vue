<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="max-w-md w-full p-6 rounded-2xl shadow-lg bg-white">
      <h2 class="text-2xl font-bold text-center mb-4">Logowanie</h2>
      <div class="space-y-4">
        <input
          v-model="email"
          type="email"
          placeholder="Adres email"
          class="w-full p-2 border rounded-xl"
        />
        <input
          v-model="password"
          type="password"
          placeholder="Hasło"
          class="w-full p-2 border rounded-xl"
        />
        <button
          @click="handleLogin"
          class="w-full bg-blue-500 text-white hover:bg-blue-600 p-2 rounded-2xl"
        >
          Zaloguj się
        </button>
        <p v-if="errorMessage" class="text-center text-sm text-red-500">{{ errorMessage }}</p>
        <p class="text-center text-sm text-gray-500">Nie masz konta?</p>
        <button
          @click="handleRegister"
          class="w-full bg-gray-200 text-black hover:bg-gray-300 p-2 rounded-2xl"
        >
          Zarejestruj się
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { login, setToken, fetchUserDetails } from '@/api/auth';

export default {
  setup() {
    const email = ref('');
    const password = ref('');
    const errorMessage = ref('');
    const router = useRouter();

    const handleLogin = async () => {
      errorMessage.value = '';
      try {
        const data = await login(email.value, password.value);
        setToken(data.access_token);
        fetchUserDetails(data.access_token);
        router.push('/home');
      } catch (error) {
        errorMessage.value = error.message;
      }
    };

    const handleRegister = () => {
      router.push('/register');
    };

    return {
      email,
      password,
      errorMessage,
      handleLogin,
      handleRegister,
    };
  },
};
</script>

<style scoped>
.min-h-screen {
  min-height: 100vh;
}
</style>
