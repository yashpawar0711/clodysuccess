import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    port: 5173,
    watch: {
      ignored: ['**/env/**', '**/.venv/**', '**/db.sqlite3', '**/media/**', '**/staticfiles/**', '**/__pycache__/**']
    }
  }
});
