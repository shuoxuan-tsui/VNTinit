<template>
  <div class="min-h-screen bg-gradient-to-br from-sky-50 via-indigo-50 to-purple-50 flex items-center justify-center p-4 relative overflow-hidden">
    <!-- 背景装饰元素 -->
    <div class="absolute inset-0 overflow-hidden">
      <!-- 大圆形装饰 -->
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-sky-200/30 to-indigo-200/30 rounded-full blur-3xl animate-pulse"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-tr from-purple-200/30 to-pink-200/30 rounded-full blur-3xl animate-pulse" style="animation-delay: 2s;"></div>
      
      <!-- 中等圆形装饰 -->
      <div class="absolute top-20 left-20 w-32 h-32 bg-gradient-to-br from-blue-300/20 to-cyan-300/20 rounded-full blur-2xl animate-bounce" style="animation-duration: 3s;"></div>
      <div class="absolute bottom-20 right-20 w-24 h-24 bg-gradient-to-br from-indigo-300/20 to-purple-300/20 rounded-full blur-2xl animate-bounce" style="animation-duration: 4s; animation-delay: 1s;"></div>
      
      <!-- 小装饰点 -->
      <div class="absolute top-1/4 right-1/4 w-4 h-4 bg-sky-400/40 rounded-full animate-ping" style="animation-duration: 2s;"></div>
      <div class="absolute bottom-1/3 left-1/3 w-3 h-3 bg-indigo-400/40 rounded-full animate-ping" style="animation-duration: 3s; animation-delay: 1s;"></div>
      <div class="absolute top-1/2 left-1/4 w-2 h-2 bg-purple-400/40 rounded-full animate-ping" style="animation-duration: 4s; animation-delay: 2s;"></div>
      
      <!-- 几何线条 -->
      <svg class="absolute top-0 left-0 w-full h-full opacity-10" viewBox="0 0 100 100" preserveAspectRatio="none">
        <defs>
          <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#3B82F6;stop-opacity:0.3" />
            <stop offset="100%" style="stop-color:#8B5CF6;stop-opacity:0.1" />
          </linearGradient>
        </defs>
        <path d="M0,20 Q25,10 50,20 T100,20" stroke="url(#lineGradient)" stroke-width="0.5" fill="none">
          <animate attributeName="d" dur="8s" repeatCount="indefinite" 
                   values="M0,20 Q25,10 50,20 T100,20;M0,25 Q25,15 50,25 T100,25;M0,20 Q25,10 50,20 T100,20"/>
        </path>
        <path d="M0,80 Q25,70 50,80 T100,80" stroke="url(#lineGradient)" stroke-width="0.5" fill="none">
          <animate attributeName="d" dur="10s" repeatCount="indefinite" 
                   values="M0,80 Q25,70 50,80 T100,80;M0,75 Q25,85 50,75 T100,75;M0,80 Q25,70 50,80 T100,80"/>
        </path>
      </svg>
    </div>

    <div class="max-w-md w-full space-y-8 relative z-10">
      <!-- Logo and Title -->
      <div class="text-center">
        <div class="mx-auto h-16 w-16 bg-gradient-to-r from-orange-600 to-red-600 rounded-full flex items-center justify-center mb-4 shadow-lg">
          <svg class="h-8 w-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"></path>
          </svg>
        </div>
        <h2 class="text-3xl font-bold text-gray-900">忘记密码</h2>
        <p class="mt-2 text-sm text-gray-600">输入您的邮箱地址，我们将发送重置链接</p>
      </div>

      <!-- Reset Form -->
      <div class="bg-white/80 backdrop-blur-sm rounded-xl shadow-xl border border-white/20 p-8">
        <div v-if="!emailSent">
          <form @submit.prevent="handleResetRequest" class="space-y-6">
            <!-- Email Field -->
            <div>
              <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
                邮箱地址 <span class="text-red-500">*</span>
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"></path>
                  </svg>
                </div>
                <input
                  id="email"
                  v-model="form.email"
                  type="email"
                  required
                  class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-colors bg-white/90"
                  :class="{ 'border-red-500': errors.email }"
                  placeholder="请输入您的邮箱地址"
                />
              </div>
              <p v-if="errors.email" class="mt-1 text-sm text-red-600">{{ errors.email }}</p>
            </div>

            <!-- Error Message -->
            <div v-if="resetError" class="bg-red-50 border border-red-200 rounded-lg p-3">
              <div class="flex">
                <svg class="h-5 w-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <p class="ml-2 text-sm text-red-600">{{ resetError }}</p>
              </div>
            </div>

            <!-- Submit Button -->
            <button
              type="submit"
              :disabled="loading"
              class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-gradient-to-r from-orange-600 to-red-600 hover:from-orange-700 hover:to-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-105"
            >
              <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ loading ? '发送中...' : '发送重置链接' }}
            </button>
          </form>
        </div>

        <!-- Success Message -->
        <div v-else class="text-center space-y-4">
          <div class="mx-auto h-16 w-16 bg-green-100 rounded-full flex items-center justify-center">
            <svg class="h-8 w-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900">重置链接已发送</h3>
          <p class="text-sm text-gray-600">
            我们已向 <span class="font-medium">{{ form.email }}</span> 发送了密码重置链接。
            请检查您的邮箱并点击链接重置密码。
          </p>
          <p class="text-xs text-gray-500">
            如果您没有收到邮件，请检查垃圾邮件文件夹，或者 
            <button @click="resendEmail" class="text-orange-600 hover:text-orange-500 font-medium">
              重新发送
            </button>
          </p>
        </div>

        <!-- Back to Login -->
        <div class="mt-6 text-center">
          <NuxtLink to="/login" class="font-medium text-orange-600 hover:text-orange-500 transition-colors">
            ← 返回登录
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 设置页面布局
definePageMeta({
  layout: false
})

// 响应式数据
const form = ref({
  email: ''
})

const errors = ref({})
const resetError = ref('')
const loading = ref(false)
const emailSent = ref(false)

// 表单验证
const validateForm = () => {
  errors.value = {}
  
  if (!form.value.email.trim()) {
    errors.value.email = '请输入邮箱地址'
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) {
    errors.value.email = '请输入有效的邮箱地址'
  }
  
  return Object.keys(errors.value).length === 0
}

// 处理重置请求
const handleResetRequest = async () => {
  if (!validateForm()) {
    return
  }
  
  resetError.value = ''
  loading.value = true
  
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // 这里应该调用实际的API
    // await $fetch('/api/auth/forgot-password/', {
    //   method: 'POST',
    //   body: { email: form.value.email }
    // })
    
    emailSent.value = true
    
  } catch (error) {
    console.error('Reset password error:', error)
    resetError.value = '发送重置链接失败，请稍后重试'
  } finally {
    loading.value = false
  }
}

// 重新发送邮件
const resendEmail = async () => {
  emailSent.value = false
  await handleResetRequest()
}

// 页面标题
useHead({
  title: '忘记密码 - 企业管理系统'
})
</script>

<style scoped>
/* 自定义动画 */
@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

.animate-float {
  animation: float 3s ease-in-out infinite;
}

/* 增强的动画效果 */
.animate-pulse {
  animation: pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.animate-bounce {
  animation: bounce 2s infinite;
}

.animate-ping {
  animation: ping 2s cubic-bezier(0, 0, 0.2, 1) infinite;
}

/* 毛玻璃效果增强 */
.backdrop-blur-sm {
  backdrop-filter: blur(8px);
}
</style> 