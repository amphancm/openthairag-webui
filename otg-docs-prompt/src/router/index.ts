import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import DocsView from '../views/DocsView.vue'
import EditDocsView from '@/views/EditDocsView.vue'
import SystemPromptView from '@/views/SystemPromptView.vue'
import CreateDocsView from '@/views/CreateDocsView.vue'
import SettingView from '@/views/SettingView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: HomeView,
    },
    {
      path: '/docs',
      name: 'docs',
      component: DocsView,
    },
    {
      path: '/system_prompt',
      name: 'system_prompt',
      component: SystemPromptView,
    },
    {
      path: '/docs/:id',
      name: 'editing-docs',
      component: EditDocsView,
    },
    {
      path: '/docs/create',
      name: 'create-doc',
      component: CreateDocsView,
    },
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/chat',
      name: 'chat',
      component: HomeView,
    },
    {
      path: '/setting',
      name: 'setting',
      component: SettingView,
    },
  ],
})

export default router
