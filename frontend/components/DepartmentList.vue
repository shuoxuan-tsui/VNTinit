<template>
  <div>
    <!-- 部门统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <Icon name="heroicons:building-office" class="h-6 w-6 text-blue-400" />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">部门总数</dt>
                <dd class="text-lg font-medium text-gray-900">{{ departments.length }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <Icon name="heroicons:users" class="h-6 w-6 text-green-400" />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">员工总数</dt>
                <dd class="text-lg font-medium text-gray-900">{{ totalEmployees }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <Icon name="heroicons:user-group" class="h-6 w-6 text-yellow-400" />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">平均部门规模</dt>
                <dd class="text-lg font-medium text-gray-900">{{ averageDeptSize }}人</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <Icon name="heroicons:chart-pie" class="h-6 w-6 text-purple-400" />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">最大部门</dt>
                <dd class="text-lg font-medium text-gray-900">{{ largestDept.name }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 部门列表 -->
    <div class="bg-white shadow-sm rounded-lg border border-gray-200 overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-medium text-gray-900">部门列表</h3>
      </div>
      
      <div v-if="loading" class="p-6 text-center">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div>
        <p class="mt-2 text-gray-500">加载中...</p>
      </div>
      
      <div v-else-if="departments.length === 0" class="p-6 text-center text-gray-500">
        暂无部门数据
      </div>
      
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">部门信息</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">部门经理</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">员工数量</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">成立时间</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="dept in departments" :key="dept.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-10 w-10">
                    <div class="h-10 w-10 rounded-lg flex items-center justify-center" :style="{ backgroundColor: dept.color + '20', color: dept.color }">
                      <Icon :name="dept.icon" class="h-5 w-5" />
                    </div>
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">{{ dept.name }}</div>
                    <div class="text-sm text-gray-500">{{ dept.description }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-8 w-8">
                    <div class="h-8 w-8 rounded-full bg-gray-300 flex items-center justify-center">
                      <span class="text-xs font-medium text-gray-700">{{ dept.manager.charAt(0) }}</span>
                    </div>
                  </div>
                  <div class="ml-3">
                    <div class="text-sm font-medium text-gray-900">{{ dept.manager }}</div>
                    <div class="text-sm text-gray-500">{{ dept.manager_title }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <span class="text-sm font-medium text-gray-900">{{ dept.employee_count }}</span>
                  <span class="ml-2 text-xs text-gray-500">人</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-1.5 mt-1">
                  <div 
                    class="h-1.5 rounded-full" 
                    :style="{ 
                      backgroundColor: dept.color, 
                      width: `${(dept.employee_count / Math.max(...departments.map(d => d.employee_count))) * 100}%` 
                    }"
                  ></div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(dept.created_at) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium" :class="dept.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'">
                  {{ dept.status === 'active' ? '活跃' : '停用' }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div class="flex items-center justify-end space-x-2">
                  <button class="text-primary hover:text-primary-dark p-1 rounded" title="查看详情">
                    <Icon name="heroicons:eye" class="h-4 w-4" />
                  </button>
                  <button class="text-accent hover:text-accent-dark p-1 rounded" title="编辑">
                    <Icon name="heroicons:pencil" class="h-4 w-4" />
                  </button>
                  <button class="text-danger hover:text-red-700 p-1 rounded" title="删除">
                    <Icon name="heroicons:trash" class="h-4 w-4" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const departments = ref([])
const loading = ref(false)

// 计算属性
const totalEmployees = computed(() => {
  return departments.value.reduce((sum, dept) => sum + (dept.employee_count || 0), 0)
})

const averageDeptSize = computed(() => {
  if (departments.value.length === 0) return 0
  return Math.round(totalEmployees.value / departments.value.length)
})

const largestDept = computed(() => {
  if (departments.value.length === 0) return { name: '暂无' }
  return departments.value.reduce((max, dept) => 
    (dept.employee_count || 0) > (max.employee_count || 0) ? dept : max
  )
})

// 为部门添加默认的图标和颜色
const getDepartmentIcon = (deptName) => {
  const iconMap = {
    '技术部': 'heroicons:code-bracket',
    '人事部': 'heroicons:users',
    '财务部': 'heroicons:currency-dollar',
    '市场部': 'heroicons:megaphone',
    '运营部': 'heroicons:cog-6-tooth',
    '销售部': 'heroicons:chart-bar',
    '客服部': 'heroicons:phone',
    '行政部': 'heroicons:building-office',
    '法务部': 'heroicons:scale',
    '采购部': 'heroicons:shopping-cart',
    '研发部': 'heroicons:beaker',
    '产品部': 'heroicons:cube',
    '设计部': 'heroicons:paint-brush',
    '质量部': 'heroicons:shield-check',
    '安全部': 'heroicons:shield-exclamation'
  }
  return iconMap[deptName] || 'heroicons:building-office'
}

const getDepartmentColor = (deptName) => {
  const colorMap = {
    '技术部': '#3B82F6',
    '人事部': '#10B981',
    '财务部': '#F59E0B',
    '市场部': '#EF4444',
    '运营部': '#8B5CF6',
    '销售部': '#06B6D4',
    '客服部': '#84CC16',
    '行政部': '#6B7280',
    '法务部': '#1F2937',
    '采购部': '#F97316',
    '研发部': '#EC4899',
    '产品部': '#14B8A6',
    '设计部': '#A855F7',
    '质量部': '#22C55E',
    '安全部': '#DC2626'
  }
  return colorMap[deptName] || '#6B7280'
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('zh-CN')
}

const fetchDepartments = async () => {
  loading.value = true
  try {
    // 先尝试登录
    const existingToken = localStorage.getItem('auth_token')
    if (!existingToken) {
      console.log('No token found, attempting auto-login...')
      const loginResponse = await $fetch('/api/auth/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: {
          username: 'admin',
          password: 'admin123'
        }
      })
      
      if (loginResponse && loginResponse.success && loginResponse.data && loginResponse.data.token) {
        localStorage.setItem('auth_token', loginResponse.data.token)
        localStorage.setItem('user_info', JSON.stringify(loginResponse.data.user))
        console.log('Auto-login successful')
      }
    }
    
    // 获取部门数据
    const token = localStorage.getItem('auth_token')
    const response = await $fetch('/api/departments/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': token ? `Token ${token}` : ''
      }
    })
    
    console.log('Departments response:', response)
    
    if (response && response.success && response.data && response.data.results) {
      departments.value = response.data.results.map(dept => ({
        ...dept,
        icon: getDepartmentIcon(dept.name),
        color: getDepartmentColor(dept.name),
        employee_count: dept.employee_count || 0
      }))
    } else {
      console.error('Failed to fetch departments:', response)
    }
  } catch (error) {
    console.error('Error fetching departments:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchDepartments()
})
</script> 