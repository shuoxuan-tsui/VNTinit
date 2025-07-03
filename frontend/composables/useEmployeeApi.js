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

  /**
   * 根据员工ID获取单个员工详细信息
   * @param {string} id - 员工ID
   * @returns {Promise<{success: boolean, data?: object, error?: string}>} 返回包含操作结果的对象
   */
  const getEmployeeById = async (id) => {
    try {
      const response = await $fetch(`/api/employees/${id}/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders() // 添加认证头信息
        }
      })
      // 验证响应数据格式，确保包含有效的员工ID
      if (response && response.id) {
        return { success: true, data: response }
      }
      return { success: false, error: '未找到该员工信息' }
    } catch (error) {
      console.error(`获取员工${id}信息失败:`, error)
      // 优先返回服务器提供的详细错误信息
      if (error.data) {
        return { success: false, error: error.data.detail || error.message }
      }
      return { success: false, error: error.message }
    }
  }
  
  /**
   * 创建新员工记录
   * @param {object} employeeData - 新员工数据对象
   * @returns {Promise<{success: boolean, data?: object, error?: string, errors?: object}>} 返回创建结果
   */
  const createEmployee = async (employeeData) => {
    try {
      const response = await $fetch('/api/employees/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders() // 添加认证头信息
        },
        body: employeeData // 请求体包含员工数据
      })
      // 验证响应是否包含新创建的员工ID
      if (response && response.id) {
        return { success: true, data: response }
      }
      return { success: false, error: '无效的响应格式' }
    } catch (error) {
      console.error('创建员工失败:', error)
      // 返回详细的错误信息，包括字段级验证错误
      if (error.data) {
        return { 
          success: false, 
          error: error.data.detail || error.message, 
          errors: error.data // 包含字段级错误详情
        }
      }
      return { success: false, error: error.message }
    }
  }

  /**
   * 更新员工信息
   * @param {string} id - 要更新的员工ID
   * @param {object} employeeData - 更新的员工数据
   * @returns {Promise<{success: boolean, data?: object, error?: string, errors?: object}>} 返回更新结果
   */
  const updateEmployee = async (id, employeeData) => {
    try {
      const response = await $fetch(`/api/employees/${id}/`, {
        method: 'PUT', // 使用PUT方法进行完整更新
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders()
        },
        body: employeeData
      })
      // 验证响应是否包含更新后的员工ID
      if (response && response.id) {
        return { success: true, data: response }
      }
      return { success: false, error: '无效的响应格式' }
    } catch (error) {
      console.error(`更新员工${id}信息失败:`, error)
      // 返回详细的错误信息
      if (error.data) {
        return { 
          success: false, 
          error: error.data.detail || error.message, 
          errors: error.data 
        }
      }
      return { success: false, error: error.message }
    }
  }

  /**
   * 删除员工记录
   * @param {string} id - 要删除的员工ID
   * @returns {Promise<{success: boolean, error?: string}>} 返回删除结果
   */
  const deleteEmployee = async (id) => {
    try {
      await $fetch(`/api/employees/${id}/`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders()
        }
      })
      return { success: true } // 删除成功无需返回数据
    } catch (error) {
      console.error(`删除员工${id}失败:`, error)
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