<script setup>
import { ref, computed, onMounted } from 'vue'

// 页面元数据
definePageMeta({
  layout: 'default'
})

// 响应式数据
const loading = ref(false)
const selectedReport = ref('employee')
const dateRange = ref({
  start: '2024-01-01',
  end: '2024-12-31'
})

// 报表类型
const reportTypes = ref([
  {
    id: 'employee',
    name: '员工统计报表',
    description: '员工数量、分布、流动等统计',
    icon: 'heroicons:users',
    color: 'blue'
  },
  {
    id: 'salary',
    name: '薪资分析报表',
    description: '薪资水平、成本分析等',
    icon: 'heroicons:banknotes',
    color: 'green'
  },
  {
    id: 'attendance',
    name: '考勤统计报表',
    description: '出勤率、加班、请假统计',
    icon: 'heroicons:clock',
    color: 'yellow'
  },
  {
    id: 'performance',
    name: '绩效分析报表',
    description: '绩效评估、目标完成情况',
    icon: 'heroicons:chart-bar',
    color: 'purple'
  },
  {
    id: 'department',
    name: '部门分析报表',
    description: '部门效率、成本分析',
    icon: 'heroicons:building-office',
    color: 'indigo'
  },
  {
    id: 'recruitment',
    name: '招聘分析报表',
    description: '招聘效果、渠道分析',
    icon: 'heroicons:user-plus',
    color: 'pink'
  }
])

// 员工统计数据
const employeeStats = ref({
  totalEmployees: 156,
  newHires: 12,
  departures: 5,
  turnoverRate: 3.2,
  departmentDistribution: [
    { name: '技术部', count: 45, percentage: 28.8 },
    { name: '市场部', count: 28, percentage: 17.9 },
    { name: '人事部', count: 18, percentage: 11.5 },
    { name: '财务部', count: 15, percentage: 9.6 },
    { name: '运营部', count: 22, percentage: 14.1 },
    { name: '客服部', count: 12, percentage: 7.7 },
    { name: '行政部', count: 10, percentage: 6.4 },
    { name: '法务部', count: 6, percentage: 3.8 }
  ],
  ageDistribution: [
    { range: '20-25岁', count: 25, percentage: 16.0 },
    { range: '26-30岁', count: 48, percentage: 30.8 },
    { range: '31-35岁', count: 42, percentage: 26.9 },
    { range: '36-40岁', count: 28, percentage: 17.9 },
    { range: '41-45岁', count: 10, percentage: 6.4 },
    { range: '46岁以上', count: 3, percentage: 1.9 }
  ],
  educationDistribution: [
    { level: '博士', count: 8, percentage: 5.1 },
    { level: '硕士', count: 45, percentage: 28.8 },
    { level: '本科', count: 89, percentage: 57.1 },
    { level: '专科', count: 12, percentage: 7.7 },
    { level: '其他', count: 2, percentage: 1.3 }
  ]
})

// 薪资统计数据
const salaryStats = ref({
  averageSalary: 12500,
  medianSalary: 11200,
  totalPayroll: 1950000,
  salaryGrowth: 8.5,
  departmentSalary: [
    { name: '技术部', average: 15800, total: 711000 },
    { name: '市场部', average: 11200, total: 313600 },
    { name: '人事部', average: 9800, total: 176400 },
    { name: '财务部', average: 12500, total: 187500 },
    { name: '运营部', average: 10800, total: 237600 },
    { name: '客服部', average: 8500, total: 102000 },
    { name: '行政部', average: 9200, total: 92000 },
    { name: '法务部', average: 18000, total: 108000 }
  ],
  salaryRanges: [
    { range: '5000以下', count: 8, percentage: 5.1 },
    { range: '5000-8000', count: 22, percentage: 14.1 },
    { range: '8000-12000', count: 45, percentage: 28.8 },
    { range: '12000-18000', count: 52, percentage: 33.3 },
    { range: '18000-25000', count: 23, percentage: 14.7 },
    { range: '25000以上', count: 6, percentage: 3.8 }
  ]
})

// 考勤统计数据
const attendanceStats = ref({
  averageAttendanceRate: 96.8,
  totalWorkDays: 22,
  totalAbsences: 45,
  overtimeHours: 1250,
  leaveRequests: 28,
  departmentAttendance: [
    { name: '技术部', rate: 97.2, absences: 12, overtime: 450 },
    { name: '市场部', rate: 95.8, absences: 8, overtime: 280 },
    { name: '人事部', rate: 98.1, absences: 3, overtime: 120 },
    { name: '财务部', rate: 97.5, absences: 4, overtime: 150 },
    { name: '运营部', rate: 96.2, absences: 9, overtime: 180 },
    { name: '客服部', rate: 95.5, absences: 6, overtime: 45 },
    { name: '行政部', rate: 98.0, absences: 2, overtime: 20 },
    { name: '法务部', rate: 97.8, absences: 1, overtime: 5 }
  ]
})

// 计算属性
const currentReportData = computed(() => {
  switch (selectedReport.value) {
    case 'employee':
      return employeeStats.value
    case 'salary':
      return salaryStats.value
    case 'attendance':
      return attendanceStats.value
    default:
      return {}
  }
})

const currentReportType = computed(() => {
  return reportTypes.value.find(type => type.id === selectedReport.value)
})

// 方法
const generateReport = async () => {
  loading.value = true
  try {
    // 模拟生成报表
    await new Promise(resolve => setTimeout(resolve, 2000))
    console.log('报表生成完成')
  } catch (error) {
    console.error('报表生成失败:', error)
  } finally {
    loading.value = false
  }
}

const exportReport = (format) => {
  console.log(`导出${format}格式报表`)
}

const getColorClass = (color) => {
  const colorMap = {
    blue: 'text-blue-600 bg-blue-100',
    green: 'text-green-600 bg-green-100',
    yellow: 'text-yellow-600 bg-yellow-100',
    purple: 'text-purple-600 bg-purple-100',
    indigo: 'text-indigo-600 bg-indigo-100',
    pink: 'text-pink-600 bg-pink-100'
  }
  return colorMap[color] || 'text-gray-600 bg-gray-100'
}

// 生命周期
onMounted(() => {
  console.log('报表中心页面加载完成')
})
</script>

<template>
  <div class="space-y-6">
    <!-- 页面标题 -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">报表中心</h1>
        <p class="mt-2 text-sm text-gray-600">查看和生成各类数据报表和分析</p>
      </div>
      <div class="mt-4 sm:mt-0 flex space-x-3">
        <button
          @click="exportReport('PDF')"
          class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-all duration-200 shadow-sm"
        >
          <Icon name="heroicons:document-arrow-down" class="mr-2 h-4 w-4" />
          导出PDF
        </button>
        <button
          @click="exportReport('Excel')"
          class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-all duration-200 shadow-sm"
        >
          <Icon name="heroicons:table-cells" class="mr-2 h-4 w-4" />
          导出Excel
        </button>
        <button
          @click="generateReport"
          :disabled="loading"
          class="inline-flex items-center px-6 py-2.5 border border-transparent text-sm font-semibold rounded-lg shadow-md text-white bg-gradient-to-r from-primary to-primary-dark hover:from-primary-dark hover:to-primary focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transform hover:scale-105 transition-all duration-200 disabled:opacity-50"
        >
          <Icon name="heroicons:arrow-path" class="mr-2 h-4 w-4" :class="{ 'animate-spin': loading }" />
          {{ loading ? '生成中...' : '生成报表' }}
        </button>
      </div>
    </div>

    <!-- 报表类型选择 -->
    <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <h3 class="text-lg font-medium text-gray-900 mb-4">选择报表类型</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <button
          v-for="report in reportTypes"
          :key="report.id"
          @click="selectedReport = report.id"
          class="relative p-4 border rounded-lg text-left transition-all duration-200 hover:shadow-md"
          :class="selectedReport === report.id 
            ? 'border-primary bg-primary/5 ring-2 ring-primary/20' 
            : 'border-gray-200 hover:border-gray-300'"
        >
          <div class="flex items-start space-x-3">
            <div class="flex-shrink-0">
              <div class="h-10 w-10 rounded-lg flex items-center justify-center" :class="getColorClass(report.color)">
                <Icon :name="report.icon" class="h-5 w-5" />
              </div>
            </div>
            <div class="flex-1 min-w-0">
              <h4 class="text-sm font-medium text-gray-900">{{ report.name }}</h4>
              <p class="text-sm text-gray-500 mt-1">{{ report.description }}</p>
            </div>
          </div>
          <div v-if="selectedReport === report.id" class="absolute top-2 right-2">
            <Icon name="heroicons:check-circle" class="h-5 w-5 text-primary" />
          </div>
        </button>
      </div>
    </div>

    <!-- 时间范围选择 -->
    <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <h3 class="text-lg font-medium text-gray-900 mb-4">时间范围</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">开始日期</label>
          <input
            v-model="dateRange.start"
            type="date"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">结束日期</label>
          <input
            v-model="dateRange.end"
            type="date"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
          />
        </div>
      </div>
    </div>

    <!-- 报表内容 -->
    <div v-if="currentReportType" class="space-y-6">
      <!-- 员工统计报表 -->
      <div v-if="selectedReport === 'employee'" class="space-y-6">
        <!-- 概览统计 -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
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
                    <dd class="text-2xl font-semibold text-gray-900">{{ employeeStats.totalEmployees }}</dd>
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
                    <Icon name="heroicons:user-plus" class="h-6 w-6 text-green-600" />
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">新入职</dt>
                    <dd class="text-2xl font-semibold text-gray-900">{{ employeeStats.newHires }}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="h-12 w-12 rounded-lg bg-red-100 flex items-center justify-center">
                    <Icon name="heroicons:user-minus" class="h-6 w-6 text-red-600" />
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">离职人数</dt>
                    <dd class="text-2xl font-semibold text-gray-900">{{ employeeStats.departures }}</dd>
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
                    <Icon name="heroicons:arrow-trending-up" class="h-6 w-6 text-yellow-600" />
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">流失率</dt>
                    <dd class="text-2xl font-semibold text-gray-900">{{ employeeStats.turnoverRate }}%</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 部门分布 -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-medium text-gray-900">部门人员分布</h3>
          </div>
          <div class="p-6">
            <div class="space-y-4">
              <div v-for="dept in employeeStats.departmentDistribution" :key="dept.name" class="flex items-center justify-between">
                <div class="flex items-center">
                  <span class="text-sm font-medium text-gray-900 w-20">{{ dept.name }}</span>
                  <div class="ml-4 flex-1">
                    <div class="w-full bg-gray-200 rounded-full h-2">
                      <div class="bg-primary h-2 rounded-full" :style="{ width: `${dept.percentage}%` }"></div>
                    </div>
                  </div>
                </div>
                <div class="flex items-center space-x-4 ml-4">
                  <span class="text-sm text-gray-500">{{ dept.count }}人</span>
                  <span class="text-sm font-medium text-gray-900 w-12 text-right">{{ dept.percentage }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 年龄分布 -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div class="bg-white shadow rounded-lg">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-medium text-gray-900">年龄分布</h3>
            </div>
            <div class="p-6">
              <div class="space-y-3">
                <div v-for="age in employeeStats.ageDistribution" :key="age.range" class="flex items-center justify-between">
                  <span class="text-sm text-gray-900">{{ age.range }}</span>
                  <div class="flex items-center space-x-2">
                    <span class="text-sm text-gray-500">{{ age.count }}人</span>
                    <span class="text-sm font-medium text-gray-900">{{ age.percentage }}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white shadow rounded-lg">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-medium text-gray-900">学历分布</h3>
            </div>
            <div class="p-6">
              <div class="space-y-3">
                <div v-for="edu in employeeStats.educationDistribution" :key="edu.level" class="flex items-center justify-between">
                  <span class="text-sm text-gray-900">{{ edu.level }}</span>
                  <div class="flex items-center space-x-2">
                    <span class="text-sm text-gray-500">{{ edu.count }}人</span>
                    <span class="text-sm font-medium text-gray-900">{{ edu.percentage }}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 薪资分析报表 -->
      <div v-if="selectedReport === 'salary'" class="space-y-6">
        <!-- 薪资概览 -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="h-12 w-12 rounded-lg bg-green-100 flex items-center justify-center">
                    <Icon name="heroicons:banknotes" class="h-6 w-6 text-green-600" />
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">平均薪资</dt>
                    <dd class="text-2xl font-semibold text-gray-900">¥{{ salaryStats.averageSalary.toLocaleString() }}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

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
                    <dt class="text-sm font-medium text-gray-500 truncate">中位数薪资</dt>
                    <dd class="text-2xl font-semibold text-gray-900">¥{{ salaryStats.medianSalary.toLocaleString() }}</dd>
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
                    <Icon name="heroicons:calculator" class="h-6 w-6 text-purple-600" />
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">总薪资成本</dt>
                    <dd class="text-2xl font-semibold text-gray-900">¥{{ (salaryStats.totalPayroll / 10000).toFixed(1) }}万</dd>
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
                    <Icon name="heroicons:arrow-trending-up" class="h-6 w-6 text-yellow-600" />
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">薪资增长</dt>
                    <dd class="text-2xl font-semibold text-gray-900">{{ salaryStats.salaryGrowth }}%</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 部门薪资分析 -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-medium text-gray-900">部门薪资分析</h3>
          </div>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">部门</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">平均薪资</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">总薪资</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">占比</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="dept in salaryStats.departmentSalary" :key="dept.name" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ dept.name }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">¥{{ dept.average.toLocaleString() }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">¥{{ dept.total.toLocaleString() }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ ((dept.total / salaryStats.totalPayroll) * 100).toFixed(1) }}%
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- 考勤统计报表 -->
      <div v-if="selectedReport === 'attendance'" class="space-y-6">
        <!-- 考勤概览 -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
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
                    <dt class="text-sm font-medium text-gray-500 truncate">平均出勤率</dt>
                    <dd class="text-2xl font-semibold text-gray-900">{{ attendanceStats.averageAttendanceRate }}%</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="h-12 w-12 rounded-lg bg-blue-100 flex items-center justify-center">
                    <Icon name="heroicons:calendar-days" class="h-6 w-6 text-blue-600" />
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">工作日数</dt>
                    <dd class="text-2xl font-semibold text-gray-900">{{ attendanceStats.totalWorkDays }}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="h-12 w-12 rounded-lg bg-red-100 flex items-center justify-center">
                    <Icon name="heroicons:x-circle" class="h-6 w-6 text-red-600" />
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">缺勤次数</dt>
                    <dd class="text-2xl font-semibold text-gray-900">{{ attendanceStats.totalAbsences }}</dd>
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
                    <dt class="text-sm font-medium text-gray-500 truncate">加班时长</dt>
                    <dd class="text-2xl font-semibold text-gray-900">{{ attendanceStats.overtimeHours }}h</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 部门考勤分析 -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-medium text-gray-900">部门考勤分析</h3>
          </div>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">部门</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">出勤率</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">缺勤次数</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">加班时长</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="dept in attendanceStats.departmentAttendance" :key="dept.name" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ dept.name }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <div class="flex items-center">
                      <span class="mr-2">{{ dept.rate }}%</span>
                      <div class="w-16 bg-gray-200 rounded-full h-2">
                        <div class="bg-green-500 h-2 rounded-full" :style="{ width: `${dept.rate}%` }"></div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ dept.absences }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ dept.overtime }}h</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- 其他报表类型的占位符 -->
      <div v-if="!['employee', 'salary', 'attendance'].includes(selectedReport)" class="bg-white shadow rounded-lg">
        <div class="px-6 py-12 text-center">
          <Icon :name="currentReportType.icon" class="mx-auto h-12 w-12 text-gray-400" />
          <h3 class="mt-4 text-lg font-medium text-gray-900">{{ currentReportType.name }}</h3>
          <p class="mt-2 text-sm text-gray-500">{{ currentReportType.description }}</p>
          <p class="mt-4 text-sm text-gray-400">此报表功能正在开发中...</p>
        </div>
      </div>
    </div>
  </div>
</template> 