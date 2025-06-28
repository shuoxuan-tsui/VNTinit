/**
 * Nuxt 客户端认证插件
 *
 * 设计目的:
 * - **提升开发效率**: 这个插件的核心目的是在开发环境中自动使用预设的管理员账户（admin/admin123）进行登录。
 *   这样，开发者在启动项目或刷新页面后，无需手动输入凭据即可进入需要认证的页面，极大地简化了开发和调试流程。
 * - **仅限客户端**: 文件名后缀 `.client.js` 是 Nuxt 的一个约定，它确保此插件中的代码只会在客户端（浏览器）执行。
 *   这是非常重要的，因为：
 *     1. `localStorage` 是浏览器环境独有的 API，在服务端（Node.js）执行会直接报错。
 *     2. 登录操作是与用户会话相关的，理应在客户端发起。
 * - **幂等性检查**: 插件在执行自动登录前，会先检查 `localStorage.getItem('auth_token')`。
 *   如果 token 已存在，则跳过登录流程。这可以防止不必要的重复登录请求，并避免在页面切换时反复执行登录逻辑。
 * - **简化调试**: 这个插件与 `test-api.vue` 类似，都属于开发辅助工具，不应包含在生产构建中。
 *   在实际部署时，应通过配置（例如环境变量）禁用或移除此类插件。
 *
 * @param {import('#app').NuxtApp} nuxtApp Nuxt 应用实例
 */
export default defineNuxtPlugin(async () => {
  // 检查 localStorage 中是否已存在认证令牌。
  // localStorage 是浏览器端的持久化存储，比 sessionStorage 的生命周期更长（关闭浏览器后不清空）。
  const existingToken = localStorage.getItem('auth_token')
  
  // 如果没有 token，说明用户尚未登录或 token 已被清除。
  if (!existingToken) {
    // 自动登录admin用户。这通常是一个用于开发的后门，方便调试。
    // 在生产环境中，此类代码应该被移除或禁用。
    try {
      // 使用 $fetch 向后端登录接口发送请求
      const response = await $fetch('/api/auth/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: {
          username: 'admin',
          password: 'admin123'
        }
      })
      
      console.log('Login response:', response)
      
      // 登录成功后，后端会返回 token 和 user 信息。
      if (response && response.success && response.data && response.data.token) {
        // 将获取到的 token 和用户信息存储到 localStorage，以便后续的 API 请求使用。
        localStorage.setItem('auth_token', response.data.token)
        localStorage.setItem('user_info', JSON.stringify(response.data.user))
        console.log('Auto-login successful, token:', response.data.token)
      } else {
        // 如果登录失败，打印错误信息，便于排查问题。
        console.error('Login failed:', response)
      }
    } catch (error) {
      // 捕获并打印请求过程中可能发生的网络错误或其他异常。
      console.error('Auto-login failed:', error)
    }
  } else {
    // 如果 token 已存在，则直接在控制台打印信息，不做任何操作。
    console.log('Existing token found:', existingToken)
  }
}) 