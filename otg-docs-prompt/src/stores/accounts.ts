import { defineStore } from 'pinia'

export const useAccountStore = defineStore('accountStore', {
  state: () => ({
    accounts: {} as Record<string, { id: string; username: string; email: string; role: string }>, // Adjust fields based on your API response
  }),
  actions: {
    async fetchAccounts() {
      try {
        const response = await fetch('http://localhost:5500/account')
        const data = await response.json()
        data.forEach((element: { id: string; username: string; email: string; role: string }) => {
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
    async createAccount(newDoc: { username: string; email: string }) {
      try {
        await fetch('http://localhost:5500/account', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(newDoc),
        })
      } catch (error) {
        console.error('Failed to create account:', error)
      }
    },
    async saveAccount(newAcc: { id: string; username: string; email: string; role: string }) {
      try {
        await fetch('http://localhost:5500/account', {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(newAcc),
        })
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
        await fetch('http://localhost:5500/account/' + id, {
          method: 'DELETE',
        })
        delete this.accounts[id]
      } catch (error) {
        console.error('Failed to create account:', error)
      }
    },
  },
})
