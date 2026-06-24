import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api/legacy': {
        target: process.env.VITE_LEGACY_API_URL || 'http://localhost:8001',
        rewrite: (path) => path.replace('/api/legacy', ''),
      },
      '/api/modern': {
        target: process.env.VITE_MODERN_API_URL || 'http://localhost:8002',
        rewrite: (path) => path.replace('/api/modern', ''),
      },
    },
  },
})
