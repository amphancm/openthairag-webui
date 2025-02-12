import { defineStore } from 'pinia'
import { CONFIG } from '@/config'
const token = localStorage.getItem("token");
export const useAccountStore = defineStore('accountStore', {
  state: () => ({
    accounts: {} as Record<string, { id: string; username: string; email: string; role: string }>, // Adjust fields based on your API response
  }),
  actions: {
    async fetchAccounts() {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/user`, {
          headers: { 
            'Content-Type': 'application/json',
            'Authorization' : 'Bearer '+token
          },
        })

        if (response.status === 401) {
          localStorage.removeItem("token");
          window.location.href = "/login"; // Redirect to login page
          return;
        }

        const data = await response.json()
        data.data.forEach((element: { id: string; username: string; email: string; role: string }) => {
          this.accounts[element.id] = {
            id: element.id,
            username: element.username,
            email: element.email,
            role: element.role,
          }
        })
      } catch (error) {
        console.error('Failed to fetch accounts:', error)
      }
    },
    async fetchDetailAccounts(id: string) {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/user/${id}`, {
          headers: { 
            'Content-Type': 'application/json',
            'Authorization' : 'Bearer '+token
          },
        })

        if (response.status === 401) {
          localStorage.removeItem("token");
          window.location.href = "/login"; // Redirect to login page
          return;
        }
        const data = await response.json()
        return data.data;
      } catch (error) {
        console.error('Failed to fetch accounts:', error)
      }
    },
    async createAccount(newDoc: { username: string; email: string }) {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/user`, {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization' : 'Bearer '+token
          },
          body: JSON.stringify(newDoc),
        })

        if (response.status === 401) {
          localStorage.removeItem("token");
          window.location.href = "/login"; // Redirect to login page
          return;
        }
      } catch (error) {
        console.error('Failed to create account:', error)
      }
    },
    async changePasswordAccount(password: string, id: string){
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/user/password/${id}`, {
          method: 'PATCH',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization' : 'Bearer '+token
          },
          body: JSON.stringify({password: password}),
        })

        if (response.status === 401) {
          localStorage.removeItem("token");
          window.location.href = "/login"; // Redirect to login page
          return;
        }
      } catch (error) {
        console.error('Failed to create account:', error)
      }
    },
    async saveAccount(newAcc: { id: string; username: string; email: string; role: string }) {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/user`, {
          method: 'PATCH',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization' : 'Bearer '+token
          },
          body: JSON.stringify(newAcc),
        })
        if (response.status === 401) {
          localStorage.removeItem("token");
          window.location.href = "/login"; // Redirect to login page
          return;
        }
        this.accounts[newAcc.id] = {
          id: newAcc.id,
          username: newAcc.username,
          email: newAcc.email,
          role: newAcc.role,
        }
      } catch (error) {
        console.error('Failed to create account:', error)
      }
    },
    async deleteAccount(id: string) {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/user/` + id, {
          method: 'DELETE',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization' : 'Bearer '+token
          },
        })
        if (response.status === 401) {
          localStorage.removeItem("token");
          window.location.href = "/login"; // Redirect to login page
          return;
        }
        delete this.accounts[id]
      } catch (error) {
        console.error('Failed to create account:', error)
      }
    },
  },
})
