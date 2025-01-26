<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="max-w-md w-full p-6 rounded-2xl shadow-lg bg-white">
      <h2 class="text-2xl font-bold text-center mb-4">Rejestracja</h2>
      <div class="space-y-4">
        <input
          v-model="firstName"
          :class="{'border-red-500': missingFields.includes('firstName')}"
          type="text"
          placeholder="Imię"
          class="w-full p-2 border rounded-xl"
        />
        <input
          v-model="lastName"
          :class="{'border-red-500': missingFields.includes('lastName')}"
          type="text"
          placeholder="Nazwisko"
          class="w-full p-2 border rounded-xl"
        />
        <input
          v-model="email"
          :class="{'border-red-500': missingFields.includes('email') || (emailTouched && !isValidEmail)}"
          type="email"
          placeholder="Adres email"
          class="w-full p-2 border rounded-xl"
          @blur="emailTouched = true"
        />
        <input
          v-model="password"
          :class="{'border-red-500': missingFields.includes('password')}"
          type="password"
          placeholder="Hasło"
          class="w-full p-2 border rounded-xl"
        />
        <input
          v-model="confirmPassword"
          :class="{'border-red-500': missingFields.includes('confirmPassword') || (confirmPasswordTouched && !arePasswordsMatching)}"
          type="password"
          placeholder="Powtórz hasło"
          class="w-full p-2 border rounded-xl"
          @blur="confirmPasswordTouched = true"
        />
        <button
          @click="handleRegister"
          class="w-full bg-blue-500 text-white hover:bg-blue-600 p-2 rounded-2xl"
        >
          Zarejestruj się
        </button>
        <p v-if="errorMessage" class="text-red-500 text-sm text-center">{{ errorMessage }}</p>
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
import { registerUser, login, fetchUserDetails } from '@/api/auth'; 

export default {
  setup() {
    const firstName = ref('');
    const lastName = ref('');
    const email = ref('');
    const password = ref('');
    const confirmPassword = ref('');
    const emailTouched = ref(false);
    const confirmPasswordTouched = ref(false);
    const missingFields = ref([]);
    const errorMessage = ref('');
    const router = useRouter();

    const isValidEmail = () => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value);

    const arePasswordsMatching = () => password.value === confirmPassword.value;

    const handleRegister = async () => {
      errorMessage.value = '';
      missingFields.value = [];

      if (!firstName.value) missingFields.value.push('firstName');
      if (!lastName.value) missingFields.value.push('lastName');
      if (!email.value) missingFields.value.push('email');
      if (!password.value) missingFields.value.push('password');
      if (!confirmPassword.value) missingFields.value.push('confirmPassword');

      if (missingFields.value.length > 0) {
        errorMessage.value = 'Uzupełnij brakujące pola.';
        return;
      }

      if (!isValidEmail()) {
        emailTouched.value = true;
        errorMessage.value = 'Adres email jest niepoprawny.';
        return;
      }

      if (!arePasswordsMatching()) {
        confirmPasswordTouched.value = true;
        errorMessage.value = 'Hasła nie są takie same.';
        return;
      }

      try {
        await registerUser(
          firstName.value, 
          lastName.value,
          email.value,
          password.value
        );
        const loginResponse = await login(email.value, password.value);
        if (loginResponse) {
          fetchUserDetails(loginResponse.access_token);
          router.push('/home');
        }
      } catch (error) {
        errorMessage.value = error.message;
      }
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
      emailTouched,
      confirmPasswordTouched,
      missingFields,
      errorMessage,
      handleRegister,
      handleLogin,
      isValidEmail,
      arePasswordsMatching,
    };
  },
};
</script>

<style scoped>
.min-h-screen {
  min-height: 100vh;
}
.border-red-500 {
  border-color: #f87171;
}
</style>
