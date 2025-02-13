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
import FacebookChatView from '@/views/FacebookChatView.vue'
import LoginView from '@/views/LoginView.vue'
import ProductView from '@/views/ProductView.vue'
import IssueView from '@/views/IssueView.vue'
import CreateProductView from '@/views/CreateProductView.vue'
import EditProductView from '@/views/EditProductView.vue'
import EditIssueView from '@/views/EditIssueView.vue'

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
      path: '/products',
      name: 'products',
      component: ProductView,
    },
    {
      path: '/issues',
      name: 'issues',
      component: IssueView,
    },
    {
      path: '/system_prompt',
      name: 'system_prompt',
      component: SystemPromptView,
    },
    {
      path: '/products/:id',
      name: 'editing-product',
      component: EditProductView,
    },
    {
      path: '/issues/:id',
      name: 'editing-issue',
      component: EditIssueView,
    },
    {
      path: '/products/create',
      name: 'create-product',
      component: CreateProductView,
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
      path: '/chat/facebook',
      name: 'chatFacebook',
      component: FacebookChatView,
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
