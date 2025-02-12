import { defineStore } from 'pinia'
import { CONFIG } from '@/config'
import router from '@/router';
const token = localStorage.getItem("token");

export const useIssueStore = defineStore('issueStore', {
  state: () => ({
    issues: {} as Record<string, { 
      id: string; 
      name: String, 
      detail: String, 
      user_name: String, 
    }>, // Adjust fields based on your API response
  }),
  actions: {
    async fetchIssues() {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/issue`,{
          headers: { 
            'Content-Type': 'application/json',
            'Authorization' : 'Bearer '+token
          },
        })
        const data = await response.json()
        data.data.forEach((element: { 
          id: string; 
          name: String, 
          detail: String, 
          user_name: String, 
         }) => {
          this.issues[element.id] = {
            id: element.id,
            name: element.name,
            detail: element.detail,
            user_name: element.user_name,
          }
        })
        if (response.status === 401) {
          localStorage.removeItem("token");
          router.push({ path: "/login" }).catch((err) => console.error(err));
          return;
        }
      } catch (error) {
        console.error('Failed to fetch issues:', error)
      }
    },
    async createIssue(newIssue: { 
      name: String, 
      detail: String, 
      user_name: String, 
    }) {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/issue`, {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization' : 'Bearer '+token
          },
          body: JSON.stringify(newIssue),
        })
        if (response.status === 401) {
          localStorage.removeItem("token");
          router.push({ path: "/login" }).catch((err) => console.error(err));
          return;
        }
      } catch (error) {
        console.error('Failed to create issue:', error)
      }
    },
    async detailIssue(id: string) {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/issue/${id}`, {
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
        return response.json()
      } catch (error) {
        console.error('Failed to create issue:', error)
      }
    },
    async saveIssue(newIssue: { 
      id: string; 
      name: String, 
      detail: String, 
      user_name: String, 
    }) {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/issue`, {
          method: 'PATCH',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization' : 'Bearer '+token
          },
          body: JSON.stringify(newIssue),
        })
        if (response.status === 401) {
          localStorage.removeItem("token");
          router.push({ path: "/login" }).catch((err) => console.error(err));
          return;
        }
        const result = await response.json()
        // if (result) this.issues[result._id.$oid].doc_id = result.indexing_id
      } catch (error) {
        console.error('Failed to create issue:', error)
      }
    },
    async deleteIssue(id: string) {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/issue/` + id, {
          method: 'DELETE',
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
        delete this.issues[id]
      } catch (error) {
        console.error('Failed to create issue:', error)
      }
    },
  },
})
