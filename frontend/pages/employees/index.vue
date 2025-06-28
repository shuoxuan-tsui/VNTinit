<template>
  <div class="space-y-6">
    <!-- 页面标题和操作栏 -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">员工管理</h1>
        <p class="mt-2 text-sm text-gray-600">管理公司员工信息，共 {{ totalServerEmployees }} 名员工</p>
      </div>
      
      <!-- 添加员工按钮 (仅管理员可见) -->
      <div class="mt-4 sm:mt-0 flex space-x-3">
        <button
          @click="exportEmployees"
          class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-all duration-200 shadow-sm"
        >
          <Icon name="heroicons:arrow-down-tray" class="mr-2 h-4 w-4" />
          导出
        </button>
        <NuxtLink
          v-if="isAdmin"
          to="/employees/add"
          class="animated-button"
        >
          <svg viewBox="0 0 24 24" class="arr-2" xmlns="http://www.w3.org/2000/svg">
            <path d="m16.172 11-5.364-5.364 1.414-1.414L20 12l-7.778 7.778-1.414-1.414L16.172 13H4v-2z"></path>
          </svg>
          <span class="text">添加员工</span>
          <span class="circle"></span>
          <svg viewBox="0 0 24 24" class="arr-1" xmlns="http://www.w3.org/2000/svg">
            <path d="m16.172 11-5.364-5.364 1.414-1.414L20 12l-7.778 7.778-1.414-1.414L16.172 13H4v-2z"></path>
          </svg>
        </NuxtLink>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <Icon name="heroicons:users" class="h-6 w-6 text-gray-400" />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">总员工数</dt>
                <dd class="text-lg font-medium text-gray-900">{{ totalServerEmployees }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <Icon name="heroicons:building-office" class="h-6 w-6 text-blue-400" />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">部门数量</dt>
                <dd class="text-lg font-medium text-gray-900">{{ uniqueDepartments.length }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <Icon name="heroicons:user-plus" class="h-6 w-6 text-green-400" />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">本月新入职</dt>
                <dd class="text-lg font-medium text-gray-900">{{ newEmployeesThisMonth }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <Icon name="heroicons:chart-bar" class="h-6 w-6 text-purple-400" />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">平均薪资</dt>
                <dd class="text-lg font-medium text-gray-900">¥{{ averageSalary.toLocaleString() }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 搜索和筛选区域 -->
    <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
        <!-- 搜索框 -->
        <div class="lg:col-span-2">
          <label for="search" class="block text-sm font-medium text-gray-700 mb-2">搜索员工</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Icon name="heroicons:magnifying-glass" class="h-5 w-5 text-gray-400" />
            </div>
            <input
              id="search"
              v-model="searchQuery"
              type="text"
              placeholder="搜索姓名、工号、电话..."
              class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary focus:border-primary sm:text-sm"
            />
            <div v-if="searchQuery" class="absolute inset-y-0 right-0 pr-3 flex items-center">
              <button @click="clearSearch" class="text-gray-400 hover:text-gray-600">
                <Icon name="heroicons:x-mark" class="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>

        <!-- 部门筛选 -->
        <div>
          <label for="department" class="block text-sm font-medium text-gray-700 mb-2">部门</label>
          <select
            id="department"
            v-model="filters.department"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
          >
            <option value="">全部部门</option>
            <option v-for="dept in uniqueDepartments" :key="dept" :value="dept">{{ dept }}</option>
          </select>
        </div>

        <!-- 职称筛选 -->
        <div>
          <label for="position" class="block text-sm font-medium text-gray-700 mb-2">职称</label>
          <select
            id="position"
            v-model="filters.position"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
          >
            <option value="">全部职称</option>
            <option v-for="pos in uniquePositions" :key="pos" :value="pos">{{ pos }}</option>
          </select>
        </div>
      </div>

      <!-- 高级筛选 -->
      <div v-if="showAdvancedFilters" class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t border-gray-200">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">性别</label>
          <select v-model="filters.gender" class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm">
            <option value="">全部</option>
            <option value="M">男</option>
            <option value="F">女</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">入职年份</label>
          <select v-model="filters.hireYear" class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm">
            <option value="">全部年份</option>
            <option v-for="year in uniqueHireYears" :key="year" :value="year">{{ year }}年</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">薪资范围</label>
          <select v-model="filters.salaryRange" class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm">
            <option value="">全部范围</option>
            <option value="0-5000">5000以下</option>
            <option value="5000-10000">5000-10000</option>
            <option value="10000-15000">10000-15000</option>
            <option value="15000-20000">15000-20000</option>
            <option value="20000+">20000以上</option>
          </select>
        </div>
      </div>

      <!-- 筛选操作按钮 -->
      <div class="flex items-center justify-between mt-4">
        <button
          @click="showAdvancedFilters = !showAdvancedFilters"
          class="text-sm text-primary hover:text-primary-dark font-medium"
        >
          {{ showAdvancedFilters ? '收起高级筛选' : '展开高级筛选' }}
          <Icon :name="showAdvancedFilters ? 'heroicons:chevron-up' : 'heroicons:chevron-down'" class="ml-1 h-4 w-4 inline" />
        </button>
        <div class="flex space-x-2">
          <button
            @click="clearFilters"
            class="px-3 py-1 text-sm text-gray-600 hover:text-gray-800"
          >
            清空筛选
          </button>
          <span class="text-sm text-gray-500">
            显示 {{ filteredEmployees.length }} / {{ totalServerEmployees }} 条记录
          </span>
        </div>
      </div>
    </div>

    <!-- 数据表格 -->
    <div class="bg-white shadow-sm rounded-lg border border-gray-200 overflow-hidden">
      <!-- 加载状态 -->
      <div v-if="loading" class="p-12 text-center">
        <div class="inline-flex items-center">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mr-3"></div>
          <span class="text-gray-600 text-lg">加载中，请稍候...</span>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else-if="!filteredEmployees.length && !loading" class="p-12 text-center">
        <Icon name="heroicons:users" class="mx-auto h-16 w-16 text-gray-400" />
        <h3 class="mt-4 text-lg font-medium text-gray-900">
          {{ searchQuery || Object.values(filters).some(v => v) ? '未找到匹配的员工' : '暂无员工信息' }}
        </h3>
        <p class="mt-2 text-sm text-gray-500">
          {{ searchQuery || Object.values(filters).some(v => v) ? '请尝试调整搜索条件' : '开始添加第一个员工吧' }}
        </p>
        <div class="mt-6">
          <button
            v-if="searchQuery || Object.values(filters).some(v => v)"
            @click="clearFilters"
            class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary mr-3"
          >
            清空筛选
          </button>
          <NuxtLink
            v-if="isAdmin"
            to="/employees/add"
            class="animated-button"
          >
            <svg viewBox="0 0 24 24" class="arr-2" xmlns="http://www.w3.org/2000/svg">
              <path d="m16.172 11-5.364-5.364 1.414-1.414L20 12l-7.778 7.778-1.414-1.414L16.172 13H4v-2z"></path>
            </svg>
            <span class="text">添加员工</span>
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
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
                @click="column.sortable && toggleSort(column.key)"
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
              v-for="employee in paginatedEmployees"
              :key="employee.id"
              class="hover:bg-gray-50 transition-colors"
            >
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {{ employee.employee_id }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-10 w-10">
                    <div class="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center">
                      <span class="text-sm font-medium text-gray-700">{{ employee.name.charAt(0) }}</span>
                    </div>
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">{{ employee.name }}</div>
                    <div class="text-sm text-gray-500">{{ employee.phone }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium" :class="employee.gender === 'M' ? 'bg-blue-100 text-blue-800' : 'bg-pink-100 text-pink-800'">
                  {{ employee.gender === 'M' ? '男' : '女' }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  {{ employee.department }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ employee.position }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(employee.hire_date) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <span :class="getEmployeeStatusClass(employee.status)">
                  {{ formatEmployeeStatus(employee.status) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ employee.location }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                ¥{{ employee.base_salary?.toLocaleString() || '未设置' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div class="flex items-center justify-end space-x-2">
                  <!-- 查看详情 -->
                  <button
                    @click="viewEmployee(employee)"
                    class="text-primary hover:text-primary-dark transition-colors p-1 rounded"
                    title="查看详情"
                  >
                    <Icon name="heroicons:eye" class="h-4 w-4" />
                  </button>
                  
                  <!-- 快速编辑 (仅管理员) -->
                  <button
                    v-if="isAdmin"
                    @click="openEditModal(employee)"
                    class="text-accent hover:text-accent-dark transition-colors p-1 rounded"
                    title="快速编辑"
                  >
                    <Icon name="heroicons:pencil" class="h-4 w-4" />
                  </button>
                  
                  <!-- 详细编辑 (仅管理员) -->
                  <NuxtLink
                    v-if="isAdmin"
                    :to="`/employees/edit/${employee.id}`"
                    class="text-blue-600 hover:text-blue-800 transition-colors p-1 rounded"
                    title="详细编辑"
                  >
                    <Icon name="heroicons:cog-6-tooth" class="h-4 w-4" />
                  </NuxtLink>
                  
                  <!-- 删除 (仅管理员) -->
                  <button
                    v-if="isAdmin"
                    @click="confirmDelete(employee)"
                    class="text-danger hover:text-red-700 transition-colors p-1 rounded"
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
      <div v-if="totalPages > 1 && !loading" class="bg-white px-4 py-3 border-t border-gray-200 sm:px-6">
        <div class="flex items-center justify-between">
          <div class="flex-1 flex justify-between sm:hidden">
            <button
              @click="changePage(currentPage - 1)"
              :disabled="currentPage <= 1"
              class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              上一页
            </button>
            <button
              @click="changePage(currentPage + 1)"
              :disabled="currentPage >= totalPages"
              class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              下一页
            </button>
          </div>
          <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p class="text-sm text-gray-700">
                显示第
                <span class="font-medium">{{ (currentPage - 1) * pageSize + 1 }}</span>
                到
                <span class="font-medium">{{ Math.min(currentPage * pageSize, filteredEmployees.length) }}</span>
                条，共
                <span class="font-medium">{{ filteredEmployees.length }}</span>
                条记录
                <span v-if="filteredEmployees.length !== totalServerEmployees">(总 {{ totalServerEmployees }} 条)</span>
              </p>
            </div>
            <div>
              <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
                <button
                  @click="changePage(currentPage - 1)"
                  :disabled="currentPage <= 1"
                  class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Icon name="heroicons:chevron-left" class="h-5 w-5" />
                </button>
                
                <button
                  v-for="page in visiblePages"
                  :key="page"
                  @click="changePage(page)"
                  :class="[
                    'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                    page === currentPage
                      ? 'z-10 bg-primary border-primary text-white'
                      : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
                  ]"
                >
                  {{ page }}
                </button>
                
                <button
                  @click="changePage(currentPage + 1)"
                  :disabled="currentPage >= totalPages"
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

    <!-- 删除确认模态框 -->
    <div
      v-if="showDeleteModal"
      class="fixed inset-0 z-50 overflow-y-auto"
      @click.self="closeDeleteModal"
    >
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
        
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10">
                <Icon name="heroicons:exclamation-triangle" class="h-6 w-6 text-red-600" />
              </div>
              <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                <h3 class="text-lg leading-6 font-medium text-gray-900">确认删除员工</h3>
                <div class="mt-2">
                  <p class="text-sm text-gray-500">
                    您确定要删除员工 <strong>{{ employeeToDelete?.name }}</strong> (工号: {{ employeeToDelete?.employee_id }}) 吗？
                    此操作不可撤销。
                  </p>
                </div>
              </div>
            </div>
          </div>
          <!-- set the button to disabled to prevent the user from click it again -->
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              @click="deleteEmployeeAction"
              :disabled="deleting"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-red-600 text-base font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <div v-if="deleting" class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              {{ deleting ? '删除中...' : '确认删除' }}
            </button>
            <button
              @click="closeDeleteModal"
              :disabled="deleting"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed"
            >
              取消
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 快速编辑模态框 -->
    <div
      v-if="showEditModal"
      class="fixed inset-0 z-50 overflow-y-auto"
      @click.self="closeEditModal"
    >
      <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
        
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="mt-3 text-center sm:mt-0 sm:text-left w-full">
                <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">快速编辑员工信息</h3>
                
                <form @submit.prevent="updateEmployeeAction" class="space-y-4">
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <!-- 姓名 -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">姓名 *</label>
                      <input
                        v-model="editForm.name"
                        type="text"
                        class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                        :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500': editErrors.name }"
                      />
                      <p v-if="editErrors.name" class="mt-1 text-sm text-red-600">{{ editErrors.name }}</p>
                    </div>

                    <!-- 工号 -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">工号 *</label>
                      <input
                        v-model="editForm.employee_id"
                        type="text"
                        class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                        :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500': editErrors.employee_id }"
                      />
                      <p v-if="editErrors.employee_id" class="mt-1 text-sm text-red-600">{{ editErrors.employee_id }}</p>
                    </div>

                    <!-- 性别 -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">性别 *</label>
                      <select
                        v-model="editForm.gender"
                        class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                        :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500': editErrors.gender }"
                      >
                        <option value="">请选择性别</option>
                        <option value="M">男</option>
                        <option value="F">女</option>
                      </select>
                      <p v-if="editErrors.gender" class="mt-1 text-sm text-red-600">{{ editErrors.gender }}</p>
                    </div>

                    <!-- 电话 -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">电话号码 *</label>
                      <input
                        v-model="editForm.phone"
                        type="tel"
                        class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                        :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500': editErrors.phone }"
                      />
                      <p v-if="editErrors.phone" class="mt-1 text-sm text-red-600">{{ editErrors.phone }}</p>
                    </div>

                    <!-- 部门 -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">部门 *</label>
                      <select
                        v-model="editForm.department_ref"
                        class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                        :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500': editErrors.department }"
                      >
                        <option value="">请选择部门</option>
                        <option v-for="dept in departments" :key="dept.id" :value="dept.id">{{ dept.name }}</option>
                      </select>
                      <p v-if="editErrors.department" class="mt-1 text-sm text-red-600">{{ editErrors.department }}</p>
                    </div>

                    <!-- 职称 -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">职称 *</label>
                      <select
                        v-model="editForm.position"
                        class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                        :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500': editErrors.position }"
                      >
                        <option value="">请选择职称</option>
                        <option v-for="pos in uniquePositions" :key="pos" :value="pos">{{ pos }}</option>
                      </select>
                      <p v-if="editErrors.position" class="mt-1 text-sm text-red-600">{{ editErrors.position }}</p>
                    </div>

                    <!-- 员工状态 -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">状态</label>
                      <select
                        v-model="editForm.status"
                        class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                      >
                        <option value="active">在职</option>
                        <option value="on_leave">休假</option>
                        <option value="terminated">离职</option>
                      </select>
                    </div>

                    <!-- 基础工资 -->
                    <div class="sm:col-span-2">
                      <label class="block text-sm font-medium text-gray-700 mb-1">基础工资 *</label>
                      <div class="relative">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                          <span class="text-gray-500 sm:text-sm">¥</span>
                        </div>
                        <input
                          v-model.number="editForm.base_salary"
                          type="number"
                          step="0.01"
                          min="0"
                          class="block w-full pl-8 pr-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                          :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500': editErrors.base_salary }"
                        />
                      </div>
                      <p v-if="editErrors.base_salary" class="mt-1 text-sm text-red-600">{{ editErrors.base_salary }}</p>
                    </div>

                    <!-- 备注 -->
                    <div class="sm:col-span-2">
                      <label class="block text-sm font-medium text-gray-700 mb-1">备注</label>
                      <textarea
                        v-model="editForm.notes"
                        rows="2"
                        class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                        placeholder="可选的备注信息..."
                      ></textarea>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
          
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              @click="updateEmployeeAction"
              :disabled="updating"
              class="save-button"
            >
              <svg viewBox="0 0 24 24" class="arr-2" xmlns="http://www.w3.org/2000/svg">
                <path d="m16.172 11-5.364-5.364 1.414-1.414L20 12l-7.778 7.778-1.414-1.414L16.172 13H4v-2z"></path>
              </svg>
              <span class="text">{{ updating ? '更新中...' : '保存更改' }}</span>
              <span class="circle"></span>
              <svg viewBox="0 0 24 24" class="arr-1" xmlns="http://www.w3.org/2000/svg">
                <path d="m16.172 11-5.364-5.364 1.414-1.414L20 12l-7.778 7.778-1.414-1.414L16.172 13H4v-2z"></path>
              </svg>
              <div v-if="updating" class="loading-spinner"></div>
            </button>
            <button
              @click="closeEditModal"
              :disabled="updating"
              class="cancel-button"
            >
              取消
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useEmployeeApi } from '@/composables/useEmployeeApi' 

// 页面元数据
definePageMeta({
  layout: 'default'
})

const { 
  getEmployees, 
  deleteEmployee: apiDeleteEmployee,
  updateEmployee: apiUpdateEmployee
} = useEmployeeApi()

const { getDepartments } = useDepartmentApi()

// responsive data
const allEmployees = ref([]) // fetch from API
const totalServerEmployees = ref(0) // total number of employees returned from API
const departments = ref([]) // departments list
const loading = ref(true) // variable name for storing the state of the loading
const deleting = ref(false) // variable name for storing the state of the deleting
const searchQuery = ref('') // variable name for storing search input
const showDeleteModal = ref(false) // variable name for storing the state of the delete modal
const showAdvancedFilters = ref(false) // variable name for storing the state of the advanced filters
const showEditModal = ref(false) // variable name for storing the state of the edit modal
const employeeToDelete = ref(null) // variable name for storing the employee to delete
const employeeToEdit = ref(null) // variable name for storing the employee to edit
const editForm = ref({}) // form data for editing employee
const editErrors = ref({}) // validation errors for edit form
const updating = ref(false) // variable name for storing the state of the updating

// filters
const filters = ref({
  department: '',
  position: '',
  gender: '',
  hireYear: '',
  salaryRange: ''
})

// sorting
const sort = ref({
  field: 'hire_date', // default sorting by hire date
  direction: 'desc' // default sorting direction
})

// pagination
const currentPage = ref(1)
const pageSize = ref(10)

const tableColumns = [
  { key: 'employee_id', label: '工号', sortable: true },
  { key: 'name', label: '姓名', sortable: true },
  { key: 'gender', label: '性别', sortable: true }, // M or F   
  { key: 'department', label: '部门', sortable: true },
  { key: 'position', label: '职称', sortable: true },
  { key: 'hire_date', label: '入职日期', sortable: true },
  { key: 'status', label: '状态', sortable: true },
  { key: 'location', label: '办公地点', sortable: true },
  { key: 'base_salary', label: '薪资', sortable: true },
]

// fetch and process employee data
const fetchEmployees = async () => {
  loading.value = true  
  try {
    // prepare API parameters - get all employee data for front-end processing
    const apiParams = {
      page: 1,
      page_size: 1000, // set a large enough number to get all employees
      include_all_status: 'true', // include all status employees
      ordering: (sort.value.direction === 'desc' ? '-' : '') + sort.value.field,
      search: searchQuery.value,
      department: filters.value.department,
      position: filters.value.position,
      gender: filters.value.gender,
      hire_year: filters.value.hireYear,
      // salary_range: filters.value.salaryRange, // salary range filtering may need special handling in backend
    };
    // remove empty filter parameters
    for (const key in apiParams) {
      if (apiParams[key] === '' || apiParams[key] === null || apiParams[key] === undefined) {
        delete apiParams[key];
      }
    }

    // log API request parameters for debugging
    console.log('Fetching employees with params:', apiParams)
    
    // make API call to fetch employee data
    const response = await getEmployees(apiParams)
    console.log('API response:', response)
    
    // handle different response formats:
    // 1. standard paginated response (contains results and count)
    if (response && response.results) {
      allEmployees.value = response.results
      // use response.count if available, otherwise fallback to results length
      totalServerEmployees.value = response.count || response.results.length;
      console.log(`Loaded ${allEmployees.value.length} employees, total: ${totalServerEmployees.value}`)
    } 
    // 2. direct array response (non-paginated API)
    else if (response && Array.isArray(response)) {
      allEmployees.value = response
      totalServerEmployees.value = response.length;
      console.log(`Loaded ${allEmployees.value.length} employees (direct array)`)
    } 
    // 3. invalid response format
    else {
      allEmployees.value = []
      totalServerEmployees.value = 0;
      console.error("Failed to fetch employees or invalid data structure", response);
    }
  } catch (error) {
    // handle any errors during API call
    console.error('Error fetching employees:', error)
    allEmployees.value = []
    totalServerEmployees.value = 0;
  } finally {
    // always reset
    loading.value = false
  }
}

const filteredEmployees = computed(() => {
  let employees = [...allEmployees.value]

  if (searchQuery.value) {
    const lowerSearchQuery = searchQuery.value.toLowerCase()
    employees = employees.filter(emp => 
      emp.name.toLowerCase().includes(lowerSearchQuery) ||
      emp.employee_id.toLowerCase().includes(lowerSearchQuery) ||
      (emp.phone && emp.phone.toLowerCase().includes(lowerSearchQuery))
    )
  }

  // Filter by department if specified
  if (filters.value.department) {
    employees = employees.filter(emp => emp.department === filters.value.department)
  }

  // Filter by position if specified
  if (filters.value.position) {
    employees = employees.filter(emp => emp.position === filters.value.position)
  }

  // Filter by gender if specified
  if (filters.value.gender) {
    employees = employees.filter(emp => emp.gender === filters.value.gender)
  }

  // Filter by hire year if specified
  if (filters.value.hireYear) {
    employees = employees.filter(emp => emp.hire_date && emp.hire_date.startsWith(filters.value.hireYear))
  }

  // Filter by salary range if specified
  if (filters.value.salaryRange) {
    // Parse min and max salary from the range string (format: "min-max")
    const [min, max] = filters.value.salaryRange.split('-').map(Number);
    employees = employees.filter(emp => {
      const salary = emp.base_salary;
      // If max is specified, check if salary is between min and max
      // Otherwise just check if salary is >= min
      if (max) return salary >= min && salary <= max;
      return salary >= min;
    });
  }

  // sort (if the backend has already implemented, this part can be simplified or removed)
  if (sort.value.field) {
    employees.sort((a, b) => {
      let valA = a[sort.value.field]
      let valB = b[sort.value.field]
      // for case insensitivity, for example, the capital letters "Apple" and "apple" should be sorted together.
      if (typeof valA === 'string') valA = valA.toLowerCase();
      if (typeof valB === 'string') valB = valB.toLowerCase();

      let comparison = 0;
      if (valA > valB) comparison = 1;
      else if (valA < valB) comparison = -1;
      
      return sort.value.direction === 'asc' ? comparison : -comparison;
    });
  }
  return employees
})

// Computed property for paginated employee list
const paginatedEmployees = computed(() => {
  // Calculate start and end indices for current page
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  // Return sliced array of filtered employees
  return filteredEmployees.value.slice(start, end)
})

// Computed property for total number of pages
const totalPages = computed(() => {
  // Calculate total pages based on filtered employees count and page size
  return Math.ceil(filteredEmployees.value.length / pageSize.value)
})

// Computed property for unique department names
const uniqueDepartments = computed(() => {
  // Extract and sort department names from departments data
  return departments.value.map(dept => dept.name).sort()
})

// Computed property for unique position names
const uniquePositions = computed(() => {
  // Get unique positions from all employees data
  const positions = new Set(allEmployees.value.map(emp => emp.position).filter(Boolean))
  const positionsArray = Array.from(positions).sort()
  
  // 如果没有从员工数据中获取到职称，提供默认职称列表
  if (positionsArray.length === 0) {
    return [
      '总经理',
      '副总经理',
      '部门经理',
      '高级工程师',
      '工程师',
      '初级工程师',
      '人事经理',
      '人事专员',
      '财务经理',
      '会计师',
      '市场经理',
      '市场专员',
      '运营经理',
      '运营专员',
      '客服主管',
      '客服专员',
      '行政主管',
      '行政专员'
    ]
  }
  
  return positionsArray
})

// Computed property for unique hire years
const uniqueHireYears = computed(() => {
  // Extract hire years from all employees and sort in descending order
  const years = new Set(allEmployees.value.map(emp => emp.hire_date ? emp.hire_date.substring(0, 4) : null).filter(Boolean))
  return Array.from(years).sort((a, b) => b - a)
})

// Computed property for new employees count in current month
const newEmployeesThisMonth = computed(() => {
  // Filter employees hired in current month
  const currentMonth = new Date().toISOString().substring(0, 7)
  return allEmployees.value.filter(emp => emp.hire_date && emp.hire_date.startsWith(currentMonth)).length
})

// Computed property for average salary calculation
const averageSalary = computed(() => {
  // Return 0 if no employees
  if (!allEmployees.value.length) return 0
  
  // Filter employees with valid salary data
  const employeesWithSalary = allEmployees.value.filter(emp => 
    emp.base_salary && 
    !isNaN(emp.base_salary) && 
    emp.base_salary > 0
  )
  
  // Return 0 if no employees have valid salary data
  if (!employeesWithSalary.length) return 0
  
  // Calculate total salary and return rounded average
  const totalSalary = employeesWithSalary.reduce((sum, emp) => sum + Number(emp.base_salary), 0)
  return Math.round(totalSalary / employeesWithSalary.length)
})

// 获取部门数据
const fetchDepartments = async () => {
  try {
    const response = await getDepartments()
    if (response && response.results) {
      departments.value = response.results
    }
  } catch (error) {
    console.error('Error fetching departments:', error)
  }
}


// 监控筛选变化，重置到第一页
watch([searchQuery, filters], () => {
  currentPage.value = 1
}, { deep: true })

// 初始化时获取数据
onMounted(() => {
  if (process.client) { // 确保只在客户端执行，因为 localStorage 依赖
    // 尝试自动登录，如果未登录
    const existingToken = localStorage.getItem('auth_token');
    if (!existingToken) {
      const config = useRuntimeConfig();
      $fetch('/api/auth/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: { username: 'admin', password: 'admin123' }
      }).then(loginResponse => {
        if (loginResponse && loginResponse.success && loginResponse.data && loginResponse.data.token) {
          localStorage.setItem('auth_token', loginResponse.data.token);
          localStorage.setItem('user_info', JSON.stringify(loginResponse.data.user));
          console.log('Auto-login successful in employees page');
          fetchEmployees(); // 登录成功后获取员工数据
          fetchDepartments(); // 获取部门数据
        }
      }).catch(err => {
        console.error('Auto-login failed in employees page:', err);
        fetchEmployees(); // 即使登录失败，也尝试获取员工（如果API允许匿名访问部分数据）
        fetchDepartments(); // 获取部门数据
      });
    } else {
      fetchEmployees(); // 已有token，直接获取员工数据
      fetchDepartments(); // 获取部门数据
    }
  }
});

const clearSearch = () => {
  searchQuery.value = ''
}

const clearFilters = () => {
  filters.value = {
    department: '',
    position: '',
    gender: '',
    hireYear: '',
    salaryRange: ''
  }
  searchQuery.value = '' // 也清空搜索查询
  currentPage.value = 1 // 重置到第一页
  // fetchEmployees() 会被 watch 自动触发
}

const toggleSort = (field) => {
  if (sort.value.field === field) {
    sort.value.direction = sort.value.direction === 'asc' ? 'desc' : 'asc'
  } else {
    sort.value.field = field
    sort.value.direction = 'asc'
  }
  currentPage.value = 1 // 排序变化时回到第一页
  // 前端排序，不需要重新请求API
}

const getSortIcon = (field) => {
  if (sort.value.field !== field) return 'heroicons:bars-arrow-down' // 默认向下，表示可排序
  return sort.value.direction === 'asc' ? 'heroicons:bars-arrow-up' : 'heroicons:bars-arrow-down'
}

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    // 前端分页，不需要重新请求API
  }
}

const visiblePages = computed(() => {
  const maxVisible = 5;
  let startPage = Math.max(1, currentPage.value - Math.floor(maxVisible / 2));
  let endPage = Math.min(totalPages.value, startPage + maxVisible - 1);
  if (endPage - startPage + 1 < maxVisible) {
    startPage = Math.max(1, endPage - maxVisible + 1);
  }
  const pages = [];
  for (let i = startPage; i <= endPage; i++) {
    pages.push(i);
  }
  return pages;
});

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' })
}

const formatEmployeeStatus = (statusKey) => {
  const map = { active: '在职', on_leave: '休假', terminated: '离职' };
  return map[statusKey] || statusKey;
};

const getEmployeeStatusClass = (statusKey) => {
  const baseClass = 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium';
  if (statusKey === 'active') return `${baseClass} bg-green-100 text-green-800`;
  if (statusKey === 'on_leave') return `${baseClass} bg-yellow-100 text-yellow-800`;
  if (statusKey === 'terminated') return `${baseClass} bg-red-100 text-red-800`;
  return `${baseClass} bg-gray-100 text-gray-800`;
};

const isAdmin = ref(true); // 假设用户是管理员，后续应从认证状态获取

const viewEmployee = (employee) => {
  // 导航到员工详情页或显示模态框
  console.log('View employee:', employee)
  // router.push(`/employees/${employee.id}`)
}

const confirmDelete = (employee) => {
  employeeToDelete.value = employee
  showDeleteModal.value = true
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
  employeeToDelete.value = null
}

const deleteEmployeeAction = async () => {
  if (!employeeToDelete.value) return;
  deleting.value = true;
  try {
    const response = await apiDeleteEmployee(employeeToDelete.value.id);
    if (response.success) {
      // alert('员工删除成功！'); // 可以替换为更友好的通知
      fetchEmployees(); // 重新获取数据
      closeDeleteModal();
    } else {
      // alert(`删除失败: ${response.error || '未知错误'}`);
      console.error("Delete failed:", response.error);
    }
  } catch (error) {
    // alert('删除过程中发生错误');
    console.error("Error deleting employee:", error);
  } finally {
    deleting.value = false;
  }
};

// Quick edit functions
const openEditModal = (employee) => {
  employeeToEdit.value = employee
  editForm.value = {
    name: employee.name,
    employee_id: employee.employee_id,
    gender: employee.gender,
    phone: employee.phone,
    birth_date: employee.birth_date,
    hire_date: employee.hire_date,
    department_ref: employee.department_ref,
    position: employee.position,
    status: employee.status,
    location: employee.location,
    base_salary: employee.base_salary,
    notes: employee.notes || ''
  }
  editErrors.value = {}
  showEditModal.value = true
}

const closeEditModal = () => {
  showEditModal.value = false
  employeeToEdit.value = null
  editForm.value = {}
  editErrors.value = {}
}

const validateEditForm = () => {
  editErrors.value = {}
  
  // 姓名验证
  if (!editForm.value.name?.trim()) {
    editErrors.value.name = '请输入员工姓名'
  } else if (editForm.value.name.trim().length < 2) {
    editErrors.value.name = '姓名至少需要2个字符'
  }
  
  // 工号验证
  if (!editForm.value.employee_id?.trim()) {
    editErrors.value.employee_id = '请输入员工工号'
  } else if (!/^[A-Z0-9]+$/.test(editForm.value.employee_id.trim())) {
    editErrors.value.employee_id = '工号只能包含大写字母和数字'
  }
  
  // 性别验证
  if (!editForm.value.gender) {
    editErrors.value.gender = '请选择性别'
  }
  
  // 电话验证
  if (!editForm.value.phone?.trim()) {
    editErrors.value.phone = '请输入电话号码'
  } else if (!/^1[3-9]\d{9}$/.test(editForm.value.phone.trim())) {
    editErrors.value.phone = '请输入有效的手机号码'
  }
  
  // 部门验证
  if (!editForm.value.department_ref) {
    editErrors.value.department = '请选择部门'
  }
  
  // 职称验证
  if (!editForm.value.position) {
    editErrors.value.position = '请选择职称'
  }
  
  // 基础工资验证
  if (!editForm.value.base_salary || editForm.value.base_salary <= 0) {
    editErrors.value.base_salary = '请输入有效的基础工资'
  } else if (editForm.value.base_salary < 1000) {
    editErrors.value.base_salary = '基础工资不能低于1000元'
  } else if (editForm.value.base_salary > 100000) {
    editErrors.value.base_salary = '基础工资不能超过100000元'
  }
  
  return Object.keys(editErrors.value).length === 0
}

const updateEmployeeAction = async () => {
  if (!validateEditForm()) return
  
  updating.value = true
  try {
    const response = await apiUpdateEmployee(employeeToEdit.value.id, editForm.value)
    
    if (response.success) {
      fetchEmployees() // 重新获取数据
      closeEditModal()
      console.log('员工信息更新成功')
    } else {
      // 处理API返回的错误
      if (response.errors) {
        Object.keys(response.errors).forEach(field => {
          if (editErrors.value.hasOwnProperty(field)) {
            editErrors.value[field] = Array.isArray(response.errors[field]) 
              ? response.errors[field][0] 
              : response.errors[field]
          }
        })
      } else {
        console.error('更新员工失败:', response.error)
      }
    }
  } catch (error) {
    console.error('更新员工失败:', error)
  } finally {
    updating.value = false
  }
}

const exportEmployees = () => {
  // 简单的CSV导出逻辑，可以按需扩展
  let csvContent = "data:text/csv;charset=utf-8,";
  // 表头
  const headers = tableColumns.map(col => col.label).join(",");
  csvContent += headers + "\r\n";
  // 数据行
  filteredEmployees.value.forEach(emp => {
    const row = tableColumns.map(col => {
      let val = emp[col.key];
      if (col.key === 'gender') val = emp.gender === 'M' ? '男' : '女';
      if (col.key === 'hire_date') val = formatDate(emp.hire_date);
      if (col.key === 'base_salary') val = emp.base_salary?.toLocaleString();
      if (col.key === 'status') val = formatEmployeeStatus(emp.status);
      return `"${String(val || '').replace(/"/g, '""')}"`; // 处理包含逗号和引号的单元格
    }).join(",");
    csvContent += row + "\r\n";
  });

  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", "employees_export.csv");
  document.body.appendChild(link); 
  link.click();
  document.body.removeChild(link);
};

</script>

<style scoped>
/* From Uiverse.io by mask_guy_0 */ 
.animated-button {
  position: relative;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 16px 36px;
  border: 4px solid;
  border-color: #3b82f6;
  font-size: 16px;
  background-color: #3b82f6;
  border-radius: 100px;
  font-weight: 600;
  color: white;
  box-shadow: 0 0 0 2px #3b82f6;
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

/* Save Button Styles */
.save-button {
  position: relative;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 12px 32px;
  border: 3px solid;
  border-color: #10b981;
  font-size: 14px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-radius: 50px;
  font-weight: 600;
  color: white;
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
  cursor: pointer;
  overflow: hidden;
  transition: all 0.6s cubic-bezier(0.23, 1, 0.32, 1);
  transform: translateY(0);
  width: auto;
  margin-left: 12px;
}

.save-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.save-button:disabled:hover {
  transform: none;
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
}

.save-button svg {
  position: absolute;
  width: 20px;
  fill: white;
  z-index: 9;
  transition: all 0.8s cubic-bezier(0.23, 1, 0.32, 1);
}

.save-button .arr-1 {
  right: 12px;
}

.save-button .arr-2 {
  left: -25%;
}

.save-button .circle {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 16px;
  height: 16px;
  background-color: white;
  border-radius: 50%;
  opacity: 0;
  transition: all 0.8s cubic-bezier(0.23, 1, 0.32, 1);
}

.save-button .text {
  position: relative;
  z-index: 1;
  transform: translateX(-8px);
  transition: all 0.8s cubic-bezier(0.23, 1, 0.32, 1);
}

.save-button:hover:not(:disabled) {
  box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
  color: #065f46;
  border-radius: 12px;
  transform: translateY(-2px);
}

.save-button:hover:not(:disabled) .arr-1 {
  right: -25%;
}

.save-button:hover:not(:disabled) .arr-2 {
  left: 12px;
}

.save-button:hover:not(:disabled) .text {
  transform: translateX(8px);
}

.save-button:hover:not(:disabled) svg {
  fill: #065f46;
}

.save-button:active:not(:disabled) {
  scale: 0.98;
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
}

.save-button:hover:not(:disabled) .circle {
  width: 180px;
  height: 180px;
  opacity: 1;
}

.loading-spinner {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  z-index: 10;
}

@keyframes spin {
  0% { transform: translate(-50%, -50%) rotate(0deg); }
  100% { transform: translate(-50%, -50%) rotate(360deg); }
}

/* Cancel Button Styles */
.cancel-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 12px 24px;
  border: 2px solid #d1d5db;
  border-radius: 8px;
  background-color: white;
  color: #6b7280;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 12px;
  width: 100%;
}

.cancel-button:hover:not(:disabled) {
  background-color: #f9fafb;
  border-color: #9ca3af;
  color: #374151;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.cancel-button:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.cancel-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Responsive adjustments */
@media (min-width: 640px) {
  .cancel-button {
    margin-top: 0;
    margin-left: 12px;
    width: auto;
  }
}
</style> 