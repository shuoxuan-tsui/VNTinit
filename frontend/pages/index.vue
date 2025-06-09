<script setup>
import { ref, computed, onMounted } from 'vue'

// 页面元数据
definePageMeta({
  layout: 'default',
  middleware: 'auth'
})

// 使用认证store
const authStore = useAuthStore()

// 响应式数据
const loading = ref(false)

// 用户信息从store获取
const user = computed(() => authStore.user)

// 当前日期
const currentDate = computed(() => {
  return new Date().toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  })
})

// 统计数据
const stats = ref({
  totalEmployees: 156,
  employeeGrowth: 12.5,
  totalDepartments: 8,
  attendanceRate: 96.8,
  averageSalary: 12500
})

// 部门统计
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

// 最近活动
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

// 待办事项
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

// 系统通知
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

// 方法
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

// 生命周期
onMounted(() => {
  // 初始化数据
  console.log('仪表盘加载完成')
})
</script>

<template>
  <div class="space-y-6">
    <!-- 页面标题 -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">仪表盘</h1>
        <p class="mt-2 text-sm text-gray-600">欢迎回来，{{ user?.username }}！今天是 {{ currentDate }}</p>
      </div>
      <div class="mt-4 sm:mt-0">
        <button
          @click="refreshData"
          :disabled="loading"
          class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary disabled:opacity-50"
        >
          <Icon name="heroicons:arrow-path" class="mr-2 h-4 w-4" :class="{ 'animate-spin': loading }" />
          刷新数据
        </button>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <!-- 员工总数 -->
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
            <NuxtLink to="/employees" class="font-medium text-primary hover:text-primary-dark">
              查看详情
            </NuxtLink>
          </div>
        </div>
      </div>

      <!-- 部门数量 -->
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

      <!-- 本月考勤率 -->
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

      <!-- 平均薪资 -->
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
      <!-- 部门员工分布 -->
      <div class="bg-white shadow rounded-lg">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-medium text-gray-900">部门员工分布</h3>
        </div>
        <div class="p-6">
          <div class="space-y-4">
            <div v-for="dept in departmentStats" :key="dept.name" class="flex items-center justify-between">
              <div class="flex items-center">
                <div class="w-3 h-3 rounded-full mr-3" :style="{ backgroundColor: dept.color }"></div>
                <span class="text-sm font-medium text-gray-900">{{ dept.name }}</span>
              </div>
              <div class="flex items-center space-x-2">
                <span class="text-sm text-gray-500">{{ dept.count }}人</span>
                <div class="w-20 bg-gray-200 rounded-full h-2">
                  <div 
                    class="h-2 rounded-full" 
                    :style="{ 
                      backgroundColor: dept.color, 
                      width: `${(dept.count / stats.totalEmployees) * 100}%` 
                    }"
                  ></div>
                </div>
                <span class="text-sm font-medium text-gray-900">{{ Math.round((dept.count / stats.totalEmployees) * 100) }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 最近活动 -->
      <div class="bg-white shadow rounded-lg">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-medium text-gray-900">最近活动</h3>
        </div>
        <div class="p-6">
          <div class="flow-root">
            <ul class="-mb-8">
              <li v-for="(activity, index) in recentActivities" :key="activity.id">
                <div class="relative pb-8" :class="{ 'pb-0': index === recentActivities.length - 1 }">
                  <span 
                    v-if="index !== recentActivities.length - 1"
                    class="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200"
                  ></span>
                  <div class="relative flex space-x-3">
                    <div>
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
      <!-- 待处理事项 -->
      <div class="bg-white shadow rounded-lg">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-medium text-gray-900">待处理事项</h3>
        </div>
        <div class="p-6">
          <div class="space-y-4">
            <div v-for="todo in todos" :key="todo.id" class="flex items-start space-x-3">
              <div class="flex-shrink-0">
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

      <!-- 系统通知 -->
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