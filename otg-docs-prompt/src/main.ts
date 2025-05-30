import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import './index.css'
import SvgIcon from 'vue3-icon'

const app = createApp(App)

app.use(createPinia())
app.component('svg-icon', SvgIcon)
app.use(router)

app.mount('#app')
