import { defineStore } from 'pinia'
import { CONFIG } from '@/config'
import router from '@/router';
const token = localStorage.getItem("token");

export const useDocumentStore = defineStore('documentStore', {
  state: () => ({
    documents: {} as Record<string, { id: string; title: string; content: string; doc_id: string }>, // Adjust fields based on your API response
  }),
  actions: {
    async fetchDocuments() {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/document`,{
          headers: { 
            'Content-Type': 'application/json',
            'Authorization' : 'Bearer '+token
          },
        })
        const data = await response.json()
        data.forEach((element: { id: string; title: string; content: string; doc_id: string }) => {
          this.documents[element.id] = {
            id: element.id,
            title: element.title,
            content: element.content,
            doc_id: element.doc_id,
          }
        })
        if (response.status === 401) {
          localStorage.removeItem("token");
          router.push({ path: "/login" }).catch((err) => console.error(err));
          return;
        }
      } catch (error) {
        console.error('Failed to fetch documents:', error)
      }
    },
    async createDocument(newDoc: { title: string; content: string }) {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/document`, {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization' : 'Bearer '+token
          },
          body: JSON.stringify(newDoc),
        })
        if (response.status === 401) {
          localStorage.removeItem("token");
          router.push({ path: "/login" }).catch((err) => console.error(err));
          return;
        }
      } catch (error) {
        console.error('Failed to create document:', error)
      }
    },
    async saveDocument(newDoc: { id: string; title: string; content: string; doc_id: string }) {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/document`, {
          method: 'PATCH',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization' : 'Bearer '+token
          },
          body: JSON.stringify(newDoc),
        })
        if (response.status === 401) {
          localStorage.removeItem("token");
          router.push({ path: "/login" }).catch((err) => console.error(err));
          return;
        }
        const result = await response.json()
        if (result) this.documents[result._id.$oid].doc_id = result.indexing_id
      } catch (error) {
        console.error('Failed to create document:', error)
      }
    },
    async deleteDocument(id: string) {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/document/` + id, {
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
        delete this.documents[id]
      } catch (error) {
        console.error('Failed to create document:', error)
      }
    },
  },
})
