<template>
  <div>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>

<script setup>
// 初始化认证状态
const authStore = useAuthStore()

onMounted(() => {
  authStore.initAuth()
})
</script>
