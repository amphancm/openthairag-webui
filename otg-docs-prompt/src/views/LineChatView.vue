<template>
  <div class="flex w-full">
    <div class="flex-none w-[200px] bg-white">
      <div class="h-screen flex flex-col p-4">
        <div class="flex-none w-full text-center">
          <h3>Line Chat</h3>
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
            <p>{{ chatRoom.sender.displayName }}</p>
          </div>
        </div>
      </div>
    </div>
    <div class="flex-auto w-full">
      <div class="h-screen flex flex-col p-4">
        <div class="bg-slate-500 h-12 flex items-center justify-between">
          <h3 class="text-white">{{ chatRoomsList[selectIndexing]?.sender.displayName }}</h3>
          <div @click="toggleSubmenu" ref="targetRef">
            <div class="flex justify-between">
              <div class="flex items-center pr-2">
                <p class=" pr-1" >Bot Toggle :</p>
                <div class="flex flex-col items-center justify-center">
                  <label class="relative inline-flex cursor-pointer items-center">
                    <input id="switch-3" type="checkbox" class="peer sr-only" v-model="isOn" @change="handleToggle" />
                    <label for="switch-3" class="hidden"></label> 
                    <div class="peer h-4 w-11 rounded border bg-slate-200 after:absolute after:-top-1 after:left-0 after:h-6 after:w-6 after:rounded-md after:border after:border-gray-300 after:bg-white after:transition-all after:content-[''] peer-checked:bg-green-300 peer-checked:after:translate-x-full peer-focus:ring-green-300"></div>
                  </label>
                </div>
              </div>
              <Icon icon="material-symbols:menu" width="36" height="36" />
            </div>
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
                <div
                  v-if="message.type == 'text'"
                  class="py-1" 
                >
                  <p v-for="(messager, index) in message.content.split('\n')"
                  :key="index" class="text-black" >
                    {{ messager }}
                  </p>
                </div>
                <img
                  v-else
                  :src="message.content"
                  alt="image"
                  class="w-40 h-40 object-cover rounded-md"
                />
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
      <h5 class="pb-2">Temperature :</h5>
        <input class="border-2 border-blue-500 rounded-md w-full p-4 mb-2" v-model="temperature" 
        @input="validateInput" type="number"
      />
      <h5 class="pb-2">System Prompt :</h5>
      <textarea
        class="border-2 border-blue-500 rounded-md w-full p-4 h-[300px]"
        v-model="systemPrompt"
      />
    </template>
  </Modal>

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
import { computed, nextTick, onBeforeUnmount, onMounted, onUnmounted, ref, watch } from 'vue'
import Modal from '../components/CustomModal.vue'
import { Icon } from '@iconify/vue'
import { useSystemPromptStore } from '@/stores/systemPrompt'
import { useChatLineRoomStore } from '@/stores/chatLineRoom'
import { CONFIG } from '@/config'

interface MessageData {
    message: {
        role: 'assistant' | 'user';
        user: number;
        content: string;
        timestamp: string;
    };
    line_ids: string;
}
const tempMessage = ref< MessageData | null >(null);
let pollingInterval: ReturnType<typeof setInterval>;

const selectIndexing = ref(0)
const isSubmenuVisible = ref(false)
const name = ref('')
const systemPrompt = ref('')
const temperature = ref('')
const type = ref('')
const inputMessage = ref('')
const isSuccess = ref(false)

const isAssistantTyping = ref(false)
const isUserTyping = ref(false)
const targetRef = ref<HTMLElement | null>(null)
const messagesContainer = ref<HTMLElement | null>(null)
const message = ref('');
const messages = ref([]);

const isOn = ref(false);

function handleToggle() {
  console.log(`Switch is now ${isOn.value ? 'On' : 'Off'}`);
}

const chatLineRoomStore = useChatLineRoomStore()
const chatRooms = computed(() => chatLineRoomStore.chatLineRoom) // Replace `chatRoom` with your actual state variable

const systemPromptStore = useSystemPromptStore()
const system_prompt = computed(() => systemPromptStore.systemPrompts)

function validateInput() {
  const value = parseFloat(temperature.value);

  if (value < 0 || value > 1 || isNaN(value)) {
    temperature.value = ''; // Reset invalid inputå
  }
}

let chatRoomsList: {
  id: string
  sender: {
    displayName: string;
    language: string;
    pictureUrl: string;
    userId: string;
  }
  chatOption: {
    temperature: string;
    systemPrompt: string; 
    greeting: string; 
    botToggle: boolean;
  }
  messages: Array<{ type: string; role: string; content: string }>
  userId: string
}[] = []

onMounted(async () => {
  await chatLineRoomStore.fetchChatLineRooms();
  await systemPromptStore.fetchSystemPrompts()
  chatRoomsList = Object.values(chatRooms.value)
  selectIndexing.value = chatRoomsList.length > 0 ? chatRoomsList.length - 1 : 0;

  await chatLineRoomStore.deleteTempLineRooms(chatRoomsList[selectIndexing.value].sender.userId);
  isOn.value = chatRoomsList[selectIndexing.value].chatOption.botToggle

  nextTick(() => {
        if (messagesContainer.value) {
          messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
        }
      })
  startPolling(1000);
})

function openModal() {
  isSuccess.value = true;
}
function closeModal() {
  isSuccess.value = false;
}

function sendMessage() {
  if (message.value.trim()) {
    message.value = "";
  }
}

async function fetchTempMessages() {
  try {
    const response = await fetch(`${CONFIG.API_BASE_URL}/chat/short_polling_message`);
    const data = await response.json();
    if(data.message != null) {
      console.log("data : ",data)
      appendMessageToChatRoom(data.message)
    }
    tempMessage.value = data.message;
  } catch (error) {
    console.error('Failed to fetch temporary messages:', error);
  }
}

function startPolling(interval: number) {
  fetchTempMessages();
  pollingInterval = setInterval(fetchTempMessages, interval);
}

function stopPolling() {
  clearInterval(pollingInterval);
}

function appendMessageToChatRoom(
  message_obj: MessageData,
) {
  const index = chatRoomsList.findIndex(
    (chatRoom) => chatRoom.sender.userId === message_obj.line_ids
  );

  if (index !== -1) {
    const parts = processText(message_obj.message.content)
    for (const part of parts) {
      if(isValidImageUrl(part)) {
        chatRoomsList[index].messages.push({
          type: 'image',
          role: message_obj.message.role,
          content: part,
        })
      } else if(part != '-' && part != ',' && part != '' && part.length > 1) {
        chatRoomsList[index].messages.push({
          type: 'text',
          role: message_obj.message.role,
          content: part,
        })
      }
    }

    nextTick(() => {
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
      }
    })
  } else {
    console.warn(`No chat room found for line_ids: ${message_obj.line_ids}`);
  }
}

function processText(input: string) {
  const regex = /!?\[.*?\]\((.*?)\)/g;
  const parts: string[] = [];

  let lastIndex = 0;
  let match: RegExpExecArray | null;

  while ((match = regex.exec(input)) !== null) {
    // Add the part of the text before the current match
    if (lastIndex !== match.index) {
      parts.push(input.slice(lastIndex, match.index).trim());
    }
    // Add the matched image markdown
    if (match[0].startsWith('!')) {
      parts.push(match[1]);
    } else {
      parts.push(match[0].trim());
    }
    
    lastIndex = regex.lastIndex;
  }

  // Add the remaining text after the last match
  if (lastIndex < input.length) {
    parts.push(input.slice(lastIndex).trim());
  }

  return parts;
}

function isValidImageUrl(url: string): boolean {
  const regex = /^http.*\.(jpg|png)$/;
  return regex.test(url);
}

onUnmounted(() => {
  stopPolling();
});

watch(
  chatRooms,
  (newValue) => {
    chatRoomsList = Object.values(chatRooms.value)
  },
  { deep: true },
)

watch(
  isOn,
  async (newValue) => {
    chatRoomsList[selectIndexing.value].chatOption.botToggle = isOn.value
    await chatLineRoomStore.saveChatLineRooms({
      id: chatRoomsList[selectIndexing.value].id,
      chatOption: chatRoomsList[selectIndexing.value].chatOption
    })
  },
  { deep: true },
)


watch(inputMessage, (newValue) => {
  if (newValue.trim() !== '') {
    isUserTyping.value = true
    nextTick(() => {
        if (messagesContainer.value) {
          messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
        }
      })
  } else {
    isUserTyping.value = false
  }
})

async function handleSubmitMessage() {

  isOn.value = false
  chatRoomsList[selectIndexing.value].chatOption.botToggle = false
  await chatLineRoomStore.saveChatLineRooms({
    id: chatRoomsList[selectIndexing.value].id,
    chatOption: chatRoomsList[selectIndexing.value].chatOption
  })

  if (chatRoomsList.length == 0) {
    openCreateModalSystemPrompt()
  } else {
    const messageContent = inputMessage.value
    inputMessage.value = ''
    if (messageContent.trim() != '') {
      isAssistantTyping.value = true
      nextTick(() => {
        if (messagesContainer.value) {
          messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
        }
      })
      await chatLineRoomStore.submitMessage({
        id: chatRoomsList[selectIndexing.value].id,
        line_ids: chatRoomsList[selectIndexing.value].sender.userId,
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

async function selectRoom(index: number) {
  selectIndexing.value = index
  await chatLineRoomStore.deleteTempLineRooms(chatRoomsList[selectIndexing.value].sender.userId);
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
  temperature.value = system_prompt.value.temperature
  isModalSystemPromptOpen.value = true
}

function openModalSystemPrompt() {
  type.value = 'edit'
  console.log('chatRoomsList', chatRoomsList)
  name.value = chatRoomsList[selectIndexing.value].sender.displayName
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
  chatRoomsList[selectIndexing.value].chatOption.temperature = temperature.value
  chatRoomsList[selectIndexing.value].chatOption.systemPrompt = systemPrompt.value
  await chatLineRoomStore.saveChatLineRooms({
    id: chatRoomsList[selectIndexing.value].id,
    chatOption: chatRoomsList[selectIndexing.value].chatOption
  })
  closeModalSystemPrompt()
}

async function handleConfirmDelete() {
  // await chatLineRoomStore.deleteChatRooms(chatRoomsList[selectIndexing.value].id)
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
