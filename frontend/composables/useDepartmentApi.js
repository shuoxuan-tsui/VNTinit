export const useDepartmentApi = () => {
  const config = useRuntimeConfig()

  const getAuthHeaders = () => {
    if (process.client) {
      const token = localStorage.getItem('auth_token')
      return token ? { 'Authorization': `Token ${token}` } : {}
    }
    return {}
  }

  const getDepartments = async (params = {}) => {
    try {
      const response = await $fetch('/api/departments/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders()
        },
        params: params
      })
      
      if (response && response.success && response.data && Array.isArray(response.data.results)) {
        return response.data
      } else if (Array.isArray(response)) {
        return { results: response, count: response.length }
      } else if (response && Array.isArray(response.results)) {
        return response
      }
      console.error('Invalid API response structure for getDepartments:', response)
      return { results: [], count: 0 }
    } catch (error) {
      console.error('Error fetching departments:', error)
      return { results: [], count: 0, error: error.message }
    }
  }

  const getDepartmentById = async (id) => {
    try {
      const response = await $fetch(`/api/departments/${id}/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders()
        }
      })
      return response
    } catch (error) {
      console.error(`Error fetching department ${id}:`, error)
      return { success: false, error: error.message }
    }
  }

  const createDepartment = async (departmentData) => {
    try {
      const response = await $fetch('/api/departments/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders()
        },
        body: departmentData
      })
      return response
    } catch (error) {
      console.error('Error creating department:', error)
      return { success: false, error: error.message, errors: error.data?.errors || error.response?._data?.errors }
    }
  }

  const updateDepartment = async (id, departmentData) => {
    try {
      const response = await $fetch(`/api/departments/${id}/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders()
        },
        body: departmentData
      })
      return response
    } catch (error) {
      console.error(`Error updating department ${id}:`, error)
      return { success: false, error: error.message, errors: error.data?.errors || error.response?._data?.errors }
    }
  }

  const deleteDepartment = async (id) => {
    try {
      await $fetch(`/api/departments/${id}/`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders()
        }
      })
      return { success: true }
    } catch (error) {
      console.error(`Error deleting department ${id}:`, error)
      return { success: false, error: error.message }
    }
  }

  return {
    getDepartments,
    getDepartmentById,
    createDepartment,
    updateDepartment,
    deleteDepartment
  }
} 