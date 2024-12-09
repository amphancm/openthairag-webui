<template>
  <div class="h-full flex flex-col p-4">
    <div class="bg-slate-500 h-12 w-full flex items-center">
      <h3>System Prompt Default</h3>
    </div>
    <div class="flex parent overflow-y-auto mt-4">
      <div class="overflow-x-auto w-full">
        <div class="flex mt-4">
          <div class="w-40 flex text-left items-center">
            <h4 for="title" class="text-black">Temerature</h4>
          </div>
          <div class="flex-4 w-full">
            <input
              type="number"
              @input="validateInput"
              v-model="system_prompt.temperature"
              id="content"
              rows="4"
              class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Enter Temperature"
            />
          </div>
        </div>

        <div class="flex mt-4">
          <div class="w-40 flex text-left py-2">
            <h4 for="title" class="text-black">System Prompt</h4>
          </div>
          <div class="flex-4 w-full">
            <textarea
              v-model="system_prompt.content"
              id="content"
              rows="4"
              class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 h-[500px]"
              placeholder="Enter System Prompt"
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

  <div
      v-if="isSuccess"
      class="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white rounded-lg shadow-lg p-6 w-96">
        <h2 class="text-lg font-semibold text-green-600">Success!</h2>
        <p class="mt-2 text-gray-600">
          Your operation was completed successfully.
        </p>
        <div class="flex justify-end mt-4">
          <button
            @click="closeModal"
            class="bg-green-600 text-white py-2 px-4 rounded hover:bg-green-700"
          >
            OK
          </button>
        </div>
      </div>
    </div>

</template>

<script lang="ts" setup>
import { useSystemPromptStore } from '@/stores/systemPrompt'
import { computed, onMounted, ref } from 'vue'

const systemPromptStore = useSystemPromptStore()
const system_prompt = computed(() => systemPromptStore.systemPrompts)
const isLoading = ref(false)
const isSuccess = ref(false)

onMounted(async () => {
  await systemPromptStore.fetchSystemPrompts()
})

function openModal() {
  isSuccess.value = true;
}
function closeModal() {
  isSuccess.value = false;
}

function validateInput() {
  const value = parseFloat(system_prompt.value.temperature);

  if (value < 0 || value > 1 || isNaN(value)) {
    system_prompt.value.temperature = ''; // Reset invalid input
  }
}

async function handleSave() {
  if (!system_prompt.value.id) {
    await systemPromptStore.createSystemPrompt({
      content: system_prompt.value.content,
      temperature: system_prompt.value.temperature,
    })
    openModal()
  } else {
    isLoading.value = true
    try {
      await systemPromptStore.saveSystemPrompt({
        id: system_prompt.value.id,
        content: system_prompt.value.content,
        temperature: system_prompt.value.temperature,
      })
    } catch (error) {
      console.error('Error deleting document:', error)
    } finally {
      openModal()
      isLoading.value = false
    }
  }
}
</script>
