import router from '@/router'
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthenticationStore = defineStore('authenticationStore', {
  state: () => ({
    profile: {} as Record<string, { username:string; token:string; }>
  }),
  actions: {
    async login(body: { username: string, password: string, remember: boolean }) {
      try {
          const response = await fetch('https://otg-server.odoo365cloud.com/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
          })
          const data = await response.json()
          if(data.access_token) {
            localStorage.setItem('username', body.username);
            localStorage.setItem('token', data.access_token);
          }
      } catch (error) {
          console.error('Failed to fetch authentications:', error)
      }
    },
    async logout() {
      try {
          const token = ref(localStorage.getItem("token"));
          const response = await fetch('https://otg-server.odoo365cloud.com/logout', {
            method: 'POST',
            headers:{
              'Authorization' : 'Bearer '+token.value
            }
          })
          const data = await response.json()
          if(data.access_token) {
            localStorage.removeItem('username');
            localStorage.removeItem('token');
          }
      } catch (error) {
          console.error('Failed to fetch authentications:', error)
      }
    },
    async getProfile() {
      try {
        const token = ref(localStorage.getItem("token"));
        const response = await fetch('https://otg-server.odoo365cloud.com/profile', {headers:{
          'Authorization' : 'Bearer '+token.value
        }})
        const res = await handleResponse(response);
        this.profile = res
        return res
      } catch (error) {
        console.error('Failed to fetch systemPrompts:', error)
      }
    },
  },
})

async function handleResponse(response: Response) {
  if (response.status != 200) {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    router.push({ path: "/login" }).catch((err) => console.error(err));
    return null
  }
  return response.json();
}

