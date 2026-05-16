import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// GitHub Pages serves from /<repo>/, so set base accordingly.
// In dev (npm run dev), base is "/" so localhost works.
const base = process.env.GITHUB_PAGES === 'true'
  ? '/rig-systems-engineering-studio/'
  : '/';

export default defineConfig({
  plugins: [react()],
  base,
  build: {
    outDir: 'dist',
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          three: ['three'],
          r3f: ['@react-three/fiber', '@react-three/drei'],
        },
      },
    },
  },
  server: {
    port: 5173,
    host: '0.0.0.0',
  },
});
