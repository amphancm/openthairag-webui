<template>
  <div class="h-full flex flex-col p-4">
    <div class="bg-slate-500 h-12 w-full flex items-center">
      <h3>Edit Feedback</h3>
    </div>
    <div class="flex parent overflow-y-auto mt-4">
      <div class="overflow-x-auto w-full">
        <div class="flex">
          <div class="w-40 flex items-center text-left">
            <h4 for="title" class="text-black">Name</h4>
          </div>
          <div class="flex-4 w-full">
            <input
              v-model="issue.name"
              type="text"
              id="title"
              class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Enter title"
            />
          </div>
        </div>
        
        <div class="flex mt-4">
          <div class="w-40 flex text-left py-2">
            <h4 for="title" class="text-black">User name</h4>
          </div>
          <div class="flex-4 w-full">
            <input
              v-model="issue.user_name"
              type="text"
              id="title"
              class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Enter title"
            />
          </div>
        </div>

        <div class="flex mt-4">
          <div class="w-40 flex text-left py-2">
            <h4 for="title" class="text-black">Detail</h4>
          </div>
          <div class="flex-4 w-full">
            <textarea
              v-model="issue.detail"
              rows="4"
              type="text"
              id="title"
              class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Enter title"
            />
          </div>
        </div>

        <div class="float-end mt-4">
          <button class="bg-green-600 p-4 rounded-md text-white" @click="handleUpdate">Submit</button>
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
import { useIssueStore } from '@/stores/issues'
import { Icon } from '@iconify/vue/dist/iconify.js'
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const id = route.params.id as string
const pictures = ref<string[]>([])
const issueStore = useIssueStore()

const issues = computed(() => issueStore.issues)
 
const issue = ref<{
  id: string;
  name: string;
  detail: string;
  user_name: string;
}>({
  id: '',
  name: '',
  detail: '',
  user_name: '',
})

onMounted(async () => {
  const prod = issues.value[id]
  console.log("issue :", prod)
  if (prod) {
    issue.value = {
      id: prod['id'],
      name: String(prod['name']),
      detail: String(prod['detail']),
      user_name: String(prod['user_name']),
    }
  } else {
    const fetchedIssue = await issueStore.detailIssue(id)
    if (fetchedIssue) {
      console.log('fetchedIssue :', fetchedIssue)
    }
    issue.value = {
      id: fetchedIssue.data.id || '',
      name: fetchedIssue.data.name || '',
      detail: fetchedIssue.data.detail || '',
      user_name: fetchedIssue.data.user_name || '',
    }

  }
})

const isLoading = ref(false)
const newIssue = ref<{ 
  id: string; 
  name: string; 
  detail: string; 
  user_name: string; 
}>({ 
  id: '', 
  name: '', 
  detail: '', 
  user_name: '', 
})


async function handleUpdate() {
  isLoading.value = true
  try {
    await issueStore.saveIssue(issue.value)
  } catch (error) {
    console.error('Error deleting issue:', error)
  } finally {
    isLoading.value = false
  }
  newIssue.value = { 
    id: '', 
    name: '', 
    detail: '', 
    user_name: '', 
  }
  router.push('/issues')
}


</script>
<style scoped>
img {
  border: 1px solid #ddd;
}
</style>