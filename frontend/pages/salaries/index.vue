<template>
  <div class="space-y-6">
    <!-- 页面标题和操作栏 -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">薪资查询</h1>
        <p class="mt-1 text-sm text-gray-500">查看和管理员工薪资记录</p>
      </div>
      
      <!-- 计算薪资按钮 (仅管理员可见) -->
      <div class="mt-4 sm:mt-0">
        <NuxtLink
          v-if="isAdmin"
          to="/salaries/generate"
          class="animated-button"
        >
          <svg viewBox="0 0 24 24" class="arr-2" xmlns="http://www.w3.org/2000/svg">
            <path d="m16.172 11-5.364-5.364 1.414-1.414L20 12l-7.778 7.778-1.414-1.414L16.172 13H4v-2z"></path>
          </svg>
          <span class="text">计算并生成薪资</span>
          <span class="circle"></span>
          <svg viewBox="0 0 24 24" class="arr-1" xmlns="http://www.w3.org/2000/svg">
            <path d="m16.172 11-5.364-5.364 1.414-1.414L20 12l-7.778 7.778-1.414-1.414L16.172 13H4v-2z"></path>
          </svg>
        </NuxtLink>
      </div>
    </div>

    <!-- 搜索和筛选区域 -->
    <div class="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <!-- 员工搜索 -->
        <div>
          <label for="employee-search" class="block text-sm font-medium text-gray-700 mb-1">员工搜索</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Icon name="heroicons:magnifying-glass" class="h-5 w-5 text-gray-400" />
            </div>
            <input
              id="employee-search"
              v-model="searchQuery"
              type="text"
              placeholder="搜索姓名、工号..."
              class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary focus:border-primary"
              @input="debouncedSearch"
            />
          </div>
        </div>

        <!-- 部门筛选 -->
        <div>
          <label for="department" class="block text-sm font-medium text-gray-700 mb-1">部门</label>
          <select
            id="department"
            v-model="filters.department"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
            @change="applyFilters"
          >
            <option value="">全部部门</option>
            <option v-for="dept in departments" :key="dept" :value="dept">{{ dept }}</option>
          </select>
        </div>

        <!-- 薪资期间筛选 -->
        <div>
          <label for="salary-period" class="block text-sm font-medium text-gray-700 mb-1">薪资期间</label>
          <input
            id="salary-period"
            v-model="filters.salaryPeriod"
            type="month"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
            @change="applyFilters"
          />
        </div>

        <!-- 薪资范围筛选 -->
        <div>
          <label for="salary-range" class="block text-sm font-medium text-gray-700 mb-1">薪资范围</label>
          <select
            id="salary-range"
            v-model="filters.salaryRange"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
            @change="applyFilters"
          >
            <option value="">全部范围</option>
            <option value="0-5000">0-5000元</option>
            <option value="5000-10000">5000-10000元</option>
            <option value="10000-15000">10000-15000元</option>
            <option value="15000-20000">15000-20000元</option>
            <option value="20000+">20000元以上</option>
          </select>
        </div>
      </div>
    </div>

    <!-- 数据表格 -->
    <div class="bg-white shadow-sm rounded-lg border border-gray-200 overflow-hidden">
      <!-- 加载状态 -->
      <div v-if="loading" class="p-8 text-center">
        <div class="inline-flex items-center">
          <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-primary mr-3"></div>
          <span class="text-gray-600">加载中...</span>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else-if="!salaryRecords.length" class="p-8 text-center">
        <Icon name="heroicons:currency-dollar" class="mx-auto h-12 w-12 text-gray-400" />
        <h3 class="mt-2 text-sm font-medium text-gray-900">暂无薪资记录</h3>
        <p class="mt-1 text-sm text-gray-500">还没有生成任何薪资记录</p>
        <div class="mt-6" v-if="isAdmin">
          <NuxtLink
            to="/salaries/generate"
            class="animated-button"
          >
            <svg viewBox="0 0 24 24" class="arr-2" xmlns="http://www.w3.org/2000/svg">
              <path d="m16.172 11-5.364-5.364 1.414-1.414L20 12l-7.778 7.778-1.414-1.414L16.172 13H4v-2z"></path>
            </svg>
            <span class="text">计算并生成薪资</span>
            <span class="circle"></span>
            <svg viewBox="0 0 24 24" class="arr-1" xmlns="http://www.w3.org/2000/svg">
              <path d="m16.172 11-5.364-5.364 1.414-1.414L20 12l-7.778 7.778-1.414-1.414L16.172 13H4v-2z"></path>
            </svg>
          </NuxtLink>
        </div>
      </div>

      <!-- 表格内容 -->
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th
                v-for="column in tableColumns"
                :key="column.key"
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                :class="{ 'cursor-pointer hover:bg-gray-100': column.sortable }"
                @click.stop="column.sortable && toggleSort(column.key)"
              >
                <div class="flex items-center space-x-1">
                  <span>{{ column.label }}</span>
                  <Icon
                    v-if="column.sortable"
                    :name="getSortIcon(column.key)"
                    class="h-4 w-4 text-gray-400"
                  />
                </div>
              </th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                操作
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr
              v-for="record in salaryRecords"
              :key="record.id"
              class="hover:bg-gray-50 transition-colors"
            >
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {{ record.employee_name }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-mono">
                {{ record.employee_id }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ record.department }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatSalaryPeriod(record.salary_period) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ record.position_snapshot }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                ¥{{ formatCurrency(record.base_salary_snapshot || record.base_salary) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                ¥{{ formatCurrency(record.gross_salary || calculateGrossSalary(record)) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                <span class="text-green-600">+¥{{ formatCurrency(record.bonus || 0) }}</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                <span class="text-red-600">-¥{{ formatCurrency(record.deductions || 0) }}</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-900">
                ¥{{ formatCurrency(record.net_salary || calculateNetSalary(record)) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(record.pay_date) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div class="flex items-center justify-end space-x-2">
                  <!-- 查看详情 -->
                  <button
                    @click="viewSalaryDetail(record)"
                    class="text-primary hover:text-primary-dark transition-colors"
                    title="查看详情"
                  >
                    <Icon name="heroicons:eye" class="h-4 w-4" />
                  </button>
                  
                  <!-- 打印 -->
                  <button
                    @click="printSalary(record)"
                    class="text-gray-600 hover:text-gray-800 transition-colors"
                    title="打印"
                  >
                    <Icon name="heroicons:printer" class="h-4 w-4" />
                  </button>
                  
                  <!-- 编辑 (仅管理员) -->
                  <button
                    v-if="isAdmin"
                    @click="editSalaryRecord(record)"
                    class="text-accent hover:text-accent-dark transition-colors"
                    title="编辑"
                  >
                    <Icon name="heroicons:pencil" class="h-4 w-4" />
                  </button>
                  
                  <!-- 删除 (仅管理员) -->
                  <button
                    v-if="isAdmin"
                    @click="confirmDeleteSalary(record)"
                    class="text-danger hover:text-red-700 transition-colors"
                    title="删除"
                  >
                    <Icon name="heroicons:trash" class="h-4 w-4" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 分页 -->
      <div v-if="pagination.totalPages > 1" class="bg-white px-4 py-3 border-t border-gray-200 sm:px-6">
        <div class="flex items-center justify-between">
          <div class="flex-1 flex justify-between sm:hidden">
            <button
              @click="changePage(pagination.currentPage - 1)"
              :disabled="pagination.currentPage <= 1"
              class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              上一页
            </button>
            <button
              @click="changePage(pagination.currentPage + 1)"
              :disabled="pagination.currentPage >= pagination.totalPages"
              class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              下一页
            </button>
          </div>
          <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p class="text-sm text-gray-700">
                显示第
                <span class="font-medium">{{ (pagination.currentPage - 1) * pagination.pageSize + 1 }}</span>
                到
                <span class="font-medium">{{ Math.min(pagination.currentPage * pagination.pageSize, pagination.totalItems) }}</span>
                条，共
                <span class="font-medium">{{ pagination.totalItems }}</span>
                条记录
              </p>
            </div>
            <div>
              <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
                <button
                  @click="changePage(pagination.currentPage - 1)"
                  :disabled="pagination.currentPage <= 1"
                  class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Icon name="heroicons:chevron-left" class="h-5 w-5" />
                </button>
                
                <template v-for="page in visiblePages" :key="page">
                  <span
                    v-if="page === '...'"
                    class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700"
                  >
                    ...
                  </span>
                  <button
                    v-else
                    @click="changePage(page)"
                    :class="[
                      'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                      page === pagination.currentPage
                        ? 'z-10 bg-primary border-primary text-white'
                        : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
                    ]"
                  >
                    {{ page }}
                  </button>
                </template>
                
                <button
                  @click="changePage(pagination.currentPage + 1)"
                  :disabled="pagination.currentPage >= pagination.totalPages"
                  class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Icon name="heroicons:chevron-right" class="h-5 w-5" />
                </button>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 计算薪资模态框 -->
    <div
      v-if="showCalculateModal"
      class="fixed inset-0 z-50 overflow-y-auto"
      @click.self="closeCalculateModal"
    >
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
        
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <form @submit.prevent="calculateSalary">
            <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
              <div class="sm:flex sm:items-start">
                <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-accent-light sm:mx-0 sm:h-10 sm:w-10">
                  <Icon name="heroicons:calculator" class="h-6 w-6 text-accent-dark" />
                </div>
                <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
                  <h3 class="text-lg leading-6 font-medium text-gray-900">计算并生成薪资</h3>
                  <div class="mt-4 space-y-4">
                    <!-- 员工选择 -->
                    <div>
                      <label for="calc-employee" class="block text-sm font-medium text-gray-700 mb-1">选择员工</label>
                      <select
                        id="calc-employee"
                        v-model="calculateForm.employeeId"
                        class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-accent focus:border-accent"
                      >
                        <option value="">为所有员工计算薪资</option>
                        <option v-for="emp in employees" :key="emp.id" :value="emp.id">
                          {{ emp.name }} ({{ emp.employee_id }})
                        </option>
                      </select>
                      <p class="mt-1 text-sm text-gray-500">留空将为所有员工计算薪资</p>
                    </div>

                    <!-- 薪资期间 -->
                    <div>
                      <label for="calc-period" class="block text-sm font-medium text-gray-700 mb-1">薪资期间</label>
                      <input
                        id="calc-period"
                        v-model="calculateForm.salaryPeriod"
                        type="month"
                        required
                        class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-accent focus:border-accent"
                      />
                    </div>

                    <!-- 奖金 -->
                    <div>
                      <label for="calc-bonus" class="block text-sm font-medium text-gray-700 mb-1">奖金</label>
                      <div class="relative">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                          <span class="text-gray-500 sm:text-sm">¥</span>
                        </div>
                        <input
                          id="calc-bonus"
                          v-model.number="calculateForm.bonus"
                          type="number"
                          step="0.01"
                          min="0"
                          class="block w-full pl-8 pr-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-accent focus:border-accent"
                          placeholder="0.00"
                        />
                      </div>
                    </div>

                    <!-- 扣除 -->
                    <div>
                      <label for="calc-deduction" class="block text-sm font-medium text-gray-700 mb-1">扣除</label>
                      <div class="relative">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                          <span class="text-gray-500 sm:text-sm">¥</span>
                        </div>
                        <input
                          id="calc-deduction"
                          v-model.number="calculateForm.deductions"
                          type="number"
                          step="0.01"
                          min="0"
                          class="block w-full pl-8 pr-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-accent focus:border-accent"
                          placeholder="0.00"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
              <button
                type="submit"
                :disabled="calculating"
                class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-accent text-base font-medium text-white hover:bg-accent-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <div v-if="calculating" class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                {{ calculating ? '计算中...' : '计算并生成' }}
              </button>
              <button
                type="button"
                @click="closeCalculateModal"
                :disabled="calculating"
                class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                取消
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- 详情模态框 -->
    <div v-if="showDetailModal" class="fixed inset-0 z-50 overflow-y-auto" @click.self="showDetailModal = false">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75"></div>
        <div class="inline-block bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:max-w-lg sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">薪资详情</h3>
            <pre class="whitespace-pre-wrap text-sm text-gray-700">{{ JSON.stringify(selectedRecord, null, 2) }}</pre>
          </div>
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button @click="showDetailModal = false" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">关闭</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 编辑模态框 -->
    <div v-if="showEditModal" class="fixed inset-0 z-50 overflow-y-auto" @click.self="showEditModal = false">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75"></div>
        <div class="inline-block bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:max-w-md sm:w-full">
          <form @submit.prevent="submitEditSalary">
            <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4 space-y-4">
              <h3 class="text-lg leading-6 font-medium text-gray-900">编辑薪资记录</h3>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">奖金</label>
                <input v-model.number="editForm.bonus" type="number" step="0.01" min="0" class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-accent focus:border-accent" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">扣除</label>
                <input v-model.number="editForm.deductions" type="number" step="0.01" min="0" class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-accent focus:border-accent" />
              </div>
            </div>
            <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
              <button type="submit" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-accent text-base font-medium text-white hover:bg-accent-dark sm:ml-3 sm:w-auto sm:text-sm">保存</button>
              <button type="button" @click="showEditModal = false" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">取消</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- 删除确认模态框 -->
    <div v-if="confirmDeleteModal" class="fixed inset-0 z-50 overflow-y-auto" @click.self="confirmDeleteModal = false">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75"></div>
        <div class="inline-block bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:max-w-sm sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-2">确认删除</h3>
            <p class="text-sm text-gray-700">确定要删除该薪资记录吗？此操作无法撤销。</p>
          </div>
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button @click="deleteSalaryRecord" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-danger text-base font-medium text-white hover:bg-red-700 sm:ml-3 sm:w-auto sm:text-sm">删除</button>
            <button @click="confirmDeleteModal = false" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">取消</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue'

// --- 页面元数据 ---
// 为页面设置 'default' 布局，这通常意味着它会包含网站的通用页眉、页脚和导航。
definePageMeta({
  layout: 'default'
})

// --- API 组合式函数 ---
// 引入封装好的 API 调用逻辑。这种方式使得组件更专注于视图和状态管理，
// 而将数据获取的细节（如端点、头部信息等）抽象出去，提高了代码的可维护性和复用性。
const salaryApi = useSalaryApi()
const employeeApi = useEmployeeApi()
const departmentApi = useDepartmentApi()

// --- 响应式状态 ---
// UI 状态
const loading = ref(false) // 控制表格加载状态的显示，在数据获取期间向用户提供反馈。
const calculating = ref(false) // 控制计算薪资模态框中提交按钮的状态，防止重复提交。
const showCalculateModal = ref(false) // 控制计算薪资模态框的可见性。
const showDetailModal = ref(false) // 控制薪资详情模态框的可见性。
const showEditModal = ref(false) // 控制编辑薪资模态框的可见性。
const confirmDeleteModal = ref(false) // 控制删除确认模态框的可见性。
const selectedRecord = ref(null) // 存储用户当前选中操作的薪资记录。

// 搜索与筛选
const searchQuery = ref('') // 绑定搜索输入框的值。
const filters = ref({ // 存储筛选条件。这些条件将作为参数发送到后端进行数据过滤。
  department: '',
  salaryPeriod: '',
  salaryRange: ''
})

// 排序
const sort = ref({ // 存储排序字段和方向，同样会发送到后端。
  field: '',
  direction: 'asc'
})

// 分页
// 与员工页面不同，薪资记录可能非常多，因此采用后端分页是更高效的策略。
// 前端只负责维护当前页码、每页大小，并将这些信息发送给后端。
const pagination = ref({
  currentPage: 1,
  pageSize: 20,
  totalItems: 0,
  totalPages: 0
})

// 表单数据
// 使用 reactive 来创建响应式对象，适用于管理一组相关的表单字段。
const calculateForm = reactive({
  employeeId: '',
  salaryPeriod: '',
  bonus: 0,
  deductions: 0
})
const editForm = reactive({
  bonus: 0,
  deductions: 0
})

// 核心数据
const salaryRecords = ref([]) // 存储从后端获取的当前页的薪资记录。
const employees = ref([]) // 存储员工列表，用于"计算薪资"模态框的下拉选择。
const departments = ref([]) // 存储部门列表，用于筛选。

// 权限控制
// 在实际应用中，此值应从用户状态管理（如 Pinia/Vuex）中获取。
// 这里硬编码为 true 是为了方便开发和演示。
const isAdmin = ref(true)

// 表格列定义
// 将列配置抽离出来，使模板更简洁，并且方便动态修改列（例如根据权限显示/隐藏列）。
const tableColumns = [
  { key: 'employee_name', label: '员工姓名', sortable: true },
  { key: 'employee_id', label: '工号', sortable: true },
  { key: 'department', label: '部门', sortable: true },
  { key: 'salary_period', label: '薪资期间', sortable: true },
  { key: 'position_snapshot', label: '职称', sortable: false },
  { key: 'base_salary_snapshot', label: '基础工资', sortable: true },
  { key: 'gross_salary', label: '应发工资', sortable: true },
  { key: 'bonus', label: '奖金', sortable: true },
  { key: 'deductions', label: '扣除', sortable: true },
  { key: 'net_salary', label: '实发工资', sortable: true },
  { key: 'pay_date', label: '发放日期', sortable: true }
]

// --- 计算属性 ---
/**
 * @description 计算分页导航中应显示的页码。
 * 当页数过多时，此逻辑可以生成一个紧凑且用户友好的分页控件（如 "1 ... 5 6 7 ... 12"），
 * 而不是将所有页码都列出来，从而改善了大规模数据下的用户体验。
 */
const visiblePages = computed(() => {
  const pages = []
  const total = pagination.value.totalPages
  const current = pagination.value.currentPage
  
  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i);
  } else {
    if (current <= 4) {
      for (let i = 1; i <= 5; i++) pages.push(i);
      pages.push('...');
      pages.push(total);
    } else if (current >= total - 3) {
      pages.push(1);
      pages.push('...');
      for (let i = Math.max(total - 4, 1); i <= total; i++) pages.push(i);
    } else {
      pages.push(1);
      pages.push('...');
      for (let i = current - 1; i <= current + 1; i++) pages.push(i);
      pages.push('...');
      pages.push(total);
    }
  }
  
  return pages.filter((val, index, self) => self.indexOf(val) === index); // 移除可能的重复项
})

// --- 方法 ---

/**
 * @description 核心函数：从后端加载薪资记录。
 * 它构建API请求参数，包括分页、排序和筛选条件。
 * 这是后端分页和筛选策略的典型实现。
 */
const loadSalaryRecords = async () => {
  loading.value = true
  try {
    const apiParams = {
      page: pagination.value.currentPage,
      page_size: pagination.value.pageSize,
      search: searchQuery.value,
      department: filters.value.department,
      salary_period: filters.value.salaryPeriod,
    }
    // 将薪资范围 "5000-10000" 转换为 min_salary 和 max_salary 参数
    if (filters.value.salaryRange) {
      const range = filters.value.salaryRange
      if (range.includes('-')) {
        const [min, max] = range.split('-')
        if (min) apiParams.min_salary = min
        if (max) apiParams.max_salary = max
      } else if (range.endsWith('+')) {
        apiParams.min_salary = range.replace('+', '')
      }
    }
    // 添加排序参数
    if (sort.value.field) {
      apiParams.ordering = sort.value.direction === 'asc' ? sort.value.field : `-${sort.value.field}`
    }
    
    // 移除所有空值的参数，保持请求的整洁性
    Object.keys(apiParams).forEach(key => {
      if (apiParams[key] === '' || apiParams[key] === null || apiParams[key] === undefined) {
        delete apiParams[key]
      }
    });

    const response = await salaryApi.getSalaries(apiParams)
    if (response && response.results) {
      salaryRecords.value = response.results
      pagination.value.totalItems = response.count || response.results.length
      pagination.value.totalPages = Math.ceil(pagination.value.totalItems / pagination.value.pageSize)
    } else {
      // 在API响应无效时，重置数据状态，避免UI显示旧数据
      salaryRecords.value = []
      pagination.value.totalItems = 0
      pagination.value.totalPages = 0
    }
  } catch (error) {
    console.error('加载薪资记录失败:', error)
    salaryRecords.value = []
    pagination.value.totalItems = 0
    pagination.value.totalPages = 0
  } finally {
    loading.value = false
  }
}

/**
 * @description 加载员工列表，用于"计算薪资"模态框中的下拉选项。
 */
const loadEmployees = async () => {
  try {
    // 这里获取所有员工，因为下拉列表通常需要完整数据。
    const response = await employeeApi.getEmployees({ page_size: 1000 })
    if (response && response.results) {
      employees.value = response.results.map(emp => ({
        id: emp.id,
        name: emp.name,
        employee_id: emp.employee_id
      }))
    }
  } catch (error) {
    console.error('加载员工列表失败:', error)
  }
}

/**
 * @description 加载部门列表，用于筛选下拉选项。
 */
const loadDepartments = async () => {
  try {
    const response = await departmentApi.getDepartments()
    if (response && response.results) {
      departments.value = response.results.map(dept => dept.name)
    }
  } catch (error) {
    console.error('加载部门列表失败:', error)
  }
}

/**
 * @description 防抖处理的搜索函数。
 * 使用防抖可以防止用户在快速输入时频繁触发API请求，
 * 只有在用户停止输入一段时间（300毫秒）后才执行搜索，
 * 极大地优化了性能并减少了服务器负载。
 */
const debouncedSearch = debounce(() => {
  applyFilters()
}, 300)

/**
 * @description 应用筛选条件并重新加载数据。
 */
const applyFilters = () => {
  pagination.value.currentPage = 1; // 筛选条件改变时，应回到第一页
  console.log('应用筛选:', { searchQuery: searchQuery.value, filters: filters.value })
  loadSalaryRecords()
}

/**
 * @description 切换排序并重新加载数据。
 */
const toggleSort = (field) => {
  if (sort.value.field === field) {
    sort.value.direction = sort.value.direction === 'asc' ? 'desc' : 'asc'
  } else {
    sort.value.field = field
    sort.value.direction = 'asc'
  }
  loadSalaryRecords()
}

/**
 * @description 获取排序图标，为用户提供视觉反馈。
 */
const getSortIcon = (field) => {
  if (sort.value.field !== field) {
    return 'heroicons:chevron-up-down'
  }
  return sort.value.direction === 'asc' ? 'heroicons:chevron-up' : 'heroicons:chevron-down'
}

/**
 * @description 切换分页。
 */
const changePage = (page) => {
  if (page >= 1 && page <= pagination.value.totalPages) {
    pagination.value.currentPage = page
    loadSalaryRecords()
  }
}

/**
 * @description 显示薪资详情模态框。
 */
const viewSalaryDetail = (record) => {
  selectedRecord.value = record
  showDetailModal.value = true
}

/**
 * @description 打印薪资条。
 * 这是一个简单的实现，通过打开一个新窗口并调用浏览器的打印功能。
 * 在实际应用中，这里可以渲染一个更专业、格式化的薪资条模板。
 */
const printSalary = (record) => {
  const printWindow = window.open('', '_blank')
  printWindow.document.write(`<pre>${JSON.stringify(record, null, 2)}</pre>`)  
  printWindow.document.close()
  printWindow.focus()
  printWindow.print()
  printWindow.close()
}

/**
 * @description 打开编辑模态框并填充当前记录的数据。
 */
const editSalaryRecord = (record) => {
  selectedRecord.value = record
  editForm.bonus = Number(record.bonus || 0)
  editForm.deductions = Number(record.deductions || 0)
  showEditModal.value = true
}

/**
 * @description 提交编辑后的薪资数据。
 */
const submitEditSalary = async () => {
  try {
    const payload = {
      bonus: editForm.bonus,
      deductions: editForm.deductions
    }
    const res = await salaryApi.updateSalary(selectedRecord.value.id, payload)
    if (res && res.success !== false) {
      await loadSalaryRecords() // 成功后刷新数据
      showEditModal.value = false
    }
  } catch (err) {
    console.error('更新薪资记录失败:', err)
  }
}

/**
 * @description 显示删除确认模态框，防止用户误操作。
 */
const confirmDeleteSalary = (record) => {
  selectedRecord.value = record
  confirmDeleteModal.value = true
}

/**
 * @description 执行删除操作。
 */
const deleteSalaryRecord = async () => {
  try {
    const res = await salaryApi.deleteSalary(selectedRecord.value.id)
    if (res && res.success !== false) {
      await loadSalaryRecords() // 成功后刷新数据
      confirmDeleteModal.value = false
    }
  } catch (err) {
    console.error('删除薪资记录失败:', err)
}
}

/**
 * @description 关闭计算薪资模态框并重置表单。
 */
const closeCalculateModal = () => {
  showCalculateModal.value = false
  Object.assign(calculateForm, {
    employeeId: '',
    salaryPeriod: '',
    bonus: 0,
    deductions: 0
  })
}

/**
 * @description 核心业务逻辑：计算和生成薪资。
 * 此函数处理两种情况：为单个员工或为所有员工生成薪资记录。
 * 这是通过检查 `calculateForm.employeeId` 是否有值来区分的。
 */
const calculateSalary = async () => {
  calculating.value = true
  try {
    console.log('计算薪资:', calculateForm)
    
    const salaryData = {
      salary_period: calculateForm.salaryPeriod,
      bonus: calculateForm.bonus || 0,
      deduction: calculateForm.deductions || 0
    }
    
    let response
    if (calculateForm.employeeId) {
      // 为单个员工计算薪资
      response = await salaryApi.calculateSalary(calculateForm.employeeId, salaryData)
    } else {
      // 为所有员工批量生成薪资
      response = await salaryApi.generateSalaries(salaryData)
    }
    
    if (response.success || response.data) {
      await loadSalaryRecords() // 成功后刷新列表
      closeCalculateModal()
      console.log('薪资计算完成')
    } else {
      console.error('薪资计算失败:', response.error)
      // 可以在此处添加用户友好的错误提示
    }
  } catch (error) {
    console.error('计算薪资失败:', error)
  } finally {
    calculating.value = false
  }
}

// --- 格式化辅助函数 ---

/**
 * @description 格式化货币值。
 * 统一处理了 null、undefined 和 NaN 等无效输入，确保UI显示的健壮性。
 */
const formatCurrency = (amount) => {
  if (amount === null || amount === undefined || isNaN(amount)) {
    return '0.00'
  }
  const numAmount = Number(amount)
  if (isNaN(numAmount)) {
    return '0.00'
  }
  return new Intl.NumberFormat('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(numAmount)
}

/**
 * @description 格式化日期。
 */
const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('zh-CN')
}

/**
 * @description 格式化薪资期间（例如 '2024-05' -> '2024年05月'）。
 */
const formatSalaryPeriod = (period) => {
  if (!period) return ''
  const [year, month] = period.split('-')
  return `${year}年${month}月`
}

// --- 客户端计算 ---
// 这些函数用于在前端动态计算一些值，当API没有直接返回这些字段时非常有用。
// 它们可以减轻后端的计算压力，并使前端展示更灵活。

const calculateGrossSalary = (record) => {
  const baseSalary = Number(record.base_salary_snapshot || record.base_salary || 0)
  const bonus = Number(record.bonus || 0)
  return baseSalary + bonus
}

const calculateNetSalary = (record) => {
  const grossSalary = record.gross_salary || calculateGrossSalary(record)
  const deductions = Number(record.deductions || 0)
  return Number(grossSalary) - deductions
}

// --- 工具函数 ---
/**
 * @description 一个通用的防抖函数。
 * @param {Function} func - 需要防抖的函数。
 * @param {number} wait - 延迟时间（毫秒）。
 */
function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

// --- 生命周期钩子 ---
/**
 * @description 组件挂载后执行初始化操作。
 * 包括开发环境下的自动登录和加载初始数据。
 * 将默认的薪资期间设置为当前月份，提升了用户体验。
 */
onMounted(() => {
  if (process.client) {
    const existingToken = localStorage.getItem('auth_token');
    if (!existingToken) {
      // 方便开发，自动登录
      $fetch('/api/auth/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: { username: 'admin', password: 'admin123' }
      }).then(loginResponse => {
        if (loginResponse?.success && loginResponse.data?.token) {
          localStorage.setItem('auth_token', loginResponse.data.token);
          localStorage.setItem('user_info', JSON.stringify(loginResponse.data.user));
          console.log('Auto-login successful in salaries page');
          loadSalaryRecords();
          loadEmployees();
          loadDepartments();
        }
      }).catch(err => {
        console.error('Auto-login failed in salaries page:', err);
        // 即使登录失败，也尝试加载数据，因为某些数据可能是公开的
        loadSalaryRecords();
        loadEmployees();
        loadDepartments();
      });
    } else {
      loadSalaryRecords();
      loadEmployees();
      loadDepartments();
    }
  }
  
  // 将计算薪资表单的默认期间设置为当前月份，方便用户操作。
  const now = new Date()
  calculateForm.salaryPeriod = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
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
  border: 4px solid #3b83f659;
  border-color: #3b82f6;
  font-size: 16px;
  background-color: #3b83f6;
  border-radius: 100px;
  font-weight: 600;
  color: white;
  box-shadow: 0 0 0 2px #3b83f665;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.6s cubic-bezier(0.23, 1, 0.32, 1);
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

.animated-button:hover {
  box-shadow: 0 0 0 12px transparent;
  color: black;
  border-radius: 12px;
}

.animated-button:hover .arr-1 {
  right: -25%;
}

.animated-button:hover .arr-2 {
  left: 16px;
}

.animated-button:hover .text {
  transform: translateX(12px);
}

.animated-button:hover svg {
  fill: #212121;
}

.animated-button:active {
  scale: 0.95;
  box-shadow: 0 0 0 4px white;
}

.animated-button:hover .circle {
  width: 220px;
  height: 220px;
  opacity: 1;
}
</style> 