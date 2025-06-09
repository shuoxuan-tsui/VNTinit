<template>
  <div class="space-y-6">
    <!-- 页面标题和操作栏 -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">薪资查询</h1>
        <p class="mt-1 text-sm text-gray-500">查看和管理员工薪资记录</p>
      </div>
      
      <!-- 计算薪资按钮 (仅管理员可见) -->
      <div class="mt-4 sm:mt-0">
        <button
          v-if="isAdmin"
          @click="showCalculateModal = true"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-accent hover:bg-accent-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent transition-colors"
        >
          <Icon name="heroicons:calculator" class="mr-2 h-4 w-4" />
          计算并生成薪资
        </button>
      </div>
    </div>

    <!-- 搜索和筛选区域 -->
    <div class="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <!-- 员工搜索 -->
        <div>
          <label for="employee-search" class="block text-sm font-medium text-gray-700 mb-1">员工搜索</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Icon name="heroicons:magnifying-glass" class="h-5 w-5 text-gray-400" />
            </div>
            <input
              id="employee-search"
              v-model="searchQuery"
              type="text"
              placeholder="搜索姓名、工号..."
              class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary focus:border-primary"
              @input="debouncedSearch"
            />
          </div>
        </div>

        <!-- 部门筛选 -->
        <div>
          <label for="department" class="block text-sm font-medium text-gray-700 mb-1">部门</label>
          <select
            id="department"
            v-model="filters.department"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
            @change="applyFilters"
          >
            <option value="">全部部门</option>
            <option v-for="dept in departments" :key="dept" :value="dept">{{ dept }}</option>
          </select>
        </div>

        <!-- 薪资期间筛选 -->
        <div>
          <label for="salary-period" class="block text-sm font-medium text-gray-700 mb-1">薪资期间</label>
          <input
            id="salary-period"
            v-model="filters.salaryPeriod"
            type="month"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
            @change="applyFilters"
          />
        </div>

        <!-- 薪资范围筛选 -->
        <div>
          <label for="salary-range" class="block text-sm font-medium text-gray-700 mb-1">薪资范围</label>
          <select
            id="salary-range"
            v-model="filters.salaryRange"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
            @change="applyFilters"
          >
            <option value="">全部范围</option>
            <option value="0-5000">0-5000元</option>
            <option value="5000-10000">5000-10000元</option>
            <option value="10000-15000">10000-15000元</option>
            <option value="15000-20000">15000-20000元</option>
            <option value="20000+">20000元以上</option>
          </select>
        </div>
      </div>
    </div>

    <!-- 数据表格 -->
    <div class="bg-white shadow-sm rounded-lg border border-gray-200 overflow-hidden">
      <!-- 加载状态 -->
      <div v-if="loading" class="p-8 text-center">
        <div class="inline-flex items-center">
          <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-primary mr-3"></div>
          <span class="text-gray-600">加载中...</span>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else-if="!salaryRecords.length" class="p-8 text-center">
        <Icon name="heroicons:currency-dollar" class="mx-auto h-12 w-12 text-gray-400" />
        <h3 class="mt-2 text-sm font-medium text-gray-900">暂无薪资记录</h3>
        <p class="mt-1 text-sm text-gray-500">还没有生成任何薪资记录</p>
        <div class="mt-6" v-if="isAdmin">
          <button
            @click="showCalculateModal = true"
            class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-accent hover:bg-accent-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent"
          >
            <Icon name="heroicons:calculator" class="mr-2 h-4 w-4" />
            计算并生成薪资
          </button>
        </div>
      </div>

      <!-- 表格内容 -->
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th
                v-for="column in tableColumns"
                :key="column.key"
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                @click="column.sortable && toggleSort(column.key)"
              >
                <div class="flex items-center space-x-1">
                  <span>{{ column.label }}</span>
                  <Icon
                    v-if="column.sortable"
                    :name="getSortIcon(column.key)"
                    class="h-4 w-4 text-gray-400"
                  />
                </div>
              </th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                操作
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr
              v-for="record in salaryRecords"
              :key="record.id"
              class="hover:bg-gray-50 transition-colors"
            >
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {{ record.employee_name }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-mono">
                {{ record.employee_id }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ record.department }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatSalaryPeriod(record.salary_period) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ record.position_snapshot }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                ¥{{ formatCurrency(record.base_salary_snapshot) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                ¥{{ formatCurrency(record.gross_salary) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                <span class="text-green-600">+¥{{ formatCurrency(record.bonus) }}</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                <span class="text-red-600">-¥{{ formatCurrency(record.deduction) }}</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-900">
                ¥{{ formatCurrency(record.net_salary) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(record.pay_date) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div class="flex items-center justify-end space-x-2">
                  <!-- 查看详情 -->
                  <button
                    @click="viewSalaryDetail(record)"
                    class="text-primary hover:text-primary-dark transition-colors"
                    title="查看详情"
                  >
                    <Icon name="heroicons:eye" class="h-4 w-4" />
                  </button>
                  
                  <!-- 打印 -->
                  <button
                    @click="printSalary(record)"
                    class="text-gray-600 hover:text-gray-800 transition-colors"
                    title="打印"
                  >
                    <Icon name="heroicons:printer" class="h-4 w-4" />
                  </button>
                  
                  <!-- 编辑 (仅管理员) -->
                  <button
                    v-if="isAdmin"
                    @click="editSalaryRecord(record)"
                    class="text-accent hover:text-accent-dark transition-colors"
                    title="编辑"
                  >
                    <Icon name="heroicons:pencil" class="h-4 w-4" />
                  </button>
                  
                  <!-- 删除 (仅管理员) -->
                  <button
                    v-if="isAdmin"
                    @click="confirmDeleteSalary(record)"
                    class="text-danger hover:text-red-700 transition-colors"
                    title="删除"
                  >
                    <Icon name="heroicons:trash" class="h-4 w-4" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 分页 -->
      <div v-if="pagination.totalPages > 1" class="bg-white px-4 py-3 border-t border-gray-200 sm:px-6">
        <div class="flex items-center justify-between">
          <div class="flex-1 flex justify-between sm:hidden">
            <button
              @click="changePage(pagination.currentPage - 1)"
              :disabled="pagination.currentPage <= 1"
              class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              上一页
            </button>
            <button
              @click="changePage(pagination.currentPage + 1)"
              :disabled="pagination.currentPage >= pagination.totalPages"
              class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              下一页
            </button>
          </div>
          <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p class="text-sm text-gray-700">
                显示第
                <span class="font-medium">{{ (pagination.currentPage - 1) * pagination.pageSize + 1 }}</span>
                到
                <span class="font-medium">{{ Math.min(pagination.currentPage * pagination.pageSize, pagination.totalItems) }}</span>
                条，共
                <span class="font-medium">{{ pagination.totalItems }}</span>
                条记录
              </p>
            </div>
            <div>
              <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
                <button
                  @click="changePage(pagination.currentPage - 1)"
                  :disabled="pagination.currentPage <= 1"
                  class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Icon name="heroicons:chevron-left" class="h-5 w-5" />
                </button>
                
                <button
                  v-for="page in visiblePages"
                  :key="page"
                  @click="changePage(page)"
                  :class="[
                    'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                    page === pagination.currentPage
                      ? 'z-10 bg-primary border-primary text-white'
                      : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
                  ]"
                >
                  {{ page }}
                </button>
                
                <button
                  @click="changePage(pagination.currentPage + 1)"
                  :disabled="pagination.currentPage >= pagination.totalPages"
                  class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Icon name="heroicons:chevron-right" class="h-5 w-5" />
                </button>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 计算薪资模态框 -->
    <div
      v-if="showCalculateModal"
      class="fixed inset-0 z-50 overflow-y-auto"
      @click.self="closeCalculateModal"
    >
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
        
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <form @submit.prevent="calculateSalary">
            <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
              <div class="sm:flex sm:items-start">
                <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-accent-light sm:mx-0 sm:h-10 sm:w-10">
                  <Icon name="heroicons:calculator" class="h-6 w-6 text-accent-dark" />
                </div>
                <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
                  <h3 class="text-lg leading-6 font-medium text-gray-900">计算并生成薪资</h3>
                  <div class="mt-4 space-y-4">
                    <!-- 员工选择 -->
                    <div>
                      <label for="calc-employee" class="block text-sm font-medium text-gray-700 mb-1">选择员工</label>
                      <select
                        id="calc-employee"
                        v-model="calculateForm.employeeId"
                        required
                        class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-accent focus:border-accent"
                      >
                        <option value="">请选择员工</option>
                        <option v-for="emp in employees" :key="emp.id" :value="emp.id">
                          {{ emp.name }} ({{ emp.employee_id }})
                        </option>
                      </select>
                    </div>

                    <!-- 薪资期间 -->
                    <div>
                      <label for="calc-period" class="block text-sm font-medium text-gray-700 mb-1">薪资期间</label>
                      <input
                        id="calc-period"
                        v-model="calculateForm.salaryPeriod"
                        type="month"
                        required
                        class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-accent focus:border-accent"
                      />
                    </div>

                    <!-- 奖金 -->
                    <div>
                      <label for="calc-bonus" class="block text-sm font-medium text-gray-700 mb-1">奖金</label>
                      <div class="relative">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                          <span class="text-gray-500 sm:text-sm">¥</span>
                        </div>
                        <input
                          id="calc-bonus"
                          v-model.number="calculateForm.bonus"
                          type="number"
                          step="0.01"
                          min="0"
                          class="block w-full pl-8 pr-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-accent focus:border-accent"
                          placeholder="0.00"
                        />
                      </div>
                    </div>

                    <!-- 扣除 -->
                    <div>
                      <label for="calc-deduction" class="block text-sm font-medium text-gray-700 mb-1">扣除</label>
                      <div class="relative">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                          <span class="text-gray-500 sm:text-sm">¥</span>
                        </div>
                        <input
                          id="calc-deduction"
                          v-model.number="calculateForm.deduction"
                          type="number"
                          step="0.01"
                          min="0"
                          class="block w-full pl-8 pr-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-accent focus:border-accent"
                          placeholder="0.00"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
              <button
                type="submit"
                :disabled="calculating"
                class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-accent text-base font-medium text-white hover:bg-accent-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <div v-if="calculating" class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                {{ calculating ? '计算中...' : '计算并生成' }}
              </button>
              <button
                type="button"
                @click="closeCalculateModal"
                :disabled="calculating"
                class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                取消
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue'

// 页面元数据
definePageMeta({
  layout: 'default'
})

// 响应式数据
const loading = ref(false)
const calculating = ref(false)
const searchQuery = ref('')
const showCalculateModal = ref(false)

// 筛选条件
const filters = ref({
  department: '',
  salaryPeriod: '',
  salaryRange: ''
})

// 排序
const sort = ref({
  field: '',
  direction: 'asc'
})

// 分页
const pagination = ref({
  currentPage: 1,
  pageSize: 10,
  totalItems: 0,
  totalPages: 0
})

// 计算薪资表单
const calculateForm = reactive({
  employeeId: '',
  salaryPeriod: '',
  bonus: 0,
  deduction: 0
})

// 模拟数据
const salaryRecords = ref([
  {
    id: 1,
    employee_name: '张三',
    employee_id: 'EMP001',
    department: '技术部',
    salary_period: '2024-01',
    position_snapshot: '高级工程师',
    base_salary_snapshot: 15000,
    gross_salary: 15000,
    bonus: 2000,
    deduction: 500,
    net_salary: 16500,
    pay_date: '2024-02-01'
  },
  {
    id: 2,
    employee_name: '李四',
    employee_id: 'EMP002',
    department: '人事部',
    salary_period: '2024-01',
    position_snapshot: '人事专员',
    base_salary_snapshot: 8000,
    gross_salary: 8000,
    bonus: 1000,
    deduction: 200,
    net_salary: 8800,
    pay_date: '2024-02-01'
  }
])

const employees = ref([
  { id: 1, name: '张三', employee_id: 'EMP001' },
  { id: 2, name: '李四', employee_id: 'EMP002' },
  { id: 3, name: '王五', employee_id: 'EMP003' }
])

const departments = ref(['技术部', '人事部', '财务部', '市场部', '运营部'])

// 用户权限
const isAdmin = ref(true)

// 表格列定义
const tableColumns = [
  { key: 'employee_name', label: '员工姓名', sortable: true },
  { key: 'employee_id', label: '工号', sortable: true },
  { key: 'department', label: '部门', sortable: true },
  { key: 'salary_period', label: '薪资期间', sortable: true },
  { key: 'position_snapshot', label: '职称', sortable: false },
  { key: 'base_salary_snapshot', label: '基础工资', sortable: true },
  { key: 'gross_salary', label: '应发工资', sortable: true },
  { key: 'bonus', label: '奖金', sortable: true },
  { key: 'deduction', label: '扣除', sortable: true },
  { key: 'net_salary', label: '实发工资', sortable: true },
  { key: 'pay_date', label: '发放日期', sortable: true }
]

// 计算属性
const visiblePages = computed(() => {
  const pages = []
  const total = pagination.value.totalPages
  const current = pagination.value.currentPage
  
  if (total <= 7) {
    for (let i = 1; i <= total; i++) {
      pages.push(i)
    }
  } else {
    if (current <= 4) {
      for (let i = 1; i <= 5; i++) {
        pages.push(i)
      }
      pages.push('...')
      pages.push(total)
    } else if (current >= total - 3) {
      pages.push(1)
      pages.push('...')
      for (let i = total - 4; i <= total; i++) {
        pages.push(i)
      }
    } else {
      pages.push(1)
      pages.push('...')
      for (let i = current - 1; i <= current + 1; i++) {
        pages.push(i)
      }
      pages.push('...')
      pages.push(total)
    }
  }
  
  return pages.filter(page => page !== '...' || pages.indexOf(page) === pages.lastIndexOf(page))
})

// 方法
const loadSalaryRecords = async () => {
  loading.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 500))
    pagination.value.totalItems = salaryRecords.value.length
    pagination.value.totalPages = Math.ceil(pagination.value.totalItems / pagination.value.pageSize)
  } catch (error) {
    console.error('加载薪资记录失败:', error)
  } finally {
    loading.value = false
  }
}

const debouncedSearch = debounce(() => {
  applyFilters()
}, 300)

const applyFilters = () => {
  console.log('应用筛选:', { searchQuery: searchQuery.value, filters: filters.value })
  loadSalaryRecords()
}

const toggleSort = (field) => {
  if (sort.value.field === field) {
    sort.value.direction = sort.value.direction === 'asc' ? 'desc' : 'asc'
  } else {
    sort.value.field = field
    sort.value.direction = 'asc'
  }
  loadSalaryRecords()
}

const getSortIcon = (field) => {
  if (sort.value.field !== field) {
    return 'heroicons:chevron-up-down'
  }
  return sort.value.direction === 'asc' ? 'heroicons:chevron-up' : 'heroicons:chevron-down'
}

const changePage = (page) => {
  if (page >= 1 && page <= pagination.value.totalPages) {
    pagination.value.currentPage = page
    loadSalaryRecords()
  }
}

const viewSalaryDetail = (record) => {
  console.log('查看薪资详情:', record)
}

const printSalary = (record) => {
  console.log('打印薪资单:', record)
  // 后续实现打印功能
}

const editSalaryRecord = (record) => {
  console.log('编辑薪资记录:', record)
}

const confirmDeleteSalary = (record) => {
  console.log('删除薪资记录:', record)
}

const closeCalculateModal = () => {
  showCalculateModal.value = false
  Object.assign(calculateForm, {
    employeeId: '',
    salaryPeriod: '',
    bonus: 0,
    deduction: 0
  })
}

const calculateSalary = async () => {
  calculating.value = true
  try {
    console.log('计算薪资:', calculateForm)
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // 模拟生成新的薪资记录
    const newRecord = {
      id: Date.now(),
      employee_name: employees.value.find(emp => emp.id == calculateForm.employeeId)?.name || '',
      employee_id: employees.value.find(emp => emp.id == calculateForm.employeeId)?.employee_id || '',
      department: '技术部',
      salary_period: calculateForm.salaryPeriod,
      position_snapshot: '工程师',
      base_salary_snapshot: 10000,
      gross_salary: 10000,
      bonus: calculateForm.bonus || 0,
      deduction: calculateForm.deduction || 0,
      net_salary: 10000 + (calculateForm.bonus || 0) - (calculateForm.deduction || 0),
      pay_date: new Date().toISOString().split('T')[0]
    }
    
    salaryRecords.value.unshift(newRecord)
    closeCalculateModal()
    console.log('薪资计算完成')
  } catch (error) {
    console.error('计算薪资失败:', error)
  } finally {
    calculating.value = false
  }
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(amount)
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('zh-CN')
}

const formatSalaryPeriod = (period) => {
  if (!period) return ''
  const [year, month] = period.split('-')
  return `${year}年${month}月`
}

// 防抖函数
function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

// 生命周期
onMounted(() => {
  loadSalaryRecords()
  
  // 设置默认薪资期间为当前月份
  const now = new Date()
  calculateForm.salaryPeriod = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
})
</script> 