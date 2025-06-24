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
          class="animated-button"
        >
          <svg viewBox="0 0 24 24" class="arr-2" xmlns="http://www.w3.org/2000/svg">
            <path d="m16.172 11-5.364-5.364 1.414-1.414L20 12l-7.778 7.778-1.414-1.414L16.172 13H4v-2z"></path>
          </svg>
          <span class="text">{{ submitting ? '保存中...' : '保存员工信息' }}</span>
          <span class="circle"></span>
          <svg viewBox="0 0 24 24" class="arr-1" xmlns="http://www.w3.org/2000/svg">
            <path d="m16.172 11-5.364-5.364 1.414-1.414L20 12l-7.778 7.778-1.414-1.414L16.172 13H4v-2z"></path>
          </svg>
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
const departments = ref([])

// 获取部门列表
const fetchDepartments = async () => {
  try {
    const response = await departmentApi.getDepartments()
    console.log('Department API response:', response)
    
    if (response && response.results && Array.isArray(response.results)) {
      departments.value = response.results
    } else if (response && response.success && response.data && Array.isArray(response.data.results)) {
      departments.value = response.data.results
    } else {
      console.error('Invalid department response structure:', response)
      // 如果API失败，使用默认部门列表
      departments.value = [
        { id: 1, name: "人力资源部" },
        { id: 2, name: "客服部" },
        { id: 3, name: "技术部" },
        { id: 4, name: "市场部" },
        { id: 5, name: "财务部" },
        { id: 6, name: "采购部" }
      ]
    }
  } catch (error) {
    console.error('Error fetching departments:', error)
    // 如果API失败，使用默认部门列表
    departments.value = [
      { id: 1, name: "人力资源部" },
      { id: 2, name: "客服部" },
      { id: 3, name: "技术部" },
      { id: 4, name: "市场部" },
      { id: 5, name: "财务部" },
      { id: 6, name: "采购部" }
    ]
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
  
  // Check if running on client side (browser)
  if (process.client) {
    // Check if auth token exists in localStorage
    const existingToken = localStorage.getItem('auth_token');
    
    // If no token exists, attempt auto-login with default admin credentials
    if (!existingToken) {
      $fetch('/api/auth/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: { username: 'admin', password: 'admin123' }
      }).then(loginResponse => {
        // On successful login, store token and user info
        if (loginResponse && loginResponse.success && loginResponse.data && loginResponse.data.token) {
          localStorage.setItem('auth_token', loginResponse.data.token);
          localStorage.setItem('user_info', JSON.stringify(loginResponse.data.user));
          console.log('Auto-login successful in add employee page');
          // Fetch departments after successful login
          fetchDepartments();
        }
      }).catch(err => {
        // Log error if auto-login fails but still attempt to fetch departments
        console.error('Auto-login failed in add employee page:', err);
        fetchDepartments();
      });
    } else {
      // If token exists, directly fetch departments
      fetchDepartments();
    }
  }
})
</script>

<style scoped>
/* From Uiverse.io by mask_guy_0 */ 
.animated-button {
  position: relative;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 16px 36px;
  border: 4px solid #3b82f6;
  border-color: #3b82f6;
  font-size: 16px;
  background-color: #3b82f6;

  
  border-radius: 100px;
  font-weight: 600;
  color: white;
  box-shadow: 0 0 0 2px #3b82f6;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.6s cubic-bezier(0.23, 1, 0.32, 1);
}

.animated-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.animated-button svg {
  position: absolute;
  width: 24px;
  fill: white;
  z-index: 9;
  transition: all 0.8s cubic-bezier(0.23, 1, 0.32, 1);
}

.animated-button .arr-1 {
  right: 16px;
}

.animated-button .arr-2 {
  left: -25%;
}

.animated-button .circle {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 20px;
  height: 20px;
  background-color: white;
  border-radius: 50%;
  opacity: 0;
  transition: all 0.8s cubic-bezier(0.23, 1, 0.32, 1);
}

.animated-button .text {
  position: relative;
  z-index: 1;
  transform: translateX(-12px);
  transition: all 0.8s cubic-bezier(0.23, 1, 0.32, 1);
}

.animated-button:hover:not(:disabled) {
  box-shadow: 0 0 0 12px transparent;
  color: black;
  border-radius: 12px;
}

.animated-button:hover:not(:disabled) .arr-1 {
  right: -25%;
}

.animated-button:hover:not(:disabled) .arr-2 {
  left: 16px;
}

.animated-button:hover:not(:disabled) .text {
  transform: translateX(12px);
}

.animated-button:hover:not(:disabled) svg {
  fill: #212121;
}

.animated-button:active:not(:disabled) {
  scale: 0.95;
  box-shadow: 0 0 0 4px #3b82f6;
}

.animated-button:hover:not(:disabled) .circle {
  width: 220px;
  height: 220px;
  opacity: 1;
}
</style> 