<template>
  <div class="flex w-full">
    <div class="flex-none w-[200px] bg-white">
      <div class="h-screen flex flex-col p-4">
        <div class="flex-none w-full text-center">
          <h3>Room</h3>
        </div>
        <div class="flex-grow py-4 overflow-y-auto mb-2">
          <div
            v-for="(chatRoom, index) in Object.values(chatRooms).reverse()"
            :key="index"
            @click="selectRoom(Object.values(chatRooms).length - 1 - index)"
            class="w-full h-14 border border-black rounded-lg mb-2 flex items-center px-4 overflow-x-scroll cursor-pointer"
            :class="
              Object.values(chatRooms).length - 1 - index == selectIndexing
                ? 'bg-slate-400 text-white'
                : 'bg-white'
            "
          >
            <p>{{ chatRoom.chatOption.name }}</p>
          </div>
        </div>
        <div class="flex-none">
          <button
            class="bg-slate-600 text-white px-4 py-2 rounded hover:bg-green-600 w-full"
            @click="openCreateModalSystemPrompt()"
          >
            Create Room
          </button>
        </div>
      </div>
    </div>
    <div class="flex-auto w-full">
      <div class="h-screen flex flex-col p-4">
        <div class="bg-slate-500 h-12 flex items-center justify-between">
          <h3 class="text-white">Prompt labs</h3>
          <div @click="toggleSubmenu" ref="targetRef">
            <Icon icon="material-symbols:menu" width="36" height="36" />
            <div
              v-if="isSubmenuVisible"
              class="absolute mt-2 bg-white border rounded shadow-lg w-48 right-5"
            >
              <ul class="text-gray-700">
                <li
                  class="px-4 py-2 hover:bg-gray-100 cursor-pointer"
                  @click="openModalSystemPrompt"
                >
                  <h6>System Prompt</h6>
                </li>
                <li class="px-4 py-2 hover:bg-gray-100 cursor-pointer" @click="openModalDelete">
                  <h6>Delete</h6>
                </li>
              </ul>
            </div>
          </div>
        </div>
        <div class="flex flex-grow parent overflow-y-auto w-full">
          <div class="overflow-y-auto my-4 rounded-md w-full" ref="messagesContainer">
            <div v-if="chatRoomsList.length > 0 && chatRoomsList[selectIndexing]?.messages">
              <div
                v-for="(message, index) in chatRoomsList[selectIndexing].messages"
                :key="index"
                :class="message.role"
              >
                <p
                  class="py-1"
                  v-for="(messager, index) in message.content.split('\\n')"
                  :key="index"
                >
                  {{ messager }}
                </p>
              </div>
            </div>
            <div v-if="isAssistantTyping" class="assistant">
              <div class="loader">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
            <div v-if="isUserTyping" class="user">
              <div class="loader">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        </div>
        <div class="bg-slate-500 h-12 w-full flex">
          <div class="flex flex-grow">
            <input
              type="text"
              class="w-full p-4 rounded-full border-2 mr-2"
              placeholder="Input Here......"
              v-model="inputMessage"
              @keydown.enter="handleSubmitMessage"
            />
          </div>
          <div
            class="flex items-center border-2 rounded-full border-white p-3 outline-slate-500"
            @click="handleSubmitMessage"
          >
            <Icon icon="material-symbols:send" width="24" height="24" class="text-white" />
          </div>
        </div>
      </div>
    </div>
  </div>
  <Modal
    :isOpen="isModalSystemPromptOpen"
    title="System Prompt Edit"
    @close="closeModalSystemPrompt"
    @confirm="handleConfirmSystemPrompt"
  >
    <template #body>
      <h5 class="pb-2">Name :</h5>
      <input class="border-2 border-blue-500 rounded-md w-full p-4 mb-2" v-model="name" />
      <h5 class="pb-2">Temperature :</h5>
      <input class="border-2 border-blue-500 rounded-md w-full p-4 mb-2" v-model="temperature" />
      <h5 class="pb-2">System Prompt :</h5>
      <textarea
        class="border-2 border-blue-500 rounded-md w-full p-4 h-[300px]"
        v-model="systemPrompt"
      />
    </template>
  </Modal>
  <Modal
    :isOpen="isModalDeleteOpen"
    title="Confirm Delete"
    @close="closeModalDelete"
    :isAlert="true"
    @confirm="handleConfirmDelete"
  >
    <template #body>
      <p>Are you sure?</p>
    </template>
  </Modal>
</template>

<script lang="ts" setup>
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from 'vue'
import Modal from '../components/CustomModal.vue'
import { useChatRoomStore } from '@/stores/chatRooms'
import { Icon } from '@iconify/vue'
import { useSystemPromptStore } from '@/stores/systemPrompt'

const selectIndexing = ref(0)
const isSubmenuVisible = ref(false)
const name = ref('')
const systemPrompt = ref('')
const temperature = ref('')
const type = ref('')
const inputMessage = ref('')

const isAssistantTyping = ref(false)
const isUserTyping = ref(false)
const targetRef = ref<HTMLElement | null>(null)
const messagesContainer = ref<HTMLElement | null>(null)

const chatRoomsStore = useChatRoomStore()
const chatRooms = computed(() => chatRoomsStore.chatRoom) // Replace `chatRoom` with your actual state variable

const systemPromptStore = useSystemPromptStore()
const system_prompt = computed(() => systemPromptStore.systemPrompts)

let chatRoomsList: {
  id: string
  chatOption: { name: string; temperature: string; systemPrompt: string }
  messages: Array<{ role: string; content: string }>
}[] = []

onMounted(async () => {
  await chatRoomsStore.fetchChatRooms()
  await systemPromptStore.fetchSystemPrompts()
  chatRoomsList = Object.values(chatRooms.value)
})

watch(
  chatRooms,
  (newValue) => {
    chatRoomsList = Object.values(chatRooms.value)
  },
  { deep: true },
)

watch(inputMessage, (newValue) => {
  console.log('inputMessage', inputMessage.value)
  if (newValue.trim() !== '') {
    isUserTyping.value = true
  } else {
    isUserTyping.value = false
  }
})

async function handleSubmitMessage() {
  if (chatRoomsList.length == 0) {
    console.log('Submit no cresata')
    openCreateModalSystemPrompt()
  } else {
    const messageContent = inputMessage.value
    inputMessage.value = ''
    if (messageContent.trim() != '') {
      console.log('Push')
      isAssistantTyping.value = true
      nextTick(() => {
        if (messagesContainer.value) {
          messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
        }
      })
      await chatRoomsStore.submitMessage({
        id: chatRoomsList[selectIndexing.value].id,
        systemPrompt: chatRoomsList[selectIndexing.value].chatOption.systemPrompt,
        temperature: chatRoomsList[selectIndexing.value].chatOption.temperature,
        message: messageContent,
      })
      isAssistantTyping.value = false
      nextTick(() => {
        if (messagesContainer.value) {
          messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
        }
      })
    }
  }
}

function selectRoom(index: number) {
  selectIndexing.value = index
}

function toggleSubmenu() {
  isSubmenuVisible.value = !isSubmenuVisible.value
}

const handleClickOutside = (event: MouseEvent) => {
  if (targetRef.value && !targetRef.value.contains(event.target as Node)) {
    isSubmenuVisible.value = false
  }
}

// Modal State
const isModalSystemPromptOpen = ref(false)
const isModalDeleteOpen = ref(false)

function openCreateModalSystemPrompt() {
  type.value = 'create'
  name.value = ''
  systemPrompt.value = system_prompt.value.content
  temperature.value = '0.4'
  isModalSystemPromptOpen.value = true
}

function openModalSystemPrompt() {
  type.value = 'edit'
  console.log('selectIndexing :', selectIndexing.value)
  console.log('chatRoomsList :', chatRoomsList)
  name.value = chatRoomsList[selectIndexing.value].chatOption.name
  systemPrompt.value = chatRoomsList[selectIndexing.value].chatOption.systemPrompt
  temperature.value = chatRoomsList[selectIndexing.value].chatOption.temperature
  isModalSystemPromptOpen.value = true
}

function closeModalSystemPrompt() {
  isModalSystemPromptOpen.value = false
}

function openModalDelete() {
  isModalDeleteOpen.value = true
}

function closeModalDelete() {
  isModalDeleteOpen.value = false
}

async function handleConfirmSystemPrompt() {
  if (type.value == 'create') {
    await chatRoomsStore.createChatRooms({
      chatOption: {
        name: name.value,
        temperature: temperature.value,
        systemPrompt: systemPrompt.value,
      },
      messages: [],
    })
  } else {
    await chatRoomsStore.saveChatRooms({
      chatOption: {
        name: name.value,
        temperature: temperature.value,
        systemPrompt: systemPrompt.value,
      },
      id: chatRoomsList[selectIndexing.value].id,
    })
  }
  closeModalSystemPrompt()
}

async function handleConfirmDelete() {
  console.log(' Delete Confirmed!', chatRoomsList[selectIndexing.value])
  await chatRoomsStore.deleteChatRooms(chatRoomsList[selectIndexing.value].id)
  closeModalDelete()
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.assistant {
  @apply bg-white max-w-96 rounded-md p-2 mb-4 text-wrap;
  width: fit-content;
  /* max-width: 400px; */
  word-wrap: break-word; /* Ensures long words are wrapped */
  overflow-wrap: break-word; /* Modern equivalent for wrapping text */
  white-space: normal;
}

.user {
  @apply bg-white max-w-96 rounded-md p-3 mb-4 text-wrap;
  margin-left: auto; /* Align to the right */
  width: fit-content;
  /* max-width: 400px; */
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
