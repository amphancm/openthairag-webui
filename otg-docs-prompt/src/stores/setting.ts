import { defineStore } from 'pinia'

export const useSettingStore = defineStore('SettingStore', {
  state: () => ({
    Settings: {} as Record<string, string>,
  }),
  actions: {
    async fetchSettings() {
      try {
        const response = await fetch('http://localhost:5000/setting')
        const data = await response.json()
        console.log(' response :', response)
        console.log(' data :', data)
        data.forEach(
          (element: { _id: { $oid: string }; line_key: string; line_secret: string }) => {
            this.Settings = {
              id: element._id.$oid,
              line_key: element.line_key,
              line_secret: element.line_secret,
            }
          },
        )
      } catch (error) {
        console.error('Failed to fetch Settings:', error)
      }
    },
    async createSetting(newSetting: { line_key: string; line_secret: string }) {
      try {
        const response = await fetch('http://localhost:5000/setting', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(newSetting),
        })
        const data = await response.json()
        this.Settings = {
          id: data.id,
          line_key: newSetting.line_key,
          line_secret: newSetting.line_secret,
        }
      } catch (error) {
        console.error('Failed to create Setting:', error)
      }
    },
    async saveSetting(newSetting: { id: string; line_key: string; line_secret: string }) {
      try {
        const response = await fetch('http://localhost:5000/setting', {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(newSetting),
        })
      } catch (error) {
        console.error('Failed to create Setting:', error)
      }
    },
  },
})
