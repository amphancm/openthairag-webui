import { defineStore } from 'pinia'
import { CONFIG } from '@/config'
import router from '@/router';
const token = localStorage.getItem("token");

export const useSystemPromptStore = defineStore('systemPromptStore', {
  state: () => ({
    systemPrompts: {} as Record<string, string>,
  }),
  actions: {
    async fetchSystemPrompts() {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/setting/system_prompt`,{
            headers: { 
              'Content-Type': 'application/json',
              'Authorization' : 'Bearer '+token
            },
          }
        )
        if (response.status === 401) {
          localStorage.removeItem("token");
          router.push({ path: "/login" }).catch((err) => console.error(err));
          return;
        }
        const data = await response.json()
        this.systemPrompts = {
          id: data._id.$oid,
          content: data.content,
          temperature: data.temperature,
          greeting: data.greeting,
        }
      } catch (error) {
        console.error('Failed to fetch systemPrompts:', error)
      }
    },
    async createSystemPrompt(newSystemPrompt: { 
      content: string; 
      temperature: string 
    }) {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/setting/system_prompt`, {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization' : 'Bearer '+token
          },
          body: JSON.stringify(newSystemPrompt),
        })
        if (response.status === 401) {
          localStorage.removeItem("token");
          router.push({ path: "/login" }).catch((err) => console.error(err));
          return;
        }
        const data = await response.json()
        this.systemPrompts = {
          id: data.id,
          content: newSystemPrompt.content,
          temperature: newSystemPrompt.temperature,
        }
      } catch (error) {
        console.error('Failed to create systemPrompt:', error)
      }
    },
    async saveSystemPrompt(newSystemPrompt: { 
      id: string; 
      content: string; 
      temperature: string 
    }) {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/setting/system_prompt`, {
          method: 'PATCH',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization' : 'Bearer '+token
          },
          body: JSON.stringify(newSystemPrompt),
        })
        if (response.status === 401) {
          localStorage.removeItem("token");
          router.push({ path: "/login" }).catch((err) => console.error(err));
          return;
        }
      } catch (error) {
        console.error('Failed to create systemPrompt:', error)
      }
    },
  },
})
