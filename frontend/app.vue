<template>
  <div>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>

<script setup>
// initialize auth state
const authStore = useAuthStore()

// onMounted 是一个生命周期钩子，在组件挂载时执行
// 在组件挂载时，调用 authStore.initAuth() 方法，初始化认证状态
// onMounted 钩子会在组件挂载到 DOM (Document Object Model) 之后被调用。这意味着：
onMounted(() => {
  authStore.initAuth()
  
})
</script>
