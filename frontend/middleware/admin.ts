export default defineNuxtRouteMiddleware((to) => {
  const authStore = useAuthStore()
  
  // 检查用户是否已认证
  if (!authStore.isAuthenticated) {
    return navigateTo('/login')
  }
  
  // 检查用户是否为管理员
  if (!authStore.isAdmin) {
    throw createError({
      statusCode: 403,
      statusMessage: '您没有权限访问此页面'
    })
  }
})