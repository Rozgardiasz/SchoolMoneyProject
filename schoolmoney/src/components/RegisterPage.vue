<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="max-w-md w-full p-6 rounded-2xl shadow-lg bg-white">
      <h2 class="text-2xl font-bold text-center mb-4">Rejestracja</h2>
      <div class="space-y-4">
        <input
          v-model="firstName"
          type="text"
          placeholder="Imię"
          class="w-full p-2 border rounded-xl"
        />
        <input
          v-model="lastName"
          type="text"
          placeholder="Nazwisko"
          class="w-full p-2 border rounded-xl"
        />
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
        <input
          v-model="confirmPassword"
          type="password"
          placeholder="Powtórz hasło"
          class="w-full p-2 border rounded-xl"
        />
        <button
          @click="handleRegister"
          class="w-full bg-blue-500 text-white hover:bg-blue-600 p-2 rounded-2xl"
        >
          Zarejestruj się
        </button>
        <p class="text-center text-sm text-gray-500">Masz już konto?</p>
        <button
          @click="handleLogin"
          class="w-full bg-gray-200 text-black hover:bg-gray-300 p-2 rounded-2xl"
        >
          Zaloguj się
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const firstName = ref('');
    const lastName = ref('');
    const email = ref('');
    const password = ref('');
    const confirmPassword = ref('');
    const router = useRouter();

    const handleRegister = () => {
      console.log({ firstName, lastName, email, password, confirmPassword });
    };

    const handleLogin = () => {
      router.push('/');
    };

    return {
      firstName,
      lastName,
      email,
      password,
      confirmPassword,
      handleRegister,
      handleLogin,
    };
  },
};
</script>

<style scoped>
.min-h-screen {
  min-height: 100vh;
}
</style>
