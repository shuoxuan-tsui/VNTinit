<script setup>
import { ref, computed, onMounted } from 'vue'

// 页面元数据
definePageMeta({
  layout: 'default'
})

// 响应式数据
const loading = ref(false)
const showAddModal = ref(false)
const showDetailModal = ref(false)
const selectedPerformance = ref(null)

// 搜索和筛选
const searchQuery = ref('')
const filters = ref({
  department: '',
  period: '',
  status: '',
  rating: ''
})

// 绩效数据
const performanceRecords = ref([
  {
    id: 1,
    employeeId: 'EMP001',
    employeeName: '张三',
    department: '技术部',
    position: '高级工程师',
    period: '2024年第一季度',
    status: 'completed',
    overallRating: 'A',
    score: 92,
    goals: [
      { name: '项目交付', target: '按时完成3个项目', actual: '完成3个项目，提前2天', score: 95 },
      { name: '代码质量', target: 'Bug率低于2%', actual: 'Bug率1.5%', score: 90 },
      { name: '团队协作', target: '积极参与团队活动', actual: '主动帮助新员工，参与所有团队活动', score: 90 }
    ],
    feedback: '表现优秀，技术能力强，团队合作良好',
    evaluator: '李经理',
    evaluatedAt: '2024-04-15'
  },
  {
    id: 2,
    employeeId: 'EMP002',
    employeeName: '李四',
    department: '市场部',
    position: '市场专员',
    period: '2024年第一季度',
    status: 'in_progress',
    overallRating: 'B+',
    score: 85,
    goals: [
      { name: '销售目标', target: '完成100万销售额', actual: '完成85万销售额', score: 85 },
      { name: '客户维护', target: '维护50个客户', actual: '维护48个客户', score: 85 },
      { name: '市场调研', target: '完成2份调研报告', actual: '完成1份调研报告', score: 80 }
    ],
    feedback: '工作积极，需要提升销售技巧',
    evaluator: '王总监',
    evaluatedAt: '2024-04-10'
  }
])

// 绩效统计
const performanceStats = ref({
  totalEvaluations: 156,
  completedEvaluations: 142,
  pendingEvaluations: 14,
  averageScore: 87.5,
  ratingDistribution: {
    'A': 45,
    'B+': 52,
    'B': 38,
    'C+': 18,
    'C': 3
  }
})

// 计算属性
const filteredRecords = computed(() => {
  let filtered = performanceRecords.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(record => 
      record.employeeName.toLowerCase().includes(query) ||
      record.employeeId.toLowerCase().includes(query) ||
      record.department.toLowerCase().includes(query)
    )
  }

  if (filters.value.department) {
    filtered = filtered.filter(record => record.department === filters.value.department)
  }

  if (filters.value.period) {
    filtered = filtered.filter(record => record.period === filters.value.period)
  }

  if (filters.value.status) {
    filtered = filtered.filter(record => record.status === filters.value.status)
  }

  if (filters.value.rating) {
    filtered = filtered.filter(record => record.overallRating === filters.value.rating)
  }

  return filtered
})

const departments = computed(() => {
  return [...new Set(performanceRecords.value.map(record => record.department))]
})

const periods = computed(() => {
  return [...new Set(performanceRecords.value.map(record => record.period))]
})

// 方法
const getStatusText = (status) => {
  const statusMap = {
    'completed': '已完成',
    'in_progress': '进行中',
    'pending': '待开始',
    'overdue': '已逾期'
  }
  return statusMap[status] || status
}

const getStatusColor = (status) => {
  const colorMap = {
    'completed': 'text-green-600 bg-green-100',
    'in_progress': 'text-blue-600 bg-blue-100',
    'pending': 'text-yellow-600 bg-yellow-100',
    'overdue': 'text-red-600 bg-red-100'
  }
  return colorMap[status] || 'text-gray-600 bg-gray-100'
}

const getRatingColor = (rating) => {
  const colorMap = {
    'A': 'text-green-600 bg-green-100',
    'B+': 'text-blue-600 bg-blue-100',
    'B': 'text-yellow-600 bg-yellow-100',
    'C+': 'text-orange-600 bg-orange-100',
    'C': 'text-red-600 bg-red-100'
  }
  return colorMap[rating] || 'text-gray-600 bg-gray-100'
}

const viewDetails = (record) => {
  selectedPerformance.value = record
  showDetailModal.value = true
}

const startEvaluation = () => {
  showAddModal.value = true
}

const exportReport = () => {
  console.log('导出绩效报告')
}

const clearFilters = () => {
  searchQuery.value = ''
  filters.value = {
    department: '',
    period: '',
    status: '',
    rating: ''
  }
}

// 生命周期
onMounted(() => {
  console.log('绩效管理页面加载完成')
})
</script>

<template>
  <div class="space-y-6">
    <!-- 页面标题 -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">绩效管理</h1>
        <p class="mt-2 text-sm text-gray-600">管理员工绩效考核和评估，共 {{ filteredRecords.length }} 条记录</p>
      </div>
      <div class="mt-4 sm:mt-0 flex space-x-3">
        <button
          @click="exportReport"
          class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-all duration-200 shadow-sm"
        >
          <Icon name="heroicons:arrow-down-tray" class="mr-2 h-4 w-4" />
          导出报告
        </button>
        <button
          @click="startEvaluation"
          class="inline-flex items-center px-6 py-2.5 border border-transparent text-sm font-semibold rounded-lg shadow-md text-white bg-gradient-to-r from-primary to-primary-dark hover:from-primary-dark hover:to-primary focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transform hover:scale-105 transition-all duration-200"
        >
          <Icon name="heroicons:plus" class="mr-2 h-4 w-4" />
          开始评估
        </button>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="h-12 w-12 rounded-lg bg-blue-100 flex items-center justify-center">
                <Icon name="heroicons:chart-bar" class="h-6 w-6 text-blue-600" />
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">总评估数</dt>
                <dd class="text-2xl font-semibold text-gray-900">{{ performanceStats.totalEvaluations }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="h-12 w-12 rounded-lg bg-green-100 flex items-center justify-center">
                <Icon name="heroicons:check-circle" class="h-6 w-6 text-green-600" />
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">已完成</dt>
                <dd class="text-2xl font-semibold text-gray-900">{{ performanceStats.completedEvaluations }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

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
                <dt class="text-sm font-medium text-gray-500 truncate">待评估</dt>
                <dd class="text-2xl font-semibold text-gray-900">{{ performanceStats.pendingEvaluations }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="h-12 w-12 rounded-lg bg-purple-100 flex items-center justify-center">
                <Icon name="heroicons:star" class="h-6 w-6 text-purple-600" />
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">平均分数</dt>
                <dd class="text-2xl font-semibold text-gray-900">{{ performanceStats.averageScore }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 搜索和筛选 -->
    <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        <div class="lg:col-span-2">
          <label class="block text-sm font-medium text-gray-700 mb-2">搜索</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Icon name="heroicons:magnifying-glass" class="h-5 w-5 text-gray-400" />
            </div>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="搜索员工姓名、工号..."
              class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary focus:border-primary sm:text-sm"
            />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">部门</label>
          <select v-model="filters.department" class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm">
            <option value="">全部部门</option>
            <option v-for="dept in departments" :key="dept" :value="dept">{{ dept }}</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">考核期间</label>
          <select v-model="filters.period" class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm">
            <option value="">全部期间</option>
            <option v-for="period in periods" :key="period" :value="period">{{ period }}</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">状态</label>
          <select v-model="filters.status" class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm">
            <option value="">全部状态</option>
            <option value="completed">已完成</option>
            <option value="in_progress">进行中</option>
            <option value="pending">待开始</option>
            <option value="overdue">已逾期</option>
          </select>
        </div>
      </div>

      <div class="flex items-center justify-between mt-4">
        <div class="text-sm text-gray-500">
          显示 {{ filteredRecords.length }} / {{ performanceRecords.length }} 条记录
        </div>
        <button
          @click="clearFilters"
          class="px-3 py-1 text-sm text-gray-600 hover:text-gray-800"
        >
          清空筛选
        </button>
      </div>
    </div>

    <!-- 绩效记录表格 -->
    <div class="bg-white shadow rounded-lg overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-medium text-gray-900">绩效记录</h3>
      </div>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">员工信息</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">考核期间</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">评级</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">分数</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">评估人</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="record in filteredRecords" :key="record.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="h-10 w-10 rounded-full bg-primary flex items-center justify-center">
                    <span class="text-sm font-medium text-white">{{ record.employeeName.charAt(0) }}</span>
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">{{ record.employeeName }}</div>
                    <div class="text-sm text-gray-500">{{ record.employeeId }} · {{ record.position }}</div>
                    <div class="text-sm text-gray-500">{{ record.department }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ record.period }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="inline-flex px-2 py-1 text-xs font-semibold rounded-full" :class="getStatusColor(record.status)">
                  {{ getStatusText(record.status) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="inline-flex px-2 py-1 text-xs font-semibold rounded-full" :class="getRatingColor(record.overallRating)">
                  {{ record.overallRating }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                <div class="flex items-center">
                  <span class="font-medium">{{ record.score }}</span>
                  <div class="ml-2 w-16 bg-gray-200 rounded-full h-2">
                    <div class="bg-primary h-2 rounded-full" :style="{ width: `${record.score}%` }"></div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ record.evaluator }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                <button
                  @click="viewDetails(record)"
                  class="text-primary hover:text-primary-dark"
                >
                  查看详情
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 绩效详情模态框 -->
    <div v-if="showDetailModal" class="fixed inset-0 z-50 overflow-y-auto">
      <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="showDetailModal = false"></div>
        
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full">
          <div class="bg-white px-6 py-4 border-b border-gray-200">
            <div class="flex items-center justify-between">
              <h3 class="text-lg font-medium text-gray-900">绩效详情</h3>
              <button @click="showDetailModal = false" class="text-gray-400 hover:text-gray-600">
                <Icon name="heroicons:x-mark" class="h-6 w-6" />
              </button>
            </div>
          </div>
          
          <div v-if="selectedPerformance" class="px-6 py-4 space-y-6">
            <!-- 基本信息 -->
            <div class="grid grid-cols-2 gap-6">
              <div>
                <h4 class="text-sm font-medium text-gray-900 mb-3">员工信息</h4>
                <dl class="space-y-2">
                  <div class="flex justify-between">
                    <dt class="text-sm text-gray-500">姓名:</dt>
                    <dd class="text-sm text-gray-900">{{ selectedPerformance.employeeName }}</dd>
                  </div>
                  <div class="flex justify-between">
                    <dt class="text-sm text-gray-500">工号:</dt>
                    <dd class="text-sm text-gray-900">{{ selectedPerformance.employeeId }}</dd>
                  </div>
                  <div class="flex justify-between">
                    <dt class="text-sm text-gray-500">部门:</dt>
                    <dd class="text-sm text-gray-900">{{ selectedPerformance.department }}</dd>
                  </div>
                  <div class="flex justify-between">
                    <dt class="text-sm text-gray-500">职位:</dt>
                    <dd class="text-sm text-gray-900">{{ selectedPerformance.position }}</dd>
                  </div>
                </dl>
              </div>
              
              <div>
                <h4 class="text-sm font-medium text-gray-900 mb-3">评估信息</h4>
                <dl class="space-y-2">
                  <div class="flex justify-between">
                    <dt class="text-sm text-gray-500">考核期间:</dt>
                    <dd class="text-sm text-gray-900">{{ selectedPerformance.period }}</dd>
                  </div>
                  <div class="flex justify-between">
                    <dt class="text-sm text-gray-500">总评级:</dt>
                    <dd class="text-sm text-gray-900">
                      <span class="inline-flex px-2 py-1 text-xs font-semibold rounded-full" :class="getRatingColor(selectedPerformance.overallRating)">
                        {{ selectedPerformance.overallRating }}
                      </span>
                    </dd>
                  </div>
                  <div class="flex justify-between">
                    <dt class="text-sm text-gray-500">总分数:</dt>
                    <dd class="text-sm text-gray-900 font-medium">{{ selectedPerformance.score }}</dd>
                  </div>
                  <div class="flex justify-between">
                    <dt class="text-sm text-gray-500">评估人:</dt>
                    <dd class="text-sm text-gray-900">{{ selectedPerformance.evaluator }}</dd>
                  </div>
                </dl>
              </div>
            </div>

            <!-- 目标完成情况 -->
            <div>
              <h4 class="text-sm font-medium text-gray-900 mb-3">目标完成情况</h4>
              <div class="space-y-4">
                <div v-for="goal in selectedPerformance.goals" :key="goal.name" class="border border-gray-200 rounded-lg p-4">
                  <div class="flex items-center justify-between mb-2">
                    <h5 class="text-sm font-medium text-gray-900">{{ goal.name }}</h5>
                    <span class="text-sm font-medium text-gray-900">{{ goal.score }}分</span>
                  </div>
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                    <div>
                      <span class="text-gray-500">目标:</span>
                      <p class="text-gray-900 mt-1">{{ goal.target }}</p>
                    </div>
                    <div>
                      <span class="text-gray-500">实际完成:</span>
                      <p class="text-gray-900 mt-1">{{ goal.actual }}</p>
                    </div>
                  </div>
                  <div class="mt-3">
                    <div class="w-full bg-gray-200 rounded-full h-2">
                      <div class="bg-primary h-2 rounded-full" :style="{ width: `${goal.score}%` }"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 评估反馈 -->
            <div>
              <h4 class="text-sm font-medium text-gray-900 mb-3">评估反馈</h4>
              <div class="bg-gray-50 rounded-lg p-4">
                <p class="text-sm text-gray-900">{{ selectedPerformance.feedback }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-gray-50 px-6 py-3 flex justify-end space-x-3">
            <button
              @click="showDetailModal = false"
              class="px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
            >
              关闭
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template> 