export const useDepartmentApi = () => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase

  // 获取认证token
  const getAuthHeaders = () => {
    if (process.client) {
      const token = localStorage.getItem('auth_token')
      console.log('Getting auth token:', token)
      return token ? { 'Authorization': `Token ${token}` } : {}
    }
    return {}
  }

  const getDepartments = async () => {
    try {
      console.log('Fetching departments from: /api/departments/')
      const headers = {
        'Content-Type': 'application/json',
        ...getAuthHeaders()
      }
      console.log('Request headers:', headers)
      
      const response = await $fetch('/api/departments/', {
        method: 'GET',
        headers
      })
      
      console.log('Departments response:', response)
      return response
    } catch (error) {
      console.error('Error fetching departments:', error)
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
      return { success: false, error: error.message, errors: error.data?.errors }
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
      console.error('Error updating department:', error)
      return { success: false, error: error.message, errors: error.data?.errors }
    }
  }

  const deleteDepartment = async (id) => {
    try {
      const response = await $fetch(`/api/departments/${id}/`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders()
        }
      })
      return { success: true }
    } catch (error) {
      console.error('Error deleting department:', error)
      return { success: false, error: error.message }
    }
  }

  return {
    getDepartments,
    createDepartment,
    updateDepartment,
    deleteDepartment
  }
} 