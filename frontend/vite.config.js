import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Configures the Vite dev server to listen on all network interfaces
    // This is crucial when running inside a Docker container
    host: '0.0.0.0',
    port: 3000,
  }
})