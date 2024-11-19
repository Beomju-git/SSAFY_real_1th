import { defineStore } from 'pinia'
import axios from 'axios'

export const useProductStore = defineStore('product', {
  state: () => ({
    products: [],
    loading: false,
    error: null
  }),

  actions: {
    async fetchProducts() {
      this.loading = true
      try {
        const response = await axios.get('http://127.0.0.1:8000/products/term_deposit/')
        this.products = response.data
      } catch (err) {
        this.error = '상품 정보를 불러오는데 실패했습니다.'
        console.error('상품 정보 로딩 에러:', err)
      } finally {
        this.loading = false
      }
    }
  }
})