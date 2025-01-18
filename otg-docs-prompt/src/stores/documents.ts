import { defineStore } from 'pinia'

export const useDocumentStore = defineStore('documentStore', {
  state: () => ({
    documents: {} as Record<string, { id: string; title: string; content: string; doc_id: string }>, // Adjust fields based on your API response
  }),
  actions: {
    async fetchDocuments() {
      try {
        const response = await fetch('https://otg-server.odoo365cloud.com/document')
        const data = await response.json()
        data.forEach((element: { id: string; title: string; content: string; doc_id: string }) => {
          this.documents[element.id] = {
            id: element.id,
            title: element.title,
            content: element.content,
            doc_id: element.doc_id,
          }
        })
      } catch (error) {
        console.error('Failed to fetch documents:', error)
      }
    },
    async createDocument(newDoc: { title: string; content: string }) {
      try {
        await fetch('https://otg-server.odoo365cloud.com/document', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(newDoc),
        })
      } catch (error) {
        console.error('Failed to create document:', error)
      }
    },
    async saveDocument(newDoc: { id: string; title: string; content: string; doc_id: string }) {
      try {
        const response = await fetch('https://otg-server.odoo365cloud.com/document', {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(newDoc),
        })
        const result = await response.json()
        if (result) this.documents[result._id.$oid].doc_id = result.indexing_id
      } catch (error) {
        console.error('Failed to create document:', error)
      }
    },
    async deleteDocument(id: string) {
      try {
        await fetch('https://otg-server.odoo365cloud.com/document/' + id, {
          method: 'DELETE',
        })
        delete this.documents[id]
      } catch (error) {
        console.error('Failed to create document:', error)
      }
    },
  },
})
