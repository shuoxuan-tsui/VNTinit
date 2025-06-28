<template>
  <div class="space-y-6">
    <!-- 标题 -->
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold text-gray-900">计算并生成薪资</h1>
      <NuxtLink to="/salaries" class="text-primary hover:underline">← 返回列表</NuxtLink>
    </div>

    <!-- 表单卡片 -->
    <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200 max-w-xl">
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <!-- 员工选择 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">员工</label>
          <select v-model="form.employeeId" class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary">
            <option value="">所有员工</option>
            <option v-for="emp in employees" :key="emp.id" :value="emp.id">
              {{ emp.name }} ({{ emp.employee_id }})
            </option>
          </select>
          <p class="mt-1 text-xs text-gray-500">留空将为所有员工生成薪资</p>
        </div>

        <!-- 薪资期间 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">薪资期间</label>
          <input v-model="form.salaryPeriod" type="month" required class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary" />
        </div>

        <!-- 奖金 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">奖金 (可选)</label>
          <input v-model.number="form.bonus" type="number" step="0.01" min="0" class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary" />
        </div>

        <!-- 扣除 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">扣除 (可选)</label>
          <input v-model.number="form.deduction" type="number" step="0.01" min="0" class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary" />
        </div>

        <!-- 提交按钮 -->
        <div class="pt-4">
          <button type="submit" :disabled="loading" class="relative w-full inline-flex items-center justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-accent text-base font-medium text-white hover:bg-accent-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent disabled:opacity-50 disabled:cursor-not-allowed">
            <svg v-if="loading" class="animate-spin h-5 w-5 text-white absolute left-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4l3-3-3-3v4a8 8 0 00-8 8h4z"></path>
            </svg>
            <span :class="loading ? 'opacity-0' : ''">计算并生成</span>
          </button>
        </div>
      </form>

      <!-- 结果提示 -->
      <div v-if="message" class="mt-4 p-4 rounded text-white" :class="messageType === 'success' ? 'bg-green-500' : 'bg-red-500'">
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'

// 页面元数据
definePageMeta({
  layout: 'default',
  middleware: ['auth'] // 假设有 auth 中间件
})

const salaryApi = useSalaryApi()
const employeeApi = useEmployeeApi()

const employees = ref([])
const loading = ref(false)
const message = ref('')
const messageType = ref('success')

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
    return
  }

  loading.value = true
  message.value = ''
  try {
    const payload = {
      salary_period: form.salaryPeriod,
      bonus: Number(form.bonus) || 0,
      deduction: Number(form.deduction) || 0
    }
    let res
    if (form.employeeId) {
      res = await salaryApi.calculateSalary(form.employeeId, payload)
    } else {
      res = await salaryApi.generateSalaries(payload)
    }

    if (res && res.success !== false) {
      messageType.value = 'success'
      message.value = res.message || '薪资计算成功！'
    } else {
      // 后端若返回 {success:false, error:'...'}
      const errMsg = res.error || (res.errors && JSON.stringify(res.errors)) || '薪资计算失败'
      throw new Error(errMsg)
    }
  } catch (err) {
    console.error(err)
    messageType.value = 'error'
    message.value = err.message || '薪资计算失败'
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
      employees.value = res.results.map(e => ({ id: e.id, name: e.name, employee_id: e.employee_id }))
    }
  } catch (err) {
    console.error('加载员工失败', err)
  }
})
</script> 