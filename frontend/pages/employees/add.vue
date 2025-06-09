<template>
  <div class="max-w-4xl mx-auto">
    <!-- 页面标题 -->
    <div class="mb-6">
      <div class="flex items-center space-x-4">
        <NuxtLink
          to="/employees"
          class="inline-flex items-center text-sm text-gray-500 hover:text-gray-700 transition-colors"
        >
          <Icon name="heroicons:arrow-left" class="mr-1 h-4 w-4" />
          返回员工列表
        </NuxtLink>
      </div>
      <h1 class="mt-2 text-2xl font-bold text-gray-900">添加员工信息</h1>
      <p class="mt-1 text-sm text-gray-500">请填写完整的员工信息</p>
    </div>

    <!-- 表单 -->
    <form @submit.prevent="submitForm" class="space-y-6">
      <div class="bg-white shadow-sm rounded-lg border border-gray-200">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-medium text-gray-900">基本信息</h3>
        </div>
        
        <div class="px-6 py-6 space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- 姓名 -->
            <div>
              <label for="name" class="block text-sm font-medium text-gray-700 mb-1">
                姓名 <span class="text-red-500">*</span>
              </label>
              <input
                id="name"
                v-model="form.name"
                type="text"
                required
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary"
                :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500': errors.name }"
                placeholder="请输入员工姓名"
              />
              <p v-if="errors.name" class="mt-1 text-sm text-red-600">{{ errors.name }}</p>
            </div>

            <!-- 工号 -->
            <div>
              <label for="employee_id" class="block text-sm font-medium text-gray-700 mb-1">
                工号 <span class="text-red-500">*</span>
              </label>
              <input
                id="employee_id"
                v-model="form.employee_id"
                type="text"
                required
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary"
                :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500': errors.employee_id }"
                placeholder="请输入员工工号"
              />
              <p v-if="errors.employee_id" class="mt-1 text-sm text-red-600">{{ errors.employee_id }}</p>
            </div>

            <!-- 性别 -->
            <div>
              <label for="gender" class="block text-sm font-medium text-gray-700 mb-1">
                性别 <span class="text-red-500">*</span>
              </label>
              <select
                id="gender"
                v-model="form.gender"
                required
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
                :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500': errors.gender }"
              >
                <option value="">请选择性别</option>
                <option value="M">男</option>
                <option value="F">女</option>
              </select>
              <p v-if="errors.gender" class="mt-1 text-sm text-red-600">{{ errors.gender }}</p>
            </div>

            <!-- 电话 -->
            <div>
              <label for="phone" class="block text-sm font-medium text-gray-700 mb-1">
                电话号码 <span class="text-red-500">*</span>
              </label>
              <input
                id="phone"
                v-model="form.phone"
                type="tel"
                required
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary"
                :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500': errors.phone }"
                placeholder="请输入手机号码"
              />
              <p v-if="errors.phone" class="mt-1 text-sm text-red-600">{{ errors.phone }}</p>
            </div>

            <!-- 出生日期 -->
            <div>
              <label for="birth_date" class="block text-sm font-medium text-gray-700 mb-1">
                出生日期 <span class="text-red-500">*</span>
              </label>
              <input
                id="birth_date"
                v-model="form.birth_date"
                type="date"
                required
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
                :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500': errors.birth_date }"
              />
              <p v-if="errors.birth_date" class="mt-1 text-sm text-red-600">{{ errors.birth_date }}</p>
            </div>

            <!-- 入职日期 -->
            <div>
              <label for="hire_date" class="block text-sm font-medium text-gray-700 mb-1">
                入职日期 <span class="text-red-500">*</span>
              </label>
              <input
                id="hire_date"
                v-model="form.hire_date"
                type="date"
                required
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
                :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500': errors.hire_date }"
              />
              <p v-if="errors.hire_date" class="mt-1 text-sm text-red-600">{{ errors.hire_date }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 工作信息 -->
      <div class="bg-white shadow-sm rounded-lg border border-gray-200">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-medium text-gray-900">工作信息</h3>
        </div>
        
        <div class="px-6 py-6 space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- 部门 -->
            <div>
              <label for="department" class="block text-sm font-medium text-gray-700 mb-1">
                部门 <span class="text-red-500">*</span>
              </label>
              <select
                id="department"
                v-model="form.department_ref"
                required
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
                :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500': errors.department }"
              >
                <option value="">请选择部门</option>
                <option v-for="dept in departments" :key="dept.id" :value="dept.id">{{ dept.name }}</option>
              </select>
              <p v-if="errors.department" class="mt-1 text-sm text-red-600">{{ errors.department }}</p>
            </div>

            <!-- 职称 -->
            <div>
              <label for="position" class="block text-sm font-medium text-gray-700 mb-1">
                职称/职务 <span class="text-red-500">*</span>
              </label>
              <select
                id="position"
                v-model="form.position"
                required
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
                :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500': errors.position }"
              >
                <option value="">请选择职称</option>
                <option v-for="pos in positions" :key="pos" :value="pos">{{ pos }}</option>
              </select>
              <p v-if="errors.position" class="mt-1 text-sm text-red-600">{{ errors.position }}</p>
            </div>

            <!-- 基础工资 -->
            <div class="md:col-span-2">
              <label for="base_salary" class="block text-sm font-medium text-gray-700 mb-1">
                基础工资 <span class="text-red-500">*</span>
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <span class="text-gray-500 sm:text-sm">¥</span>
                </div>
                <input
                  id="base_salary"
                  v-model.number="form.base_salary"
                  type="number"
                  step="0.01"
                  min="0"
                  required
                  class="block w-full pl-8 pr-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary"
                  :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500': errors.base_salary }"
                  placeholder="请输入基础工资"
                />
              </div>
              <p v-if="errors.base_salary" class="mt-1 text-sm text-red-600">{{ errors.base_salary }}</p>
              <p class="mt-1 text-sm text-gray-500">基础工资将用于薪资计算</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="flex justify-end space-x-4">
        <NuxtLink
          to="/employees"
          class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-colors"
        >
          取消
        </NuxtLink>
        <button
          type="submit"
          :disabled="submitting"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <div v-if="submitting" class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
          {{ submitting ? '保存中...' : '保存员工信息' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'

// 页面元数据
definePageMeta({
  layout: 'default'
})

// 使用API
const employeeApi = useEmployeeApi()
const departmentApi = useDepartmentApi()

// 响应式数据
const loading = ref(false)
const submitting = ref(false)

// 表单数据
const form = reactive({
  name: '',
  employee_id: '',
  gender: '',
  phone: '',
  birth_date: '',
  hire_date: '',
  department_ref: '',
  position: '?',
  base_salary: null
})

// 错误信息
const errors = ref({})

// 选项数据
const departments = ref([
  "人力资源部",
  "客服部",
  "技术部",
  "市场部",
  "财务部",
  "采购部"
])

// 获取部门列表
const fetchDepartments = async () => {
  try {
    const response = await departmentApi.getDepartments()
    if (response.success) {
      departments.value = response.data.results
    }
  } catch (error) {
    console.error('Error fetching departments:', error)
  }
}

const positions = ref([
  '总经理',
  '副总经理',
  '部门经理',
  '高级工程师',
  '工程师',
  '初级工程师',
  '人事经理',
  '人事专员',
  '财务经理',
  '会计师',
  '出纳',
  '市场经理',
  '市场专员',
  '运营经理',
  '运营专员',
  '客服主管',
  '客服专员',
  '行政主管',
  '行政专员'
])

// 表单验证
const validateForm = () => {
  errors.value = {}
  
  // 姓名验证
  if (!form.name.trim()) {
    errors.value.name = '请输入员工姓名'
  } else if (form.name.trim().length < 2) {
    errors.value.name = '姓名至少需要2个字符'
  }
  
  // 工号验证
  if (!form.employee_id.trim()) {
    errors.value.employee_id = '请输入员工工号'
  } else if (!/^[A-Z0-9]+$/.test(form.employee_id.trim())) {
    errors.value.employee_id = '工号只能包含大写字母和数字'
  }
  
  // 性别验证
  if (!form.gender) {
    errors.value.gender = '请选择性别'
  }
  
  // 电话验证
  if (!form.phone.trim()) {
    errors.value.phone = '请输入电话号码'
  } else if (!/^1[3-9]\d{9}$/.test(form.phone.trim())) {
    errors.value.phone = '请输入有效的手机号码'
  }
  
  // 出生日期验证
  if (!form.birth_date) {
    errors.value.birth_date = '请选择出生日期'
  } else {
    const birthDate = new Date(form.birth_date)
    const today = new Date()
    const age = today.getFullYear() - birthDate.getFullYear()
    if (age < 16 || age > 70) {
      errors.value.birth_date = '员工年龄应在16-70岁之间'
    }
  }
  
  // 入职日期验证
  if (!form.hire_date) {
    errors.value.hire_date = '请选择入职日期'
  } else {
    const hireDate = new Date(form.hire_date)
    const today = new Date()
    if (hireDate > today) {
      errors.value.hire_date = '入职日期不能晚于今天'
    }
    if (form.birth_date) {
      const birthDate = new Date(form.birth_date)
      const minHireDate = new Date(birthDate.getFullYear() + 16, birthDate.getMonth(), birthDate.getDate())
      if (hireDate < minHireDate) {
        errors.value.hire_date = '入职日期不能早于16岁生日'
      }
    }
  }
  
  // 部门验证
  if (!form.department_ref) {
    errors.value.department = '请选择部门'
  }
  
  // 职称验证
  if (!form.position) {
    errors.value.position = '请选择职称'
  }
  
  // 基础工资验证
  if (!form.base_salary || form.base_salary <= 0) {
    errors.value.base_salary = '请输入有效的基础工资'
  } else if (form.base_salary < 1000) {
    errors.value.base_salary = '基础工资不能低于1000元'
  } else if (form.base_salary > 100000) {
    errors.value.base_salary = '基础工资不能超过100000元'
  }
  
  return Object.keys(errors.value).length === 0
}

// 提交表单
const submitForm = async () => {
  if (!validateForm()) {
    return
  }
  
  submitting.value = true
  
  try {
    // 准备提交的数据
    const employeeData = {
      name: form.name.trim(),
      employee_id: form.employee_id.trim(),
      gender: form.gender,
      phone: form.phone.trim(),
      birth_date: form.birth_date,
      hire_date: form.hire_date,
      department_ref: form.department_ref,
      position: form.position,
      base_salary: form.base_salary,
      status: 'active', // 新员工默认为在职状态
      location: '北京总部' // 默认位置，可以后续扩展为表单字段
    }
    
    console.log('提交员工信息:', employeeData)
    
    // 调用API创建员工
    const response = await employeeApi.createEmployee(employeeData)
    
    if (response.success) {
      // 成功后跳转到员工列表
      await navigateTo('/employees')
      console.log('员工信息添加成功')
    } else {
      // 处理API返回的错误
      if (response.errors) {
        // 如果有字段级别的错误，显示在对应字段下
        Object.keys(response.errors).forEach(field => {
          if (errors.value.hasOwnProperty(field)) {
            errors.value[field] = Array.isArray(response.errors[field]) 
              ? response.errors[field][0] 
              : response.errors[field]
          }
        })
      } else {
        // 通用错误处理
        console.error('添加员工失败:', response.error)
        // 可以在这里添加全局错误提示
      }
    }
    
  } catch (error) {
    console.error('添加员工失败:', error)
    // 显示错误提示
  } finally {
    submitting.value = false
  }
}

// 设置默认入职日期为今天
onMounted(() => {
  const today = new Date()
  form.hire_date = today.toISOString().split('T')[0]
  fetchDepartments()
})
</script> 