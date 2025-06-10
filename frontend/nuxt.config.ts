// https://nuxt.com/docs/api/configuration/nuxt-config
/// <reference types="nuxt" />

export default defineNuxtConfig({
  compatibilityDate: '2025-05-15',
  devtools: { enabled: true },
  pages: true,
  modules: [
    '@nuxt/icon',
    // '@nuxt/ui',
    '@pinia/nuxt'
  ],
  css: ['~/assets/css/tailwind.css'],
  postcss: {
    plugins: {
      '@tailwindcss/postcss': {},
      autoprefixer: {},
    }
  },
  
  // 运行时配置
  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:8000'
    }
  },
  
  // 开发服务器代理配置
  // 前端/api/开头的请求转发到后端服务http://localhost:8000/api/。
  // 这样在前端开发时可以直接调用本地API而无需处理跨域问题，
  // 同时保持生产环境和开发环境的API路径一致。
  nitro: {
    devProxy: {
      '/api/': 'http://localhost:8000/api/'
    }
  }
})