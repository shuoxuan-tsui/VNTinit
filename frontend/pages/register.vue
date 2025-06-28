<template>
  <!-- 
    整体设计: 
    - 与登录页面共享相同的设计语言，包括动态的渐变背景和动画装饰元素，以保持品牌和视觉风格的一致性。
    - 这种一致性让用户在不同页面间切换时感觉流畅自然。
   -->
  <div class="min-h-screen bg-gradient-to-br from-sky-50 via-indigo-50 to-purple-50 flex items-center justify-center p-4 relative overflow-hidden">
    <!-- 背景装饰元素 (与登录页相同) -->
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
        <!-- 采用了不同的图标和颜色，以在视觉上区分注册和登录操作 -->
        <div class="mx-auto h-16 w-16 bg-gradient-to-r from-emerald-600 to-teal-600 rounded-full flex items-center justify-center mb-4 shadow-lg">
          <svg class="h-8 w-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"></path>
          </svg>
        </div>
        <h2 class="text-3xl font-bold text-gray-900">创建新账户</h2>
        <p class="mt-2 text-sm text-gray-600">加入企业管理系统</p>
      </div>

      <!-- 注册表单卡片 -->
      <div class="bg-white/80 backdrop-blur-sm rounded-xl shadow-xl border border-white/20 p-8">
        <form @submit.prevent="handleRegister" class="space-y-6">
          <!-- Username Field -->
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700 mb-2">
              用户名 <span class="text-red-500">*</span>
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
              </div>
              <input
                id="username"
                v-model="form.username"
                type="text"
                required
                class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-colors bg-white/90"
                :class="{ 'border-red-500': errors.username }"
                placeholder="请输入用户名（至少3位）"
              />
            </div>
            <p v-if="errors.username" class="mt-1 text-sm text-red-600">{{ errors.username }}</p>
          </div>

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
                class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-colors bg-white/90"
                :class="{ 'border-red-500': errors.email }"
                placeholder="请输入邮箱地址"
              />
            </div>
            <p v-if="errors.email" class="mt-1 text-sm text-red-600">{{ errors.email }}</p>
          </div>

          <!-- Password Field -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
              密码 <span class="text-red-500">*</span>
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                </svg>
              </div>
              <input
                id="password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                required
                class="block w-full pl-10 pr-10 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-colors bg-white/90"
                :class="{ 'border-red-500': errors.password }"
                placeholder="请输入密码（至少6位）"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center"
              >
                <svg v-if="showPassword" class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"></path>
                </svg>
                <svg v-else class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                </svg>
              </button>
            </div>
            <p v-if="errors.password" class="mt-1 text-sm text-red-600">{{ errors.password }}</p>
          </div>

          <!-- Confirm Password Field: 额外的字段用于确保用户正确输入密码 -->
          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-2">
              确认密码 <span class="text-red-500">*</span>
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <input
                id="confirmPassword"
                v-model="form.confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                required
                class="block w-full pl-10 pr-10 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-colors bg-white/90"
                :class="{ 'border-red-500': errors.confirmPassword }"
                placeholder="请再次输入密码"
              />
              <button
                type="button"
                @click="showConfirmPassword = !showConfirmPassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center"
              >
                <svg v-if="showConfirmPassword" class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"></path>
                </svg>
                <svg v-else class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                </svg>
              </button>
            </div>
            <p v-if="errors.confirmPassword" class="mt-1 text-sm text-red-600">{{ errors.confirmPassword }}</p>
          </div>

          <!-- Terms Agreement Checkbox: 法律合规性要求，确保用户同意相关条款 -->
          <div>
            <div class="flex items-start">
              <input
                id="agreeTerms"
                v-model="form.agreeTerms"
                type="checkbox"
                class="h-4 w-4 text-emerald-600 focus:ring-emerald-500 border-gray-300 rounded mt-1"
                :class="{ 'border-red-500': errors.agreeTerms }"
              />
              <label for="agreeTerms" class="ml-2 block text-sm text-gray-700">
                我已阅读并同意
                <a href="#" class="font-medium text-emerald-600 hover:text-emerald-500 transition-colors">服务条款</a>
                和
                <a href="#" class="font-medium text-emerald-600 hover:text-emerald-500 transition-colors">隐私政策</a>
                <span class="text-red-500">*</span>
              </label>
            </div>
            <p v-if="errors.agreeTerms" class="mt-1 text-sm text-red-600">{{ errors.agreeTerms }}</p>
          </div>

          <!-- 全局注册错误信息 -->
          <div v-if="registerError" class="bg-red-50 border border-red-200 rounded-lg p-3">
            <div class="flex">
              <svg class="h-5 w-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <p class="ml-2 text-sm text-red-600">{{ registerError }}</p>
            </div>
          </div>

          <!-- 提交按钮 -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-105"
          >
            <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ loading ? '注册中...' : '创建账户' }}
          </button>
        </form>

        <!-- Login Link -->
        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            已有账户？
            <NuxtLink to="/login" class="font-medium text-emerald-600 hover:text-emerald-500 transition-colors">
              立即登录
            </NuxtLink>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// --- 页面元数据 ---
definePageMeta({
  layout: false // 注册页同样使用无布局的独立页面
})

// --- 状态管理 ---
const authStore = useAuthStore()

// --- 响应式数据 ---
/**
 * 注册表单的响应式数据模型。
 * 设计思路:
 * - 包含了所有注册所需的字段，包括 `confirmPassword` 和 `agreeTerms`，
 *   这些是登录表单所没有的。
 */
const form = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  agreeTerms: false
})

/**
 * 存储字段级别的验证错误。
 */
const errors = ref({})

/**
 * 存储全局的注册错误。
 */
const registerError = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)

// --- 方法 ---
/**
 * 客户端表单验证。
 * 设计思路:
 * - **更全面的规则**: 相比登录，注册的验证规则更严格。
 *   - 验证用户名长度和字符集。
 *   - 使用正则表达式验证邮箱格式。
 *   - 检查密码长度。
 *   - 确认两次输入的密码是否一致。
 *   - 确保用户已勾选同意条款。
 * - 这些规则确保了提交到后端的数据有较高的质量。
 */
const validateForm = () => {
  errors.value = {}
  
  if (!form.value.username.trim()) {
    errors.value.username = '请输入用户名'
  } else if (form.value.username.length < 3) {
    errors.value.username = '用户名至少3位'
  } else if (!/^[a-zA-Z0-9_]+$/.test(form.value.username)) {
    errors.value.username = '用户名只能包含字母、数字和下划线'
  }
  
  if (!form.value.email.trim()) {
    errors.value.email = '请输入邮箱'
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) {
    errors.value.email = '请输入有效的邮箱地址'
  }
  
  if (!form.value.password) {
    errors.value.password = '请输入密码'
  } else if (form.value.password.length < 6) {
    errors.value.password = '密码至少6位'
  }
  
  if (!form.value.confirmPassword) {
    errors.value.confirmPassword = '请确认密码'
  } else if (form.value.password !== form.value.confirmPassword) {
    errors.value.confirmPassword = '两次输入的密码不一致'
  }
  
  if (!form.value.agreeTerms) {
    errors.value.agreeTerms = '请同意服务条款和隐私政策'
  }
  
  return Object.keys(errors.value).length === 0
}

/**
 * 注册处理函数。
 * 设计思路:
 * - **调用 store 的 register action**: 将注册逻辑委托给 `authStore`。
 * - **成功后的重定向**:
 *   - `await navigateTo('/login?message=注册成功，请登录')`: 这是关键。
 *   - 注册成功后，并不直接为用户登录，而是将用户重定向到登录页面，并附带一个查询参数 `message`。
 *   - 这样做是出于安全和流程清晰的考虑：
 *     1. 分离了注册和登录的流程。
 *     2. 可能需要用户进行邮箱验证等后续步骤才能登录。
 *     3. 登录页可以解析 URL 中的 `message` 参数，向用户显示一个成功的提示信息，引导他们进行下一步操作。
 * - **错误处理**: 与登录页面类似，捕获并显示来自 store 的错误信息。
 */
const handleRegister = async () => {
  if (!validateForm()) {
    return
  }
  
  registerError.value = ''
  
  try {
    // 使用认证store进行注册
    await authStore.register({
      username: form.value.username,
      email: form.value.email,
      password: form.value.password
    })
    
    // 注册成功，跳转到登录页面并附带成功提示信息
    await navigateTo('/login?message=注册成功，请登录')
    
  } catch (error) {
    console.error('Register error:', error)
    
    // 处理错误信息
    if (error.data?.message) {
      registerError.value = error.data.message
    } else if (error.message) {
      registerError.value = error.message
    } else {
      registerError.value = '注册失败，请稍后重试'
    }
  }
}

// --- 计算属性 ---
const loading = computed(() => authStore.loading)

// --- SEO 和浏览器标签页 ---
useHead({
  title: '注册 - 企业管理系统'
})

// --- 生命周期钩子 ---
// 与登录页逻辑相同，防止已登录用户访问注册页。
onMounted(() => {
  if (authStore.isAuthenticated) {
    navigateTo('/')
  }
})
</script>

<style scoped>
/* 
  样式与登录页共享，以保持视觉一致性。
  scoped 属性确保这些样式只作用于当前组件，不会泄露到全局。
*/
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