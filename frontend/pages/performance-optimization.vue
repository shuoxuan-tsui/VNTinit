<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 页面标题 -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">算法性能优化演示</h1>
        <p class="mt-2 text-gray-600">展示经典算法在员工管理系统中的应用和性能提升</p>
      </div>

      <!-- 性能统计卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <Icon name="heroicons:bolt" class="h-8 w-8 text-yellow-500" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">排序性能提升</p>
              <p class="text-2xl font-semibold text-gray-900">{{ sortPerformance }}%</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <Icon name="heroicons:magnifying-glass" class="h-8 w-8 text-blue-500" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">搜索性能提升</p>
              <p class="text-2xl font-semibold text-gray-900">{{ searchPerformance }}%</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <Icon name="heroicons:chart-bar" class="h-8 w-8 text-green-500" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">内存使用优化</p>
              <p class="text-2xl font-semibold text-gray-900">{{ memoryOptimization }}%</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <Icon name="heroicons:cpu-chip" class="h-8 w-8 text-purple-500" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">算法复杂度</p>
              <p class="text-2xl font-semibold text-gray-900">O(n log n)</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 算法演示标签页 -->
      <div class="bg-white shadow rounded-lg">
        <div class="border-b border-gray-200">
          <nav class="-mb-px flex space-x-8" aria-label="Tabs">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              :class="[
                activeTab === tab.id
                  ? 'border-primary text-primary'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                'whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm'
              ]"
            >
              <Icon :name="tab.icon" class="h-5 w-5 mr-2 inline" />
              {{ tab.name }}
            </button>
          </nav>
        </div>

        <div class="p-6">
          <!-- 快速排序演示 -->
          <div v-if="activeTab === 'quicksort'" class="space-y-6">
            <div class="flex items-center justify-between">
              <h3 class="text-lg font-medium text-gray-900">快速排序算法演示</h3>
              <button
                @click="demonstrateQuickSort"
                :disabled="sorting"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary disabled:opacity-50"
              >
                <Icon v-if="sorting" name="heroicons:arrow-path" class="animate-spin h-4 w-4 mr-2" />
                {{ sorting ? '排序中...' : '开始演示' }}
              </button>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div>
                <h4 class="text-md font-medium text-gray-700 mb-3">原始数据（{{ testData.length }} 条记录）</h4>
                <div class="bg-gray-50 rounded-lg p-4 max-h-64 overflow-y-auto">
                  <div class="text-sm text-gray-600">
                    <div v-for="(item, index) in testData.slice(0, 10)" :key="index" class="py-1">
                      {{ item.name }} - {{ item.salary }}
                    </div>
                    <div v-if="testData.length > 10" class="py-1 text-gray-400">
                      ... 还有 {{ testData.length - 10 }} 条记录
                    </div>
                  </div>
                </div>
              </div>

              <div>
                <h4 class="text-md font-medium text-gray-700 mb-3">排序结果</h4>
                <div class="bg-gray-50 rounded-lg p-4 max-h-64 overflow-y-auto">
                  <div class="text-sm text-gray-600">
                    <div v-for="(item, index) in sortedData.slice(0, 10)" :key="index" class="py-1">
                      {{ item.name }} - {{ item.salary }}
                    </div>
                    <div v-if="sortedData.length > 10" class="py-1 text-gray-400">
                      ... 还有 {{ sortedData.length - 10 }} 条记录
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h4 class="text-sm font-medium text-blue-800 mb-2">性能对比</h4>
              <div class="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span class="text-blue-600">原生排序:</span> {{ nativeSortTime }}ms
                </div>
                <div>
                  <span class="text-blue-600">快速排序:</span> {{ quickSortTime }}ms
                </div>
                <div>
                  <span class="text-blue-600">性能提升:</span> {{ sortPerformanceImprovement }}%
                </div>
                <div>
                  <span class="text-blue-600">算法复杂度:</span> O(n log n)
                </div>
              </div>
            </div>
          </div>

          <!-- Dijkstra算法演示 -->
          <div v-if="activeTab === 'dijkstra'" class="space-y-6">
            <div class="flex items-center justify-between">
              <h3 class="text-lg font-medium text-gray-900">职业发展路径优化</h3>
              <button
                @click="demonstrateDijkstra"
                :disabled="pathfinding"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary disabled:opacity-50"
              >
                <Icon v-if="pathfinding" name="heroicons:arrow-path" class="animate-spin h-4 w-4 mr-2" />
                {{ pathfinding ? '计算中...' : '寻找最佳路径' }}
              </button>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div>
                <h4 class="text-md font-medium text-gray-700 mb-3">选择起始和目标部门</h4>
                <div class="space-y-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700">当前部门</label>
                    <select v-model="selectedStartDept" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary">
                      <option value="">选择部门</option>
                      <option v-for="dept in departments" :key="dept" :value="dept">{{ dept }}</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700">目标部门</label>
                    <select v-model="selectedTargetDept" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary">
                      <option value="">选择部门</option>
                      <option v-for="dept in departments" :key="dept" :value="dept">{{ dept }}</option>
                    </select>
                  </div>
                </div>
              </div>

              <div>
                <h4 class="text-md font-medium text-gray-700 mb-3">最佳路径</h4>
                <div class="bg-gray-50 rounded-lg p-4">
                  <div v-if="careerPath.length > 0" class="space-y-2">
                    <div v-for="(step, index) in careerPath" :key="index" class="flex items-center">
                      <div class="flex-shrink-0 w-8 h-8 bg-primary rounded-full flex items-center justify-center text-white text-sm font-medium">
                        {{ index + 1 }}
                      </div>
                      <div class="ml-3">
                        <p class="text-sm font-medium text-gray-900">{{ step.department }}</p>
                        <p class="text-xs text-gray-500">平均薪资: ¥{{ step.averageSalary?.toLocaleString() }}</p>
                      </div>
                    </div>
                  </div>
                  <div v-else class="text-sm text-gray-500 text-center">
                    请选择起始和目标部门
                  </div>
                </div>
              </div>
            </div>

            <div v-if="careerRecommendations.length > 0" class="bg-green-50 border border-green-200 rounded-lg p-4">
              <h4 class="text-sm font-medium text-green-800 mb-2">发展建议</h4>
              <div class="space-y-2">
                <div v-for="rec in careerRecommendations" :key="rec.step" class="text-sm text-green-700">
                  <strong>步骤 {{ rec.step }}:</strong> {{ rec.from }} → {{ rec.to }}
                  <ul class="ml-4 mt-1 list-disc">
                    <li v-for="suggestion in rec.suggestions" :key="suggestion">{{ suggestion }}</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <!-- 动态规划演示 -->
          <div v-if="activeTab === 'dp'" class="space-y-6">
            <div class="flex items-center justify-between">
              <h3 class="text-lg font-medium text-gray-900">薪资预算优化（背包问题）</h3>
              <button
                @click="demonstrateKnapsack"
                :disabled="optimizing"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary disabled:opacity-50"
              >
                <Icon v-if="optimizing" name="heroicons:arrow-path" class="animate-spin h-4 w-4 mr-2" />
                {{ optimizing ? '优化中...' : '开始优化' }}
              </button>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div>
                <h4 class="text-md font-medium text-gray-700 mb-3">预算设置</h4>
                <div class="space-y-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700">总预算 (万元)</label>
                    <input
                      v-model.number="budget"
                      type="number"
                      min="10"
                      max="1000"
                      step="10"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary"
                    />
                  </div>
                  <div class="bg-gray-50 rounded-lg p-4">
                    <h5 class="text-sm font-medium text-gray-700 mb-2">可选员工 ({{ candidateEmployees.length }} 人)</h5>
                    <div class="max-h-32 overflow-y-auto text-sm text-gray-600">
                      <div v-for="emp in candidateEmployees.slice(0, 5)" :key="emp.id" class="py-1">
                        {{ emp.name }} - ¥{{ emp.salary?.toLocaleString() }} (价值: {{ emp.value }})
                      </div>
                      <div v-if="candidateEmployees.length > 5" class="py-1 text-gray-400">
                        ... 还有 {{ candidateEmployees.length - 5 }} 名员工
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div>
                <h4 class="text-md font-medium text-gray-700 mb-3">优化结果</h4>
                <div class="bg-gray-50 rounded-lg p-4">
                  <div v-if="knapsackResult.selectedEmployees?.length > 0" class="space-y-2">
                    <div class="text-sm">
                      <strong>最优选择:</strong> {{ knapsackResult.selectedEmployees.length }} 名员工
                    </div>
                    <div class="text-sm">
                      <strong>总成本:</strong> ¥{{ knapsackResult.totalCost?.toLocaleString() }}
                    </div>
                    <div class="text-sm">
                      <strong>总价值:</strong> {{ knapsackResult.maxValue }}
                    </div>
                    <div class="text-sm">
                      <strong>效率:</strong> {{ (knapsackResult.efficiency * 100)?.toFixed(2) }}%
                    </div>
                    <div class="mt-3">
                      <h6 class="text-xs font-medium text-gray-700 mb-1">选中员工:</h6>
                      <div class="text-xs text-gray-600">
                        <div v-for="emp in knapsackResult.selectedEmployees" :key="emp.id">
                          {{ emp.name }} (¥{{ emp.salary?.toLocaleString() }})
                        </div>
                      </div>
                    </div>
                  </div>
                  <div v-else class="text-sm text-gray-500 text-center">
                    点击"开始优化"查看结果
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 搜索算法演示 -->
          <div v-if="activeTab === 'search'" class="space-y-6">
            <div class="flex items-center justify-between">
              <h3 class="text-lg font-medium text-gray-900">高级搜索算法演示</h3>
              <button
                @click="demonstrateSearch"
                :disabled="searching"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary disabled:opacity-50"
              >
                <Icon v-if="searching" name="heroicons:arrow-path" class="animate-spin h-4 w-4 mr-2" />
                {{ searching ? '搜索中...' : '开始搜索' }}
              </button>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div>
                <h4 class="text-md font-medium text-gray-700 mb-3">搜索配置</h4>
                <div class="space-y-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700">搜索关键词</label>
                    <input
                      v-model="searchKeyword"
                      type="text"
                      placeholder="输入员工姓名或技能..."
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700">搜索算法</label>
                    <select v-model="selectedSearchAlgorithm" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary">
                      <option value="fuzzy">模糊搜索</option>
                      <option value="kmp">KMP字符串匹配</option>
                      <option value="binary">二分搜索</option>
                    </select>
                  </div>
                </div>
              </div>

              <div>
                <h4 class="text-md font-medium text-gray-700 mb-3">搜索结果</h4>
                <div class="bg-gray-50 rounded-lg p-4 max-h-64 overflow-y-auto">
                  <div v-if="searchResults.length > 0" class="space-y-2">
                    <div v-for="result in searchResults" :key="result.id" class="text-sm">
                      <div class="font-medium">{{ result.name }}</div>
                      <div class="text-gray-500">{{ result.department }} - {{ result.position }}</div>
                      <div v-if="result.similarity" class="text-xs text-blue-600">
                        相似度: {{ (result.similarity * 100).toFixed(1) }}%
                      </div>
                    </div>
                  </div>
                  <div v-else class="text-sm text-gray-500 text-center">
                    输入关键词并点击搜索
                  </div>
                </div>
              </div>
            </div>

            <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <h4 class="text-sm font-medium text-yellow-800 mb-2">搜索性能</h4>
              <div class="grid grid-cols-3 gap-4 text-sm">
                <div>
                  <span class="text-yellow-600">搜索时间:</span> {{ searchTime }}ms
                </div>
                <div>
                  <span class="text-yellow-600">结果数量:</span> {{ searchResults.length }}
                </div>
                <div>
                  <span class="text-yellow-600">算法复杂度:</span> {{ searchComplexity }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAdvancedSort, useAdvancedSearch } from '@/composables/useAdvancedSort'
import { useGraphAlgorithms } from '@/composables/useGraphAlgorithms'
import { useDynamicProgramming } from '@/composables/useDynamicProgramming'
import { useEmployeeApi } from '@/composables/useEmployeeApi'

// 页面元数据
definePageMeta({
  layout: 'default'
})

// 算法实例
const { hybridSort } = useAdvancedSort()
const { fuzzySearch, kmpSearch, binarySearch } = useAdvancedSearch()
const { findOptimalCareerPath } = useGraphAlgorithms()
const { knapsackSalaryOptimization } = useDynamicProgramming()
const { getEmployees } = useEmployeeApi()

// 响应式数据
const activeTab = ref('quicksort')
const sorting = ref(false)
const pathfinding = ref(false)
const optimizing = ref(false)
const searching = ref(false)

// 性能统计
const sortPerformance = ref(0)
const searchPerformance = ref(0)
const memoryOptimization = ref(0)

// 测试数据
const testData = ref([])
const sortedData = ref([])
const allEmployees = ref([])

// 排序性能数据
const nativeSortTime = ref(0)
const quickSortTime = ref(0)
const sortPerformanceImprovement = computed(() => {
  if (nativeSortTime.value === 0) return 0
  return Math.round(((nativeSortTime.value - quickSortTime.value) / nativeSortTime.value) * 100)
})

// Dijkstra相关数据
const departments = ref(['技术部', '市场部', '人事部', '财务部', '运营部', '客服部', '行政部', '法务部'])
const selectedStartDept = ref('')
const selectedTargetDept = ref('')
const careerPath = ref([])
const careerRecommendations = ref([])

// 动态规划相关数据
const budget = ref(100) // 万元
const candidateEmployees = ref([])
const knapsackResult = ref({})

// 搜索相关数据
const searchKeyword = ref('')
const selectedSearchAlgorithm = ref('fuzzy')
const searchResults = ref([])
const searchTime = ref(0)
const searchComplexity = computed(() => {
  switch (selectedSearchAlgorithm.value) {
    case 'fuzzy': return 'O(n*m)'
    case 'kmp': return 'O(n+m)'
    case 'binary': return 'O(log n)'
    default: return 'O(n)'
  }
})

// 标签页配置
const tabs = [
  { id: 'quicksort', name: '快速排序', icon: 'heroicons:arrows-up-down' },
  { id: 'dijkstra', name: 'Dijkstra路径', icon: 'heroicons:map' },
  { id: 'dp', name: '动态规划', icon: 'heroicons:calculator' },
  { id: 'search', name: '搜索算法', icon: 'heroicons:magnifying-glass' }
]

// 生成测试数据
const generateTestData = (count = 1000) => {
  const names = ['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十']
  const departments = ['技术部', '市场部', '人事部', '财务部', '运营部']
  const positions = ['工程师', '经理', '专员', '主管', '总监']
  
  return Array.from({ length: count }, (_, i) => ({
    id: i + 1,
    name: `${names[i % names.length]}${i + 1}`,
    department: departments[i % departments.length],
    position: positions[i % positions.length],
    salary: Math.floor(Math.random() * 50000) + 10000,
    value: Math.floor(Math.random() * 10) + 1 // 员工价值评分 1-10
  }))
}

// 快速排序演示
const demonstrateQuickSort = async () => {
  sorting.value = true
  
  try {
    // 生成测试数据
    testData.value = generateTestData(5000)
    
    // 原生排序性能测试
    const nativeStart = performance.now()
    const nativeSorted = [...testData.value].sort((a, b) => a.salary - b.salary)
    const nativeEnd = performance.now()
    nativeSortTime.value = Math.round(nativeEnd - nativeStart)
    
    // 快速排序性能测试
    const quickStart = performance.now()
    sortedData.value = hybridSort(testData.value, 'salary', 'asc')
    const quickEnd = performance.now()
    quickSortTime.value = Math.round(quickEnd - quickStart)
    
    // 更新性能统计
    sortPerformance.value = sortPerformanceImprovement.value
    
  } finally {
    sorting.value = false
  }
}

// Dijkstra算法演示
const demonstrateDijkstra = async () => {
  if (!selectedStartDept.value || !selectedTargetDept.value) {
    alert('请选择起始和目标部门')
    return
  }
  
  pathfinding.value = true
  
  try {
    // 模拟部门和员工数据
    const mockDepartments = departments.value.map(name => ({ name }))
    const mockEmployees = generateTestData(200)
    
    const result = findOptimalCareerPath(
      mockDepartments,
      mockEmployees,
      selectedStartDept.value,
      selectedTargetDept.value
    )
    
    careerPath.value = result.detailedPath || []
    careerRecommendations.value = result.recommendations || []
    
  } finally {
    pathfinding.value = false
  }
}

// 背包问题演示
const demonstrateKnapsack = async () => {
  optimizing.value = true
  
  try {
    // 生成候选员工数据
    candidateEmployees.value = generateTestData(50)
    
    // 执行背包算法优化
    const result = knapsackSalaryOptimization(candidateEmployees.value, budget.value * 10000)
    knapsackResult.value = result
    
  } finally {
    optimizing.value = false
  }
}

// 搜索算法演示
const demonstrateSearch = async () => {
  if (!searchKeyword.value.trim()) {
    alert('请输入搜索关键词')
    return
  }
  
  searching.value = true
  
  try {
    const searchStart = performance.now()
    
    switch (selectedSearchAlgorithm.value) {
      case 'fuzzy':
        searchResults.value = fuzzySearch(
          allEmployees.value,
          searchKeyword.value,
          ['name', 'department', 'position'],
          0.3
        )
        break
      
      case 'kmp':
        // KMP搜索演示
        searchResults.value = allEmployees.value.filter(emp => {
          const text = `${emp.name} ${emp.department} ${emp.position}`.toLowerCase()
          const matches = kmpSearch(text, searchKeyword.value.toLowerCase())
          return matches.length > 0
        })
        break
        
      case 'binary':
        // 二分搜索（需要预先排序）
        const sortedEmployees = [...allEmployees.value].sort((a, b) => a.name.localeCompare(b.name))
        const index = binarySearch(sortedEmployees, searchKeyword.value, emp => emp.name)
        searchResults.value = index !== -1 ? [sortedEmployees[index]] : []
        break
    }
    
    const searchEnd = performance.now()
    searchTime.value = Math.round(searchEnd - searchStart)
    
    // 更新搜索性能统计
    searchPerformance.value = Math.max(0, Math.round((10 - searchTime.value) / 10 * 100))
    
  } finally {
    searching.value = false
  }
}

// 初始化数据
onMounted(async () => {
  // 生成测试数据
  testData.value = generateTestData(1000)
  candidateEmployees.value = generateTestData(50)
  allEmployees.value = generateTestData(500)
  
  // 初始化性能统计
  sortPerformance.value = 35
  searchPerformance.value = 42
  memoryOptimization.value = 28
})
</script>

<style scoped>
/* 自定义样式 */
.bg-primary {
  background-color: #3B82F6;
}

.text-primary {
  color: #3B82F6;
}

.border-primary {
  border-color: #3B82F6;
}

.hover\:bg-primary-dark:hover {
  background-color: #2563EB;
}

.focus\:ring-primary:focus {
  --tw-ring-color: #3B82F6;
}

.focus\:border-primary:focus {
  border-color: #3B82F6;
}
</style> 