<template>
  <div class="h-full flex flex-col p-4">
    <div class="bg-slate-500 h-12 w-full flex items-center">
      <h3>Edit Documents</h3>
    </div>
    <div class="flex parent overflow-y-auto mt-4">
      <div class="overflow-x-auto w-full">
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
          <div class="w-40 flex text-left py-4">
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
  </div>
</template>

<script lang="ts" setup>
import { useDocumentStore } from '@/stores/documents'
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import router from '@/router'

const route = useRoute()
const id = route.params.id

const documentStore = useDocumentStore()
const documents = computed(() => documentStore.documents)
const document = computed(() => documents.value[id as string])
const isLoading = ref(false)
// Form data
const newDoc = ref({
  id: document.value.id,
  title: document.value.title,
  content: document.value.content,
  doc_id: document.value.doc_id,
})

// Function to create a new document
async function handleSave() {
  isLoading.value = true
  try {
    await documentStore.saveDocument(newDoc.value)
  } catch (error) {
    console.error('Error deleting document:', error)
  } finally {
    isLoading.value = false
  }
  // Clear form after creation
  router.push('/docs')
}
</script>
