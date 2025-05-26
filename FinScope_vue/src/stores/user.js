import { defineStore } from 'pinia'
import api from '@/api/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: localStorage.getItem('access') || null,
    user: null,
  }),
  getters: {
    isLoggedIn: (state) => !!state.accessToken,
  },
  actions: {
    async login(username, password) {
      try {
        const response = await api.post('api/accounts/login/', { // Ensure this path is relative to baseURL in axios.js
          username,
          password,
        });
        this.accessToken = response.data.access;
        localStorage.setItem('access', this.accessToken);
        if (response.data.refresh) {
          localStorage.setItem('refresh', response.data.refresh);
        }
        await this.loadUser(); // Load user details after successful login
        return { success: true };
      } catch (error) {
        console.error('Login failed:', error.response ? error.response.data : error.message);
        this.accessToken = null;
        this.user = null;
        localStorage.removeItem('access');
        localStorage.removeItem('refresh');
        return { success: false, message: error.response?.data?.error || 'Login failed' };
      }
    },
    async logout() {
      const refreshToken = localStorage.getItem('refresh');
      localStorage.removeItem('access');
      localStorage.removeItem('refresh'); // Remove refresh token immediately
      
      try {
        if (refreshToken) {
          await api.post('api/accounts/logout/', { refresh: refreshToken });
        }
      } catch (error) {
        console.error('Logout API error:', error.response ? error.response.data : error.message);
        // Even if API logout fails, frontend state is cleared
      }
      this.accessToken = null;
      this.user = null;
    },
    async signup(formData) {
      try {
        console.log('Attempting signup with formData:', formData);
        console.log('Axios baseURL:', api.defaults.baseURL);
        const targetUrl = 'api/accounts/sign_up/';
        console.log('Target API path:', targetUrl);
        // To see the fully resolved URL, you might need to inspect the network request in browser dev tools,
        // or construct it manually for logging if needed: console.log('Full URL (estimated):', `${api.defaults.baseURL}${targetUrl}`);

        const response = await api.post(targetUrl, formData);
        this.accessToken = response.data.access;
        localStorage.setItem('access', this.accessToken);
        if (response.data.refresh) {
          localStorage.setItem('refresh', response.data.refresh);
        }
        await this.loadUser();
        return { success: true, message: response.data.message };
      } catch (error) {
        console.error('Signup failed:', error.response ? error.response.data : error.message);
        return { success: false, message: error.response?.data?.error || 'Signup failed' };
      }
    },
    async loadUser() {
      if (this.accessToken) {
        try {
          // The Authorization header should be automatically added by the Axios interceptor if configured
          const response = await api.get('api/accounts/mypage/'); 
          this.user = response.data;
        } catch (error) {
          console.error('Failed to load user:', error.response ? error.response.data : error.message);
          // Potentially handle token refresh or logout if 401
          if (error.response && error.response.status === 401) {
            await this.logout(); // Or attempt token refresh
          }
          this.user = null; // Clear user data on failure
        }
      } else {
        this.user = null; // No token, no user
      }
    },
    async updateUserProfile(profileData) {
      if (!this.accessToken) {
        return { success: false, message: 'Not authenticated' };
      }
      try {
        // Filter out password fields if they are empty, as we might not want to send empty password fields
        const dataToUpdate = { ...profileData };
        if (!dataToUpdate.currentPassword && !dataToUpdate.newPassword && !dataToUpdate.confirmNewPassword) {
          delete dataToUpdate.currentPassword;
          delete dataToUpdate.newPassword;
          delete dataToUpdate.confirmNewPassword;
        }
        // The backend /api/accounts/mypage/ PUT expects all fields the serializer can update.
        // Ensure profileData contains all updatable fields as expected by UserSerializer.
        // Django's UserSerializer for PUT might require all fields or allow partial updates (patch=True).
        // The current Django view uses partial=True, so sending only changed fields is okay.
        
        const response = await api.put('api/accounts/mypage/', dataToUpdate);
        this.user = response.data; // Update local store state with the updated user data
        return { success: true, data: response.data };
      } catch (error) {
        console.error('Failed to update user profile:', error.response ? error.response.data : error.message);
        return { success: false, message: error.response?.data?.detail || error.response?.data?.error || 'Profile update failed' };
      }
    }
  },
})
