<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50 py-8 relative overflow-hidden">
    <!-- 背景装饰元素 -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-blue-200 bg-opacity-20 rounded-full blur-3xl"></div>
      <div class="absolute -bottom-40 -left-40 w-96 h-96 bg-indigo-200 bg-opacity-15 rounded-full blur-3xl"></div>
      <div class="absolute top-1/3 left-1/4 w-32 h-32 bg-blue-300 bg-opacity-10 rounded-full blur-2xl"></div>
      <div class="absolute bottom-1/4 right-1/3 w-24 h-24 bg-indigo-300 bg-opacity-15 rounded-full blur-xl"></div>
    </div>

    <div class="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
      <!-- 页面标题 -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-gray-800 mb-3 drop-shadow-sm">计算并生成薪资</h1>
        <p class="text-xl text-gray-600 drop-shadow-sm">为员工计算薪资并生成记录</p>
        <NuxtLink to="/salaries" class="inline-flex items-center mt-6 text-gray-700 hover:text-blue-600 transition-all duration-200 backdrop-blur-sm bg-white bg-opacity-60 px-4 py-2 rounded-full shadow-sm border border-gray-200">
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
          </svg>
          返回薪资列表
        </NuxtLink>
      </div>

      <!-- 主表单卡片 - 蓝色磨砂玻璃效果 -->
      <div class="backdrop-blur-xl bg-gradient-to-br from-blue-400 via-blue-500 to-blue-600 bg-opacity-95 rounded-3xl shadow-2xl border border-blue-300 border-opacity-30 overflow-hidden">
        <!-- 卡片头部 -->
        <div class="backdrop-blur-lg bg-white bg-opacity-15 px-8 py-10 border-b border-white border-opacity-20">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="flex items-center justify-center h-16 w-16 rounded-2xl backdrop-blur-sm bg-gradient-to-br from-yellow-400 to-orange-500 shadow-lg">
                <svg class="h-10 w-10 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z"/>
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z" clip-rule="evenodd"/>
                </svg>
              </div>
            </div>
            <div class="ml-6">
              <h2 class="text-2xl font-bold text-gray-900">薪资计算器</h2>
              <p class="text-gray-700 text-lg">选择员工和期间，系统将自动计算薪资</p>
            </div>
          </div>
        </div>

        <!-- 表单内容 -->
        <form @submit.prevent="handleSubmit" class="px-8 py-10">
          <div class="space-y-8">
            <!-- 员工选择 -->
            <div class="space-y-3">
              <label class="block text-lg font-semibold text-white drop-shadow flex items-center">
                <svg class="w-5 h-5 mr-2 text-purple-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"></path>
                </svg>
                选择员工
              </label>
              <div class="relative">
                <select v-model="form.employeeId" class="block w-full px-6 py-4 backdrop-blur-md bg-gradient-to-r from-white to-purple-50 bg-opacity-95 border-2 border-purple-200 hover:border-purple-300 rounded-2xl shadow-lg hover:shadow-xl focus:outline-none focus:ring-4 focus:ring-purple-200 focus:ring-opacity-50 focus:border-purple-400 text-gray-900 placeholder-gray-500 text-lg font-medium transition-all duration-300 transform hover:scale-[1.02] cursor-pointer">
                  <option value="" class="bg-blue-700 text-white font-semibold">🌟 为所有员工生成薪资</option>
                  <option v-for="emp in employees" :key="emp.id" :value="emp.id" class="bg-gray-50 text-gray-900 font-medium">
                    👤 {{ emp.name }} ({{ emp.employee_id }})
                  </option>
                </select>
              </div>
              <p class="text-sm text-blue-100 flex items-center drop-shadow-sm opacity-90">
                <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
                </svg>
                留空将为所有在职员工批量生成薪资记录
              </p>
            </div>

            <!-- 薪资期间 -->
            <div class="space-y-3">
              <label class="block text-lg font-semibold text-white drop-shadow flex items-center">
                <svg class="w-5 h-5 mr-2 text-blue-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
                薪资期间
              </label>
              <div class="relative group">
                <input v-model="form.salaryPeriod" type="month" required class="block w-full px-6 py-4 backdrop-blur-md bg-gradient-to-r from-white to-blue-50 bg-opacity-95 border-2 border-blue-200 hover:border-blue-300 rounded-2xl shadow-lg hover:shadow-xl focus:outline-none focus:ring-4 focus:ring-blue-200 focus:ring-opacity-50 focus:border-blue-400 text-gray-900 placeholder-gray-500 text-lg font-medium transition-all duration-300 transform hover:scale-[1.02] group-hover:shadow-blue-200/50" />
                <div class="absolute inset-0 rounded-2xl bg-gradient-to-r from-blue-400/10 to-blue-600/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"></div>
              </div>
            </div>

            <!-- 奖金和扣除 -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                              <div class="space-y-3">
                <label class="block text-lg font-semibold text-white drop-shadow flex items-center">
                  <svg class="w-5 h-5 mr-2 text-green-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
                  </svg>
                  奖金 (可选)
                </label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-6 flex items-center pointer-events-none">
                    <span class="text-green-600 text-xl font-bold drop-shadow-sm">¥</span>
                  </div>
                  <input v-model.number="form.bonus" type="number" step="0.01" min="0" placeholder="0.00" class="block w-full pl-12 pr-6 py-4 backdrop-blur-md bg-gradient-to-r from-white to-green-50 bg-opacity-95 border-2 border-green-200 hover:border-green-300 rounded-2xl shadow-lg hover:shadow-xl focus:outline-none focus:ring-4 focus:ring-green-200 focus:ring-opacity-50 focus:border-green-400 text-gray-900 placeholder-gray-500 text-lg font-medium transition-all duration-300 transform hover:scale-[1.02]" />
                </div>
              </div>

                              <div class="space-y-3">
                <label class="block text-lg font-semibold text-white drop-shadow flex items-center">
                  <svg class="w-5 h-5 mr-2 text-red-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path>
                  </svg>
                  扣除 (可选)
                </label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-6 flex items-center pointer-events-none">
                    <span class="text-red-600 text-xl font-bold drop-shadow-sm">¥</span>
                  </div>
                  <input v-model.number="form.deduction" type="number" step="0.01" min="0" placeholder="0.00" class="block w-full pl-12 pr-6 py-4 backdrop-blur-md bg-gradient-to-r from-white to-red-50 bg-opacity-95 border-2 border-red-200 hover:border-red-300 rounded-2xl shadow-lg hover:shadow-xl focus:outline-none focus:ring-4 focus:ring-red-200 focus:ring-opacity-50 focus:border-red-400 text-gray-900 placeholder-gray-500 text-lg font-medium transition-all duration-300 transform hover:scale-[1.02]" />
                </div>
              </div>
            </div>

            <!-- 提交按钮 -->
            <div class="pt-8">
              <button type="submit" :disabled="loading" class="group relative w-full flex justify-center py-5 px-8 border border-transparent text-xl font-bold rounded-2xl text-blue-600 backdrop-blur-lg bg-white bg-opacity-95 hover:bg-opacity-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-white focus:ring-opacity-60 disabled:opacity-60 disabled:cursor-not-allowed transition-all duration-300 transform hover:scale-105 disabled:transform-none shadow-2xl">
                <span v-if="loading" class="absolute left-0 inset-y-0 flex items-center pl-6">
                  <svg class="animate-spin h-6 w-6 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4l3-3-3-3v4a8 8 0 00-8 8h4z"></path>
                  </svg>
                </span>
                <span class="flex items-center">
                  <svg v-if="!loading" class="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
                  </svg>
                  {{ loading ? '正在计算薪资...' : '开始计算薪资' }}
                </span>
              </button>
            </div>
          </div>
        </form>

        <!-- 结果提示 -->
        <div v-if="message" class="mx-8 mb-8">
          <div :class="[
            'p-6 rounded-2xl border-l-4 flex items-start space-x-4 backdrop-blur-md shadow-lg',
            messageType === 'success' 
              ? 'bg-green-400 bg-opacity-25 border-green-300 text-white' 
              : 'bg-red-400 bg-opacity-25 border-red-300 text-white'
          ]">
            <div class="flex-shrink-0">
              <svg v-if="messageType === 'success'" class="h-6 w-6 text-green-200" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
              </svg>
              <svg v-else class="h-6 w-6 text-red-200" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
              </svg>
            </div>
            <div class="flex-1">
              <h3 class="text-lg font-semibold drop-shadow">
                {{ messageType === 'success' ? '操作成功' : '操作失败' }}
              </h3>
              <p class="mt-1 text-base drop-shadow-sm opacity-90">{{ message }}</p>
              <!-- 调试信息 -->
              <details v-if="messageType === 'error' && debugInfo" class="mt-3">
                <summary class="text-sm cursor-pointer hover:text-blue-100 transition-colors">查看详细信息</summary>
                <pre class="mt-2 text-sm backdrop-blur-sm bg-black bg-opacity-30 p-4 rounded-xl overflow-auto border border-white border-opacity-20 text-gray-100">{{ debugInfo }}</pre>
              </details>
            </div>
          </div>
        </div>
      </div>

      <!-- 底部说明 -->
      <div class="mt-10 text-center text-white drop-shadow-sm">
        <p class="text-lg font-medium">薪资计算基于员工基础工资 + 奖金 - 扣除项目</p>
        <p class="mt-2 text-blue-100">生成的记录可在薪资列表中查看和管理</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'

// 页面元数据
definePageMeta({
  layout: 'default'
})

const salaryApi = useSalaryApi()
const employeeApi = useEmployeeApi()

const employees = ref([])
const loading = ref(false)
const message = ref('')
const messageType = ref('success')
const debugInfo = ref('')

const form = reactive({
  employeeId: '',
  salaryPeriod: '',
  bonus: 0,
  deduction: 0
})

// 提交表单
const handleSubmit = async () => {
  if (!form.salaryPeriod) {
    messageType.value = 'error'
    message.value = '请选择薪资期间'
    debugInfo.value = ''
    return
  }

  loading.value = true
  message.value = ''
  debugInfo.value = ''
  
  try {
    const payload = {
      salary_period: form.salaryPeriod,
      bonus: Number(form.bonus) || 0,
      deduction: Number(form.deduction) || 0
    }
    
    console.log('发送请求:', { employeeId: form.employeeId, payload })
    
    let res
    if (form.employeeId) {
      res = await salaryApi.calculateSalary(form.employeeId, payload)
    } else {
      res = await salaryApi.generateSalaries(payload)
    }

    console.log('API响应:', res)

    if (res && res.success !== false) {
      messageType.value = 'success'
      message.value = res.message || '薪资计算成功！'
      // 成功后可选择性跳转回列表
      setTimeout(() => {
        navigateTo('/salaries')
      }, 2000)
    } else {
      const errMsg = res.error || (res.errors && JSON.stringify(res.errors)) || '薪资计算失败'
      throw new Error(errMsg)
    }
  } catch (err) {
    console.error('薪资计算错误:', err)
    messageType.value = 'error'
    message.value = err.message || '薪资计算失败'
    debugInfo.value = JSON.stringify({
      error: err.message,
      stack: err.stack,
      response: err.response?.data || err.data
    }, null, 2)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  // 设置默认期间为当前月份
  const now = new Date()
  form.salaryPeriod = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
  
  // 加载员工
  try {
    const res = await employeeApi.getEmployees()
    if (res && res.results) {
      employees.value = res.results.map(e => ({ 
        id: e.id, 
        name: e.name, 
        employee_id: e.employee_id 
      }))
    }
  } catch (err) {
    console.error('加载员工失败', err)
  }
})
</script>

<style scoped>
/* 自定义样式用于增强磨砂玻璃效果 */
input[type="month"]::-webkit-calendar-picker-indicator {
  filter: invert(1);
  opacity: 0.8;
}

select option {
  background-color: #f9fafb;
  color: #1f2937;
  font-weight: 600;
  padding: 8px 12px;
}

select option:hover {
  background-color: #f3f4f6;
}

select option:first-child {
  background-color: #1d4ed8;
  color: white;
}

select option:first-child:hover {
  background-color: #1e40af;
}

/* 增强输入框文字对比度 */
input::placeholder {
  color: rgba(107, 114, 128, 0.8);
  font-weight: 500;
}

/* 确保输入框文字清晰可见 */
input[type="month"],
input[type="number"],
select {
  color: #1f2937 !important;
  font-weight: 600;
}

/* 增强标签文字的可读性 */
label {
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
}

/* 确保在 Firefox 中也有良好的显示效果 */
@supports (-moz-appearance: none) {
  select {
    background-image: url("data:image/svg+xml;charset=utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 4 5'%3E%3Cpath fill='%23ffffff' d='M2 0L0 2h4zm0 5L0 3h4z'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 1.5rem center;
    background-size: 1rem;
  }
}
</style> 