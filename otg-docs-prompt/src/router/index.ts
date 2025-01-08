import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import DocsView from '../views/DocsView.vue'
import EditDocsView from '@/views/EditDocsView.vue'
import SystemPromptView from '@/views/SystemPromptView.vue'
import CreateDocsView from '@/views/CreateDocsView.vue'
import EditAccountView from '@/views/EditAccountView.vue'
import CreateAccountView from '@/views/CreateAccountView.vue'
import SettingView from '@/views/SettingView.vue'
import AccountView from '@/views/AccountView.vue'
import LineChatView from '@/views/LineChatView.vue'
import LoginView from '@/views/LoginView.vue'

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
      path: '/acc/:id',
      name: 'editing-acc',
      component: EditAccountView,
    },
    {
      path: '/acc/create',
      name: 'create-acc',
      component: CreateAccountView,
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
      path: '/chat/line',
      name: 'chatline',
      component: LineChatView,
    },
    {
      path: '/setting',
      name: 'setting',
      component: SettingView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/settings/account',
      name: 'Account',
      component: AccountView,
    },
  ],
})

export default router
