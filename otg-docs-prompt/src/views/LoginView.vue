<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center">
    <div class="w-full max-w-md bg-white rounded-lg shadow-md p-6">
      <h2 class="text-2xl font-semibold text-gray-800 text-center mb-6">Login</h2>
      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
          <input
            v-model="username"
            type="text"
            id="username"
            class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="Enter your username"
            required
          />
        </div>
        <div class="mb-4">
          <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
          <input
            v-model="password"
            type="password"
            id="password"
            class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="Enter your password"
            required
          />
        </div>
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center">
            <input
              v-model="remember"
              type="checkbox"
              id="remember"
              class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
            />
            <label for="remember" class="ml-2 block text-sm text-gray-900">Remember me</label>
          </div>
        </div>
        <button
          type="submit"
          class="w-full bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 focus:outline-none"
        >
          Login
        </button>
      </form>
    </div>
  </div>
</template>
  
<script lang="ts" setup>
  import router from "@/router";
  import { useAuthenticationStore } from "@/stores/authentication";
  import { onMounted, ref } from "vue";
  
  const username = ref("");
  const password = ref("");
  const remember = ref(false);
  const authenticationStore = useAuthenticationStore()
    
  onMounted(() => {
    const token = ref(localStorage.getItem("token"));
    if (token.value) {
      router.push({ path: "/" }).catch((err) => console.error(err));
    }
  });
  const handleLogin = async () => {
    localStorage.removeItem("token")
    await authenticationStore.login({
      username: username.value,
      password: password.value,
      remember: remember.value
    })

    const token = ref(localStorage.getItem("token"));
    console.log(token.value);
    if (token.value) {
      await authenticationStore.getProfile();
      location.reload();
      // 
      
    } else {
      // If token does not exist, log an error or redirect to login
      console.error("Token is missing in localStorage.");
      router.push({ path: "/login" }).catch((err) => console.error(err));
    }
  };
</script>

<style scoped>
/* Add any custom styles here */
</style>