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

onMounted(() => {
  authStore.initAuth()
})
</script>
