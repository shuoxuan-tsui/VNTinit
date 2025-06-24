import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

interface User {
  id: string
  username: string
  email: string
  is_superuser: boolean
  groups: string[]
}

interface LoginResponse {
  token: string
  user: User
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const loading = ref(false)

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.is_superuser || user.value?.groups.includes('Admin'))

  // 初始化认证状态
  const initAuth = () => {
    // 检查是否在客户端执行。因为 cookie 是一个浏览器才有的特定概念，所以只能在客户端执行。
    // 如果在服务器端直接访问 cookie 是会报错的
    // process.client 是一个全局变量，表示当前代码是否在客户端执行
    // 如果 process.client 为 true，则表示当前代码在客户端执行
    // 如果 process.client 为 false，则表示当前代码在服务器端执行
    // 在客户端执行时，检查是否存在 token 和 user 的 cookie
    // 如果存在，则从 cookie 中恢复认证状态
    // 如果不存在，则初始化认证状态为 null
    // 在服务器端执行时，不进行任何操作
    if (process.client) {
      const tokenCookie = useCookie('auth-token')
      const userCookie = useCookie('user')
      // 检查 Cookie 中是否存在有效的令牌和用户数据
      if (tokenCookie.value && userCookie.value) {
        // 如果存在，将 Cookie 中的令牌赋值给响应式变量 token
        token.value = tokenCookie.value as string
        try {
          // 尝试解析用户数据
        // 检查 userCookie.value 是否是字符串，如果是，则解析为 JSON 对象
          user.value = typeof userCookie.value === 'string' 
            ? JSON.parse(userCookie.value) 
            : userCookie.value as User
        } catch (e) {
          // 如果解析失败，将用户状态设置为 null
          console.error('Failed to parse user cookie:', e)
          user.value = null
        }
      }
    }
  }

  async function login(credentials: { username: string; password: string }) {
    loading.value = true
    try {
      console.log('Starting login request with credentials:', { username: credentials.username })
      
      const response = await $fetch<any>('/api/auth/login/', {
        method: 'POST',
        body: credentials,
        timeout: 30000, // 30秒超时
        retry: 1, // 重试1次
        onRequest({ request, options }) {
          console.log('Login request:', request, options)
        },
        onResponse({ response }) {
          console.log('Login response:', response.status, response.statusText)
        },
        onResponseError({ response }) {
          console.log('Login response error:', response.status, response.statusText, response._data)
        }
      })
      
      console.log('Login response received:', response)
      
      if (response && response.success && response.data) {
        token.value = response.data.token
        user.value = response.data.user
        
        // 存储到cookie
        const tokenCookie = useCookie('auth-token')
        const userCookie = useCookie('user')
        tokenCookie.value = response.data.token
        userCookie.value = JSON.stringify(response.data.user)
        
        return { success: true }
      } else {
        return { success: false, error: response.message || '登录失败' }
      }
    } catch (err: any) {
      console.error('Login error details:', {
        message: err.message,
        data: err.data,
        status: err.status,
        statusCode: err.statusCode,
        statusMessage: err.statusMessage,
        cause: err.cause,
        full: err
      })
      
      // 处理不同类型的错误
      if (err.name === 'FetchError' && err.message.includes('fetch')) {
        throw new Error('网络连接失败，请检查网络连接')
      } else if (err.status === 400 && err.data?.message) {
        throw new Error(err.data.message)
      } else if (err.statusCode === 400 && err.data?.message) {
        throw new Error(err.data.message)
      } else if (err.data?.message) {
        throw new Error(err.data.message)
      } else if (err.message) {
        throw new Error(err.message)
      } else {
        throw new Error('网络错误，请稍后重试')
      }
    } finally {
      loading.value = false
    }
  }

  async function register(userData: { username: string; email: string; password: string }) {
    loading.value = true
    try {
      console.log('Starting register request with data:', userData)
      
      const response = await $fetch<any>('/api/auth/register/', {
        method: 'POST',
        body: userData,
        timeout: 30000, // 30秒超时
        retry: 1, // 重试1次
        onRequest({ request, options }) {
          console.log('Register request:', request, options)
        },
        onResponse({ response }) {
          console.log('Register response:', response.status, response.statusText)
        },
        onResponseError({ response }) {
          console.log('Register response error:', response.status, response.statusText, response._data)
        }
      })
      
      console.log('Register response received:', response)
      
      if (response && response.success) {
        return { success: true, data: response.data, message: response.message }
      } else {
        throw new Error(response?.message || '注册失败')
      }
    } catch (err: any) {
      console.error('Register error details:', {
        message: err.message,
        data: err.data,
        status: err.status,
        statusCode: err.statusCode,
        statusMessage: err.statusMessage,
        cause: err.cause,
        full: err
      })
      
      // 处理不同类型的错误
      if (err.name === 'FetchError' && err.message.includes('fetch')) {
        throw new Error('网络连接失败，请检查网络连接')
      } else if (err.status === 400 && err.data?.message) {
        throw new Error(err.data.message)
      } else if (err.statusCode === 400 && err.data?.message) {
        throw new Error(err.data.message)
      } else if (err.data?.message) {
        throw new Error(err.data.message)
      } else if (err.message) {
        throw new Error(err.message)
      } else {
        throw new Error('注册失败，请稍后重试')
      }
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    try {
      if (token.value) {
        await $fetch('/api/auth/logout/', {
          method: 'POST',
          headers: {
            Authorization: `Token ${token.value}`
          }
        })
      }
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      // 清除状态
      user.value = null
      token.value = null
      
      // 清除cookie
      const tokenCookie = useCookie('auth-token')
      const userCookie = useCookie('user')
      tokenCookie.value = null
      userCookie.value = null
      
      // 重定向到登录页
      await navigateTo('/login')
    }
  }

  function initializeAuth() {
    // 从cookie恢复认证状态
    if (process.client) {
      const tokenCookie = useCookie('auth-token')
      const userCookie = useCookie('user')
      
      if (tokenCookie.value && userCookie.value) {
        token.value = tokenCookie.value as string
        try {
          user.value = typeof userCookie.value === 'string' 
            ? JSON.parse(userCookie.value) 
            : userCookie.value as User
        } catch (e) {
          console.error('Failed to parse user cookie:', e)
          user.value = null
        }
      }
    }
  }

  async function refreshUser() {
    if (!token.value) return
    
    try {
      const response = await $fetch<any>('/api/auth/user/', {
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      
      if (response && response.success && response.data) {
        user.value = response.data.user
        const userCookie = useCookie('user')
        userCookie.value = JSON.stringify(response.data.user)
      }
    } catch (err) {
      console.error('Failed to refresh user:', err)
      // 如果刷新失败，可能token已过期，执行登出
      await logout()
    }
  }

  return {
    user: readonly(user),
    token: readonly(token),
    loading: readonly(loading),
    isAuthenticated,
    isAdmin,
    initAuth,
    login,
    register,
    logout,
    initializeAuth,
    refreshUser
  }
}) 