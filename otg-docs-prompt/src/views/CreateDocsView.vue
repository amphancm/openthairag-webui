<template>
  <div class="h-full flex flex-col p-4">
    <div class="bg-slate-500 h-12 w-full flex items-center">
      <h3>Create Document</h3>
    </div>
    <div class="flex parent overflow-y-auto mt-4">
      <div class="overflow-x-auto w-full">
        <input type="file" @change="handleFileUpload" class="mt-2 mb-4 p-2 border rounded-md">
        <div class="flex">
          <div class="w-40 flex items-center text-left">
            <h4 for="title" class="text-black">Title</h4>
          </div>
          <div class="flex-4 w-full">
            <input
              v-model="newDoc.title"
              type="text"
              id="title"
              class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Enter title"
            />
          </div>
        </div>

        <div class="flex mt-4">
          <div class="w-40 flex text-left py-2">
            <h4 for="title" class="text-black">Content</h4>
          </div>
          <div class="flex-4 w-full">
            <textarea
              v-model="newDoc.content"
              id="content"
              rows="4"
              class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 h-[500px]"
              placeholder="Enter content"
            ></textarea>
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
import { useDocumentStore } from '@/stores/documents'
import { ref } from 'vue'

const documentStore = useDocumentStore()
const isLoading = ref(false)

const newDoc = ref({ title: '', content: '' })

async function handleCreate() {
  isLoading.value = true
  try {
    await documentStore.createDocument(newDoc.value)
  } catch (error) {
    console.error('Error deleting document:', error)
  } finally {
    isLoading.value = false
  }
  newDoc.value = { title: '', content: '' }
  router.push('/docs')
}

async function handleFileUpload(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]

  if (file) {
    newDoc.value.title = file.name
    const reader = new FileReader()
    reader.onload = (e) => {
      newDoc.value.content = e.target?.result as string
    }
    reader.onerror = (e) => {
      console.error('File reading error:', e)
      newDoc.value.content = 'Error reading file content.'
    }
    reader.readAsText(file)
  }
}
</script>
