<template>
  <div class="h-full flex flex-col p-4">
    <div class="bg-slate-500 h-12 w-full flex items-center">
      <h3>Create Account</h3>
    </div>
    <div class="flex parent overflow-y-auto mt-4">
      <div class="overflow-x-auto w-full">
        <div class="flex">
          <div class="w-40 flex items-center text-left">
            <h4 for="username" class="text-black">Username</h4>
          </div>
          <div class="flex-4 w-full">
            <input
              v-model="newAccount.username"
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
              v-model="newAccount.email"
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
              v-model="newAccount.role"
              id="role"
              class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            >
              <option value="" disabled selected>Select role</option>
              <option value="admin">Admin</option>
              <option value="editor">Editor</option>
              <option value="viewer">Chatter</option>
            </select>
          </div>
        </div>

        <div class="flex mt-4">
          <div class="w-40 flex text-left py-2">
            <h4 for="password" class="text-black">Password</h4>
          </div>
          <div class="flex-4 w-full">
            <input
              v-model="newAccount.password"
              type="password"
              id="password"
              class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Enter Password"
            />
          </div>
        </div>

        <div class="flex mt-4">
          <div class="w-40 flex text-left py-2">
            <h4 for="confirmPassword" class="text-black">Confirm Password</h4>
          </div>
          <div class="flex-4 w-full">
            <input
              v-model="newAccount.confirmPassword"
              type="password"
              id="confirmPassword"
              class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Enter Confirm Password"
            />
          </div>
        </div>
        <div class="float-end mt-4">
          <button class="bg-red-600 p-4 rounded-md text-white" @click="handleCreate">Submit</button>
        </div>
      </div>
    </div>
    <div
      v-if="isLoading"
      class="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50 z-50"
    >
      <div class="loading">Loading...</div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import router from '@/router'
import { useAccountStore } from '@/stores/accounts'
import { ref } from 'vue'

const documentStore = useAccountStore()
const isLoading = ref(false)

const newAccount = ref({ 
  username: '', 
  email: '', 
  role: '',
  password: '',
  confirmPassword: ''
 })

async function handleCreate() {
  isLoading.value = true
  try {
    await documentStore.createAccount(newAccount.value)
  } catch (error) {
    console.error('Error deleting document:', error)
  } finally {
    isLoading.value = false
  }
  newAccount.value = { 
    username: '', 
    email: '', 
    role: '',
    password: '',
    confirmPassword: ''
   }
  router.push('/settings/account')
}
</script>
