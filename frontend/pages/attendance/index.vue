<template>
  <div class="space-y-6">
    <!-- 页面标题和操作栏 -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">考勤管理</h1>
        <p class="mt-2 text-sm text-gray-600">管理员工考勤记录和请假申请</p>
      </div>
      
      <div class="mt-4 sm:mt-0 flex space-x-3">
        <button
          @click="exportAttendance"
          class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-all duration-200 shadow-sm"
        >
          <Icon name="heroicons:arrow-down-tray" class="mr-2 h-4 w-4" />
          导出数据
        </button>
        <button
          @click="applyLeave"
          class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-all duration-200 shadow-sm"
        >
          <Icon name="heroicons:calendar-days" class="mr-2 h-4 w-4" />
          申请请假
        </button>
        <button
          @click="checkIn"
          class="inline-flex items-center px-6 py-2.5 border border-transparent text-sm font-semibold rounded-lg shadow-md text-white bg-gradient-to-r from-primary to-primary-dark hover:from-primary-dark hover:to-primary focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transform hover:scale-105 transition-all duration-200"
        >
          <Icon name="heroicons:clock" class="mr-2 h-4 w-4" />
          打卡签到
        </button>
      </div>
    </div>

    <!-- 今日考勤概览 -->
    <div class="grid grid-cols-1 md:grid-cols-5 gap-6">
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
                <dt class="text-sm font-medium text-gray-500 truncate">总员工数</dt>
                <dd class="text-2xl font-semibold text-gray-900">{{ attendanceStats.today.totalEmployees }}</dd>
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
                <dt class="text-sm font-medium text-gray-500 truncate">已签到</dt>
                <dd class="text-2xl font-semibold text-gray-900">{{ attendanceStats.today.checkedIn }}</dd>
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
                <Icon name="heroicons:exclamation-triangle" class="h-6 w-6 text-yellow-600" />
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">迟到</dt>
                <dd class="text-2xl font-semibold text-gray-900">{{ attendanceStats.today.late }}</dd>
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
                <dt class="text-sm font-medium text-gray-500 truncate">缺勤</dt>
                <dd class="text-2xl font-semibold text-gray-900">{{ attendanceStats.today.absent }}</dd>
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
                <Icon name="heroicons:calendar-days" class="h-6 w-6 text-purple-600" />
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">请假</dt>
                <dd class="text-2xl font-semibold text-gray-900">{{ attendanceStats.today.onLeave }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 标签页导航 -->
    <div class="bg-white shadow rounded-lg">
      <div class="border-b border-gray-200">
        <nav class="-mb-px flex space-x-8 px-6" aria-label="Tabs">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            class="py-4 px-1 border-b-2 font-medium text-sm transition-colors duration-200"
            :class="activeTab === tab.id
              ? 'border-primary text-primary'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
          >
            <div class="flex items-center space-x-2">
              <Icon :name="tab.icon" class="h-5 w-5" />
              <span>{{ tab.name }}</span>
            </div>
          </button>
        </nav>
      </div>

      <!-- 标签页内容 -->
      <div class="p-6">
        <!-- 考勤记录 -->
        <div v-if="activeTab === 'records'" class="space-y-6">
          <!-- 搜索和筛选 -->
          <div class="bg-gray-50 p-4 rounded-lg">
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
                <label class="block text-sm font-medium text-gray-700 mb-2">状态</label>
                <select v-model="filters.status" class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm">
                  <option value="">全部状态</option>
                  <option value="normal">正常</option>
                  <option value="late">迟到</option>
                  <option value="early">早退</option>
                  <option value="absent">缺勤</option>
                  <option value="overtime">加班</option>
                  <option value="leave">请假</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">日期</label>
                <input
                  v-model="filters.dateRange.start"
                  type="date"
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                />
              </div>
            </div>

            <div class="flex items-center justify-between mt-4">
              <div class="text-sm text-gray-500">
                显示 {{ filteredRecords.length }} / {{ attendanceRecords.length }} 条记录
              </div>
              <button
                @click="clearFilters"
                class="px-3 py-1 text-sm text-gray-600 hover:text-gray-800"
              >
                清空筛选
              </button>
            </div>
          </div>

          <!-- 考勤记录表格 -->
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">员工信息</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">日期</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">签到时间</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">签退时间</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">工作时长</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">备注</th>
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
                        <div class="text-sm text-gray-500">{{ record.employeeId }} · {{ record.department }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ record.date }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ record.checkInTime || '-' }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ record.checkOutTime || '-' }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <div class="flex items-center space-x-2">
                      <span>{{ record.workHours }}h</span>
                      <span v-if="record.overtimeHours > 0" class="text-blue-600">(+{{ record.overtimeHours }}h)</span>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="inline-flex px-2 py-1 text-xs font-semibold rounded-full" :class="getStatusColor(record.status)">
                      {{ getStatusText(record.status) }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ record.notes || '-' }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 请假管理 -->
        <div v-if="activeTab === 'leave'" class="space-y-6">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">员工信息</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">请假类型</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">请假时间</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">天数</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">申请时间</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="leave in leaveRecords" :key="leave.id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="h-10 w-10 rounded-full bg-primary flex items-center justify-center">
                        <span class="text-sm font-medium text-white">{{ leave.employeeName.charAt(0) }}</span>
                      </div>
                      <div class="ml-4">
                        <div class="text-sm font-medium text-gray-900">{{ leave.employeeName }}</div>
                        <div class="text-sm text-gray-500">{{ leave.employeeId }} · {{ leave.department }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ getLeaveTypeText(leave.leaveType) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ leave.startDate }} 至 {{ leave.endDate }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ leave.days }}天
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="inline-flex px-2 py-1 text-xs font-semibold rounded-full" :class="getLeaveStatusColor(leave.status)">
                      {{ getLeaveStatusText(leave.status) }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ leave.appliedAt }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                    <button
                      v-if="leave.status === 'pending'"
                      @click="approveLeave(leave.id)"
                      class="text-green-600 hover:text-green-900"
                    >
                      批准
                    </button>
                    <button
                      v-if="leave.status === 'pending'"
                      @click="rejectLeave(leave.id)"
                      class="text-red-600 hover:text-red-900"
                    >
                      拒绝
                    </button>
                    <button class="text-primary hover:text-primary-dark">
                      查看详情
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 考勤统计 -->
        <div v-if="activeTab === 'statistics'" class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div class="bg-white border border-gray-200 rounded-lg p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="h-12 w-12 rounded-lg bg-blue-100 flex items-center justify-center">
                    <Icon name="heroicons:calendar-days" class="h-6 w-6 text-blue-600" />
                  </div>
                </div>
                <div class="ml-5">
                  <p class="text-sm font-medium text-gray-500">本月工作日</p>
                  <p class="text-2xl font-semibold text-gray-900">{{ attendanceStats.thisMonth.workDays }}天</p>
                </div>
              </div>
            </div>

            <div class="bg-white border border-gray-200 rounded-lg p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="h-12 w-12 rounded-lg bg-green-100 flex items-center justify-center">
                    <Icon name="heroicons:chart-bar" class="h-6 w-6 text-green-600" />
                  </div>
                </div>
                <div class="ml-5">
                  <p class="text-sm font-medium text-gray-500">平均出勤率</p>
                  <p class="text-2xl font-semibold text-gray-900">{{ attendanceStats.thisMonth.averageAttendanceRate }}%</p>
                </div>
              </div>
            </div>

            <div class="bg-white border border-gray-200 rounded-lg p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="h-12 w-12 rounded-lg bg-yellow-100 flex items-center justify-center">
                    <Icon name="heroicons:clock" class="h-6 w-6 text-yellow-600" />
                  </div>
                </div>
                <div class="ml-5">
                  <p class="text-sm font-medium text-gray-500">总加班时长</p>
                  <p class="text-2xl font-semibold text-gray-900">{{ attendanceStats.thisMonth.totalOvertimeHours }}h</p>
                </div>
              </div>
            </div>

            <div class="bg-white border border-gray-200 rounded-lg p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="h-12 w-12 rounded-lg bg-purple-100 flex items-center justify-center">
                    <Icon name="heroicons:document-text" class="h-6 w-6 text-purple-600" />
                  </div>
                </div>
                <div class="ml-5">
                  <p class="text-sm font-medium text-gray-500">请假申请</p>
                  <p class="text-2xl font-semibold text-gray-900">{{ attendanceStats.thisMonth.totalLeaveRequests }}次</p>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white border border-gray-200 rounded-lg p-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">考勤趋势图</h3>
            <div class="h-64 flex items-center justify-center bg-gray-50 rounded-lg">
              <p class="text-gray-500">考勤趋势图表（需要集成图表库）</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// 页面元数据
definePageMeta({
  layout: 'default'
})

// 响应式数据
const loading = ref(false)
const activeTab = ref('records')
const showCheckInModal = ref(false)
const showLeaveModal = ref(false)

// 搜索和筛选
const searchQuery = ref('')
const filters = ref({
  department: '',
  status: '',
  dateRange: {
    start: '',
    end: ''
  }
})

// 考勤记录数据
const attendanceRecords = ref([
  {
    id: 1,
    employeeId: 'EMP001',
    employeeName: '张三',
    department: '技术部',
    date: '2024-04-15',
    checkInTime: '09:00:00',
    checkOutTime: '18:30:00',
    workHours: 8.5,
    overtimeHours: 0.5,
    status: 'normal',
    location: '北京总部',
    notes: ''
  },
  {
    id: 2,
    employeeId: 'EMP002',
    employeeName: '李四',
    department: '市场部',
    date: '2024-04-15',
    checkInTime: '09:15:00',
    checkOutTime: '18:00:00',
    workHours: 7.75,
    overtimeHours: 0,
    status: 'late',
    location: '北京总部',
    notes: '迟到15分钟'
  },
  {
    id: 3,
    employeeId: 'EMP003',
    employeeName: '王五',
    department: '人事部',
    date: '2024-04-15',
    checkInTime: '',
    checkOutTime: '',
    workHours: 0,
    overtimeHours: 0,
    status: 'absent',
    location: '',
    notes: '病假'
  },
  {
    id: 4,
    employeeId: 'EMP004',
    employeeName: '赵六',
    department: '财务部',
    date: '2024-04-15',
    checkInTime: '08:45:00',
    checkOutTime: '19:30:00',
    workHours: 9.75,
    overtimeHours: 1.75,
    status: 'overtime',
    location: '北京总部',
    notes: '加班处理月末结账'
  }
])

// 请假记录数据
const leaveRecords = ref([
  {
    id: 1,
    employeeId: 'EMP003',
    employeeName: '王五',
    department: '人事部',
    leaveType: 'sick',
    startDate: '2024-04-15',
    endDate: '2024-04-16',
    days: 2,
    reason: '感冒发烧，需要休息',
    status: 'approved',
    appliedAt: '2024-04-14 10:30:00',
    approvedBy: '张经理',
    approvedAt: '2024-04-14 14:20:00'
  },
  {
    id: 2,
    employeeId: 'EMP005',
    employeeName: '钱七',
    department: '运营部',
    leaveType: 'annual',
    startDate: '2024-04-20',
    endDate: '2024-04-22',
    days: 3,
    reason: '家庭旅行',
    status: 'pending',
    appliedAt: '2024-04-13 16:45:00',
    approvedBy: '',
    approvedAt: ''
  }
])

// 考勤统计数据
const attendanceStats = ref({
  today: {
    totalEmployees: 156,
    checkedIn: 142,
    late: 8,
    absent: 6,
    onLeave: 4
  },
  thisMonth: {
    workDays: 22,
    averageAttendanceRate: 96.8,
    totalOvertimeHours: 1250,
    totalLeaveRequests: 28
  }
})

// 标签页配置
const tabs = ref([
  { id: 'records', name: '考勤记录', icon: 'heroicons:clock' },
  { id: 'leave', name: '请假管理', icon: 'heroicons:calendar-days' },
  { id: 'statistics', name: '考勤统计', icon: 'heroicons:chart-bar' }
])

// 计算属性
const filteredRecords = computed(() => {
  let filtered = attendanceRecords.value

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

  if (filters.value.status) {
    filtered = filtered.filter(record => record.status === filters.value.status)
  }

  if (filters.value.dateRange.start) {
    filtered = filtered.filter(record => record.date >= filters.value.dateRange.start)
  }

  if (filters.value.dateRange.end) {
    filtered = filtered.filter(record => record.date <= filters.value.dateRange.end)
  }

  return filtered
})

const departments = computed(() => {
  return [...new Set(attendanceRecords.value.map(record => record.department))]
})

// 方法
const getStatusText = (status) => {
  const statusMap = {
    'normal': '正常',
    'late': '迟到',
    'early': '早退',
    'absent': '缺勤',
    'overtime': '加班',
    'leave': '请假'
  }
  return statusMap[status] || status
}

const getStatusColor = (status) => {
  const colorMap = {
    'normal': 'text-green-600 bg-green-100',
    'late': 'text-yellow-600 bg-yellow-100',
    'early': 'text-orange-600 bg-orange-100',
    'absent': 'text-red-600 bg-red-100',
    'overtime': 'text-blue-600 bg-blue-100',
    'leave': 'text-purple-600 bg-purple-100'
  }
  return colorMap[status] || 'text-gray-600 bg-gray-100'
}

const getLeaveTypeText = (type) => {
  const typeMap = {
    'annual': '年假',
    'sick': '病假',
    'personal': '事假',
    'maternity': '产假',
    'paternity': '陪产假',
    'marriage': '婚假',
    'bereavement': '丧假'
  }
  return typeMap[type] || type
}

const getLeaveStatusText = (status) => {
  const statusMap = {
    'pending': '待审批',
    'approved': '已批准',
    'rejected': '已拒绝',
    'cancelled': '已取消'
  }
  return statusMap[status] || status
}

const getLeaveStatusColor = (status) => {
  const colorMap = {
    'pending': 'text-yellow-600 bg-yellow-100',
    'approved': 'text-green-600 bg-green-100',
    'rejected': 'text-red-600 bg-red-100',
    'cancelled': 'text-gray-600 bg-gray-100'
  }
  return colorMap[status] || 'text-gray-600 bg-gray-100'
}

const checkIn = () => {
  showCheckInModal.value = true
}

const applyLeave = () => {
  showLeaveModal.value = true
}

const exportAttendance = () => {
  console.log('导出考勤数据')
}

const approveLeave = (leaveId) => {
  const leave = leaveRecords.value.find(l => l.id === leaveId)
  if (leave) {
    leave.status = 'approved'
    leave.approvedBy = '当前用户'
    leave.approvedAt = new Date().toLocaleString('zh-CN')
  }
}

const rejectLeave = (leaveId) => {
  const leave = leaveRecords.value.find(l => l.id === leaveId)
  if (leave) {
    leave.status = 'rejected'
    leave.approvedBy = '当前用户'
    leave.approvedAt = new Date().toLocaleString('zh-CN')
  }
}

const clearFilters = () => {
  searchQuery.value = ''
  filters.value = {
    department: '',
    status: '',
    dateRange: {
      start: '',
      end: ''
    }
  }
}

// 生命周期
onMounted(() => {
  console.log('考勤管理页面加载完成')
})
</script> 