<script setup>
import { ref, computed, onMounted } from 'vue'

// --- 页面元数据定义 ---
/**
 * `definePageMeta` 是 Nuxt 3 提供的宏，用于设置当前页面的特定元数据。
 * 设计思路:
 * - `layout: 'default'`: 指定该页面使用名为 'default' 的布局文件。这有助于保持应用内页面风格的统一性，
 *   例如，所有使用此布局的页面都会有相同的页眉和页脚。
 * - `middleware: 'auth'`: 指定页面需要经过 'auth' 中间件的处理。中间件是在页面渲染前执行的逻辑，
 *   'auth' 中间件通常用于检查用户是否已登录，如果未登录，则会重定向到登录页面，从而保护了该页面。
 */
definePageMeta({
  layout: 'default',
  middleware: 'auth'
})

// --- 状态管理 ---
/**
 * 引入并实例化认证 store。
 * 设计思路:
 * - 通过 `useAuthStore()`，该组件可以访问和响应 Pinia store 中管理的全局认证状态（如用户信息）。
 * - 这是组件与全局状态进行交互的标准方式，使得状态管理解耦且集中。
 */
const authStore = useAuthStore()

// --- 响应式数据 ---
/**
 * 页面级别的加载状态。
 * 设计思路:
 * - 用于控制页面上需要等待异步操作（如刷新数据）的元素的UI状态，例如禁用按钮、显示加载动画。
 */
const loading = ref(false)

// --- 计算属性 (Computed Properties) ---
/**
 * 从 store 中获取当前登录的用户信息。
 * 设计思路:
 * - 使用 `computed` 可以确保当 `authStore.user` 发生变化时，所有使用 `user` 的模板部分都会自动更新。
 * - 这比直接在模板中使用 `authStore.user` 更简洁，也便于在脚本中直接访问。
 */
const user = computed(() => authStore.user)

/**
 * 获取并格式化当前日期。
 * 设计思路:
 * - `computed` 确保了日期的响应式，虽然在这里日期通常只在加载时计算一次。
 * - 将日期格式化逻辑封装在计算属性中，使模板代码更干净。
 */
const currentDate = computed(() => {
  return new Date().toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  })
})

// --- 静态模拟数据 ---
/**
 * 注意：以下数据目前是硬编码的静态数据，用于UI展示和原型开发。
 * 在实际应用中，这些数据应该通过 API 从后端获取。
 * 
 * 设计思路:
 * - **快速原型**: 在后端接口未就绪时，使用静态数据可以快速搭建和测试前端页面结构与交互。
 * - **数据结构定义**: 这些静态数据也为后端API定义了期望的数据结构。
 */

// 仪表盘顶部的核心统计指标
const stats = ref({
  totalEmployees: 68,
  employeeGrowth: 12.5,
  totalDepartments: 6,
  attendanceRate: 96.8,
  averageSalary: 12500
})

// 部门员工分布统计，用于图表展示
const departmentStats = ref([
  { name: '技术部', count: 45, color: '#3B82F6' },
  { name: '市场部', count: 28, color: '#10B981' },
  { name: '人事部', count: 18, color: '#F59E0B' },
  { name: '财务部', count: 15, color: '#EF4444' },
  { name: '运营部', count: 22, color: '#8B5CF6' },
  { name: '客服部', count: 12, color: '#06B6D4' },
  { name: '行政部', count: 10, color: '#84CC16' },
  { name: '法务部', count: 6, color: '#F97316' }
])

// 最近的系统或用户活动流
const recentActivities = ref([
  {
    id: 1,
    content: '张三 完成了入职手续',
    time: '2小时前',
    icon: 'heroicons:user-plus',
    iconBg: 'bg-green-500',
    iconColor: 'text-white'
  },
  {
    id: 2,
    content: '李四 提交了请假申请',
    time: '4小时前',
    icon: 'heroicons:calendar',
    iconBg: 'bg-blue-500',
    iconColor: 'text-white'
  },
  {
    id: 3,
    content: '王五 的薪资已发放',
    time: '6小时前',
    icon: 'heroicons:banknotes',
    iconBg: 'bg-yellow-500',
    iconColor: 'text-white'
  },
  {
    id: 4,
    content: '技术部 完成了月度考核',
    time: '1天前',
    icon: 'heroicons:chart-bar',
    iconBg: 'bg-purple-500',
    iconColor: 'text-white'
  }
])

// 用户的待办事项列表
const todos = ref([
  {
    id: 1,
    title: '审批李四的请假申请',
    description: '病假3天，需要主管审批',
    dueDate: '今天 17:00',
    priority: 'high'
  },
  {
    id: 2,
    title: '完成月度薪资核算',
    description: '核对所有员工的薪资数据',
    dueDate: '明天 12:00',
    priority: 'medium'
  },
  {
    id: 3,
    title: '更新员工手册',
    description: '根据新政策更新相关条款',
    dueDate: '本周五',
    priority: 'low'
  }
])

// 系统级别的通知信息
const notifications = ref([
  {
    id: 1,
    title: '系统维护通知',
    message: '系统将于本周日凌晨2:00-4:00进行维护',
    time: '1小时前',
    icon: 'heroicons:wrench-screwdriver',
    iconBg: 'bg-blue-100',
    iconColor: 'text-blue-600'
  },
  {
    id: 2,
    title: '新功能上线',
    message: '绩效管理模块已上线，欢迎体验',
    time: '3小时前',
    icon: 'heroicons:sparkles',
    iconBg: 'bg-green-100',
    iconColor: 'text-green-600'
  },
  {
    id: 3,
    title: '数据备份完成',
    message: '昨日数据备份已完成，数据安全有保障',
    time: '1天前',
    icon: 'heroicons:shield-check',
    iconBg: 'bg-yellow-100',
    iconColor: 'text-yellow-600'
  }
])

// --- 方法 (Methods) ---
/**
 * 刷新页面的数据。
 * 设计思路:
 * - 这是一个异步函数，用于模拟从后端重新获取数据的过程。
 * - 通过设置 `loading` 状态，可以给用户明确的反馈，并防止在刷新期间进行其他操作。
 * - 在实际应用中，`setTimeout` 会被替换为真实的 `$fetch` API 调用。
 */
const refreshData = async () => {
  loading.value = true
  try {
    // 模拟数据刷新
    await new Promise(resolve => setTimeout(resolve, 1000))
    console.log('数据刷新完成')
  } catch (error) {
    console.error('数据刷新失败:', error)
  } finally {
    loading.value = false
  }
}

// --- 生命周期钩子 (Lifecycle Hooks) ---
/**
 * `onMounted` 是 Vue 的生命周期钩子之一，在组件被挂载到 DOM 后执行。
 * 设计思路:
 * - 这里可以放置需要与DOM交互或在组件加载后立即执行的初始化代码。
 * - 例如，可以在这里触发第一次数据获取 `refreshData()`。当前实现只是打印一条日志。
 */
onMounted(() => {
  // 初始化数据
  console.log('仪表盘加载完成')
})
</script>

<template>
  <!-- 
    整体布局设计:
    - 使用 Flexbox 和 Grid 布局系统 (TailwindCSS) 来构建响应式的页面结构。
    - 采用卡片式设计 (Card) 来组织和分隔不同的信息模块，使界面清晰、易于理解。
    - 大量使用 `space-y-6` 等间距工具类，确保元素之间有一致的视觉距离。
   -->
  <div class="space-y-6">
    <!-- 页面标题和欢迎信息 -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">仪表盘</h1>
        <!-- 动态显示用户名和当前日期 -->
        <p class="mt-2 text-sm text-gray-600">欢迎回来，{{ user?.username }}！今天是 {{ currentDate }}</p>
      </div>
      <div class="mt-4 sm:mt-0">
        <!-- 刷新数据按钮 -->
        <button
          @click="refreshData"
          :disabled="loading"
          class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary disabled:opacity-50"
        >
          <!-- 
            Icon 组件: 使用 nuxt-icon 模块动态加载图标。
            - `:class="{ 'animate-spin': loading }"`: 这是一个动态类绑定。当 `loading` 为 `true` 时，会添加 `animate-spin` 类，使图标旋转，提供视觉反馈。
           -->
          <Icon name="heroicons:arrow-path" class="mr-2 h-4 w-4" :class="{ 'animate-spin': loading }" />
          刷新数据
        </button>
      </div>
    </div>

    <!-- 统计卡片区域 -->
    <!-- 响应式网格布局: 在小屏幕上是1列，中等屏幕2列，大屏幕4列 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <!-- 员工总数卡片 -->
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="h-12 w-12 rounded-lg bg-blue-100 flex items-center justify-center">
                <Icon name="heroicons:users" class="h-6 w-6 text-blue-600" />
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">员工总数</dt>
                <dd class="flex items-baseline">
                  <!-- 显示静态数据 -->
                  <div class="text-2xl font-semibold text-gray-900">{{ stats.totalEmployees }}</div>
                  <div class="ml-2 flex items-baseline text-sm font-semibold text-green-600">
                    <Icon name="heroicons:arrow-up" class="h-3 w-3 flex-shrink-0" />
                    <span class="sr-only">增长</span>
                    {{ stats.employeeGrowth }}%
                  </div>
                </dd>
              </dl>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-5 py-3">
          <div class="text-sm">
            <!-- NuxtLink 是 Nuxt 中用于应用内导航的组件，它会被渲染成 <a> 标签，但能实现更高效的客户端路由，避免页面整体刷新。 -->
            <NuxtLink to="/employees" class="font-medium text-primary hover:text-primary-dark">
              查看详情
            </NuxtLink>
          </div>
        </div>
      </div>

      <!-- 部门数量卡片 -->
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="h-12 w-12 rounded-lg bg-green-100 flex items-center justify-center">
                <Icon name="heroicons:building-office" class="h-6 w-6 text-green-600" />
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">部门数量</dt>
                <dd class="flex items-baseline">
                  <div class="text-2xl font-semibold text-gray-900">{{ stats.totalDepartments }}</div>
                </dd>
              </dl>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-5 py-3">
          <div class="text-sm">
            <NuxtLink to="/departments" class="font-medium text-primary hover:text-primary-dark">
              查看详情
            </NuxtLink>
          </div>
        </div>
      </div>

      <!-- 本月考勤率卡片 -->
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="h-12 w-12 rounded-lg bg-yellow-100 flex items-center justify-center">
                <Icon name="heroicons:clock" class="h-6 w-6 text-yellow-600" />
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">本月考勤率</dt>
                <dd class="flex items-baseline">
                  <div class="text-2xl font-semibold text-gray-900">{{ stats.attendanceRate }}%</div>
                  <div class="ml-2 flex items-baseline text-sm font-semibold text-green-600">
                    <Icon name="heroicons:arrow-up" class="h-3 w-3 flex-shrink-0" />
                    <span class="sr-only">增长</span>
                    2.1%
                  </div>
                </dd>
              </dl>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-5 py-3">
          <div class="text-sm">
            <NuxtLink to="/attendance" class="font-medium text-primary hover:text-primary-dark">
              查看详情
            </NuxtLink>
          </div>
        </div>
      </div>

      <!-- 平均薪资卡片 -->
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="h-12 w-12 rounded-lg bg-purple-100 flex items-center justify-center">
                <Icon name="heroicons:banknotes" class="h-6 w-6 text-purple-600" />
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">平均薪资</dt>
                <dd class="flex items-baseline">
                  <!-- `.toLocaleString()` 用于将数字格式化为带千位分隔符的字符串，提升可读性。 -->
                  <div class="text-2xl font-semibold text-gray-900">¥{{ stats.averageSalary.toLocaleString() }}</div>
                </dd>
              </dl>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-5 py-3">
          <div class="text-sm">
            <NuxtLink to="/salaries" class="font-medium text-primary hover:text-primary-dark">
              查看详情
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>

    <!-- 图表和数据展示 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 部门员工分布图表 -->
      <div class="bg-white shadow rounded-lg">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-medium text-gray-900">部门员工分布</h3>
        </div>
        <div class="p-6">
          <div class="space-y-4">
            <!-- 
              v-for 列表渲染:
              - 遍历 `departmentStats` 数组，为每个部门动态生成一个条目。
              - `:key="dept.name"` 为每个循环项提供一个唯一的 key，这对于 Vue 的高效更新至关重要。
             -->
            <div v-for="dept in departmentStats" :key="dept.name" class="flex items-center justify-between">
              <div class="flex items-center">
                <!-- 动态绑定样式: `:style` 用于直接绑定内联样式。这里根据每个部门的颜色数据设置色块。 -->
                <div class="w-3 h-3 rounded-full mr-3" :style="{ backgroundColor: dept.color }"></div>
                <span class="text-sm font-medium text-gray-900">{{ dept.name }}</span>
              </div>
              <div class="flex items-center space-x-2">
                <span class="text-sm text-gray-500">{{ dept.count }}人</span>
                <div class="w-20 bg-gray-200 rounded-full h-2">
                  <!-- 进度条实现: 这是一个简单的基于 div 的进度条，通过计算宽度百分比来展示。 -->
                  <div 
                    class="h-2 rounded-full" 
                    :style="{ 
                      backgroundColor: dept.color, 
                      width: `${(dept.count / stats.totalEmployees) * 100}%` 
                    }"
                  ></div>
                </div>
                <!-- 显示计算出的百分比 -->
                <span class="text-sm font-medium text-gray-900">{{ Math.round((dept.count / stats.totalEmployees) * 100) }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 最近活动时间线 -->
      <div class="bg-white shadow rounded-lg">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-medium text-gray-900">最近活动</h3>
        </div>
        <div class="p-6">
          <div class="flow-root">
            <ul class="-mb-8">
              <!-- 使用 v-for 和 index 来构建时间线 -->
              <li v-for="(activity, index) in recentActivities" :key="activity.id">
                <div class="relative pb-8" :class="{ 'pb-0': index === recentActivities.length - 1 }">
                  <!-- 时间线竖线: 通过 v-if 判断，最后一条活动下方不显示竖线 -->
                  <span 
                    v-if="index !== recentActivities.length - 1"
                    class="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200"
                  ></span>
                  <div class="relative flex space-x-3">
                    <div>
                      <!-- 动态绑定背景色和图标颜色 -->
                      <span class="h-8 w-8 rounded-full flex items-center justify-center ring-8 ring-white" :class="activity.iconBg">
                        <Icon :name="activity.icon" class="h-4 w-4" :class="activity.iconColor" />
                      </span>
                    </div>
                    <div class="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4">
                      <div>
                        <p class="text-sm text-gray-500">
                          {{ activity.content }}
                        </p>
                      </div>
                      <div class="text-right text-sm whitespace-nowrap text-gray-500">
                        {{ activity.time }}
                      </div>
                    </div>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- 快捷操作 -->
    <div class="bg-white shadow rounded-lg">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-medium text-gray-900">快捷操作</h3>
      </div>
      <div class="p-6">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <NuxtLink
            to="/employees/add"
            class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-primary border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
          >
            <div>
              <span class="rounded-lg inline-flex p-3 bg-blue-50 text-blue-700 ring-4 ring-white">
                <Icon name="heroicons:user-plus" class="h-6 w-6" />
              </span>
            </div>
            <div class="mt-4">
              <h3 class="text-lg font-medium text-gray-900">
                添加员工
              </h3>
              <p class="mt-2 text-sm text-gray-500">
                录入新员工信息
              </p>
            </div>
          </NuxtLink>

          <NuxtLink
            to="/salaries"
            class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-primary border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
          >
            <div>
              <span class="rounded-lg inline-flex p-3 bg-green-50 text-green-700 ring-4 ring-white">
                <Icon name="heroicons:calculator" class="h-6 w-6" />
              </span>
            </div>
            <div class="mt-4">
              <h3 class="text-lg font-medium text-gray-900">
                薪资计算
              </h3>
              <p class="mt-2 text-sm text-gray-500">
                计算员工薪资
              </p>
            </div>
          </NuxtLink>

          <NuxtLink
            to="/attendance"
            class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-primary border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
          >
            <div>
              <span class="rounded-lg inline-flex p-3 bg-yellow-50 text-yellow-700 ring-4 ring-white">
                <Icon name="heroicons:clock" class="h-6 w-6" />
              </span>
            </div>
            <div class="mt-4">
              <h3 class="text-lg font-medium text-gray-900">
                考勤打卡
              </h3>
              <p class="mt-2 text-sm text-gray-500">
                记录考勤信息
              </p>
            </div>
          </NuxtLink>

          <NuxtLink
            to="/reports"
            class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-primary border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
          >
            <div>
              <span class="rounded-lg inline-flex p-3 bg-purple-50 text-purple-700 ring-4 ring-white">
                <Icon name="heroicons:document-chart-bar" class="h-6 w-6" />
              </span>
            </div>
            <div class="mt-4">
              <h3 class="text-lg font-medium text-gray-900">
                生成报表
              </h3>
              <p class="mt-2 text-sm text-gray-500">
                查看数据报表
              </p>
            </div>
          </NuxtLink>
        </div>
      </div>
    </div>

    <!-- 待办事项 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 待处理事项卡片 -->
      <div class="bg-white shadow rounded-lg">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-medium text-gray-900">待处理事项</h3>
        </div>
        <div class="p-6">
          <div class="space-y-4">
            <div v-for="todo in todos" :key="todo.id" class="flex items-start space-x-3">
              <div class="flex-shrink-0">
                <!-- 根据优先级动态设置颜色 -->
                <div class="h-2 w-2 rounded-full mt-2" :class="todo.priority === 'high' ? 'bg-red-400' : todo.priority === 'medium' ? 'bg-yellow-400' : 'bg-green-400'"></div>
              </div>
              <div class="min-w-0 flex-1">
                <p class="text-sm font-medium text-gray-900">{{ todo.title }}</p>
                <p class="text-sm text-gray-500">{{ todo.description }}</p>
                <p class="text-xs text-gray-400 mt-1">{{ todo.dueDate }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 系统通知卡片 -->
      <div class="bg-white shadow rounded-lg">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-medium text-gray-900">系统通知</h3>
        </div>
        <div class="p-6">
          <div class="space-y-4">
            <div v-for="notification in notifications" :key="notification.id" class="flex items-start space-x-3">
              <div class="flex-shrink-0">
                <div class="h-8 w-8 rounded-full flex items-center justify-center" :class="notification.iconBg">
                  <Icon :name="notification.icon" class="h-4 w-4" :class="notification.iconColor" />
                </div>
              </div>
              <div class="min-w-0 flex-1">
                <p class="text-sm font-medium text-gray-900">{{ notification.title }}</p>
                <p class="text-sm text-gray-500">{{ notification.message }}</p>
                <p class="text-xs text-gray-400 mt-1">{{ notification.time }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template> 