import { defineStore } from 'pinia'
import api from '@/api/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: localStorage.getItem('access') || null,
    user: null
  }),
  getters: {
    isLoggedIn: (state) => !!state.accessToken
  },
  actions: {
    async login(username, password) {
      console.log('[authStore] Attempting login action with username:', username); // DEBUG LOG
      try {
        console.log('[authStore] Calling api.post to api/accounts/login/'); // DEBUG LOG
        const response = await api.post('api/accounts/login/', {
          username,
          password
        })
        this.accessToken = response.data.access
        localStorage.setItem('access', this.accessToken)
        if (response.data.refresh) {
          localStorage.setItem('refresh', response.data.refresh)
        }
        await this.loadUser()
        return { success: true }
      } catch (error) {
        console.error('Login failed:', error.response ? error.response.data : error.message)
        this.accessToken = null
        this.user = null
        localStorage.removeItem('access')
        localStorage.removeItem('refresh')
        return { success: false, message: error.response?.data?.error || 'Login failed' }
      }
    },
    async socialLogin(payload) { // accessToken, provider를 payload 객체로 받음
      try {
        // 백엔드로 전송할 데이터 구성 (state는 선택적으로 포함)
        const requestData = {
          token: payload.accessToken, // Google ID 토큰, Kakao/Naver 인증 코드
          provider: payload.provider
        }
        if (payload.state) {
          requestData.state = payload.state
        }

        const response = await api.post('api/accounts/social-login/', requestData, { headers: { 'Content-Type': 'application/json' } })
        this.accessToken = response.data.access
        localStorage.setItem('access', this.accessToken)
        if (response.data.refresh) {
          localStorage.setItem('refresh', response.data.refresh)
        }
        await this.loadUser()
        return { success: true }
      }
      catch (error) {
        return { success: false, message: error.response?.data?.error || 'Login failed' }
      }
    },
    async refreshToken() {
      const currentRefreshToken = localStorage.getItem('refresh');
      if (!currentRefreshToken) {
        await this.logout(); // No refresh token, logout
        return Promise.reject(new Error('No refresh token available'));
      }
      try {
        const response = await api.post('api/accounts/token/refresh/', {
          refresh: currentRefreshToken,
        });
        this.accessToken = response.data.access;
        localStorage.setItem('access', this.accessToken);
        // Django Rest Framework SimpleJWT might also return a new refresh token
        // if REFRESH_TOKEN_ROTATE is true. Handle if necessary.
        // if (response.data.refresh) {
        //   localStorage.setItem('refresh', response.data.refresh);
        // }
        console.log('Token refreshed successfully');
        return this.accessToken;
      } catch (error) {
        console.error('Failed to refresh token:', error.response ? error.response.data : error.message);
        await this.logout(); // Refresh failed, logout
        return Promise.reject(error);
      }
    },
    async logout() {
      const refreshToken = localStorage.getItem('refresh')
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')

      try {
        if (refreshToken) {
          await api.post('api/accounts/logout/', { refresh: refreshToken })
        }
      } catch (error) {
        console.error('Logout API error:', error.response ? error.response.data : error.message)
      }
      this.accessToken = null
      this.user = null
    },
    async signup(formData) {
      try {
        console.log('Attempting signup with formData:', formData)
        console.log('Axios baseURL:', api.defaults.baseURL)
        const targetUrl = 'api/accounts/sign_up/'
        console.log('Target API path:', targetUrl)

        const response = await api.post(targetUrl, formData)
        this.accessToken = response.data.access
        localStorage.setItem('access', this.accessToken)
        if (response.data.refresh) {
          localStorage.setItem('refresh', response.data.refresh)
        }
        await this.loadUser()
        return { success: true, message: response.data.message }
      } catch (error) {
        console.error('Signup failed:', error.response ? error.response.data : error.message)
        return { success: false, message: error.response?.data?.error || 'Signup failed' }
      }
    },
    async loadUser() {
      if (this.accessToken) {
        try {
          const response = await api.get('api/accounts/mypage/')
          this.user = response.data
        } catch (error) {
          console.error('Failed to load user:', error.response ? error.response.data : error.message)
          if (error.response && error.response.status === 401) {
            await this.logout()

          }
          this.user = null
        }
      } else {
        this.user = null
      }
    },
    async updateUserProfile(profileData) {
      if (!this.accessToken) {
        return { success: false, message: 'Not authenticated' }
      }
      try {
        const dataToUpdate = { ...profileData }
        if (!dataToUpdate.currentPassword && !dataToUpdate.newPassword && !dataToUpdate.confirmNewPassword) {
          delete dataToUpdate.currentPassword
          delete dataToUpdate.newPassword
          delete dataToUpdate.confirmNewPassword
        }

        const response = await api.put('api/accounts/mypage/', dataToUpdate)
        this.user = response.data
        return { success: true, data: response.data }
      } catch (error) {
        console.error('Failed to update user profile:', error.response ? error.response.data : error.message)
        return { success: false, message: error.response?.data?.detail || error.response?.data?.error || 'Profile update failed' }
      }
    }
  }
})
