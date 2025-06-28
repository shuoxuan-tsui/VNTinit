<template>
  <!-- 
    整体设计: 
    - 采用渐变背景和多个绝对定位的、带有动画效果的装饰元素，创造出一种现代、动态且富有科技感的视觉效果。
    - 这种设计旨在提升用户的第一印象，使枯燥的登录过程变得更加生动有趣。
    - `overflow-hidden` 防止装饰元素溢出造成滚动条。
  -->
  <div class="min-h-screen bg-gradient-to-br from-sky-50 via-indigo-50 to-purple-50 flex items-center justify-center p-4 relative overflow-hidden">
    <!-- 背景装饰元素 - 这些元素纯粹为了美观，通过模糊、动画和渐变效果增加页面的层次感和动态感 -->
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
      
      <!-- 几何线条装饰 -->
      <svg class="absolute top-0 left-0 w-full h-full opacity-10" viewBox="0 0 100 100" preserveAspectRatio="none">
        <defs>
          <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#3B82F6;stop-opacity:0.3" />
            <stop offset="100%" style="stop-color:#8B5CF6;stop-opacity:0.1" />
          </linearGradient>
        </defs>
        <!-- SVG 动画: 使用 <animate> 标签让线条的路径 (d) 属性在不同值之间平滑过渡，产生流动的效果 -->
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

    <!-- 
      登录表单容器:
      - `relative z-10`: 确保表单在背景装饰元素之上。
     -->
    <div class="max-w-md w-full space-y-8 relative z-10">
      <!-- Logo and Title -->
      <div class="text-center">
        <div class="mx-auto h-16 w-16 bg-gradient-to-r from-sky-600 to-indigo-600 rounded-full flex items-center justify-center mb-4 shadow-lg">
          <svg class="h-8 w-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-4m-5 0H9m0 0H5m0 0h2M7 3h10M9 9h6m-6 4h6m-6 4h6"></path>
          </svg>
        </div>
        <h2 class="text-3xl font-bold text-gray-900">企业管理系统</h2>
        <p class="mt-2 text-sm text-gray-600">请登录您的账户</p>
      </div>

      <!-- 
        登录表单卡片:
        - `bg-white/80 backdrop-blur-sm`: 实现毛玻璃效果，提升了UI的现代感和层次感。
        - `shadow-xl border border-white/20`: 精致的阴影和边框效果，使卡片从背景中脱颖而出。
       -->
      <div class="bg-white/80 backdrop-blur-sm rounded-xl shadow-xl border border-white/20 p-8">
        <!-- 
          表单提交事件:
          - `@submit.prevent="handleLogin"`: 监听表单的 submit 事件，并调用 `handleLogin` 方法。
          - `.prevent` 是一个事件修饰符，用于阻止表单提交的默认行为（即页面刷新）。
         -->
        <form @submit.prevent="handleLogin" class="space-y-6">
          <!-- Username Field -->
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700 mb-2">
              用户名
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
                class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-transparent transition-colors bg-white/90"
                :class="{ 'border-red-500': errors.username }"
                placeholder="请输入用户名"
              />
            </div>
            <!-- 
              v-if 指令:
              - 用于条件性地渲染一个元素。只有当 `errors.username` 为真（即存在错误信息）时，这个 <p> 标签才会被渲染到 DOM 中。
              - 这是实现即时表单验证反馈的关键。
             -->
            <p v-if="errors.username" class="mt-1 text-sm text-red-600">{{ errors.username }}</p>
          </div>

          <!-- Password Field -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
              密码
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
                class="block w-full pl-10 pr-10 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-transparent transition-colors bg-white/90"
                :class="{ 'border-red-500': errors.password }"
                placeholder="请输入密码"
              />
              <!-- 
                密码可见性切换按钮:
                - `@click="showPassword = !showPassword"`: 点击按钮时，切换 `showPassword` 的布尔值。
                - 输入框的 `type` 属性通过 `:type` 绑定到 `showPassword`，从而动态地在 'password' 和 'text' 类型之间切换。
                - `v-if` 和 `v-else` 用于切换显示/隐藏密码的图标。
               -->
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

          <!-- Remember Me -->
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <input
                id="remember"
                v-model="form.remember"
                type="checkbox"
                class="h-4 w-4 text-sky-600 focus:ring-sky-500 border-gray-300 rounded"
              />
              <label for="remember" class="ml-2 block text-sm text-gray-700">
                记住我
              </label>
            </div>
            <div class="text-sm">
              <NuxtLink to="/forgot-password" class="font-medium text-sky-600 hover:text-sky-500 transition-colors">
                忘记密码？
              </NuxtLink>
            </div>
          </div>

          <!-- 全局错误信息显示区域 -->
          <div v-if="loginError" class="bg-red-50 border border-red-200 rounded-lg p-3">
            <div class="flex">
              <svg class="h-5 w-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <p class="ml-2 text-sm text-red-600">{{ loginError }}</p>
            </div>
          </div>

          <!-- 
            提交按钮:
            - `:disabled="loading"`: 动态绑定 disabled 属性。当 `loading` 为 true 时，按钮被禁用，防止用户重复提交。
            - `transition-all duration-200 transform hover:scale-105`: 添加了平滑的过渡效果和悬停时的放大效果，提升了交互体验。
           -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-gradient-to-r from-sky-600 to-indigo-600 hover:from-sky-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-sky-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-105"
          >
            <!-- 加载指示器: 只有在 `loading` 为 true 时渲染，提供清晰的正在处理中的反馈 -->
            <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ loading ? '登录中...' : '登录' }}
          </button>
        </form>

        <!-- Register Link -->
        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            还没有账户？
            <NuxtLink to="/register" class="font-medium text-sky-600 hover:text-sky-500 transition-colors">
              立即注册
            </NuxtLink>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// --- 页面元数据 ---
/**
 * 设置页面元数据。
 * 设计思路:
 * - `layout: false`: 登录页面通常具有独特的、不包含全局导航栏或页脚的布局。
 *   设置为 `false` 可以禁用默认布局，使其成为一个完全独立的页面。
 */
definePageMeta({
  layout: false
})

// --- 状态管理 ---
const authStore = useAuthStore()

// --- 响应式数据 ---
/**
 * 表单数据对象。
 * 设计思路:
 * - 使用 `ref` 将整个表单数据包装成一个响应式对象。
 * - `v-model` 会直接绑定到这个对象的属性上，实现视图和数据的双向同步。
 */
const form = ref({
  username: '',
  password: '',
  remember: false
})

/**
 * 存储字段级别的验证错误。
 * 设计思路:
 * - `errors` 对象的键对应于表单字段的名称。
 * - 这种结构使得在模板中可以轻松地通过 `errors.username` 来显示特定字段的错误信息。
 */
const errors = ref({})

/**
 * 存储登录过程中发生的全局错误（例如，后端返回的认证失败信息）。
 */
const loginError = ref('')
const showPassword = ref(false)

// --- 方法 ---
/**
 * 客户端表单验证。
 * 设计思路:
 * - **即时反馈**: 在将数据发送到服务器之前进行客户端验证，可以立即向用户提供反馈，改善用户体验并减少不必要的网络请求。
 * - **错误累积**: 在函数开始时清空 `errors` 对象，然后逐个检查字段。如果发现错误，就填充相应的错误信息。
 * - **返回验证结果**: 通过返回 `Object.keys(errors.value).length === 0` 来判断整个表单是否有效。
 */
const validateForm = () => {
  errors.value = {}
  
  if (!form.value.username.trim()) {
    errors.value.username = '请输入用户名'
  }
  
  if (!form.value.password) {
    errors.value.password = '请输入密码'
  } else if (form.value.password.length < 6) {
    errors.value.password = '密码至少6位'
  }
  
  return Object.keys(errors.value).length === 0
}

/**
 * 登录处理函数。
 * 设计思路:
 * - **职责分离**: 此函数是UI层和业务逻辑层（authStore）之间的桥梁。
 * - **流程控制**:
 *   1. 首先调用 `validateForm()` 进行客户端验证，如果失败则中止执行。
 *   2. 清空之前的 `loginError`。
 *   3. 调用 `authStore.login()`，将登录的业务逻辑委托给 Pinia store。
 *   4. 使用 `try...catch` 块来处理 `authStore.login()` 可能抛出的错误。
 * - **成功导航**: 登录成功后，使用 `navigateTo('/')` 将用户重定向到仪表盘页面。
 * - **错误处理**: 捕获到错误后，将其内容赋值给 `loginError`，以便在UI上显示给用户。
 */
const handleLogin = async () => {
  if (!validateForm()) {
    return
  }
  
  loginError.value = ''
  
  try {
    // 将登录逻辑委托给 auth store
    await authStore.login({
      username: form.value.username,
      password: form.value.password
    })
    
    // 登录成功，跳转到主页
    await navigateTo('/')
    
  } catch (error) {
    console.error('Login error:', error)
    
    // 从 store 抛出的错误中提取信息并显示
    if (error.data?.message) {
      loginError.value = error.data.message
    } else if (error.message) {
      loginError.value = error.message
    } else {
      loginError.value = '登录失败，请检查用户名和密码'
    }
  }
}

// --- 计算属性 ---
/**
 * `loading` 计算属性。
 * 设计思路:
 * - 直接从 `authStore` 中派生加载状态。
 * - 这使得登录按钮的禁用状态和加载指示器的显示能够自动响应 store 中 `loading` 状态的变化。
 */
const loading = computed(() => authStore.loading)

// --- SEO 和浏览器标签页 ---
/**
 * `useHead` 是 Nuxt 3 提供的组合式函数，用于管理文档的 `<head>` 部分。
 * 设计思路:
 * - 设置页面标题可以提升SEO效果和用户体验（在浏览器标签页上显示清晰的标题）。
 */
useHead({
  title: '登录 - 企业管理系统'
})

// --- 生命周期钩子 ---
/**
 * `onMounted` 钩子。
 * 设计思路:
 * - 用于处理一种常见的用户体验场景：如果一个已经登录的用户不小心访问了登录页，
 *   系统应该自动将他们重定向到应用的主页，而不是再次显示登录表单。
 */
onMounted(() => {
  if (authStore.isAuthenticated) {
    navigateTo('/')
  }
})
</script>

<style scoped>
/* 
  自定义动画:
  - `@keyframes` 用于定义动画的各个阶段。
  - 这些自定义动画（float, pulse, bounce, ping）与 TailwindCSS 的动画工具类结合使用，
    为背景中的装饰元素提供更丰富、更具层次感的动态效果。
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