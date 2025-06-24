export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore()
  
  // 初始化认证状态
  authStore.initAuth()
  
  // 如果用户未认证，重定向到登录页
  if (!authStore.isAuthenticated) {
    return navigateTo('/login')
  }
}) 

// export function ({ store, redirect, router}) {
//   if(!store.auth.isAuthenticated){
//     return redirect('/login')
//   }
//   if(to.path === '/login' && store.auth.isAuthenticated){
//     return redirect('/')
//   }
//   if(to.path === '/forgot-password' && store.auth.isAuthenticated){
//     return redirect('/')
//   }
// }