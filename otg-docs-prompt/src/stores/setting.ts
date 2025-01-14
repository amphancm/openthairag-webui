import { defineStore } from 'pinia'

export const useSettingStore = defineStore('SettingStore', {
  state: () => ({
    Settings: {} as Record<string, string>,
  }),
  actions: {
    async fetchSettings() {
      try {
        const response = await fetch('http://localhost:5500/setting')
        const data = await response.json()
        data.forEach(
          (element: { _id: { $oid: string }; line_key: string; line_secret: string; facebook_token: string; facebook_verify_password:string; }) => {
            this.Settings = {
              id: element._id.$oid,
              line_key: element.line_key ?? '',
              line_secret: element.line_secret ?? '',
              facebook_token: element.facebook_token ?? '',
              facebook_verify_password: element.facebook_verify_password ?? '',
            }
          },
        )
      } catch (error) {
        console.error('Failed to fetch Settings:', error)
      }
    },
    async createSetting(newSetting: { 
      line_key: string; 
      line_secret: string; 
      facebook_token: string; 
      facebook_verify_password: string; 
    }) {
      try {
        const response = await fetch('http://localhost:5500/setting', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(newSetting),
        })
        const data = await response.json()
        this.Settings = {
          id: data.id,
          line_key: newSetting.line_key ?? '',
          line_secret: newSetting.line_secret ?? '',
          facebook_token: newSetting.facebook_token ?? '',
          facebook_verify_password: newSetting.facebook_verify_password ?? '',
        }
      } catch (error) {
        console.error('Failed to create Setting:', error)
      }
    },
    async saveSetting(newSetting: { 
      id: string; 
      line_key: string; 
      line_secret: string; 
      facebook_token: string; 
      facebook_verify_password: string; 
    }) {
      try {
        const response = await fetch('http://localhost:5500/setting', {
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
