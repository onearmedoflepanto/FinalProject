import axios from 'axios'

console.log('[axios.js] VITE_API_BASE_URL:', import.meta.env.VITE_API_BASE_URL)

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use(config => {
  const accessToken = localStorage.getItem('access')
  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`
  }
  return config
})

export default api
