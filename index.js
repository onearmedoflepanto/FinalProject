import { defineStore } from 'pinia'
import api from '@/api/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: localStorage.getItem('access') || null,
    user: null,
  }),
  actions: {
    async login(username, password) {
      const response = await api.post('/accounts/login/', {
        username,
        password,
      })
      this.accessToken = response.data.access
      localStorage.setItem('access', this.accessToken)
    },
    async logout() {
      localStorage.removeItem('access')
      this.accessToken = null
      this.user = null
    },
    async signup(formData) {
      const response = await api.post('/accounts/sign_up/', formData)
      this.accessToken = response.data.access
      localStorage.setItem('access', this.accessToken)
      await this.loadUser()
    },
    async loadUser() {
      if (this.accessToken) {
        const response = await axios.get('/api/accounts/mypage/', {
          headers: { Authorization: `Bearer ${this.accessToken}` },
        })
        this.user = response.data
      }
    },
  },
})
