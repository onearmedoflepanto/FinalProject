import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  envDir: '../', // Load .env files from the workspace root
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    proxy: {
      '/api-fss': {
        target: 'https://finlife.fss.or.kr/finlifeapi',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api-fss/, ''),
        secure: false, // Set to true if using HTTPS and you want to verify SSL certs
      },
    },
  },
})
