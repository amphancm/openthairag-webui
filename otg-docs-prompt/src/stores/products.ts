import { defineStore } from 'pinia'
import { CONFIG } from '@/config'
import router from '@/router';
const token = localStorage.getItem("token");

export const useProductStore = defineStore('productStore', {
  state: () => ({
    products: {} as Record<string, { 
      id: string; 
      name: String, 
      category: String, 
      detail: String, 
      pictures: string[]
    }>, // Adjust fields based on your API response
  }),
  actions: {
    async fetchProducts() {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/product`,{
          headers: { 
            'Content-Type': 'application/json',
            'Authorization' : 'Bearer '+token
          },
        })
        const data = await response.json()
        data.data.forEach((element: { 
          id: string; 
          name: String, 
          category: String, 
          detail: String, 
          pictures: string[]
         }) => {
          this.products[element.id] = {
            id: element.id,
            name: element.name,
            category: element.category,
            detail: element.detail,
            pictures: element.pictures,
          }
        })
        if (response.status === 401) {
          localStorage.removeItem("token");
          router.push({ path: "/login" }).catch((err) => console.error(err));
          return;
        }
      } catch (error) {
        console.error('Failed to fetch products:', error)
      }
    },
    async createProduct(newProduct: { 
      name: String, 
      category: String, 
      detail: String, 
      pictures: string[]
    }) {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/product`, {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization' : 'Bearer '+token
          },
          body: JSON.stringify(newProduct),
        })
        if (response.status === 401) {
          localStorage.removeItem("token");
          router.push({ path: "/login" }).catch((err) => console.error(err));
          return;
        }
      } catch (error) {
        console.error('Failed to create product:', error)
      }
    },
    async detailProduct(id: string) {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/product/${id}`, {
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
        console.error('Failed to create product:', error)
      }
    },
    async saveProduct(newProduct: { 
      id: string; 
      name: String, 
      category: String, 
      detail: String, 
      pictures: string[]
    }) {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/product`, {
          method: 'PATCH',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization' : 'Bearer '+token
          },
          body: JSON.stringify(newProduct),
        })
        if (response.status === 401) {
          localStorage.removeItem("token");
          router.push({ path: "/login" }).catch((err) => console.error(err));
          return;
        }
        const result = await response.json()
        // if (result) this.products[result._id.$oid].doc_id = result.indexing_id
      } catch (error) {
        console.error('Failed to create product:', error)
      }
    },
    async deleteProduct(id: string) {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/product/` + id, {
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
        delete this.products[id]
      } catch (error) {
        console.error('Failed to create product:', error)
      }
    },
  },
})
