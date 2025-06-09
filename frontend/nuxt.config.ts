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
  nitro: {
    devProxy: {
      '/api/': 'http://localhost:8000/api/'
    }
  }
})