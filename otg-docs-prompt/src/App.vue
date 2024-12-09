<template>
  <div class="flex h-screen">
    <div
      class="flex-none bg-gray-800 text-white w-[200px] items-center py-4 space-y-4 pt-12 text-center"
    >
      <slot name="sidebar" class="text-center">
        <h3 class="text-center"><RouterLink to="/">OTG PROMPT</RouterLink></h3>
        <div class="bg-slate-600 w-4/5 h-1 rounded-lg mx-auto"></div>
        <div class="space-y-4 text-left ml-10">
          <h4><RouterLink to="/docs">Documents</RouterLink></h4>
          <h4><RouterLink to="/system_prompt">System Prompt</RouterLink></h4>
          <h4><RouterLink to="/">Prompt Lab</RouterLink></h4>
          <h4><RouterLink to="/setting">Settings</RouterLink></h4>
        </div>
      </slot>
    </div>

    <div class="flex-auto bg-slate-500">
      <RouterView />
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>
