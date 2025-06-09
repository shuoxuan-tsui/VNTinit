<script setup>
import { ref, computed, onMounted } from 'vue'

// 页面元数据
definePageMeta({
  layout: 'default'
})

// 响应式数据
const loading = ref(false)
const activeTab = ref('general')
const showUserModal = ref(false)
const showRoleModal = ref(false)
const selectedUser = ref(null)
const selectedRole = ref(null)

// 系统设置
const systemSettings = ref({
  general: {
    systemName: '企业管理系统',
    systemVersion: 'v1.0.0',
    companyName: '示例科技有限公司',
    companyAddress: '北京市朝阳区示例大厦',
    companyPhone: '010-12345678',
    companyEmail: 'contact@example.com',
    timezone: 'Asia/Shanghai',
    language: 'zh-CN',
    dateFormat: 'YYYY-MM-DD',
    timeFormat: '24h'
  },
  security: {
    passwordMinLength: 8,
    passwordRequireUppercase: true,
    passwordRequireNumbers: true,
    passwordRequireSymbols: false,
    sessionTimeout: 30,
    maxLoginAttempts: 5,
    lockoutDuration: 15,
    enableTwoFactor: false,
    allowRememberMe: true
  },
  notification: {
    emailNotifications: true,
    smsNotifications: false,
    pushNotifications: true,
    systemAlerts: true,
    maintenanceNotices: true,
    securityAlerts: true
  },
  backup: {
    autoBackup: true,
    backupFrequency: 'daily',
    backupRetention: 30,
    backupLocation: '/backup',
    lastBackup: '2024-04-15 02:00:00'
  }
})

// 用户管理
const users = ref([
  {
    id: 1,
    username: 'admin',
    email: 'admin@example.com',
    name: '系统管理员',
    role: 'admin',
    status: 'active',
    lastLogin: '2024-04-15 10:30:00',
    createdAt: '2024-01-01 00:00:00'
  },
  {
    id: 2,
    username: 'hr_manager',
    email: 'hr@example.com',
    name: '人事经理',
    role: 'hr_manager',
    status: 'active',
    lastLogin: '2024-04-15 09:15:00',
    createdAt: '2024-01-15 00:00:00'
  },
  {
    id: 3,
    username: 'employee',
    email: 'employee@example.com',
    name: '普通员工',
    role: 'employee',
    status: 'inactive',
    lastLogin: '2024-04-10 16:45:00',
    createdAt: '2024-02-01 00:00:00'
  }
])

// 角色权限
const roles = ref([
  {
    id: 1,
    name: 'admin',
    displayName: '系统管理员',
    description: '拥有所有系统权限',
    permissions: [
      'user_management',
      'role_management',
      'employee_management',
      'salary_management',
      'attendance_management',
      'performance_management',
      'report_access',
      'system_settings'
    ],
    userCount: 1
  },
  {
    id: 2,
    name: 'hr_manager',
    displayName: '人事经理',
    description: '人事相关功能权限',
    permissions: [
      'employee_management',
      'salary_management',
      'attendance_management',
      'performance_management',
      'report_access'
    ],
    userCount: 1
  },
  {
    id: 3,
    name: 'employee',
    displayName: '普通员工',
    description: '基础查看权限',
    permissions: [
      'view_own_info',
      'attendance_checkin',
      'view_own_salary'
    ],
    userCount: 154
  }
])

// 权限列表
const permissions = ref([
  { id: 'user_management', name: '用户管理', category: '系统管理' },
  { id: 'role_management', name: '角色管理', category: '系统管理' },
  { id: 'system_settings', name: '系统设置', category: '系统管理' },
  { id: 'employee_management', name: '员工管理', category: '人事管理' },
  { id: 'salary_management', name: '薪资管理', category: '人事管理' },
  { id: 'attendance_management', name: '考勤管理', category: '人事管理' },
  { id: 'performance_management', name: '绩效管理', category: '人事管理' },
  { id: 'report_access', name: '报表查看', category: '数据分析' },
  { id: 'view_own_info', name: '查看个人信息', category: '个人权限' },
  { id: 'attendance_checkin', name: '考勤打卡', category: '个人权限' },
  { id: 'view_own_salary', name: '查看个人薪资', category: '个人权限' }
])

// 标签页配置
const tabs = ref([
  { id: 'general', name: '基本设置', icon: 'heroicons:cog-6-tooth' },
  { id: 'security', name: '安全设置', icon: 'heroicons:shield-check' },
  { id: 'users', name: '用户管理', icon: 'heroicons:users' },
  { id: 'roles', name: '角色权限', icon: 'heroicons:key' },
  { id: 'notifications', name: '通知设置', icon: 'heroicons:bell' },
  { id: 'backup', name: '备份设置', icon: 'heroicons:archive-box' }
])

// 计算属性
const permissionsByCategory = computed(() => {
  const grouped = {}
  permissions.value.forEach(permission => {
    if (!grouped[permission.category]) {
      grouped[permission.category] = []
    }
    grouped[permission.category].push(permission)
  })
  return grouped
})

// 方法
const saveSettings = async (category) => {
  loading.value = true
  try {
    // 模拟保存设置
    await new Promise(resolve => setTimeout(resolve, 1000))
    console.log(`保存${category}设置成功`)
  } catch (error) {
    console.error('保存设置失败:', error)
  } finally {
    loading.value = false
  }
}

const addUser = () => {
  selectedUser.value = null
  showUserModal.value = true
}

const editUser = (user) => {
  selectedUser.value = { ...user }
  showUserModal.value = true
}

const deleteUser = (userId) => {
  if (confirm('确定要删除这个用户吗？')) {
    users.value = users.value.filter(user => user.id !== userId)
  }
}

const toggleUserStatus = (user) => {
  user.status = user.status === 'active' ? 'inactive' : 'active'
}

const addRole = () => {
  selectedRole.value = null
  showRoleModal.value = true
}

const editRole = (role) => {
  selectedRole.value = { ...role }
  showRoleModal.value = true
}

const deleteRole = (roleId) => {
  if (confirm('确定要删除这个角色吗？')) {
    roles.value = roles.value.filter(role => role.id !== roleId)
  }
}

const performBackup = async () => {
  loading.value = true
  try {
    // 模拟备份操作
    await new Promise(resolve => setTimeout(resolve, 3000))
    systemSettings.value.backup.lastBackup = new Date().toLocaleString('zh-CN')
    console.log('备份完成')
  } catch (error) {
    console.error('备份失败:', error)
  } finally {
    loading.value = false
  }
}

const getUserStatusColor = (status) => {
  return status === 'active' 
    ? 'text-green-600 bg-green-100' 
    : 'text-red-600 bg-red-100'
}

const getUserStatusText = (status) => {
  return status === 'active' ? '活跃' : '禁用'
}

// 生命周期
onMounted(() => {
  console.log('系统设置页面加载完成')
})
</script>

<template>
  <div class="space-y-6">
    <!-- 页面标题 -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">系统设置</h1>
        <p class="mt-2 text-sm text-gray-600">管理系统配置、用户权限和安全设置</p>
      </div>
    </div>

    <!-- 标签页导航 -->
    <div class="bg-white shadow rounded-lg">
      <div class="border-b border-gray-200">
        <nav class="-mb-px flex space-x-8 px-6" aria-label="Tabs">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            class="py-4 px-1 border-b-2 font-medium text-sm transition-colors duration-200"
            :class="activeTab === tab.id
              ? 'border-primary text-primary'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
          >
            <div class="flex items-center space-x-2">
              <Icon :name="tab.icon" class="h-5 w-5" />
              <span>{{ tab.name }}</span>
            </div>
          </button>
        </nav>
      </div>

      <!-- 标签页内容 -->
      <div class="p-6">
        <!-- 基本设置 -->
        <div v-if="activeTab === 'general'" class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">系统名称</label>
              <input
                v-model="systemSettings.general.systemName"
                type="text"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">系统版本</label>
              <input
                v-model="systemSettings.general.systemVersion"
                type="text"
                readonly
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-gray-50 sm:text-sm"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">公司名称</label>
              <input
                v-model="systemSettings.general.companyName"
                type="text"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">公司地址</label>
              <input
                v-model="systemSettings.general.companyAddress"
                type="text"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">联系电话</label>
              <input
                v-model="systemSettings.general.companyPhone"
                type="text"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">联系邮箱</label>
              <input
                v-model="systemSettings.general.companyEmail"
                type="email"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">时区</label>
              <select
                v-model="systemSettings.general.timezone"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              >
                <option value="Asia/Shanghai">Asia/Shanghai</option>
                <option value="UTC">UTC</option>
                <option value="America/New_York">America/New_York</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">语言</label>
              <select
                v-model="systemSettings.general.language"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              >
                <option value="zh-CN">简体中文</option>
                <option value="en-US">English</option>
              </select>
            </div>
          </div>
          <div class="flex justify-end">
            <button
              @click="saveSettings('general')"
              :disabled="loading"
              class="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary disabled:opacity-50"
            >
              保存设置
            </button>
          </div>
        </div>

        <!-- 安全设置 -->
        <div v-if="activeTab === 'security'" class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">密码最小长度</label>
              <input
                v-model.number="systemSettings.security.passwordMinLength"
                type="number"
                min="6"
                max="20"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">会话超时时间（分钟）</label>
              <input
                v-model.number="systemSettings.security.sessionTimeout"
                type="number"
                min="5"
                max="120"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">最大登录尝试次数</label>
              <input
                v-model.number="systemSettings.security.maxLoginAttempts"
                type="number"
                min="3"
                max="10"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">锁定时长（分钟）</label>
              <input
                v-model.number="systemSettings.security.lockoutDuration"
                type="number"
                min="5"
                max="60"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              />
            </div>
          </div>
          
          <div class="space-y-4">
            <div class="flex items-center">
              <input
                id="password-uppercase"
                v-model="systemSettings.security.passwordRequireUppercase"
                type="checkbox"
                class="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
              />
              <label for="password-uppercase" class="ml-2 block text-sm text-gray-900">
                密码必须包含大写字母
              </label>
            </div>
            <div class="flex items-center">
              <input
                id="password-numbers"
                v-model="systemSettings.security.passwordRequireNumbers"
                type="checkbox"
                class="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
              />
              <label for="password-numbers" class="ml-2 block text-sm text-gray-900">
                密码必须包含数字
              </label>
            </div>
            <div class="flex items-center">
              <input
                id="password-symbols"
                v-model="systemSettings.security.passwordRequireSymbols"
                type="checkbox"
                class="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
              />
              <label for="password-symbols" class="ml-2 block text-sm text-gray-900">
                密码必须包含特殊字符
              </label>
            </div>
            <div class="flex items-center">
              <input
                id="two-factor"
                v-model="systemSettings.security.enableTwoFactor"
                type="checkbox"
                class="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
              />
              <label for="two-factor" class="ml-2 block text-sm text-gray-900">
                启用双因素认证
              </label>
            </div>
            <div class="flex items-center">
              <input
                id="remember-me"
                v-model="systemSettings.security.allowRememberMe"
                type="checkbox"
                class="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
              />
              <label for="remember-me" class="ml-2 block text-sm text-gray-900">
                允许记住登录状态
              </label>
            </div>
          </div>
          
          <div class="flex justify-end">
            <button
              @click="saveSettings('security')"
              :disabled="loading"
              class="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary disabled:opacity-50"
            >
              保存设置
            </button>
          </div>
        </div>

        <!-- 用户管理 -->
        <div v-if="activeTab === 'users'" class="space-y-6">
          <div class="flex justify-between items-center">
            <h3 class="text-lg font-medium text-gray-900">用户列表</h3>
            <button
              @click="addUser"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
            >
              <Icon name="heroicons:plus" class="mr-2 h-4 w-4" />
              添加用户
            </button>
          </div>
          
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">用户信息</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">角色</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">最后登录</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="h-10 w-10 rounded-full bg-primary flex items-center justify-center">
                        <span class="text-sm font-medium text-white">{{ user.name.charAt(0) }}</span>
                      </div>
                      <div class="ml-4">
                        <div class="text-sm font-medium text-gray-900">{{ user.name }}</div>
                        <div class="text-sm text-gray-500">{{ user.email }}</div>
                        <div class="text-sm text-gray-500">@{{ user.username }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ roles.find(r => r.name === user.role)?.displayName || user.role }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="inline-flex px-2 py-1 text-xs font-semibold rounded-full" :class="getUserStatusColor(user.status)">
                      {{ getUserStatusText(user.status) }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ user.lastLogin }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                    <button
                      @click="editUser(user)"
                      class="text-primary hover:text-primary-dark"
                    >
                      编辑
                    </button>
                    <button
                      @click="toggleUserStatus(user)"
                      class="text-yellow-600 hover:text-yellow-900"
                    >
                      {{ user.status === 'active' ? '禁用' : '启用' }}
                    </button>
                    <button
                      @click="deleteUser(user.id)"
                      class="text-red-600 hover:text-red-900"
                    >
                      删除
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 角色权限 -->
        <div v-if="activeTab === 'roles'" class="space-y-6">
          <div class="flex justify-between items-center">
            <h3 class="text-lg font-medium text-gray-900">角色列表</h3>
            <button
              @click="addRole"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
            >
              <Icon name="heroicons:plus" class="mr-2 h-4 w-4" />
              添加角色
            </button>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="role in roles" :key="role.id" class="bg-white border border-gray-200 rounded-lg p-6">
              <div class="flex items-center justify-between mb-4">
                <h4 class="text-lg font-medium text-gray-900">{{ role.displayName }}</h4>
                <span class="text-sm text-gray-500">{{ role.userCount }} 用户</span>
              </div>
              <p class="text-sm text-gray-600 mb-4">{{ role.description }}</p>
              
              <div class="space-y-2 mb-4">
                <h5 class="text-sm font-medium text-gray-900">权限列表：</h5>
                <div class="flex flex-wrap gap-1">
                  <span
                    v-for="permission in role.permissions"
                    :key="permission"
                    class="inline-flex px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-800"
                  >
                    {{ permissions.find(p => p.id === permission)?.name || permission }}
                  </span>
                </div>
              </div>
              
              <div class="flex space-x-2">
                <button
                  @click="editRole(role)"
                  class="flex-1 px-3 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
                >
                  编辑
                </button>
                <button
                  @click="deleteRole(role.id)"
                  class="px-3 py-2 border border-red-300 text-sm font-medium rounded-md text-red-700 bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                >
                  删除
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 通知设置 -->
        <div v-if="activeTab === 'notifications'" class="space-y-6">
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <h4 class="text-sm font-medium text-gray-900">邮件通知</h4>
                <p class="text-sm text-gray-500">接收系统邮件通知</p>
              </div>
              <input
                v-model="systemSettings.notification.emailNotifications"
                type="checkbox"
                class="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
              />
            </div>
            <div class="flex items-center justify-between">
              <div>
                <h4 class="text-sm font-medium text-gray-900">短信通知</h4>
                <p class="text-sm text-gray-500">接收系统短信通知</p>
              </div>
              <input
                v-model="systemSettings.notification.smsNotifications"
                type="checkbox"
                class="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
              />
            </div>
            <div class="flex items-center justify-between">
              <div>
                <h4 class="text-sm font-medium text-gray-900">推送通知</h4>
                <p class="text-sm text-gray-500">接收浏览器推送通知</p>
              </div>
              <input
                v-model="systemSettings.notification.pushNotifications"
                type="checkbox"
                class="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
              />
            </div>
            <div class="flex items-center justify-between">
              <div>
                <h4 class="text-sm font-medium text-gray-900">系统警报</h4>
                <p class="text-sm text-gray-500">接收系统异常警报</p>
              </div>
              <input
                v-model="systemSettings.notification.systemAlerts"
                type="checkbox"
                class="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
              />
            </div>
            <div class="flex items-center justify-between">
              <div>
                <h4 class="text-sm font-medium text-gray-900">维护通知</h4>
                <p class="text-sm text-gray-500">接收系统维护通知</p>
              </div>
              <input
                v-model="systemSettings.notification.maintenanceNotices"
                type="checkbox"
                class="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
              />
            </div>
            <div class="flex items-center justify-between">
              <div>
                <h4 class="text-sm font-medium text-gray-900">安全警报</h4>
                <p class="text-sm text-gray-500">接收安全相关警报</p>
              </div>
              <input
                v-model="systemSettings.notification.securityAlerts"
                type="checkbox"
                class="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
              />
            </div>
          </div>
          
          <div class="flex justify-end">
            <button
              @click="saveSettings('notifications')"
              :disabled="loading"
              class="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary disabled:opacity-50"
            >
              保存设置
            </button>
          </div>
        </div>

        <!-- 备份设置 -->
        <div v-if="activeTab === 'backup'" class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">备份频率</label>
              <select
                v-model="systemSettings.backup.backupFrequency"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              >
                <option value="daily">每日</option>
                <option value="weekly">每周</option>
                <option value="monthly">每月</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">保留天数</label>
              <input
                v-model.number="systemSettings.backup.backupRetention"
                type="number"
                min="7"
                max="365"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              />
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-2">备份位置</label>
              <input
                v-model="systemSettings.backup.backupLocation"
                type="text"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              />
            </div>
          </div>
          
          <div class="flex items-center">
            <input
              id="auto-backup"
              v-model="systemSettings.backup.autoBackup"
              type="checkbox"
              class="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
            />
            <label for="auto-backup" class="ml-2 block text-sm text-gray-900">
              启用自动备份
            </label>
          </div>
          
          <div class="bg-gray-50 rounded-lg p-4">
            <div class="flex items-center justify-between">
              <div>
                <h4 class="text-sm font-medium text-gray-900">最后备份时间</h4>
                <p class="text-sm text-gray-500">{{ systemSettings.backup.lastBackup }}</p>
              </div>
              <button
                @click="performBackup"
                :disabled="loading"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary disabled:opacity-50"
              >
                <Icon name="heroicons:arrow-path" class="mr-2 h-4 w-4" :class="{ 'animate-spin': loading }" />
                {{ loading ? '备份中...' : '立即备份' }}
              </button>
            </div>
          </div>
          
          <div class="flex justify-end">
            <button
              @click="saveSettings('backup')"
              :disabled="loading"
              class="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary disabled:opacity-50"
            >
              保存设置
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template> 