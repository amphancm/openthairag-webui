<template>
  <div class="h-full flex flex-col p-4">
    <div class="bg-slate-500 h-12 w-full flex items-center">
      <h3>Documents</h3>
    </div>
    <div class="flex parent overflow-y-auto mt-4">
      <div class="overflow-x-auto">
        <div class="float-end mb-6">
          <button
            class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
            @click="handleCreate"
          >
            Create
          </button>
        </div>
        <table class="w-full border border-gray-200 rounded-lg overflow-hidden">
          <thead>
            <tr class="bg-gray-100">
              <th class="text-left p-3 border border-gray-300 w-36">Title</th>
              <th class="text-left p-3 border border-gray-300">Content</th>
              <th class="text-center p-3 border border-gray-300 w-48">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              class="hover:bg-gray-50 bg-gray-400"
              v-for="(doc, index) in Object.values(documents)"
              :key="index"
            >
              <td class="p-3 border border-gray-300">
                <p class="truncate w-36">{{ doc.title }}</p>
              </td>
              <td class="p-3 border border-gray-300">
                <p class="truncate whitespace-pre line-clamp-1 w-[500px]">
                  {{ doc.content }}
                </p>
              </td>
              <td class="p-3 border border-gray-300 text-center space-x-2">
                <button
                  @click="handleEdit(doc.id)"
                  class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                >
                  Edit
                </button>
                <button
                  @click="handleDelete(doc.id)"
                  class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
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
import { computed, onMounted, ref } from 'vue'
import { Icon } from '@iconify/vue'
import router from '@/router'

import { useDocumentStore } from '@/stores/documents'

const isLoading = ref(false)

const documentStore = useDocumentStore()

const documents = computed(() => documentStore.documents)

onMounted(() => {
  documentStore.fetchDocuments()
})

function handleEdit(id: string) {
  router.push({ name: 'editing-docs', params: { id: id } }).catch((err) => console.error(err))
}

function handleCreate() {
  router.push({ name: 'create-doc' }).catch((err) => console.error(err))
}

// Function to create a new document
async function handleDelete(id: string) {
  isLoading.value = true
  try {
    await documentStore.deleteDocument(id)
  } catch (error) {
    console.error('Error deleting document:', error)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.assistant {
  @apply bg-white w-1/2 rounded-md p-2 mb-4 text-wrap;
  width: fit-content;
  max-width: 50%;
  word-wrap: break-word; /* Ensures long words are wrapped */
  overflow-wrap: break-word; /* Modern equivalent for wrapping text */
  white-space: normal;
}

.user {
  @apply bg-white w-1/2 rounded-md p-2 mb-4 text-wrap;
  margin-left: auto; /* Align to the right */
  width: fit-content;
  max-width: 50%;
  word-wrap: break-word;
  overflow-wrap: break-word;
  white-space: normal;
}

/* The typewriter cursor effect */
@keyframes blink-caret {
  from,
  to {
    border-color: transparent;
  }
  50% {
    border-color: orange;
  }
}

.parent {
  @apply flex flex-col justify-end;
}
.loading {
  text-align: center;
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
}

.loader {
  text-align: center;
}
.loader span {
  display: inline-block;
  vertical-align: middle;
  width: 10px;
  height: 10px;
  background: black;
  border-radius: 20px;
  animation: loader 0.8s infinite alternate;
}
.loader span:nth-of-type(2) {
  animation-delay: 0.2s;
}
.loader span:nth-of-type(3) {
  animation-delay: 0.6s;
}
@keyframes loader {
  0% {
    opacity: 0.9;
    transform: scale(0.5);
  }
  100% {
    opacity: 0.1;
    transform: scale(1);
  }
}
</style>
