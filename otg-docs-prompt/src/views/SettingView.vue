<template>
  <div class="h-full flex flex-col p-4">
    <div class="bg-slate-500 h-12 w-full flex items-center">
      <h3>Setting</h3>
    </div>
    <div class="flex parent overflow-y-auto mt-4">
      <div class="overflow-x-auto w-full">
        <div class="flex mt-4">
          <div class="w-72 flex text-left items-center">
            <h4 for="title" class="text-black">Line Issue Key</h4>
          </div>
          <div class="flex-4 w-full">
            <input
              v-model="setting.line_key"
              id="content"
              rows="4"
              class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Enter Line API Key "
            />
          </div>
        </div>

        <div class="flex mt-4">
          <div class="w-72 flex text-left items-center">
            <h4 for="title" class="text-black">Line Secret Channel Key</h4>
          </div>
          <div class="flex-4 w-full">
            <input
              v-model="setting.line_secret"
              id="content"
              rows="4"
              class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Enter Secret Channel Key"
            />
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

  </div>

</template>

<script lang="ts" setup>
import { useSettingStore } from '@/stores/setting'
import { computed, onMounted, ref } from 'vue'

const settingStore = useSettingStore()
const setting = computed(() => settingStore.Settings)
const isLoading = ref(false)
const isSuccess = ref(false)

onMounted(async () => {
  await settingStore.fetchSettings()
})

function openModal() {
  isSuccess.value = true;
}
function closeModal() {
  isSuccess.value = false;
}

async function handleSave() {
  if (!setting.value.id) {
    await settingStore.createSetting({
      line_key: setting.value.line_key,
      line_secret: setting.value.line_secret,
    })
    openModal()
  } else {
    isLoading.value = true
    try {
      await settingStore.saveSetting({
        id: setting.value.id,
        line_key: setting.value.line_key,
        line_secret: setting.value.line_secret,
      })
    } catch (error) {
      console.error('Error deleting document:', error)
    } finally {
      isLoading.value = false
      openModal()
    }
  }
}
</script>
