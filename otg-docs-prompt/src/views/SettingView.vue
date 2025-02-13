<template>
  <div class="h-full flex flex-col p-4">
    <div class="bg-slate-500 h-12 w-full flex items-center">
      <h3>Setting</h3>
    </div>
    <div class="flex parent overflow-y-auto mt-4">
      <div class="overflow-x-auto w-full">
        <div>
          <h1>Line bot Setting</h1>
          <div class="flex mt-4">
            <div class="flex items-center justify-center mt-4">
              <label class="relative inline-flex cursor-pointer items-center">
                <input id="switch-3" type="checkbox" class="peer sr-only" v-model="isLineTokenEnabled" />
                <label for="switch-3" class="hidden"></label>
                <div class="peer h-4 w-11 rounded border bg-slate-200 after:absolute after:-top-1 after:left-0 after:h-6 after:w-6 after:rounded-md after:border after:border-gray-300 after:bg-white after:transition-all after:content-[''] peer-checked:bg-green-300 peer-checked:after:translate-x-full peer-focus:ring-green-300"></div>
              </label>
              <h4 class="ml-3  text-gray-900">Enable Line Issue Token</h4>
            </div>
          </div>

          <div v-if="isLineTokenEnabled">
            <div class="flex mt-4">
              <div class="w-72 flex text-left items-center">
                <h4 for="title" class="text-black">Line Issue Token</h4>
              </div>
              <div class="flex-4 w-full">
                <input
                  v-model="settingStore.Settings.line_key"
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
                  v-model="settingStore.Settings.line_secret"
                  id="content"
                  rows="4"
                  class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  placeholder="Enter Secret Channel Key"
                />
              </div>
            </div>
          </div>
        </div>

        <div class="pt-8">
          <h1>facebook bot Setting</h1>
          <div class="flex mt-4">
            <div class="flex items-center justify-center mt-4">
              <label class="relative inline-flex cursor-pointer items-center">
                <input id="switch-3" type="checkbox" class="peer sr-only" v-model="isFacebookTokenEnabled" />
                <label for="switch-3" class="hidden"></label>
                <div class="peer h-4 w-11 rounded border bg-slate-200 after:absolute after:-top-1 after:left-0 after:h-6 after:w-6 after:rounded-md after:border after:border-gray-300 after:bg-white after:transition-all after:content-[''] peer-checked:bg-green-300 peer-checked:after:translate-x-full peer-focus:ring-green-300"></div>
              </label>
              <h4 class="ml-3 text-gray-900 mr-4">Enable Facebook Issue Token</h4>
            </div>
          </div>

          <div v-if="isFacebookTokenEnabled">
            <div class="flex mt-4">
              <div class="w-72 flex text-left items-center">
                <h4 for="title" class="text-black">Facebook Token</h4>
              </div>
              <div class="flex-4 w-full">
                <input
                  v-model="settingStore.Settings.facebook_token"
                  id="content"
                  rows="4"
                  class="w-full mt-1 pdcsax-3 p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  placeholder="Enter Facebook Token"
                />
              </div>
            </div>

            <div class="flex mt-4">
              <div class="w-72 flex text-left items-center">
                <h4 for="title" class="text-black">Password Verify</h4>
              </div>
              <div class="flex-4 w-full flex">
                <input
                  v-model="settingStore.Settings.facebook_verify_password"
                  id="content"
                  rows="4"
                  class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  placeholder="Password Verify"
                />
                <button @click="generateFacebookPassword()" class="bg-green-600 p-4 rounded-md text-white ml-4">Generate</button>
              </div>
            </div>
          </div>
        </div>

        <div class="pt-8">
          <h1>Greeting Mode</h1>
          <div class="flex mt-4">
            <div class="flex items-center justify-center mt-4">
              <label class="relative inline-flex cursor-pointer items-center">
                <input id="switch-3" type="checkbox" class="peer sr-only" v-model="isGreetingEnabled" />
                <label for="switch-3" class="hidden"></label>
                <div class="peer h-4 w-11 rounded border bg-slate-200 after:absolute after:-top-1 after:left-0 after:h-6 after:w-6 after:rounded-md after:border after:border-gray-300 after:bg-white after:transition-all after:content-[''] peer-checked:bg-green-300 peer-checked:after:translate-x-full peer-focus:ring-green-300"></div>
              </label>
              <h4 class="ml-3 text-gray-900 mr-4">First Conversation with AI</h4>
            </div>
          </div>

          <div v-if="isGreetingEnabled">
            <div class="flex mt-4">
              <div class="w-72 flex text-left items-center">
                <h4 for="title" class="text-black">Greeting Prompt</h4>
              </div>
              <div class="flex-4 w-full flex">
                <input
                  v-model="settingStore.Settings.greeting_prompt"
                  id="content"
                  rows="4"
                  class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  placeholder="Greeting Prompt"
                />
              </div>
            </div>
          </div>

        </div>

        <div class="pt-8">
          <h1>Product Setting</h1>
          <div class="flex mt-4">
            <div class="flex items-center justify-center mt-4">
              <h4 class="ml-3 text-gray-900 mr-4">Enable Product Placement in answer</h4>
              <label class="relative inline-flex cursor-pointer items-center">
                <input id="switch-3" type="checkbox" class="peer sr-only" v-model="isProductTokenEnabled" />
                <label for="switch-3" class="hidden"></label>
                <div class="peer h-4 w-11 rounded border bg-slate-200 after:absolute after:-top-1 after:left-0 after:h-6 after:w-6 after:rounded-md after:border after:border-gray-300 after:bg-white after:transition-all after:content-[''] peer-checked:bg-green-300 peer-checked:after:translate-x-full peer-focus:ring-green-300"></div>
              </label>
            </div>
          </div>
        </div>

        <div class="pt-8">
          <h1>Feedback Report Setting</h1>
          <div class="flex mt-4">
            <div class="flex items-center justify-center mt-4">
              <h4 class="ml-3 text-gray-900 mr-4">Create feedback report from user</h4>
              <label class="relative inline-flex cursor-pointer items-center">
                <input id="switch-3" type="checkbox" class="peer sr-only" v-model="isOrderTokenEnabled" />
                <label for="switch-3" class="hidden"></label>
                <div class="peer h-4 w-11 rounded border bg-slate-200 after:absolute after:-top-1 after:left-0 after:h-6 after:w-6 after:rounded-md after:border after:border-gray-300 after:bg-white after:transition-all after:content-[''] peer-checked:bg-green-300 peer-checked:after:translate-x-full peer-focus:ring-green-300"></div>
              </label>
            </div>
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
import { computed, nextTick, onMounted, ref } from 'vue'

const settingStore = useSettingStore()
const setting = computed(() => ({
  ...settingStore.Settings,
  id: settingStore.Settings.id,
  fb_activate: Boolean(settingStore.Settings.fb_activate),
  line_activate: Boolean(settingStore.Settings.line_activate),
  product_activate: Boolean(settingStore.Settings.product_activate),
  feedback_activate: Boolean(settingStore.Settings.feedback_activate),
  greeting_activate: Boolean(settingStore.Settings.greeting_activate),
  greeting_prompt: String(settingStore.Settings.greeting_prompt),
  line_key: String(settingStore.Settings.line_key),
  line_secret: String(settingStore.Settings.line_secret),
  facebook_token: String(settingStore.Settings.facebook_token),
  facebook_verify_password: String(settingStore.Settings.facebook_verify_password)
}))
const isLineTokenEnabled = ref(false)
const isFacebookTokenEnabled = ref(false)
const isProductTokenEnabled = ref(false)
const isOrderTokenEnabled = ref(false)
const isGreetingEnabled = ref(false)
const isLoading = ref(false)
const isSuccess = ref(false)

onMounted(async () => {
  await settingStore.fetchSettings()
  isFacebookTokenEnabled.value = Boolean(settingStore.Settings.fb_activate)
  isLineTokenEnabled.value = Boolean(settingStore.Settings.line_activate)
  isProductTokenEnabled.value = Boolean(settingStore.Settings.product_activate)
  isOrderTokenEnabled.value = Boolean(settingStore.Settings.feedback_activate)
  isGreetingEnabled.value = Boolean(settingStore.Settings.greeting_activate)
})

function openModal() {
  isSuccess.value = true;
}
function closeModal() {
  isSuccess.value = false;
}

async function generateFacebookPassword() {
  settingStore.Settings.facebook_verify_password = Math.random().toString(36).slice(-8)
  await nextTick();
}

async function handleSave() {
  if (!setting.value.id) {
    await settingStore.createSetting({
      fb_activate: isFacebookTokenEnabled.value,
      line_activate: isLineTokenEnabled.value,
      product_activate: isProductTokenEnabled.value,
      feedback_activate: isOrderTokenEnabled.value,
      greeting_activate: isGreetingEnabled.value,
      line_key: setting.value.line_key,
      line_secret: setting.value.line_secret,
      facebook_token: setting.value.facebook_token,
      facebook_verify_password: setting.value.facebook_verify_password,
      greeting_prompt: setting.value.greeting_prompt,
    })
    openModal()
  } else {
    isLoading.value = true
    try {
      await settingStore.saveSetting({
        id: String(setting.value.id),
        fb_activate: isFacebookTokenEnabled.value,
        line_activate: isLineTokenEnabled.value,
        product_activate: isProductTokenEnabled.value,
        feedback_activate: isOrderTokenEnabled.value,
        greeting_activate: isGreetingEnabled.value,
        line_key: setting.value.line_key,
        line_secret: setting.value.line_secret,
        facebook_token: setting.value.facebook_token,
        facebook_verify_password: setting.value.facebook_verify_password,
        greeting_prompt: setting.value.greeting_prompt,
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
