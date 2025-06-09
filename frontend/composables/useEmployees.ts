import { ref, reactive, watch } from 'vue'
import { useFetch } from '#app'

interface Employee {
  id: string
  name: string
  employee_id: string
  department: string
  position: string
  hire_date: string
  phone: string
}

interface PaginatedResponse<T> {
  results: T[]
  total_pages: number
  current_page: number
}

export function useEmployees() {
  const employees = ref<Employee[]>([])
  const loading = ref(false)
  const searchQuery = ref('')
  const filters = reactive({ department: '', position: '' })
  const pagination = reactive({ currentPage: 1, totalPages: 1 })
  const sort = reactive({ key: '', order: 'asc' })

  async function fetchEmployees() {
    loading.value = true
    const params: Record<string, any> = { page: pagination.currentPage }
    if (searchQuery.value) params.search = searchQuery.value
    if (filters.department) params.department = filters.department
    if (filters.position) params.position = filters.position
    if (sort.key) params.ordering = `${sort.order === 'asc' ? '' : '-'}${sort.key}`

    const { data, error } = await useFetch<PaginatedResponse<Employee>>('/api/v1/employees', { params })
    if (!error.value && data.value) {
      employees.value = data.value.results || []
      pagination.totalPages = data.value.total_pages || 1
      pagination.currentPage = data.value.current_page || 1
    }
    loading.value = false
  }

  watch([
    searchQuery,
    () => filters.department,
    () => filters.position,
    () => sort.key,
    () => sort.order,
    () => pagination.currentPage
  ], fetchEmployees, { immediate: true })

  function setSort(key: string) {
    if (sort.key === key) {
      sort.order = sort.order === 'asc' ? 'desc' : 'asc'
    } else {
      sort.key = key
      sort.order = 'asc'
    }
  }

  function changePage(page: number) {
    if (page >= 1 && page <= pagination.totalPages) {
      pagination.currentPage = page
    }
  }

  return { employees, loading, searchQuery, filters, pagination, sort, fetchEmployees, setSort, changePage }
} 