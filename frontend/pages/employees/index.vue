<template>
  <div class="space-y-6">
    <!-- 页面标题和操作栏 -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">员工管理</h1>
        <p class="mt-2 text-sm text-gray-600">
          管理公司员工信息，共 {{ totalServerEmployees }} 名员工
        </p>
      </div>
      
      <!-- 操作按钮区域 -->
      <div class="mt-4 sm:mt-0 flex space-x-3">
        <button
          @click="exportEmployees"
          class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-all duration-200 shadow-sm"
        >
          <Icon name="heroicons:arrow-down-tray" class="mr-2 h-4 w-4" />
          导出
        </button>
        
        <!-- 添加员工按钮 - 对所有用户可见 -->
        <NuxtLink to="/employees/add" class="animated-button">
          <svg
            viewBox="0 0 24 24"
            class="arr-2"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="m16.172 11-5.364-5.364 1.414-1.414L20 12l-7.778 7.778-1.414-1.414L16.172 13H4v-2z"
            ></path>
          </svg>
          <span class="text">添加员工</span>
          <span class="circle"></span>
          <svg
            viewBox="0 0 24 24"
            class="arr-1"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="m16.172 11-5.364-5.364 1.414-1.414L20 12l-7.778 7.778-1.414-1.414L16.172 13H4v-2z"
            ></path>
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
                <dt class="text-sm font-medium text-gray-500 truncate">
                  总员工数
                </dt>
                <dd class="text-lg font-medium text-gray-900">
                  {{ totalServerEmployees }}
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <Icon
                name="heroicons:building-office"
                class="h-6 w-6 text-blue-400"
              />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">
                  部门数量
                </dt>
                <dd class="text-lg font-medium text-gray-900">
                  {{ uniqueDepartments.length }}
                </dd>
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
                <dt class="text-sm font-medium text-gray-500 truncate">
                  本月新入职
                </dt>
                <dd class="text-lg font-medium text-gray-900">
                  {{ newEmployeesThisMonth }}
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <Icon
                name="heroicons:chart-bar"
                class="h-6 w-6 text-purple-400"
              />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">
                  平均薪资
                </dt>
                <dd class="text-lg font-medium text-gray-900">
                  ¥{{ averageSalary.toLocaleString() }}
                </dd>
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
          <label
            for="search"
            class="block text-sm font-medium text-gray-700 mb-2"
            >搜索员工</label
          >
          <div class="relative">
            <div
              class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
            >
              <Icon
                name="heroicons:magnifying-glass"
                class="h-5 w-5 text-gray-400"
              />
            </div>
            <input
              id="search"
              v-model="searchQuery"
              type="text"
              placeholder="搜索姓名、工号、电话..."
              class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary focus:border-primary sm:text-sm"
            />
            <div
              v-if="searchQuery"
              class="absolute inset-y-0 right-0 pr-3 flex items-center"
            >
              <button
                @click="clearSearch"
                class="text-gray-400 hover:text-gray-600"
              >
                <Icon name="heroicons:x-mark" class="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>

        <!-- 部门筛选 -->
        <div>
          <label
            for="department"
            class="block text-sm font-medium text-gray-700 mb-2"
            >部门</label
          >
          <select
            id="department"
            v-model="filters.department"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
          >
            <option value="">全部部门</option>
            <option v-for="dept in uniqueDepartments" :key="dept" :value="dept">
              {{ dept }}
            </option>
          </select>
        </div>

        <!-- 职称筛选 -->
        <div>
          <label
            for="position"
            class="block text-sm font-medium text-gray-700 mb-2"
            >职称</label
          >
          <select
            id="position"
            v-model="filters.position"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
          >
            <option value="">全部职称</option>
            <option v-for="pos in uniquePositions" :key="pos" :value="pos">
              {{ pos }}
            </option>
          </select>
        </div>
      </div>

      <!-- 高级筛选 -->
      <div
        v-if="showAdvancedFilters"
        class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t border-gray-200"
      >
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2"
            >性别</label
          >
          <select
            v-model="filters.gender"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
          >
            <option value="">全部</option>
            <option value="M">男</option>
            <option value="F">女</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2"
            >入职年份</label
          >
          <select
            v-model="filters.hireYear"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
          >
            <option value="">全部年份</option>
            <option v-for="year in uniqueHireYears" :key="year" :value="year">
              {{ year }}年
            </option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2"
            >薪资范围</label
          >
          <select
            v-model="filters.salaryRange"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
          >
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
          {{ showAdvancedFilters ? "收起高级筛选" : "展开高级筛选" }}
          <Icon
            :name="
              showAdvancedFilters
                ? 'heroicons:chevron-up'
                : 'heroicons:chevron-down'
            "
            class="ml-1 h-4 w-4 inline"
          />
        </button>
        <div class="flex space-x-2">
          <button
            @click="clearFilters"
            class="px-3 py-1 text-sm text-gray-600 hover:text-gray-800"
          >
            清空筛选
          </button>
          <span class="text-sm text-gray-500">
            显示 {{ filteredEmployees.length }} /
            {{ totalServerEmployees }} 条记录
          </span>
        </div>
      </div>
    </div>

    <!-- 数据表格 -->
    <div
      class="bg-white shadow-sm rounded-lg border border-gray-200 overflow-hidden"
    >
      <!-- 加载状态 -->
      <div v-if="loading" class="p-12 text-center">
        <div class="inline-flex items-center">
          <div
            class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mr-3"
          ></div>
          <span class="text-gray-600 text-lg">加载中，请稍候...</span>
        </div>
      </div>

      <!-- 空状态 -->
      <div
        v-else-if="!filteredEmployees.length && !loading"
        class="p-12 text-center"
      >
        <Icon name="heroicons:users" class="mx-auto h-16 w-16 text-gray-400" />
        <h3 class="mt-4 text-lg font-medium text-gray-900">
          {{
            searchQuery || Object.values(filters).some((v) => v)
              ? "未找到匹配的员工"
              : "暂无员工信息"
          }}
        </h3>
        <p class="mt-2 text-sm text-gray-500">
          {{
            searchQuery || Object.values(filters).some((v) => v)
              ? "请尝试调整搜索条件"
              : "开始添加第一个员工吧"
          }}
        </p>
        <div class="mt-6">
          <button
            v-if="searchQuery || Object.values(filters).some((v) => v)"
            @click="clearFilters"
            class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary mr-3"
          >
            清空筛选
          </button>
          <NuxtLink to="/employees/add" class="animated-button">
            <svg
              viewBox="0 0 24 24"
              class="arr-2"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="m16.172 11-5.364-5.364 1.414-1.414L20 12l-7.778 7.778-1.414-1.414L16.172 13H4v-2z"
              ></path>
            </svg>
            <span class="text">添加员工</span>
            <span class="circle"></span>
            <svg
              viewBox="0 0 24 24"
              class="arr-1"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="m16.172 11-5.364-5.364 1.414-1.414L20 12l-7.778 7.778-1.414-1.414L16.172 13H4v-2z"
              ></path>
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
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
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
              <td
                class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
              >
                {{ employee.employee_id }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-10 w-10">
                    <div
                      class="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center"
                    >
                      <span class="text-sm font-medium text-gray-700">{{
                        employee.name.charAt(0)
                      }}</span>
                    </div>
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">
                      {{ employee.name }}
                    </div>
                    <div class="text-sm text-gray-500">
                      {{ employee.phone }}
                    </div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <span
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                  :class="
                    employee.gender === 'M'
                      ? 'bg-blue-100 text-blue-800'
                      : 'bg-pink-100 text-pink-800'
                  "
                >
                  {{ employee.gender === "M" ? "男" : "女" }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800"
                >
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
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ employee.location }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                ¥{{ employee.base_salary?.toLocaleString() || "未设置" }}
              </td>
              <td
                class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium"
              >
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
      <div
        v-if="totalPages > 1 && !loading"
        class="bg-white px-4 py-3 border-t border-gray-200 sm:px-6"
      >
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
          <div
            class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between"
          >
            <div>
              <p class="text-sm text-gray-700">
                显示第
                <span class="font-medium">{{
                  (currentPage - 1) * pageSize + 1
                }}</span>
                到
                <span class="font-medium">{{
                  Math.min(currentPage * pageSize, filteredEmployees.length)
                }}</span>
                条，共
                <span class="font-medium">{{ filteredEmployees.length }}</span>
                条记录
                <span v-if="filteredEmployees.length !== totalServerEmployees"
                  >(总 {{ totalServerEmployees }} 条)</span
                >
              </p>
            </div>
            <div>
              <nav
                class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px"
              >
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
                      : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50',
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
      <div
        class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0"
      >
        <div
          class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
        ></div>
        
        <div
          class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full"
        >
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div
                class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10"
              >
                <Icon
                  name="heroicons:exclamation-triangle"
                  class="h-6 w-6 text-red-600"
                />
              </div>
              <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                  确认删除员工
                </h3>
                <div class="mt-2">
                  <p class="text-sm text-gray-500">
                    您确定要删除员工
                    <strong>{{ employeeToDelete?.name }}</strong> (工号:
                    {{ employeeToDelete?.employee_id }}) 吗？ 此操作不可撤销。
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
              <div
                v-if="deleting"
                class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"
              ></div>
              {{ deleting ? "删除中..." : "确认删除" }}
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
      <div
        class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0"
      >
        <div
          class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
        ></div>

        <div
          class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full"
        >
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="mt-3 text-center sm:mt-0 sm:text-left w-full">
                <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                  快速编辑员工信息
                </h3>

                <form @submit.prevent="updateEmployeeAction" class="space-y-4">
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <!-- 姓名 -->
                    <div>
                      <label
                        class="block text-sm font-medium text-gray-700 mb-1"
                        >姓名 *</label
                      >
                      <input
                        v-model="editForm.name"
                        type="text"
                        class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                        :class="{
                          'border-red-300 focus:border-red-500 focus:ring-red-500':
                            editErrors.name,
                        }"
                      />
                      <p
                        v-if="editErrors.name"
                        class="mt-1 text-sm text-red-600"
                      >
                        {{ editErrors.name }}
                      </p>
                    </div>

                    <!-- 工号 -->
                    <div>
                      <label
                        class="block text-sm font-medium text-gray-700 mb-1"
                        >工号 *</label
                      >
                      <input
                        v-model="editForm.employee_id"
                        type="text"
                        class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                        :class="{
                          'border-red-300 focus:border-red-500 focus:ring-red-500':
                            editErrors.employee_id,
                        }"
                      />
                      <p
                        v-if="editErrors.employee_id"
                        class="mt-1 text-sm text-red-600"
                      >
                        {{ editErrors.employee_id }}
                      </p>
                    </div>

                    <!-- 性别 -->
                    <div>
                      <label
                        class="block text-sm font-medium text-gray-700 mb-1"
                        >性别 *</label
                      >
                      <select
                        v-model="editForm.gender"
                        class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                        :class="{
                          'border-red-300 focus:border-red-500 focus:ring-red-500':
                            editErrors.gender,
                        }"
                      >
                        <option value="">请选择性别</option>
                        <option value="M">男</option>
                        <option value="F">女</option>
                      </select>
                      <p
                        v-if="editErrors.gender"
                        class="mt-1 text-sm text-red-600"
                      >
                        {{ editErrors.gender }}
                      </p>
                    </div>

                    <!-- 电话 -->
                    <div>
                      <label
                        class="block text-sm font-medium text-gray-700 mb-1"
                        >电话号码 *</label
                      >
                      <input
                        v-model="editForm.phone"
                        type="tel"
                        class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                        :class="{
                          'border-red-300 focus:border-red-500 focus:ring-red-500':
                            editErrors.phone,
                        }"
                      />
                      <p
                        v-if="editErrors.phone"
                        class="mt-1 text-sm text-red-600"
                      >
                        {{ editErrors.phone }}
                      </p>
                    </div>

                    <!-- 部门 -->
                    <div>
                      <label
                        class="block text-sm font-medium text-gray-700 mb-1"
                        >部门 *</label
                      >
                      <select
                        v-model="editForm.department_ref"
                        class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                        :class="{
                          'border-red-300 focus:border-red-500 focus:ring-red-500':
                            editErrors.department,
                        }"
                      >
                        <option value="">请选择部门</option>
                        <option
                          v-for="dept in departments"
                          :key="dept.id"
                          :value="dept.id"
                        >
                          {{ dept.name }}
                        </option>
                      </select>
                      <p
                        v-if="editErrors.department"
                        class="mt-1 text-sm text-red-600"
                      >
                        {{ editErrors.department }}
                      </p>
                    </div>

                    <!-- 职称 -->
                    <div>
                      <label
                        class="block text-sm font-medium text-gray-700 mb-1"
                        >职称 *</label
                      >
                      <select
                        v-model="editForm.position"
                        class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                        :class="{
                          'border-red-300 focus:border-red-500 focus:ring-red-500':
                            editErrors.position,
                        }"
                      >
                        <option value="">请选择职称</option>
                        <option
                          v-for="pos in uniquePositions"
                          :key="pos"
                          :value="pos"
                        >
                          {{ pos }}
                        </option>
                      </select>
                      <p
                        v-if="editErrors.position"
                        class="mt-1 text-sm text-red-600"
                      >
                        {{ editErrors.position }}
                      </p>
                    </div>

                    <!-- 员工状态 -->
                    <div>
                      <label
                        class="block text-sm font-medium text-gray-700 mb-1"
                        >状态</label
                      >
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
                      <label
                        class="block text-sm font-medium text-gray-700 mb-1"
                        >基础工资 *</label
                      >
                      <div class="relative">
                        <div
                          class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
                        >
                          <span class="text-gray-500 sm:text-sm">¥</span>
                        </div>
                        <input
                          v-model.number="editForm.base_salary"
                          type="number"
                          step="0.01"
                          min="0"
                          class="block w-full pl-8 pr-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                          :class="{
                            'border-red-300 focus:border-red-500 focus:ring-red-500':
                              editErrors.base_salary,
                          }"
                        />
                      </div>
                      <p
                        v-if="editErrors.base_salary"
                        class="mt-1 text-sm text-red-600"
                      >
                        {{ editErrors.base_salary }}
                      </p>
                    </div>

                    <!-- 备注 -->
                    <div class="sm:col-span-2">
                      <label
                        class="block text-sm font-medium text-gray-700 mb-1"
                        >备注</label
                      >
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
              <svg
                viewBox="0 0 24 24"
                class="arr-2"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="m16.172 11-5.364-5.364 1.414-1.414L20 12l-7.778 7.778-1.414-1.414L16.172 13H4v-2z"
                ></path>
              </svg>
              <span class="text">{{
                updating ? "更新中..." : "保存更改"
              }}</span>
              <span class="circle"></span>
              <svg
                viewBox="0 0 24 24"
                class="arr-1"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="m16.172 11-5.364-5.364 1.414-1.414L20 12l-7.778 7.778-1.414-1.414L16.172 13H4v-2z"
                ></path>
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
import { ref, computed, watch, onMounted } from "vue";
import { useEmployeeApi } from "@/composables/useEmployeeApi";
import { useAuthStore } from "@/stores/auth";
import { useAdvancedSort, useAdvancedSearch } from "@/composables/useAdvancedSort";
import { useGraphAlgorithms } from "@/composables/useGraphAlgorithms";
import { useDynamicProgramming } from "@/composables/useDynamicProgramming";

// --- 页面元数据 ---
// definePageMeta 用于设置页面特定的元数据，例如布局。
// 这使得页面可以轻松地重用不同的布局模板，例如 'default' 布局包含了导航栏和页脚，而 'auth' 布局则可能用于登录页面。
definePageMeta({
  layout: "default",
});

// --- API 调用 ---
// 通过 useEmployeeApi 和 useDepartmentApi 组合式函数来封装 API 调用。
// 这种设计模式（Composition API）使得逻辑可以被轻松地重用和组织。
// 将 API 调用抽象出来，可以使得组件代码更关注于视图逻辑，而不是数据获取的实现细节。
const { 
  getEmployees, 
  deleteEmployee: apiDeleteEmployee,
  updateEmployee: apiUpdateEmployee,
} = useEmployeeApi();

const { getDepartments } = useDepartmentApi();

// --- 响应式状态管理 (State Management) ---
// 使用 ref 来定义组件的响应式状态。这使得当状态值改变时，Vue 能够自动更新 UI。

// 核心数据
const allEmployees = ref([]); // 存储从后端获取的原始员工列表。采用一次性获取全部数据的方式，简化了前端的分页、排序和筛选逻辑，对于中小型数据量（如少于1000条）提供了极佳的用户体验，因为所有操作都无需等待网络请求。
const totalServerEmployees = ref(0); // 服务器端的员工总数，用于在UI上显示真实的总数。
const departments = ref([]); // 部门列表，用于筛选下拉框。

// UI 状态
const loading = ref(true); // 控制加载动画的显示，提升用户体验，告知用户数据正在获取中。
const deleting = ref(false); // 控制删除按钮的禁用状态和加载动画，防止用户重复点击。
const updating = ref(false); // 控制编辑模态框中保存按钮的状态，防止重复提交。
const showDeleteModal = ref(false); // 控制删除确认模态框的显示。
const showEditModal = ref(false); // 控制快速编辑模态框的显示。
const showAdvancedFilters = ref(false); // 控制高级筛选区域的展开和折叠。

// 数据引用
const employeeToDelete = ref(null); // 存储待删除的员工对象，用于在确认模态框中显示信息。
const employeeToEdit = ref(null); // 存储待编辑的员工对象，用于填充编辑表单。

// 表单数据
const editForm = ref({}); // 快速编辑表单的数据模型。
const editErrors = ref({}); // 存储快速编辑表单的验证错误。

// 筛选与排序
const searchQuery = ref(""); // 搜索框的输入值。
const filters = ref({
  // 存储所有筛选条件的对象。
  department: "",
  position: "",
  gender: "",
  hireYear: "",
  salaryRange: "",
});
const sort = ref({
  // 存储当前的排序字段和方向。
  field: "hire_date",
  direction: "desc",
});

// 分页
const currentPage = ref(1);
const pageSize = ref(10);

// 表格列定义
// 将表格列的配置抽象成一个数组，使得表格的渲染和管理更加灵活。
// 如果需要调整列的顺序、标签或是否可排序，只需修改这个数组即可。
const tableColumns = [
  { key: "employee_id", label: "工号", sortable: true },
  { key: "name", label: "姓名", sortable: true },
  { key: "gender", label: "性别", sortable: true }, // M or F
  { key: "department", label: "部门", sortable: true },
  { key: "position", label: "职称", sortable: true },
  { key: "hire_date", label: "入职日期", sortable: true },
  { key: "status", label: "状态", sortable: true },
  { key: "location", label: "办公地点", sortable: true },
  { key: "base_salary", label: "薪资", sortable: true },
];

// --- 数据获取 (Data Fetching) ---
/**
 * @description 异步获取员工列表。
 * 设计为一次性获取所有员工数据，以便在前端进行快速的筛选、排序和分页。
 * 这种策略适用于员工数量在可控范围内的场景（例如几百到一千），
 * 优点是初始加载后用户操作响应极快，无需额外API请求。
 * 如果员工数量非常大（例如上万），则应切换到后端分页和筛选策略。
 */
const fetchEmployees = async () => {
  loading.value = true;
  try {
    // 准备API参数，一次性获取所有数据用于前端处理
    const apiParams = {
      page: 1,
      page_size: 1000, // 设置一个足够大的数值以获取所有员工
      include_all_status: "true", // 包括所有状态的员工，如在职、离职等
      ordering: (sort.value.direction === "desc" ? "-" : "") + sort.value.field,
      // 注意：这里的筛选参数主要是为了演示，在当前前端处理所有数据的模式下，这些参数不会被后端使用。
      // 如果切换到后端筛选模式，这些参数将变得至关重要。
      search: searchQuery.value,
      department: filters.value.department,
      position: filters.value.position,
      gender: filters.value.gender,
      hire_year: filters.value.hireYear,
    };
    // 移除空的筛选参数，避免向API发送无效参数
    for (const key in apiParams) {
      if (
        apiParams[key] === "" ||
        apiParams[key] === null ||
        apiParams[key] === undefined
      ) {
        delete apiParams[key];
      }
    }

    console.log("Fetching employees with params:", apiParams);
    
    // 调用API获取员工数据
    const response = await getEmployees(apiParams);
    console.log("API response:", response);
    
    // 处理不同格式的API响应，增强代码的健壮性
    if (response && response.results) {
      // 1. 标准分页响应
      allEmployees.value = response.results;
      totalServerEmployees.value = response.count || response.results.length;
      console.log(
        `Loaded ${allEmployees.value.length} employees, total: ${totalServerEmployees.value}`
      );
    } else if (response && Array.isArray(response)) {
      // 2. 直接返回数组的响应
      allEmployees.value = response;
      totalServerEmployees.value = response.length;
      console.log(
        `Loaded ${allEmployees.value.length} employees (direct array)`
      );
    } else {
      // 3. 无效的响应格式
      allEmployees.value = [];
      totalServerEmployees.value = 0;
      console.error(
        "Failed to fetch employees or invalid data structure",
        response
      );
    }
  } catch (error) {
    console.error("Error fetching employees:", error);
    allEmployees.value = [];
    totalServerEmployees.value = 0;
  } finally {
    loading.value = false; // 无论成功或失败，都结束加载状态
  }
};

// --- 计算属性 (Computed Properties) ---
// 使用 computed 来派生状态。计算属性是基于它们的响应式依赖进行缓存的。
// 这意味着只要相关依赖没有改变，多次访问计算属性会立即返回之前的计算结果，而不会再次执行函数，从而优化性能。

/**
 * @description 根据搜索和筛选条件过滤员工列表。
 * 这是前端处理的核心，它响应 `searchQuery` 和 `filters` 的变化，
 * 实时计算出应在表格中显示的员工数据，提供了非常流畅的用户体验。
 */
const filteredEmployees = computed(() => {
  let employees = [...allEmployees.value];

  // 应用搜索查询
  if (searchQuery.value) {
    const lowerSearchQuery = searchQuery.value.toLowerCase();
    employees = employees.filter(
      (emp) =>
      emp.name.toLowerCase().includes(lowerSearchQuery) ||
      emp.employee_id.toLowerCase().includes(lowerSearchQuery) ||
      (emp.phone && emp.phone.toLowerCase().includes(lowerSearchQuery))
    );
  }

  // 应用部门筛选
  if (filters.value.department) {
    employees = employees.filter(
      (emp) => emp.department === filters.value.department
    );
  }

  // 应用职称筛选
  if (filters.value.position) {
    employees = employees.filter(
      (emp) => emp.position === filters.value.position
    );
  }

  // 应用性别筛选
  if (filters.value.gender) {
    employees = employees.filter((emp) => emp.gender === filters.value.gender);
  }

  // 应用入职年份筛选
  if (filters.value.hireYear) {
    employees = employees.filter(
      (emp) => emp.hire_date && emp.hire_date.startsWith(filters.value.hireYear)
    );
  }

  // 应用薪资范围筛选
  if (filters.value.salaryRange) {
    const [min, max] = filters.value.salaryRange.split("-").map(Number);
    employees = employees.filter((emp) => {
      const salary = emp.base_salary;
      if (max) return salary >= min && salary <= max;
      return salary >= min;
    });
  }

  // 应用优化的排序算法
  if (sort.value.field) {
    // 导入高性能排序算法
    const { hybridSort } = useAdvancedSort();
    employees = hybridSort(employees, sort.value.field, sort.value.direction);
  }
  return employees;
});

/**
 * @description 从已过滤的员工列表中计算出当前页应显示的数据。
 * 依赖于 `currentPage` 和 `pageSize`。
 */
const paginatedEmployees = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return filteredEmployees.value.slice(start, end);
});

/**
 * @description 计算总页数，用于分页组件。
 */
const totalPages = computed(() => {
  return Math.ceil(filteredEmployees.value.length / pageSize.value);
});

/**
 * @description 从部门数据中提取唯一的部门名称列表，用于筛选下拉框。
 */
const uniqueDepartments = computed(() => {
  return departments.value.map((dept) => dept.name).sort();
});

/**
 * @description 从员工数据中提取唯一的职称列表。
 * 使用 Set 来确保唯一性，并提供一个备用列表以防API数据不完整。
 */
const uniquePositions = computed(() => {
  const positions = new Set(
    allEmployees.value.map((emp) => emp.position).filter(Boolean)
  );
  const positionsArray = Array.from(positions).sort();

  // 如果API数据中没有职称信息，提供一个默认列表以保证UI正常工作。
  if (positionsArray.length === 0) {
    return [
      "总经理",
      "副总经理",
      "部门经理",
      "高级工程师",
      "工程师",
      "初级工程师",
      "人事经理",
      "人事专员",
      "财务经理",
      "会计师",
      "市场经理",
      "市场专员",
      "运营经理",
      "运营专员",
      "客服主管",
      "客服专员",
      "行政主管",
      "行政专员",
    ];
  }

  return positionsArray;
});

/**
 * @description 从员工数据中提取唯一的入职年份列表。
 */
const uniqueHireYears = computed(() => {
  const years = new Set(
    allEmployees.value
      .map((emp) => (emp.hire_date ? emp.hire_date.substring(0, 4) : null))
      .filter(Boolean)
  );
  return Array.from(years).sort((a, b) => b - a); // 降序排序，最新的年份在前
});

/**
 * @description 计算本月新入职员工数量，用于统计卡片。
 */
const newEmployeesThisMonth = computed(() => {
  const currentMonth = new Date().toISOString().substring(0, 7);
  return allEmployees.value.filter(
    (emp) => emp.hire_date && emp.hire_date.startsWith(currentMonth)
  ).length;
});

/**
 * @description 计算所有员工的平均薪资。
 * 在计算前会过滤掉无效或不存在的薪资数据，确保结果的准确性。
 */
const averageSalary = computed(() => {
  if (!allEmployees.value.length) return 0;

  // 过滤掉薪资数据无效的员工
  const employeesWithSalary = allEmployees.value.filter(
    (emp) => emp.base_salary && !isNaN(emp.base_salary) && emp.base_salary > 0
  );

  if (!employeesWithSalary.length) return 0;

  const totalSalary = employeesWithSalary.reduce(
    (sum, emp) => sum + Number(emp.base_salary),
    0
  );
  return Math.round(totalSalary / employeesWithSalary.length);
});

/**
 * @description 获取部门列表，用于筛选下拉框和编辑模态框。
 */
const fetchDepartments = async () => {
  try {
    const response = await getDepartments();
    if (response && response.results) {
      departments.value = response.results;
    }
  } catch (error) {
    console.error("Error fetching departments:", error);
  }
};

// --- 侦听器 (Watchers) ---
/**
 * @description 侦听筛选条件的变化。
 * 当用户更改任何筛选条件时，自动将分页重置到第一页，
 * 这是一个符合用户直觉的良好体验设计。
 */
watch(
  [searchQuery, filters],
  () => {
    currentPage.value = 1;
  },
  { deep: true }
); // 使用 deep: true 来侦听对象内部属性的变化。

// --- 生命周期钩子 (Lifecycle Hooks) ---
/**
 * @description onMounted 是 Vue 的生命周期钩子之一，在组件被挂载到 DOM 后执行。
 * 这里用于执行初始化操作，例如获取初始数据。
 * 同时包含了自动登录逻辑，这在开发环境中非常方便，可以免去每次刷新页面都手动登录的麻烦。
 */
onMounted(() => {
  if (process.client) {
    // 首先初始化认证状态
    authStore.initAuth();
    
    console.log("页面加载时的认证状态:");
    console.log("- Token:", authStore.token);
    console.log("- User:", authStore.user);
    console.log("- Is authenticated:", authStore.isAuthenticated);
    console.log("- Is admin:", authStore.isAdmin);
    
    // 检查是否已经有认证状态
    if (authStore.isAuthenticated) {
      console.log("用户已认证，直接获取数据...");
      fetchEmployees();
      fetchDepartments();
    } else {
      // 如果没有认证状态，尝试使用默认凭据自动登录
      console.log("未找到认证状态，尝试自动登录...");
      $fetch("/api/auth/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: { username: "admin", password: "admin123" },
      })
        .then((loginResponse) => {
          if (
            loginResponse &&
            loginResponse.success &&
            loginResponse.data &&
            loginResponse.data.token
          ) {
            console.log("自动登录成功");
            console.log("登录响应用户数据:", loginResponse.data.user);
            
            // 使用cookie持久化认证状态
            const tokenCookie = useCookie('auth-token');
            const userCookie = useCookie('user');
            tokenCookie.value = loginResponse.data.token;
            userCookie.value = JSON.stringify(loginResponse.data.user);
            
            // 重新初始化store以读取cookie中的数据
            authStore.initAuth();
            
            console.log("登录后的认证状态:");
            console.log("- Token:", authStore.token);
            console.log("- User:", authStore.user);
            console.log("- Is authenticated:", authStore.isAuthenticated);
            console.log("- Is admin:", authStore.isAdmin);
            
            // 登录成功后获取所需数据
            fetchEmployees();
            fetchDepartments();
          } else {
            console.error("自动登录失败:", loginResponse);
        }
        })
        .catch((err) => {
          console.error("自动登录错误:", err);
          // 即使登录失败，也尝试获取数据（某些API可能允许匿名访问）
          fetchEmployees();
          fetchDepartments();
        });
    }
  }
});

// --- 方法 (Methods) ---
// 存放组件的业务逻辑和事件处理函数。

/**
 * @description 清空搜索框。
 */
const clearSearch = () => {
  searchQuery.value = "";
};

/**
 * @description 重置所有筛选条件到初始状态。
 */
const clearFilters = () => {
  filters.value = {
    department: "",
    position: "",
    gender: "",
    hireYear: "",
    salaryRange: "",
  };
  searchQuery.value = "";
  currentPage.value = 1;
};

/**
 * @description 切换表格的排序字段和方向。
 */
const toggleSort = (field) => {
  if (sort.value.field === field) {
    // 如果点击的是当前排序列，则切换排序方向
    sort.value.direction = sort.value.direction === "asc" ? "desc" : "asc";
  } else {
    // 如果点击的是新的列，则按升序排序
    sort.value.field = field;
    sort.value.direction = "asc";
  }
  currentPage.value = 1; // 排序变化后回到第一页
};

/**
 * @description 获取当前排序列的图标。
 */
const getSortIcon = (field) => {
  if (sort.value.field !== field) return "heroicons:bars-arrow-down"; // 默认图标
  return sort.value.direction === "asc"
    ? "heroicons:bars-arrow-up"
    : "heroicons:bars-arrow-down";
};

/**
 * @description 切换分页。
 */
const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
  }
};

/**
 * @description 计算分页组件中应显示的页码。
 * 这个逻辑旨在提供一个智能的分页导航，例如 `1 ... 4 5 6 ... 10`，而不是列出所有页码。
 */
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

/**
 * @description 格式化日期字符串。
 */
const formatDate = (dateString) => {
  if (!dateString) return "N/A";
  return new Date(dateString).toLocaleDateString("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });
};

/**
 * @description 将员工状态的 key 转换为用户可读的文本。
 */
const formatEmployeeStatus = (statusKey) => {
  const map = { active: "在职", on_leave: "休假", terminated: "离职" };
  return map[statusKey] || statusKey;
};

/**
 * @description 根据员工状态返回对应的 CSS 类，用于显示不同颜色的标签。
 */
const getEmployeeStatusClass = (statusKey) => {
  const baseClass =
    "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium";
  if (statusKey === "active") return `${baseClass} bg-green-100 text-green-800`;
  if (statusKey === "on_leave")
    return `${baseClass} bg-yellow-100 text-yellow-800`;
  if (statusKey === "terminated") return `${baseClass} bg-red-100 text-red-800`;
  return `${baseClass} bg-gray-100 text-gray-800`;
};

// 权限控制 - 从认证系统获取真实的管理员权限
const authStore = useAuthStore();
const isAdmin = computed(() => {
  const adminStatus = authStore.isAdmin;
  console.log('当前用户信息:', authStore.user);
  console.log('管理员权限状态:', adminStatus);
  return adminStatus;
});

/**
 * @description 查看员工详情。
 * 目前只是打印日志，可以扩展为导航到详情页或打开一个详情模态框。
 */
const viewEmployee = (employee) => {
  console.log("View employee:", employee);
  // router.push(`/employees/${employee.id}`)
};

/**
 * @description 打开删除确认模态框。
 */
const confirmDelete = (employee) => {
  employeeToDelete.value = employee;
  showDeleteModal.value = true;
};

/**
 * @description 关闭删除确认模态框。
 */
const closeDeleteModal = () => {
  showDeleteModal.value = false;
  employeeToDelete.value = null;
};

/**
 * @description 执行删除操作。
 * 在调用API期间，会禁用按钮以防止重复操作。
 * 操作结束后会重新获取员工列表以更新UI。
 */
const deleteEmployeeAction = async () => {
  if (!employeeToDelete.value) return;
  deleting.value = true;
  try {
    const response = await apiDeleteEmployee(employeeToDelete.value.id);
    if (response.success) {
      fetchEmployees(); // 重新获取数据
      closeDeleteModal();
    } else {
      console.error("Delete failed:", response.error);
    }
  } catch (error) {
    console.error("Error deleting employee:", error);
  } finally {
    deleting.value = false;
  }
};

/**
 * @description 打开快速编辑模态框。
 * 这种设计提供了一个快捷的编辑入口，用户无需离开当前列表页面即可修改常用字段，提升了操作效率。
 * 详细信息或不常用字段的修改则通过"详细编辑"页面完成。
 * @param {object} employee - 要编辑的员工对象。
 */
const openEditModal = (employee) => {
  employeeToEdit.value = employee;
  // 创建一个员工对象的深拷贝用于表单，避免直接修改原始数据。
  editForm.value = {
    ...employee,
    notes: employee.notes || "", // 确保 notes 字段存在
  };
  editErrors.value = {};
  showEditModal.value = true;
};

/**
 * @description 关闭快速编辑模态框，并重置相关状态。
 */
const closeEditModal = () => {
  showEditModal.value = false;
  employeeToEdit.value = null;
  editForm.value = {};
  editErrors.value = {};
};

/**
 * @description 验证快速编辑表单。
 * 提供即时的客户端验证反馈，但不能替代后端的最终验证。
 * @returns {boolean} - 表单是否有效。
 */
const validateEditForm = () => {
  editErrors.value = {};

  // 姓名验证
  if (!editForm.value.name?.trim()) {
    editErrors.value.name = "请输入员工姓名";
  } else if (editForm.value.name.trim().length < 2) {
    editErrors.value.name = "姓名至少需要2个字符";
  }

  // 工号验证
  if (!editForm.value.employee_id?.trim()) {
    editErrors.value.employee_id = "请输入员工工号";
  } else if (!/^[A-Z0-9]+$/.test(editForm.value.employee_id.trim())) {
    editErrors.value.employee_id = "工号只能包含大写字母和数字";
  }

  // 性别验证
  if (!editForm.value.gender) {
    editErrors.value.gender = "请选择性别";
  }

  // 电话验证
  if (!editForm.value.phone?.trim()) {
    editErrors.value.phone = "请输入电话号码";
  } else if (!/^1[3-9]\d{9}$/.test(editForm.value.phone.trim())) {
    editErrors.value.phone = "请输入有效的手机号码";
  }

  // 部门验证
  if (!editForm.value.department_ref) {
    editErrors.value.department = "请选择部门";
  }

  // 职称验证
  if (!editForm.value.position) {
    editErrors.value.position = "请选择职称";
  }

  // 基础工资验证
  if (!editForm.value.base_salary || editForm.value.base_salary <= 0) {
    editErrors.value.base_salary = "请输入有效的基础工资";
  } else if (editForm.value.base_salary < 1000) {
    editErrors.value.base_salary = "基础工资不能低于1000元";
  } else if (editForm.value.base_salary > 100000) {
    editErrors.value.base_salary = "基础工资不能超过100000元";
  }

  return Object.keys(editErrors.value).length === 0;
};

/**
 * @description 提交更新后的员工信息。
 * 包含错误处理逻辑，如果API返回字段级错误，会将其显示在表单中。
 */
const updateEmployeeAction = async () => {
  if (!validateEditForm()) return;

  updating.value = true;
  try {
    const response = await apiUpdateEmployee(
      employeeToEdit.value.id,
      editForm.value
    );

    if (response.success) {
      fetchEmployees(); // 成功后刷新列表
      closeEditModal();
      console.log("员工信息更新成功");
    } else {
      if (response.errors) {
        // 将后端返回的验证错误映射到表单
        Object.keys(response.errors).forEach((field) => {
          if (editErrors.value.hasOwnProperty(field)) {
            editErrors.value[field] = Array.isArray(response.errors[field])
              ? response.errors[field][0]
              : response.errors[field];
          }
        });
      } else {
        console.error("更新员工失败:", response.error);
      }
    }
  } catch (error) {
    console.error("更新员工失败:", error);
  } finally {
    updating.value = false;
  }
};

/**
 * @description 将当前筛选出的员工数据导出为 CSV 文件。
 * 这是一个纯前端的实现，可以快速生成文件供用户下载。
 */
const exportEmployees = () => {
  let csvContent = "data:text/csv;charset=utf-8,";
  // 添加表头
  const headers = tableColumns.map((col) => col.label).join(",");
  csvContent += headers + "\r\n";
  // 添加数据行
  filteredEmployees.value.forEach((emp) => {
    const row = tableColumns
      .map((col) => {
      let val = emp[col.key];
        // 格式化特殊字段
        if (col.key === "gender") val = emp.gender === "M" ? "男" : "女";
        if (col.key === "hire_date") val = formatDate(emp.hire_date);
        if (col.key === "base_salary") val = emp.base_salary?.toLocaleString();
        if (col.key === "status") val = formatEmployeeStatus(emp.status);
        // 处理单元格中可能包含的逗号和引号
        return `"${String(val || "").replace(/"/g, '""')}"`;
      })
      .join(",");
    csvContent += row + "\r\n";
  });

  // 创建并触发下载链接
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
  0% {
    transform: translate(-50%, -50%) rotate(0deg);
  }
  100% {
    transform: translate(-50%, -50%) rotate(360deg);
  }
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
