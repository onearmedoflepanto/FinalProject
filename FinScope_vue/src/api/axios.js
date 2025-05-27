import axios from 'axios'
import { useAuthStore } from '@/stores/user' // Import the auth store

console.log('[axios.js] VITE_API_BASE_URL:', import.meta.env.VITE_API_BASE_URL)

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use(config => {
  const authStore = useAuthStore(); // Get store instance
  const accessToken = authStore.accessToken; // Use accessToken from store state
  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`
  }
  return config
})

// Response interceptor for API calls
api.interceptors.response.use(response => {
  return response;
}, async function (error) {
  const originalRequest = error.config;
  const authStore = useAuthStore(); // Get store instance

  // Check if it's a 401 error and not a retry request
  if (error.response && error.response.status === 401 && !originalRequest._retry) {
    originalRequest._retry = true; // Mark it as a retry
    try {
      console.log('Attempting to refresh token...');
      const newAccessToken = await authStore.refreshToken();
      if (newAccessToken) {
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + newAccessToken;
        originalRequest.headers['Authorization'] = 'Bearer ' + newAccessToken;
        return api(originalRequest); // Retry the original request with the new token
      }
    } catch (refreshError) {
      console.error('Interceptor refresh error:', refreshError);
      // If refresh token fails (e.g., also expired), logout will be handled by refreshToken action
      // Redirect to login or show a global message might be needed here if not handled by router guards
      // For now, the refreshToken action handles logout.
      return Promise.reject(refreshError);
    }
  }

  // For other errors, or if refresh fails and logout is handled, just reject
  return Promise.reject(error);
});

export default api
