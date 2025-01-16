<template>
  <div>
    <div v-if="isLoginPage" class="h-screen bg-gray-100 flex items-center justify-center">
      <RouterView />
    </div>
    <div class="flex h-screen">
      <div
        class="flex-none bg-gray-800 text-white w-[200px] items-center text-center"
      >
        <div class="flex flex-col h-screen py-4 ">
          <div class="flex-grow space-y-4 ">
            <slot name="sidebar" class="text-center ">
              <h3 class="text-center"><RouterLink to="/">OTG PROMPT</RouterLink></h3>
              <div class="bg-slate-600 w-4/5 h-1 rounded-lg mx-auto"></div>
              <div class="space-y-4 text-left ml-10">
                <h4><RouterLink to="/docs">Documents</RouterLink></h4>
                <h4><RouterLink to="/system_prompt">System Prompt</RouterLink></h4>
                <h4>
                  <button
                    class="w-full text-left focus:outline-none"
                    @click="toggleSubmenu('chat')"
                  >
                    Chat
                  </button>
                </h4>
                <div v-if="submenuOpen['chat']" class="ml-4 space-y-2">
                  <h5>
                    <RouterLink to="/">Prompt Lab</RouterLink>
                  </h5>
                  <h5>
                    <RouterLink to="/chat/line">Line</RouterLink>
                  </h5>
                  <h5>
                    <RouterLink to="/chat/facebook">Facebook</RouterLink>
                  </h5>
                </div>
                <h4>
                  <button
                    class="w-full text-left focus:outline-none"
                    @click="toggleSubmenu('settings')"
                  >
                    Settings
                  </button>
                </h4>
                <div v-if="submenuOpen['settings']" class="ml-4 space-y-2">
                  <h5>
                    <RouterLink to="/setting">General</RouterLink>
                  </h5>
                  <h5>
                    <RouterLink to="/settings/account">Account</RouterLink>
                  </h5>
                </div>
              </div>
            </slot>
          </div>
          <div class="flex-none px-4">
            <div v-if="profile != null" class="flex">
              <div class="flex-auto items-center flex justify-center">
                <p>{{ profile.username }}</p>
              </div>
              <div class=" w-5 justify-end cursor-pointer" @click="toggleIconMenu" ref="menuIcon">
                <Icon icon="system-uicons:menu-vertical" width="24" height="24" />                 
                <div
                  v-if="isIconmenuVisible"
                  class="absolute mt-2 bg-white border rounded shadow-lg w-48 bottom-14 left-1 "
                >
                  <ul class="text-gray-700">
                    <li
                      class="px-4 py-2 hover:bg-gray-100 cursor-pointer"
                      @click="logout"
                    >
                      <h6>Logout</h6>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
            <button
              v-else
              @click="pushRouteLogin"
              class="bg-slate-600 text-white px-4 py-2 rounded hover:bg-green-600 w-full"
            >
              Login
            </button>
          </div>
        </div>
      </div>

      <div class="flex-auto bg-slate-500">
        <RouterView />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, reactive, ref } from "vue";
import { RouterLink, RouterView, useRoute } from 'vue-router'
import router from '@/router'
import { useAuthenticationStore } from "./stores/authentication";
import { Icon } from "@iconify/vue/dist/iconify.js";
import { useChatRoomStore } from "./stores/chatRooms";

const route = useRoute();

// Determine if the current route is the login page
const isLoginPage = computed(() => route.path === '/login');
const token = ref(localStorage.getItem("token"));
const authentication = useAuthenticationStore()
const chatroom = useChatRoomStore()
const isIconmenuVisible = ref(false);
const menuIcon = ref<HTMLElement | null>(null)

const profile = computed(() => authentication.profile)

// Sidebar submenu state
const submenuOpen: Record<string, boolean> = reactive({
  chat: false,
  settings: false,
});

onMounted(() => {
  getProfile()
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

function toggleIconMenu(){
  isIconmenuVisible.value = true;
}
const handleClickOutside = (event: MouseEvent) => {
  if (menuIcon.value && !menuIcon.value.contains(event.target as Node)) {
    isIconmenuVisible.value = false
  }
}

function toggleSubmenu(menu: string) {
  submenuOpen[menu] = !submenuOpen[menu];
}

async function getProfile() {
  if (token.value) {
    await authentication.getProfile();
  } else {
    console.error("Token is missing in localStorage.");
    router.push({ path: "/login" }).catch((err) => console.error(err));
  }
}

function pushRouteLogin() {
  router.push({ name: 'login' }).catch((err) => console.error(err))
}

async function logout(){
  isIconmenuVisible.value = false
  await chatroom.resetChatRooms()
  await authentication.logout()
  router.push({ path: "/login" }).catch((err) => console.error(err));
}
</script>
