export default defineNuxtPlugin(async () => {
  // 检查是否已有token
  const existingToken = localStorage.getItem('auth_token')
  
  if (!existingToken) {
    // 自动登录admin用户
    try {
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
      
      if (response && response.success && response.data && response.data.token) {
        localStorage.setItem('auth_token', response.data.token)
        localStorage.setItem('user_info', JSON.stringify(response.data.user))
        console.log('Auto-login successful, token:', response.data.token)
      } else {
        console.error('Login failed:', response)
      }
    } catch (error) {
      console.error('Auto-login failed:', error)
    }
  } else {
    console.log('Existing token found:', existingToken)
  }
}) 