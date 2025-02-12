import router from '@/router'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { CONFIG } from '@/config'

export const useAuthenticationStore = defineStore('authenticationStore', {
  state: () => ({
    profile: {} as Record<string, { username:string; token:string; }>
  }),
  actions: {
    async login(body: { username: string, password: string, remember: boolean }) {
      try {
          const response = await fetch(`${CONFIG.API_BASE_URL}/auth/login`, {
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
          const response = await fetch(`${CONFIG.API_BASE_URL}/auth/logout`, {
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
        const response = await fetch(`${CONFIG.API_BASE_URL}/auth/profile`, {headers:{
          'Authorization' : 'Bearer '+token.value
        }})
        // const res = await handleResponse(response);
        if (response.status === 401) {
          localStorage.removeItem("token");
          router.push({ path: "/login" }).catch((err) => console.error(err));
          return;
        }

        const profileData = await response.json();
        this.profile = profileData;
        return profileData
      } catch (error) {
        console.error('Failed to fetch systemPrompts:', error)
      }
    },
  },
})
