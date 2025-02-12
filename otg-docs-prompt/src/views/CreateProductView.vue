<template>
  <div class="h-full flex flex-col p-4">
    <div class="bg-slate-500 h-12 w-full flex items-center">
      <h3>Create Product</h3>
    </div>
    <div class="flex parent overflow-y-auto mt-4">
      <div class="overflow-x-auto w-full">
        <div class="flex">
          <div class="w-40 flex items-center text-left">
            <h4 for="title" class="text-black">Name</h4>
          </div>
          <div class="flex-4 w-full">
            <input
              v-model="newProduct.name"
              type="text"
              id="title"
              class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Enter title"
            />
          </div>
        </div>

        <div class="flex mt-4">
          <div class="w-40 flex items-center text-left">
            <h4 for="title" class="text-black">Category</h4>
          </div>
          <div class="flex-4 w-full">
            <select
              v-model="newProduct.category"
              id="category"
              class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            >
              <option value="" disabled selected>Select a category</option>
              <option value="food">Food</option>
              <option value="service">Service</option>
              <option value="travel">Travel</option>
            </select>
          </div>
        </div>

        <div class="flex mt-4">
          <div class="w-40 flex text-left py-2">
            <h4 for="title" class="text-black">Detail</h4>
          </div>
          <div class="flex-4 w-full">
            <textarea
              v-model="newProduct.detail"
              id="content"
              rows="4"
              class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 h-[200px]"
              placeholder="Enter content"
            ></textarea>
          </div>
        </div>

        <div class="flex mt-4">
          <div class="w-40 flex text-left py-2">
            <h4 for="title" class="text-black">Pictures</h4>
          </div>
          <div class="flex-4 w-full">
            <div class="flex items-center gap-4">
              <label class="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600 cursor-pointer">
                Upload Image
                <input
                  type="file"
                  multiple
                  accept="image/*"
                  class="hidden"
                  @change="handleFileUpload"
                />
              </label>
            </div>

            <div v-if="newProduct.pictures.length" class="flex flex-wrap gap-4 my-4">
              <div
                v-for="(preview, index) in newProduct.pictures"
                :key="index"
                class="relative"
                style="width: 150px; height: 150px;"
              >
                <img
                  :src="preview"
                  alt="Preview"
                  class="w-full h-full object-cover rounded-md shadow"
                />
                <button
                  @click="removePreview(index)"
                  class="absolute top-2 right-2 bg-red-600 text-white p-1 rounded"
                >
                  &times;
                </button>
              </div>
            </div>
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
import { useProductStore } from '@/stores/products'
import { Icon } from '@iconify/vue/dist/iconify.js'
import { ref } from 'vue'

const productStore = useProductStore()
const isLoading = ref(false)
const newProduct = ref<{ 
  name: string; 
  category: string; 
  detail: string; 
  pictures: string[]; 
}>({ 
  name: '', 
  category: '', 
  detail: '', 
  pictures: [], 
})

// const pictures = ref<string[]>([])

// Handle file input change
const handleFileUpload = (event: Event) => {
  const files = (event.target as HTMLInputElement).files
  if (!files) return

  Array.from(files).forEach((file) => {
    const reader = new FileReader()
    reader.onload = (e) => {
      newProduct.value.pictures.push(e.target?.result as string)
    }
    reader.readAsDataURL(file)
  })
  // Reset the input so the same file can be reselected
  ;(event.target as HTMLInputElement).value = ''
}

// Remove preview
const removePreview = (index: number) => {
  newProduct.value.pictures.splice(index, 1)
}
async function handleCreate() {
  isLoading.value = true
  try {
    await productStore.createProduct(newProduct.value)
  } catch (error) {
    console.error('Error deleting document:', error)
  } finally {
    isLoading.value = false
  }
  newProduct.value = { 
    name: '', 
    category: '', 
    detail: '', 
    pictures: [] 
  }
  router.push('/products')
}


</script>
<style scoped>
img {
  border: 1px solid #ddd;
}
</style>