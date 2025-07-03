<template>
  <div class="space-y-6">
    <!-- 页面标题和操作栏 -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">部门管理</h1>
        <p class="mt-2 text-sm text-gray-600">管理公司组织架构和部门信息</p>
      </div>

      <div class="mt-4 sm:mt-0 flex space-x-3">
        <button
          @click="showOrgChart = !showOrgChart"
          class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-colors"
        >
          <Icon name="heroicons:chart-bar" class="mr-2 h-4 w-4" />
          {{ showOrgChart ? "隐藏" : "显示" }}组织架构
        </button>
        <button
          @click="openAddModal"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-colors"
        >
          <Icon name="heroicons:plus" class="mr-2 h-4 w-4" />
          添加部门
        </button>
      </div>
    </div>

    <!-- 部门统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
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
                  部门总数
                </dt>
                <dd class="text-lg font-medium text-gray-900">
                  {{ departments.length }}
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
              <Icon name="heroicons:users" class="h-6 w-6 text-green-400" />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">
                  员工总数
                </dt>
                <dd class="text-lg font-medium text-gray-900">
                  {{ totalEmployees }}
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
                name="heroicons:user-group"
                class="h-6 w-6 text-yellow-400"
              />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">
                  平均部门规模
                </dt>
                <dd class="text-lg font-medium text-gray-900">
                  {{ averageDeptSize }}人
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
                name="heroicons:chart-pie"
                class="h-6 w-6 text-purple-400"
              />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">
                  最大部门
                </dt>
                <dd class="text-lg font-medium text-gray-900">
                  {{ largestDept.name }}
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 部门列表 -->
    <div
      class="bg-white shadow-sm rounded-lg border border-gray-200 overflow-hidden"
    >
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-medium text-gray-900">部门列表</h3>
      </div>
      
      <div v-if="loading" class="p-6 text-center">
        <div
          class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"
        ></div>
        <p class="mt-2 text-gray-500">加载中...</p>
      </div>
      
      <div
        v-else-if="departments.length === 0"
        class="p-6 text-center text-gray-500"
      >
        暂无部门数据
      </div>
      
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                部门信息
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                部门经理
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                员工数量
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                成立时间
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                状态
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
              v-for="dept in departments"
              :key="dept.id"
              class="hover:bg-gray-50"
            >
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-10 w-10">
                    <div
                      class="h-10 w-10 rounded-lg flex items-center justify-center"
                      :style="{
                        backgroundColor: dept.color + '20',
                        color: dept.color,
                      }"
                    >
                      <Icon :name="dept.icon" class="h-5 w-5" />
                    </div>
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">
                      {{ dept.name }}
                    </div>
                    <div class="text-sm text-gray-500">
                      {{ dept.description }}
                    </div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-8 w-8">
                    <div
                      class="h-8 w-8 rounded-full bg-gray-300 flex items-center justify-center"
                    >
                      <span class="text-xs font-medium text-gray-700">{{
                        dept.manager.charAt(0)
                      }}</span>
                    </div>
                  </div>
                  <div class="ml-3">
                    <div class="text-sm font-medium text-gray-900">
                      {{ dept.manager }}
                    </div>
                    <div class="text-sm text-gray-500">
                      {{ dept.manager_title }}
                    </div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <span class="text-sm font-medium text-gray-900">{{
                    dept.employee_count
                  }}</span>
                  <span class="ml-2 text-xs text-gray-500">人</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-1.5 mt-1">
                  <div 
                    class="h-1.5 rounded-full" 
                    :style="{ 
                      backgroundColor: dept.color, 
                      width: `${
                        (dept.employee_count /
                          Math.max(
                            ...departments.map((d) => d.employee_count)
                          )) *
                        100
                      }%`,
                    }"
                  ></div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(dept.created_at) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                  :class="
                    dept.status === 'active'
                      ? 'bg-green-100 text-green-800'
                      : 'bg-gray-100 text-gray-800'
                  "
                >
                  {{ dept.status === "active" ? "活跃" : "停用" }}
                </span>
              </td>
              <td
                class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium"
              >
                <div class="flex items-center justify-end space-x-2">
                  <button
                    class="text-primary hover:text-primary-dark p-1 rounded"
                    title="查看详情"
                  >
                    <Icon name="heroicons:eye" class="h-4 w-4" />
                  </button>
                  <button
                    class="text-accent hover:text-accent-dark p-1 rounded"
                    title="编辑"
                  >
                    <Icon name="heroicons:pencil" class="h-4 w-4" />
                  </button>
                  <button
                    class="text-danger hover:text-red-700 p-1 rounded"
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
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import DepartmentList from "~/components/DepartmentList.vue";

// --- 页面元数据 ---
// 设置页面布局，确保 UI 的一致性。
definePageMeta({
  layout: "default",
});

// --- 组合式 API ---
// 引入封装好的 useDepartmentApi，使得组件内无需关心 API 请求的底层实现细节，
// 例如认证头部、API基地址等，这让代码更简洁、更易于维护。
const departmentApi = useDepartmentApi();

// --- 响应式状态 ---
const departments = ref([]); // 存储从 API 获取的部门列表。
const loading = ref(true); // 控制加载状态的显示，向用户反馈数据正在获取中。
const error = ref(null); // 存储 API 请求可能发生的错误信息。
const selectedDepartmentId = ref(null); // 存储当前选中的部门 ID。

// --- 计算属性 ---

/**
 * @description 根据 selectedDepartmentId 找到并返回当前选中的部门对象。
 * 使用计算属性的好处是，当 selectedDepartmentId 或 departments 列表变化时，
 * 它会自动重新计算，确保 selectedDepartment 总是最新的。
 * 这比在每次选择变化时手动更新一个 ref 变量要高效和简洁。
 */
const selectedDepartment = computed(() => {
  if (!selectedDepartmentId.value) {
    return null;
  }
  return departments.value.find(
    (dept) => dept.id === selectedDepartmentId.value
  );
});

const showOrgChart = ref(false);

// 计算属性
const totalEmployees = computed(() => {
  return departments.value.reduce(
    (sum, dept) => sum + (dept.employee_count || 0),
    0
  );
});

const averageDeptSize = computed(() => {
  if (departments.value.length === 0) return 0;
  return Math.round(totalEmployees.value / departments.value.length);
});

const largestDept = computed(() => {
  if (departments.value.length === 0) return { name: "暂无" };
  return departments.value.reduce((max, dept) => 
    (dept.employee_count || 0) > (max.employee_count || 0) ? dept : max
  );
});

// 为部门添加默认的图标和颜色
const getDepartmentIcon = (deptName) => {
  const iconMap = {
    技术部: "heroicons:code-bracket",
    人事部: "heroicons:users",
    财务部: "heroicons:currency-dollar",
    市场部: "heroicons:megaphone",
    运营部: "heroicons:cog-6-tooth",
    销售部: "heroicons:chart-bar",
    客服部: "heroicons:phone",
    行政部: "heroicons:building-office",
    法务部: "heroicons:scale",
    采购部: "heroicons:shopping-cart",
    研发部: "heroicons:beaker",
    产品部: "heroicons:cube",
    设计部: "heroicons:paint-brush",
    质量部: "heroicons:shield-check",
    安全部: "heroicons:shield-exclamation",
  };
  return iconMap[deptName] || "heroicons:building-office";
};

const getDepartmentColor = (deptName) => {
  const colorMap = {
    技术部: "#3B82F6",
    人事部: "#10B981",
    财务部: "#F59E0B",
    市场部: "#EF4444",
    运营部: "#8B5CF6",
    销售部: "#06B6D4",
    客服部: "#84CC16",
    行政部: "#6B7280",
    法务部: "#1F2937",
    采购部: "#F97316",
    研发部: "#EC4899",
    产品部: "#14B8A6",
    设计部: "#A855F7",
    质量部: "#22C55E",
    安全部: "#DC2626",
  };
  return colorMap[deptName] || "#6B7280";
};

const formatDate = (dateString) => {
  if (!dateString) return "";
  return new Date(dateString).toLocaleDateString("zh-CN");
};

// --- 方法 ---

/**
 * @description 从后端 API 加载所有部门的数据。
 * 这是一个典型的异步数据获取模式，包含了加载状态和错误处理，
 * 提高了用户体验和应用的健壮性。
 */
const loadDepartments = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await departmentApi.getDepartments({ page_size: 1000 });
    console.log('部门API响应:', response);
    
    if (response && response.results) {
      // 对返回的数据进行处理，计算每个部门的员工数和平均薪资。
      // 在前端进行这种轻量的数据聚合可以减轻后端负担，并为UI提供更丰富的信息。
      departments.value = response.results.map((dept) => ({
        ...dept,
        employee_count: dept.employees ? dept.employees.length : 0,
        average_salary: dept.employees ? calculateAverageSalary(dept.employees) : 'N/A',
        icon: getDepartmentIcon(dept.name),
        color: getDepartmentColor(dept.name),
        manager: dept.manager || '待分配',
        manager_title: dept.manager_title || '部门经理'
      }));
      console.log('处理后的部门数据:', departments.value);
    } else if (response && Array.isArray(response)) {
      // 如果直接返回数组
      departments.value = response.map((dept) => ({
        ...dept,
        employee_count: dept.employees ? dept.employees.length : 0,
        average_salary: dept.employees ? calculateAverageSalary(dept.employees) : 'N/A',
        icon: getDepartmentIcon(dept.name),
        color: getDepartmentColor(dept.name),
        manager: dept.manager || '待分配',
        manager_title: dept.manager_title || '部门经理'
      }));
      console.log('处理后的部门数据(数组):', departments.value);
    } else {
      departments.value = [];
      console.log('没有部门数据');
    }
  } catch (err) {
    console.error("加载部门数据失败:", err);
    error.value = "无法加载部门数据，请稍后再试。";
    departments.value = [];
  } finally {
    loading.value = false;
  }
};

/**
 * @description 计算一个部门内所有员工的平均薪资。
 * @param {Array} employees - 员工对象数组，每个员工应包含 salary 属性。
 * @returns {string} - 格式化后的平均薪资字符串，或在没有有效薪资时返回 'N/A'。
 */
const calculateAverageSalary = (employees) => {
  if (!employees || employees.length === 0) {
    return "N/A";
  }
  const salaries = employees
    .map((e) => Number(e.salary))
    .filter((s) => !isNaN(s) && s > 0);
  if (salaries.length === 0) {
    return "N/A";
  }
  const average =
    salaries.reduce((sum, salary) => sum + salary, 0) / salaries.length;
  return average.toFixed(2);
};

/**
 * @description 当子组件 DepartmentList 触发 select-department 事件时调用此函数。
 * 这是父子组件通信的标准实践：子组件通过 $emit 发送事件和数据，父组件通过 @-syntax 监听并响应。
 * @param {number} departmentId - 从子组件传递过来的部门 ID。
 */
const handleSelectDepartment = (departmentId) => {
  selectedDepartmentId.value = departmentId;
};

// --- 生命周期钩子 ---

/**
 * @description 组件挂载后，自动加载部门数据。
 * onMounted 是执行初始化数据获取的理想位置。
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
          console.log('Auto-login successful in departments page');
          loadDepartments();
  }
      }).catch(err => {
        console.error('Auto-login failed in departments page:', err);
        // 即使登录失败，也尝试加载数据，因为某些数据可能是公开的
        loadDepartments();
      });
    } else {
      loadDepartments();
    }
  }
});

const openAddModal = () => {
  console.log("Open add modal");
};
</script>

<style scoped>
/* 在 scoped 样式中，你可以定义一些仅适用于此页面的特定样式，
   而不用担心会影响到全局或其他组件。*/
.page-container {
  display: flex;
  gap: 1.5rem;
}

.department-list-container {
  flex: 1;
  min-width: 300px;
}

.department-details-container {
  flex: 2;
}
</style>
