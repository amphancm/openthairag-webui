<template>
  <div class="h-full flex flex-col p-4">
    <div class="bg-slate-500 h-12 w-full flex items-center justify-between">
      <h3>Edit Accounts</h3>
      <div class="float-end mt-4">
          <button class="bg-slate-600 p-2 rounded-md text-white" @click="isModalOpen = true">Change Password</button>
        </div>
    </div>
    <div class="flex parent overflow-y-auto mt-4">
      <div class="overflow-x-auto w-full">
        <div class="flex">
          <div class="w-40 flex items-center text-left">
            <h4 for="username" class="text-black">Username</h4>
          </div>
          <div class="flex-4 w-full">
            <input
              v-model="account.username"
              type="text"
              id="username"
              class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Enter username"
            />
          </div>
        </div>

        <div class="flex mt-4">
          <div class="w-40 flex text-left py-2">
            <h4 for="email" class="text-black">Email</h4>
          </div>
          <div class="flex-4 w-full">
            <input
              v-model="account.email"
              type="text"
              id="email"
              class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Enter email"
            />
          </div>
        </div>

        <div class="flex mt-4">
          <div class="w-40 flex text-left py-2">
            <h4 for="role" class="text-black">Role</h4>
          </div>
          <div class="flex-4 w-full">
            <select
              v-model="account.role"
              id="role"
              class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            >
              <option value="" disabled selected>Select role</option>
              <option value="admin">Admin</option>
              <option value="editor">Editor</option>
              <option value="viewer">Viewer</option>
            </select>
          </div>
        </div>
        <div class="float-end mt-4">
          <button class="bg-red-600 p-4 rounded-md text-white" @click="handleSave">Save</button>
        </div>
      </div>
    </div>
    <div
      v-if="isLoading"
      class="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50 z-50"
    >
      <div class="loading">Loading...</div>
    </div>

    <Modal
      :isOpen="isModalOpen"
      title="Change Password"
      @close="isModalOpen = false"
      :isAlert="true"
      @confirm="chagePassword"
    >
      <template #body>
        <!-- <p>Are you sure?</p> -->
         <div class="mb-4">
          <div class="w-40 flex text-left py-2">
            <h4 for="password" class="text-black">Password</h4>
          </div>
          <div class=" w-full mb-4">
            <input
              v-model="password"
              type="password"
              id="password"
              class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Enter password"
            />
          </div>
          <div class=" w-full">
            <input
              v-model="verifyPassword"
              type="password"
              id="password"
              class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Enter verify password"
            />
          </div>
        </div>
      </template>
    </Modal>


  </div>
</template>

<script lang="ts" setup>
import { useAccountStore } from '@/stores/accounts'
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import router from '@/router'
import Modal from '../components/CustomModal.vue'

const route = useRoute()
const id = Array.isArray(route.params.id) ? route.params.id[0] : route.params.id

const accountStore = useAccountStore()
const accounts = computed(() => accountStore.accounts)
const account = ref<{
  id: string;
  username: string;
  email: string;
  role: string;
}>({
  id: '',
  username: '',
  email: '',
  role: '',
})


const password = ref('')
const verifyPassword = ref('')

const isLoading = ref(false)
const isModalOpen = ref(false)
// Form data

onMounted(async () => {
  account.value = await accountStore.fetchDetailAccounts(id)
})

// Function to create a new account
async function handleSave() {
  isLoading.value = true
  try {
    await accountStore.saveAccount(account.value)
  } catch (error) {
    console.error('Error deleting account:', error)
  } finally {
    isLoading.value = false
  }
  // Clear form after creation
  router.push('/settings/account')
}

async function chagePassword() {
  isLoading.value = true
  try {
    if(password.value !== verifyPassword.value){
      alert('Password not match')
      return
    }
    await accountStore.changePasswordAccount(password.value, id)
  } catch (error) {
    console.error('Error deleting account:', error)
  } finally {
    isLoading.value = false
  }
  // Clear form after creation
  router.push('/settings/account')
}
</script>
