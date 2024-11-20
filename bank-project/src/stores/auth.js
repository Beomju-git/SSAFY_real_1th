import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null,
    userId: localStorage.getItem('userId') || null
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    username: (state) => state.user?.username
  },
  actions: {
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  }
  
})
