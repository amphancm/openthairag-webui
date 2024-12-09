import { defineStore } from 'pinia'

export const useSystemPromptStore = defineStore('systemPromptStore', {
  state: () => ({
    systemPrompts: {} as Record<string, string>,
  }),
  actions: {
    async fetchSystemPrompts() {
      try {
        const response = await fetch('http://localhost:5500/system_prompt')
        const data = await response.json()
        data.forEach((element: { _id: { $oid: string }; content: string; temperature: string }) => {
          this.systemPrompts = {
            id: element._id.$oid,
            content: element.content,
            temperature: element.temperature,
          }
        })
      } catch (error) {
        console.error('Failed to fetch systemPrompts:', error)
      }
    },
    async createSystemPrompt(newSystemPrompt: { content: string; temperature: string }) {
      try {
        const response = await fetch('http://localhost:5500/system_prompt', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(newSystemPrompt),
        })
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
    async saveSystemPrompt(newSystemPrompt: { id: string; content: string; temperature: string }) {
      try {
        const response = await fetch('http://localhost:5500/system_prompt', {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(newSystemPrompt),
        })
      } catch (error) {
        console.error('Failed to create systemPrompt:', error)
      }
    },
  },
})
