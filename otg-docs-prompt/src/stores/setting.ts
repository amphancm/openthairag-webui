import { defineStore } from 'pinia'
import { CONFIG } from '@/config'
import router from '@/router';
const token = localStorage.getItem("token");

export const useSettingStore = defineStore('SettingStore', {
  state: () => ({
    Settings: {} as Record<string, string | boolean>,
  }),
  actions: {
    async fetchSettings() {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/setting/general`,{
          headers: { 
            'Content-Type': 'application/json',
            'Authorization' : 'Bearer '+token
          },
        })
        if (response.status === 401) {
          localStorage.removeItem("token");
          router.push({ path: "/login" }).catch((err) => console.error(err));
          return;
        }
        const data = await response.json()
        data.forEach(
          (element: { _id: { $oid: string }; fb_activate: boolean;  line_activate: boolean;  product_activate: boolean;  feedback_activate: boolean; greeting_activate: boolean; line_key: string; line_secret: string; facebook_token: string; facebook_verify_password:string; greeting_prompt:string; }) => {
            this.Settings = {
              id: element._id.$oid,
              fb_activate: element.fb_activate ?? false,
              line_activate: element.line_activate ?? false,
              product_activate: element.product_activate ?? false,
              feedback_activate: element.feedback_activate ?? false,
              greeting_activate: element.greeting_activate ?? false,
              line_key: element.line_key ?? '',
              line_secret: element.line_secret ?? '',
              facebook_token: element.facebook_token ?? '',
              facebook_verify_password: element.facebook_verify_password ?? '',
              greeting_prompt: element.greeting_prompt ?? '',
            }
          },
        )
      } catch (error) {
        console.error('Failed to fetch Settings:', error)
      }
    },
    async createSetting(newSetting: { 
      line_activate: boolean; 
      fb_activate: boolean; 
      product_activate: boolean; 
      feedback_activate: boolean; 
      greeting_activate: boolean; 
      line_key: string; 
      line_secret: string; 
      facebook_token: string; 
      facebook_verify_password: string; 
      greeting_prompt: string; 
    }) {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/setting/general`, {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization' : 'Bearer '+token
          },
          body: JSON.stringify(newSetting),
        })
        if (response.status === 401) {
          localStorage.removeItem("token");
          router.push({ path: "/login" }).catch((err) => console.error(err));
          return;
        }
        const data = await response.json()
        this.Settings = {
          id: data.id,
          line_activate: newSetting.line_activate ?? false,
          fb_activate: newSetting.fb_activate ?? false,
          product_activate: newSetting.product_activate ?? false,
          feedback_activate: newSetting.feedback_activate ?? false,
          line_key: newSetting.line_key ?? '',
          line_secret: newSetting.line_secret ?? '',
          facebook_token: newSetting.facebook_token ?? '',
          facebook_verify_password: newSetting.facebook_verify_password ?? '',
          greeting_prompt: newSetting.greeting_prompt ?? '',
        }
      } catch (error) {
        console.error('Failed to create Setting:', error)
      }
    },
    async saveSetting(newSetting: { 
      id: string; 
      line_activate: boolean; 
      fb_activate: boolean; 
      product_activate: boolean; 
      feedback_activate: boolean; 
      greeting_activate: boolean; 
      line_key: string; 
      line_secret: string; 
      facebook_token: string; 
      facebook_verify_password: string; 
      greeting_prompt: string; 
    }) {
      try {
        console.log("newSetting :",newSetting)
        const response = await fetch(`${CONFIG.API_BASE_URL}/setting/general`, {
          method: 'PATCH',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization' : 'Bearer '+token
          },
          body: JSON.stringify(newSetting),
        })
        if (response.status === 401) {
          localStorage.removeItem("token");
          router.push({ path: "/login" }).catch((err) => console.error(err));
          return;
        }
      } catch (error) {
        console.error('Failed to create Setting:', error)
      }
    },
  },
})
