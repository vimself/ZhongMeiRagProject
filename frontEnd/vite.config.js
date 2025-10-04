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
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    port: 5173,
    host: '0.0.0.0',  // 允许外部访问（方便后端开发人员访问）
    open: true,  // 启动时自动打开浏览器
    // API 代理配置 - 将 /api 请求转发到后端服务
    proxy: {
      '/api': {
        target: 'http://localhost:8000',  // 后端服务地址（可修改）
        changeOrigin: true,
        rewrite: (path) => path,  // 保留 /api 前缀
        // 如果后端不需要 /api 前缀，可以取消下面的注释
        // rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },
  // 生产环境构建配置
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,  // 生产环境移除 console
        drop_debugger: true
      }
    }
  }
})
