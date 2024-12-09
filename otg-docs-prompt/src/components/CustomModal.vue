<template>
  <div
    v-if="isOpen"
    class="fixed inset-0 bg-gray-900 bg-opacity-50 flex justify-center items-center"
    @click.self="closeModal"
  >
    <div class="bg-white rounded-lg shadow-lg w-3/5">
      <!-- Modal Header -->
      <div class="flex justify-between items-center bg-gray-100 p-4 border-b">
        <h3 class="text-lg font-semibold">{{ title }}</h3>
        <button @click="closeModal" class="text-gray-400 hover:text-gray-600">&times;</button>
      </div>
      <!-- Modal Body -->
      <div class="p-4">
        <slot name="body">
          <p class="text-gray-700">This is the modal content.</p>
        </slot>
      </div>
      <!-- Modal Footer -->
      <div class="flex justify-end items-center p-4 border-t bg-gray-100">
        <button
          @click="closeModal"
          class="px-4 py-2 bg-gray-300 text-gray-800 rounded-lg hover:bg-gray-400 mr-2"
        >
          Cancel
        </button>
        <button
          @click="confirmAction"
          class="px-4 py-2 text-white rounded-lg hover:bg-blue-700"
          :class="isAlert ? 'bg-red-600 hover:bg-red-700' : 'bg-blue-600 hover:bg-blue-700'"
        >
          Confirm
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { defineProps, defineEmits } from 'vue'

// Props
defineProps({
  isOpen: Boolean,
  isAlert: {
    type: Boolean,
    default: false,
  },
  title: {
    type: String,
    default: 'Modal Title',
  },
})

// Emits
const emit = defineEmits(['close', 'confirm'])

// Methods
function closeModal() {
  emit('close')
}

function confirmAction() {
  emit('confirm')
}
</script>

<style scoped>
/* Additional styling if needed */
</style>
