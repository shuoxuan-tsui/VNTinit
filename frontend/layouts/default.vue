<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 顶部导航栏 -->
    <header class="bg-white shadow-sm border-b border-gray-200 fixed w-full top-0 z-50">
      <div class="px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- Logo 和菜单按钮 -->
          <div class="flex items-center">
            <button
              @click="toggleSidebar"
              class="p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary lg:hidden"
            >
              <Icon name="heroicons:bars-3" class="h-6 w-6" />
            </button>
            <div class="flex-shrink-0 flex items-center ml-4 lg:ml-0">
              <div class="flex items-center space-x-3">
                <div class="h-8 w-8 rounded-lg bg-primary flex items-center justify-center">
                  <Icon name="heroicons:building-office-2" class="h-5 w-5 text-white" />
                </div>
                <h1 class="text-xl font-bold text-gray-900">企业管理系统</h1>
              </div>
            </div>
          </div>

          <!-- 用户信息和通知 -->
          <div class="flex items-center space-x-4">
            <!-- 通知按钮 -->
            <button class="relative p-2 text-gray-400 hover:text-gray-500 hover:bg-gray-100 rounded-md">
              <Icon name="heroicons:bell" class="h-5 w-5" />
              <span class="absolute top-1 right-1 block h-2 w-2 rounded-full bg-red-400"></span>
            </button>
            
            <!-- 用户信息 -->
            <div class="flex items-center space-x-3">
              <div class="h-8 w-8 rounded-full bg-primary flex items-center justify-center">
                <Icon name="heroicons:user" class="h-5 w-5 text-white" />
              </div>
              <div class="hidden sm:block">
                <div class="text-sm font-medium text-gray-700">{{ user?.username || '管理员' }}</div>
                <div class="text-xs text-gray-500">{{ user?.role || '系统管理员' }}</div>
              </div>
            </div>
            
            <button
              @click="logout"
              class="text-gray-400 hover:text-gray-500 p-2 rounded-md hover:bg-gray-100"
              title="退出登录"
            >
              <Icon name="heroicons:arrow-right-on-rectangle" class="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- 侧边栏 -->
    <div class="flex pt-16">
      <!-- 侧边栏背景遮罩 (移动端) -->
      <div
        v-if="sidebarOpen"
        class="fixed inset-0 z-40 lg:hidden"
        @click="closeSidebar"
      >
        <div class="absolute inset-0 bg-gray-600 opacity-75"></div>
      </div>

      <!-- 侧边栏内容 -->
      <div
        :class="[
          'fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0',
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        ]"
        class="pt-16 lg:pt-0"
      >
        <div class="flex flex-col h-full">
          <!-- 导航菜单 -->
          <nav class="flex-1 px-3 py-6 space-y-1 overflow-y-auto">
            <NuxtLink
              v-for="item in navigation"
              :key="item.name"
              :to="item.href"
              class="group flex items-center px-3 py-2.5 text-sm font-medium rounded-xl transition-all duration-200 relative"
              :class="isActiveRoute(item.href) 
                ? 'bg-gradient-to-r from-primary to-primary-dark text-black shadow-lg transform scale-105' 
                : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900 hover:shadow-sm'"
              @click="closeSidebar"
            >
              <!-- 活跃状态的左侧指示条 -->
              <div 
                v-if="isActiveRoute(item.href)"
                class="absolute left-0 top-0 bottom-0 w-1 bg-black rounded-r-full"
              ></div>
              
              <Icon 
                :name="item.icon" 
                class="mr-3 h-5 w-5 flex-shrink-0 transition-colors duration-200"
                :class="isActiveRoute(item.href) ? 'text-black' : 'text-gray-400 group-hover:text-primary'"
              />
              <span class="truncate font-medium">{{ item.name }}</span>
              
              <!-- 活跃指示器 -->
              <div 
                v-if="isActiveRoute(item.href)"
                class="ml-auto flex items-center space-x-1"
              >
                <div class="w-1.5 h-1.5 bg-white rounded-full animate-pulse"></div>
                <div class="w-1 h-1 bg-white/70 rounded-full"></div>
              </div>
              
              <!-- 悬停时的箭头指示器 -->
              <Icon 
                v-if="!isActiveRoute(item.href)"
                name="heroicons:chevron-right" 
                class="ml-auto h-4 w-4 text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity duration-200"
              />
            </NuxtLink>
          </nav>

          <!-- 底部信息 -->
          <div class="p-4 border-t border-gray-200 bg-gray-50">
            <div class="text-xs text-gray-500 text-center space-y-1">
              <div>© 2024 企业管理系统</div>
              <div>版本 v1.0.0</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 主内容区域 -->
      <div class="flex-1 lg:ml-64">
        <main class="p-4 sm:p-6 lg:p-8 min-h-screen">
          <slot />
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'

// 使用认证store
const authStore = useAuthStore()

// 侧边栏状态
const sidebarOpen = ref(false)

// 用户信息从store获取
const user = computed(() => authStore.user)

// 当前路由
const route = useRoute()

// 导航菜单项
const navigation = ref([
  { name: '首页', href: '/', icon: 'heroicons:home' },
  { name: '员工管理', href: '/employees', icon: 'heroicons:users' },
  { name: '部门管理', href: '/departments', icon: 'heroicons:building-office' },
  { name: '薪资管理', href: '/salaries', icon: 'heroicons:banknotes' },
  { name: '考勤管理', href: '/attendance', icon: 'heroicons:clock' },
  { name: '绩效管理', href: '/performance', icon: 'heroicons:chart-bar' },
  { name: '报表中心', href: '/reports', icon: 'heroicons:document-chart-bar' },
  { name: '系统设置', href: '/settings', icon: 'heroicons:cog-6-tooth' }
])

// 切换侧边栏
const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}

// 关闭侧边栏
const closeSidebar = () => {
  sidebarOpen.value = false
}

// 判断当前路由是否激活
const isActiveRoute = (path) => {
  if (path === '/') {
    return route.path === '/'
  }
  return route.path.startsWith(path)
}

// 退出登录
const logout = async () => {
  try {
    await authStore.logout()
    await navigateTo('/login')
  } catch (error) {
    console.error('Logout error:', error)
  }
}

// 监听路由变化，自动关闭移动端侧边栏
watch(() => route.path, () => {
  if (process.client && window.innerWidth < 1024) {
    closeSidebar()
  }
})

// 初始化认证状态
onMounted(() => {
  authStore.initAuth()
})
</script> 