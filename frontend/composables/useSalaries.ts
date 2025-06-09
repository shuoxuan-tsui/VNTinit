import { ref, reactive, watch } from 'vue'
import { useFetch } from '#app'

interface SalaryRecord {
  id: string
  employee_id: string
  employee_name: string
  department: string
  position: string
  salary_period: string
  base_salary: number
  bonus: number
  deductions: number
  net_salary: number
  created_at: string
}

interface PaginatedResponse<T> {
  results: T[]
  total_pages: number
  current_page: number
}

export function useSalaries() {
  const salaries = ref<SalaryRecord[]>([])
  const loading = ref(false)
  const searchQuery = ref('')
  const filters = reactive({ 
    department: '', 
    position: '', 
    salary_period: '',
    min_salary: '',
    max_salary: ''
  })
  const pagination = reactive({ currentPage: 1, totalPages: 1 })
  const sort = reactive({ key: '', order: 'asc' })

  async function fetchSalaries() {
    loading.value = true
    const params: Record<string, any> = { page: pagination.currentPage }
    if (searchQuery.value) params.search = searchQuery.value
    if (filters.department) params.department = filters.department
    if (filters.position) params.position = filters.position
    if (filters.salary_period) params.salary_period = filters.salary_period
    if (filters.min_salary) params.min_salary = filters.min_salary
    if (filters.max_salary) params.max_salary = filters.max_salary
    if (sort.key) params.ordering = `${sort.order === 'asc' ? '' : '-'}${sort.key}`

    const { data, error } = await useFetch<PaginatedResponse<SalaryRecord>>('/api/v1/salaries', { params })
    if (!error.value && data.value) {
      salaries.value = data.value.results || []
      pagination.totalPages = data.value.total_pages || 1
      pagination.currentPage = data.value.current_page || 1
    }
    loading.value = false
  }

  async function calculateSalary(employeeId: string, salaryData: any) {
    const { data, error } = await useFetch('/api/v1/salaries/calculate_and_create/', {
      method: 'POST',
      body: { employee_id: employeeId, ...salaryData }
    })
    return { data, error }
  }

  async function getSalaryRecord(recordId: string) {
    const { data, error } = await useFetch(`/api/v1/salaries/${recordId}/`)
    return { data, error }
  }

  async function getPrintView(recordId: string) {
    const { data, error } = await useFetch(`/api/v1/salaries/${recordId}/print_view/`)
    return { data, error }
  }

  watch([
    searchQuery,
    () => filters.department,
    () => filters.position,
    () => filters.salary_period,
    () => filters.min_salary,
    () => filters.max_salary,
    () => sort.key,
    () => sort.order,
    () => pagination.currentPage
  ], fetchSalaries, { immediate: true })

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

  return { 
    salaries, 
    loading, 
    searchQuery, 
    filters, 
    pagination, 
    sort, 
    fetchSalaries, 
    setSort, 
    changePage,
    calculateSalary,
    getSalaryRecord,
    getPrintView
  }
} 