export const useSalaryApi = () => {
  const config = useRuntimeConfig()

  const getAuthHeaders = () => {
    if (process.client) {
      const token = localStorage.getItem('auth_token')
      return token ? { 'Authorization': `Token ${token}` } : {}
    }
    return {}
  }

  const getSalaries = async (params = {}) => {
    try {
      const response = await $fetch('/api/salaries/', {
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
      console.error('Invalid API response structure for getSalaries:', response)
      return { results: [], count: 0 }
    } catch (error) {
      console.error('Error fetching salaries:', error)
      return { results: [], count: 0, error: error.message }
    }
  }

  const getSalaryById = async (id) => {
    try {
      const response = await $fetch(`/api/salaries/${id}/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders()
        }
      })
      return response
    } catch (error) {
      console.error(`Error fetching salary ${id}:`, error)
      return { success: false, error: error.message }
    }
  }

  const createSalary = async (salaryData) => {
    try {
      const response = await $fetch('/api/salaries/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders()
        },
        body: salaryData
      })
      return response
    } catch (error) {
      console.error('Error creating salary:', error)
      return { success: false, error: error.message, errors: error.data?.errors || error.response?._data?.errors }
    }
  }

  const updateSalary = async (id, salaryData) => {
    try {
      const response = await $fetch(`/api/salaries/${id}/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders()
        },
        body: salaryData
      })
      return response
    } catch (error) {
      console.error(`Error updating salary ${id}:`, error)
      return { success: false, error: error.message, errors: error.data?.errors || error.response?._data?.errors }
    }
  }

  const deleteSalary = async (id) => {
    try {
      await $fetch(`/api/salaries/${id}/`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders()
        }
      })
      return { success: true }
    } catch (error) {
      console.error(`Error deleting salary ${id}:`, error)
      return { success: false, error: error.message }
    }
  }

  const generateSalaries = async (period) => {
    try {
      const response = await $fetch('/api/salaries/generate/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders()
        },
        body: { period }
      })
      return response
    } catch (error) {
      console.error('Error generating salaries:', error)
      return { success: false, error: error.message, errors: error.data?.errors || error.response?._data?.errors }
    }
  }

  return {
    getSalaries,
    getSalaryById,
    createSalary,
    updateSalary,
    deleteSalary,
    generateSalaries
  }
} 