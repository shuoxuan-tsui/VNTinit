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

/**
 * 认证状态管理 (Pinia Store)
 * 
 * 设计思路:
 * - **单一职责原则**: 这个 Store 专门负责用户的认证状态，包括用户信息、令牌、加载状态等。
 * - **集中式状态管理**: Pinia 提供了一个集中的地方来管理全局状态，避免了状态在组件间零散传递（Prop Drilling）。
 * - **可组合式API (Composition API)**: 采用 Vue 3 的 Composition API 风格 (`setup store`)，使得代码组织更灵活、逻辑更清晰，且对 TypeScript 支持更友好。
 * - **持久化**: 通过与 `useCookie` 组合，实现了认证状态的持久化，即使用户刷新页面或关闭浏览器后重新打开，也能保持登录状态。
 * - **安全性**: 
 *   - 将 `user` 和 `token` 状态设为 `readonly` 对外暴露，防止外部组件直接修改状态，强制所有状态变更都必须通过 store 中定义的 actions (如 login, logout) 来进行，保证了状态变更的可追溯性和安全性。
 *   - 登出时会向后端发请求，这可以让后端有机会清理服务器端的 session 或记录，比单纯清理前端 cookie 更安全。
 * - **SSR 兼容性**: 通过 `process.client` 判断，确保操作 Cookie 等仅限客户端环境的代码只在浏览器中执行，避免了在服务端渲染（SSR）时出错。
 */
export const useAuthStore = defineStore('auth', () => {
  // --- State ---
  // 使用 ref 创建响应式状态
  
  /**
   * 当前登录的用户对象。
   * 设计：
   * - `User | null`: 初始值为 null，表示未登录状态。登录成功后，存储从后端获取的用户信息。
   * - 使用 ref 是因为它既可以存储基本类型，也可以存储对象类型，并且可以被整个替换（例如 `user.value = newUser`），这在登录/登出时更新整个用户对象很方便。
   */
  const user = ref<User | null>(null)
  
  /**
   * 认证令牌 (JWT/Token)。
   * 设计：
   * - `string | null`: 初始值为 null。登录后存储从后端获取的 token。
   * - 这是与后端进行认证通信的关键凭证，通常放在请求的 Authorization 头中。
   */
  const token = ref<string | null>(null)
  
  /**
   * 加载状态。
   * 设计：
   * - `boolean`: 用于跟踪异步操作（如登录、注册）是否正在进行中。
   * - 这对于在 UI 上显示加载指示器（如 loading spinner）非常有用，可以提升用户体验，防止用户在请求期间重复提交。
   */
  const loading = ref(false)

  // --- Getters (Computed Properties) ---
  // 使用 computed 创建派生状态，它们会根据依赖的状态自动更新

  /**
   * 用户是否已认证。
   * 设计：
   * - `computed`: 这是一个派生状态，其值依赖于 `token.value`。
   * - 相比于在组件中反复编写 `!!token.value`，计算属性提供了更好的可读性和可复用性。
   * - 当 `token` 变化时，所有依赖 `isAuthenticated` 的地方都会自动更新。
   */
  const isAuthenticated = computed(() => !!token.value)
  
  /**
   * 当前用户是否是管理员。
   * 设计：
   * - `computed`: 派生自 `user.value`。
   * - 将权限判断逻辑集中在此处，使得权限检查标准化。如果未来管理员的判断标准改变（例如增加新的角色），只需修改这里一处即可。
   * - `?.` 可选链操作符确保在 `user.value` 为 `null` 时不会抛出错误。
   */
  const isAdmin = computed(() => user.value?.is_superuser || user.value?.groups.includes('Admin'))

  // --- Actions ---
  // 定义可以改变状态的函数
  
  /**
   * 初始化认证状态。
   * 设计：
   * - 客户端执行: if (process.client) 是关键。Cookie 是浏览器特有的 API，在 Node.js 服务端渲染环境中不存在 document.cookie。
   *   此检查确保这段代码只在客户端（浏览器）执行，避免了 SSR 错误。
   * - 持久化恢复: 此函数的目标是从 Cookie 中恢复用户的登录状态。当应用加载时（特别是刷新页面后），它可以读取之前存储的 token 和 user 信息，
   *   让用户无需重新登录。这是提升用户体验的重要一环。
   * - 健壮性: 使用 try-catch 块来解析用户 JSON 数据。如果 Cookie 中的数据格式损坏或不合法，程序不会崩溃，而是会安全地将 user 置为 null。
   */
  const initAuth = () => {
    // 检查是否在客户端执行。因为 cookie 是一个浏览器才有的特定概念，所以只能在客户端执行。
    // 如果在服务器端直接访问 cookie 是会报错的
    // process.client 是一个 Nuxt 提供的全局变量，表示当前代码是否在客户端执行
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
          // 如果解析失败，将用户状态设置为 null，防止应用因数据损坏而出错
          console.error('Failed to parse user cookie:', e)
          user.value = null
        }
      }
    }
  }

  /**
   * 用户登录。
   * 设计：
   * - 异步操作: 登录是一个网络请求，因此是 async 函数。
   * - 状态管理: 登录开始时设置 loading.value = true，结束时（无论成功或失败）在 finally 块中设置 loading.value = false。
   *   这确保了加载状态的正确切换。
   * - 成功处理: 登录成功后，更新 token 和 user 状态，并使用 useCookie 将这些信息持久化到 Cookie 中。
   * - 错误处理: 
   *   - 使用 try-catch 捕获请求过程中的任何错误。
   *   - 提供了详细的错误日志，便于调试。
   *   - 对不同类型的错误（网络错误、服务器返回的业务错误）进行分类处理，并向上抛出对用户更友好的错误信息。
   *   - 不直接在 store 中处理 UI 反馈（如弹窗），而是通过抛出错误，让调用此函数的组件（如登录页面）来决定如何向用户展示错误。
   */
  async function login(credentials: { username: string; password: string }) {
    loading.value = true
    try {
      console.log('Starting login request with credentials:', { username: credentials.username })
      
      const response = await $fetch<any>('/api/auth/login/', {
        method: 'POST',
        body: credentials,
        timeout: 30000, // 设置30秒超时，防止请求长时间无响应
        retry: 1, // 请求失败时自动重试1次，增加网络不佳时的成功率
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
        
        // 持久化登录状态: 使用 useCookie 将 token 和用户信息存储在 Cookie 中。
        // 这使得用户刷新页面或下次访问时可以保持登录状态。
        const tokenCookie = useCookie('auth-token')
        const userCookie = useCookie('user')
        tokenCookie.value = response.data.token
        userCookie.value = JSON.stringify(response.data.user)
        
        return { success: true }
      } else {
        // 如果后端返回成功但数据结构不符合预期，也视为失败
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
      
      // 错误分类与封装: 对捕获到的错误进行分类判断，提取关键信息，并向上抛出一个标准化的 Error 对象。
      // 这样做的好处是，调用 login 的组件不需要关心底层的 fetch 错误细节，只需要捕获并显示这个更具可读性的错误信息。
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
      // 确保无论成功或失败，加载状态都会被重置
      loading.value = false
    }
  }

  /**
   * 用户注册。
   * 设计思路与 login 函数类似：
   * - 管理 loading 状态。
   * - 调用后端注册接口。
   * - 详细的日志记录和健壮的错误处理。
   * - 注册成功后不直接登录，而是返回成功信息，通常由页面引导用户去登录。
   */
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
        // 如果后端返回的格式不符合预期，也抛出错误
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
      
      // 错误处理逻辑同登录函数
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

  /**
   * 用户登出。
   * 设计：
   * - 通知后端: 首先尝试向后端 `/api/auth/logout/` 发送请求。这可以让后端有机会执行一些清理操作，比如销毁 session、记录登出时间等。
   *   即使这个请求失败（例如网络中断），finally 块依然会执行，确保前端状态和 Cookie 被清理。
   * - 清理本地状态: 在 finally 块中，将 user 和 token 状态重置为 null。
   * - 清理持久化数据: 将相关的 Cookie 值设为 null，以清除持久化的登录状态。
   * - 重定向: 使用 navigateTo('/login') 将用户重定向到登录页面，这是一个清晰的用户体验流程。
   */
  async function logout() {
    try {
      if (token.value) {
        // 向后端发送登出请求，让后端有机会清理 session
        await $fetch('/api/auth/logout/', {
          method: 'POST',
          headers: {
            Authorization: `Token ${token.value}`
          }
        })
      }
    } catch (err) {
      // 即使后端登出请求失败（例如token失效或网络问题），我们仍然要清理前端状态。
      // 所以这里只打印错误，不中断流程。
      console.error('Logout error:', err)
    } finally {
      // 清理 Pinia store 中的状态
      user.value = null
      token.value = null
      
      // 清理 Cookie 中的持久化状态
      const tokenCookie = useCookie('auth-token')
      const userCookie = useCookie('user')
      tokenCookie.value = null
      userCookie.value = null
      
      // 重定向到登录页，确保用户回到未登录的初始状态
      await navigateTo('/login')
    }
  }

  /**
   * 初始化认证状态（兼容旧版或备用）。
   * 设计思路与 `initAuth` 完全相同，可能是开发过程中的冗余代码。
   * 在大型应用中，应审查并统一这类功能相同的函数。
   * @deprecated 建议使用 `initAuth`
   */
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

  /**
   * 刷新当前用户信息。
   * 设计：
   * - 数据同步: 用于在需要时（例如，用户修改了个人资料后）从后端获取最新的用户信息，并更新本地状态和 Cookie。
   * - Token 验证: 此请求也间接验证了当前 token 的有效性。如果请求失败（特别是401 Unauthorized），
   *   说明 token 可能已过期或无效，此时应执行登出操作，强制用户重新登录。
   */
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
        // 刷新成功后，同步更新 Cookie 中的用户信息
        const userCookie = useCookie('user')
        userCookie.value = JSON.stringify(response.data.user)
      }
    } catch (err) {
      console.error('Failed to refresh user:', err)
      // 如果刷新失败，很可能是 token 已过期，执行登出流程以清理无效状态。
      await logout()
    }
  }

  // 返回 store 的公共 API
  return {
    // --- State & Getters ---
    // 使用 readonly 包装 state，防止在组件中直接修改 store 的状态，强制使用 actions 进行修改，保证数据流的可控性。
    user: readonly(user),
    token: readonly(token),
    loading: readonly(loading),
    isAuthenticated,
    isAdmin,

    // --- Actions ---
    initAuth,
    login,
    register,
    logout,
    initializeAuth, // 注意：此函数与 initAuth 功能重复 但不知道为什么删了会崩
    refreshUser
  }
}) 