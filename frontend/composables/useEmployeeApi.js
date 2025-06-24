export const useEmployeeApi = () => {
  const config = useRuntimeConfig()
  // const apiBase = config.public.apiBase // Nuxt 代理会自动处理，不需要 apiBase

  const getAuthHeaders = () => {
    if (process.client) {
      const token = localStorage.getItem('auth_token')
      return token ? { 'Authorization': `Token ${token}` } : {}
    }
    return {}
  }

  const getEmployees = async (params = {}) => {
    try {
      const response = await $fetch('/api/employees/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders()
        },
        params: params // 用于将来的分页、排序、筛选
      })
      // API 返回的数据结构可能是 { success: true, data: { results: [], total_count: 0, ... } }
      // 或者直接是 { results: [], total_count: 0, ... }
      // 我们需要确保返回的是员工数组
      if (response && response.success && response.data && Array.isArray(response.data.results)) {
        return {
          results: response.data.results,
          count: response.data.total_count || response.data.count || response.data.results.length
        }
      } else if (Array.isArray(response)) { // 如果直接返回数组
        return { results: response, count: response.length } 
      } else if (response && Array.isArray(response.results)) { // 如果返回对象包含results数组
        return {
          results: response.results,
          count: response.total_count || response.count || response.results.length
        }
      }
      console.error('Invalid API response structure for getEmployees:', response)
      return { results: [], count: 0 } // 返回空数据结构以避免错误
    } catch (error) {
      console.error('Error fetching employees:', error)
      return { results: [], count: 0, error: error.message } // 附带错误信息
    }
  }

  const getEmployeeById = async (id) => {
    try {
      const response = await $fetch(`/api/employees/${id}/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders()
        }
      })
      // Django REST Framework 直接返回对象
      if (response && response.id) {
        return { success: true, data: response }
      }
      return { success: false, error: 'Employee not found' }
    } catch (error) {
      console.error(`Error fetching employee ${id}:`, error)
      if (error.data) {
        return { success: false, error: error.data.detail || error.message }
      }
      return { success: false, error: error.message }
    }
  }
  
  const createEmployee = async (employeeData) => {
    try {
      const response = await $fetch('/api/employees/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders()
        },
        body: employeeData
      })
      // Django REST Framework 直接返回创建的对象，不包装在success字段中
      if (response && response.id) {
        return { success: true, data: response }
      }
      return { success: false, error: 'Invalid response format' }
    } catch (error) {
      console.error('Error creating employee:', error)
      // 处理不同类型的错误响应
      if (error.data) {
        return { success: false, error: error.data.detail || error.message, errors: error.data }
      }
      return { success: false, error: error.message }
    }
  }

  const updateEmployee = async (id, employeeData) => {
    try {
      const response = await $fetch(`/api/employees/${id}/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders()
        },
        body: employeeData
      })
      // Django REST Framework 直接返回更新的对象
      if (response && response.id) {
        return { success: true, data: response }
      }
      return { success: false, error: 'Invalid response format' }
    } catch (error) {
      console.error(`Error updating employee ${id}:`, error)
      if (error.data) {
        return { success: false, error: error.data.detail || error.message, errors: error.data }
      }
      return { success: false, error: error.message }
    }
  }

  const deleteEmployee = async (id) => {
    try {
      await $fetch(`/api/employees/${id}/`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders()
        }
      })
      return { success: true }
    } catch (error) {
      console.error(`Error deleting employee ${id}:`, error)
      return { success: false, error: error.message }
    }
  }

  return {
    getEmployees,
    getEmployeeById,
    createEmployee,
    updateEmployee,
    deleteEmployee
  }
} 