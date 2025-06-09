// API基础配置
export const useApi = () => {
  // 获取运行时配置
  const config = useRuntimeConfig()
  const API_BASE_URL = process.client ? '/api' : `${config.public.apiBase}/api`
  
  // 获取token
  const getToken = () => {
    const token = useCookie('auth-token')
    return token.value
  }
  
  // 创建请求头
  const createHeaders = () => {
    const headers = {
      'Content-Type': 'application/json',
    }
    
    const token = getToken()
    if (token) {
      headers['Authorization'] = `Token ${token}`
    }
    
    return headers
  }
  
  // 基础请求方法
  const request = async (url, options = {}) => {
    const fullUrl = url.startsWith('http') ? url : `${API_BASE_URL}${url}`
    
    const defaultOptions = {
      headers: createHeaders(),
      ...options
    }
    
    try {
      const response = await $fetch(fullUrl, defaultOptions)
      return response
    } catch (error) {
      console.error('API Request Error:', error)
      throw error
    }
  }
  
  // GET请求
  const get = (url, params = {}) => {
    const query = new URLSearchParams(params).toString()
    const fullUrl = query ? `${url}?${query}` : url
    return request(fullUrl, { method: 'GET' })
  }
  
  // POST请求
  const post = (url, data = {}) => {
    return request(url, {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }
  
  // PUT请求
  const put = (url, data = {}) => {
    return request(url, {
      method: 'PUT',
      body: JSON.stringify(data)
    })
  }
  
  // PATCH请求
  const patch = (url, data = {}) => {
    return request(url, {
      method: 'PATCH',
      body: JSON.stringify(data)
    })
  }
  
  // DELETE请求
  const del = (url) => {
    return request(url, { method: 'DELETE' })
  }
  
  return {
    get,
    post,
    put,
    patch,
    delete: del,
    request
  }
}

// 认证API
export const useAuthApi = () => {
  const api = useApi()
  
  return {
    // 登录
    login: (credentials) => api.post('/auth/login/', credentials),
    
    // 注册
    register: (userData) => api.post('/auth/register/', userData),
    
    // 登出
    logout: () => api.post('/auth/logout/'),
    
    // 获取当前用户
    getCurrentUser: () => api.get('/auth/user/'),
    
    // 修改密码
    changePassword: (passwordData) => api.post('/auth/change-password/', passwordData),
    
    // 检查认证状态
    checkAuth: () => api.get('/auth/check/')
  }
}

// 部门API
export const useDepartmentApi = () => {
  const api = useApi()
  
  return {
    // 获取部门列表
    getDepartments: (params = {}) => api.get('/departments/', params),
    
    // 获取部门详情
    getDepartment: (id) => api.get(`/departments/${id}/`),
    
    // 创建部门
    createDepartment: (departmentData) => api.post('/departments/', departmentData),
    
    // 更新部门
    updateDepartment: (id, departmentData) => api.put(`/departments/${id}/`, departmentData),
    
    // 删除部门
    deleteDepartment: (id) => api.delete(`/departments/${id}/`)
  }
}

// 员工API
export const useEmployeeApi = () => {
  const api = useApi()
  
  return {
    // 获取员工列表
    getEmployees: (params = {}) => api.get('/employees/', params),
    
    // 获取员工详情
    getEmployee: (id) => api.get(`/employees/${id}/`),
    
    // 创建员工
    createEmployee: (employeeData) => api.post('/employees/', employeeData),
    
    // 更新员工
    updateEmployee: (id, employeeData) => api.put(`/employees/${id}/`, employeeData),
    
    // 删除员工
    deleteEmployee: (id) => api.delete(`/employees/${id}/`),
    
    // 获取员工薪资历史
    getEmployeeSalaryHistory: (employeeId) => api.get(`/employees/${employeeId}/salary/`)
  }
}

// 薪资API
export const useSalaryApi = () => {
  const api = useApi()
  
  return {
    // 获取薪资记录列表
    getSalaries: (params = {}) => api.get('/salaries/', params),
    
    // 获取薪资记录详情
    getSalary: (id) => api.get(`/salaries/${id}/`),
    
    // 计算并创建薪资记录
    calculateSalary: (salaryData) => api.post('/salaries/calculate_and_create/', salaryData),
    
    // 更新薪资记录
    updateSalary: (id, salaryData) => api.put(`/salaries/${id}/`, salaryData),
    
    // 删除薪资记录
    deleteSalary: (id) => api.delete(`/salaries/${id}/`),
    
    // 获取薪资打印视图
    getSalaryPrintView: (recordId) => api.get(`/salaries/${recordId}/print_view/`)
  }
} 