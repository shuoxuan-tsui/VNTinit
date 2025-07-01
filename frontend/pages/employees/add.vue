<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50 py-8 relative overflow-hidden">
    <!-- 背景装饰元素 -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-blue-200 bg-opacity-20 rounded-full blur-3xl"></div>
      <div class="absolute -bottom-40 -left-40 w-96 h-96 bg-indigo-200 bg-opacity-15 rounded-full blur-3xl"></div>
      <div class="absolute top-1/3 left-1/4 w-32 h-32 bg-blue-300 bg-opacity-10 rounded-full blur-2xl"></div>
      <div class="absolute bottom-1/4 right-1/3 w-24 h-24 bg-indigo-300 bg-opacity-15 rounded-full blur-xl"></div>
    </div>

    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
      <!-- 页面标题 -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-gray-800 mb-3 drop-shadow-sm">添加员工信息</h1>
        <p class="text-xl text-gray-600 drop-shadow-sm">请填写完整的员工信息</p>
        <NuxtLink to="/employees" class="inline-flex items-center mt-6 text-gray-700 hover:text-blue-600 transition-all duration-200 backdrop-blur-sm bg-white bg-opacity-60 px-4 py-2 rounded-full shadow-sm border border-gray-200">
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
          </svg>
          返回员工列表
        </NuxtLink>
      </div>

      <!-- 主表单卡片 - 蓝色磨砂玻璃效果 -->
      <div class="backdrop-blur-xl bg-gradient-to-br from-blue-400 via-blue-500 to-blue-600 bg-opacity-95 rounded-3xl shadow-2xl border border-blue-300 border-opacity-30 overflow-hidden">
        <!-- 卡片头部 -->
        <div class="backdrop-blur-lg bg-white bg-opacity-15 px-8 py-10 border-b border-white border-opacity-20">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="flex items-center justify-center h-16 w-16 rounded-2xl backdrop-blur-sm bg-gradient-to-br from-green-400 to-emerald-500 shadow-lg">
                <svg class="h-10 w-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"></path>
                </svg>
              </div>
            </div>
            <div class="ml-6">
              <h2 class="text-2xl font-bold text-gray-900">员工信息录入</h2>
              <p class="text-gray-700 text-lg">创建新的员工档案记录</p>
            </div>
          </div>
        </div>

        <!-- 表单内容 -->
        <form @submit.prevent="submitForm" class="px-8 py-10">
          <div class="space-y-10">
            <!-- 基本信息区域 -->
            <div class="space-y-6">
              <h3 class="text-xl font-bold text-white drop-shadow flex items-center">
                <svg class="w-6 h-6 mr-3 text-blue-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
                基本信息
              </h3>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- 姓名 -->
                <div class="space-y-2">
                  <label class="block text-lg font-semibold text-white drop-shadow flex items-center">
                    <svg class="w-4 h-4 mr-2 text-purple-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                    </svg>
                    姓名 <span class="text-red-300 ml-1">*</span>
                  </label>
                  <input
                    v-model="form.name"
                    type="text"
                    required
                    placeholder="请输入员工姓名"
                    class="block w-full px-6 py-4 backdrop-blur-md bg-gradient-to-r from-white to-purple-50 bg-opacity-95 border-2 border-purple-200 hover:border-purple-300 rounded-2xl shadow-lg hover:shadow-xl focus:outline-none focus:ring-4 focus:ring-purple-200 focus:ring-opacity-50 focus:border-purple-400 text-gray-900 placeholder-gray-500 text-lg font-medium transition-all duration-300 transform hover:scale-[1.02]"
                    :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-200': errors.name }"
                  />
                  <p v-if="errors.name" class="text-sm text-red-200 drop-shadow flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
                    </svg>
                    {{ errors.name }}
                  </p>
                </div>

                <!-- 工号 -->
                <div class="space-y-2">
                  <label class="block text-lg font-semibold text-white drop-shadow flex items-center">
                    <svg class="w-4 h-4 mr-2 text-blue-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"></path>
                    </svg>
                    工号 <span class="text-red-300 ml-1">*</span>
                  </label>
                  <input
                    v-model="form.employee_id"
                    type="text"
                    required
                    placeholder="请输入员工工号"
                    class="block w-full px-6 py-4 backdrop-blur-md bg-gradient-to-r from-white to-blue-50 bg-opacity-95 border-2 border-blue-200 hover:border-blue-300 rounded-2xl shadow-lg hover:shadow-xl focus:outline-none focus:ring-4 focus:ring-blue-200 focus:ring-opacity-50 focus:border-blue-400 text-gray-900 placeholder-gray-500 text-lg font-medium transition-all duration-300 transform hover:scale-[1.02]"
                    :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-200': errors.employee_id }"
                  />
                  <p v-if="errors.employee_id" class="text-sm text-red-200 drop-shadow flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 。、1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
                    </svg>
                    {{ errors.employee_id }}
                  </p>
                </div>

                <!-- 性别 -->
                <div class="space-y-2">
                  <label class="block text-lg font-semibold text-white drop-shadow flex items-center">
                    <svg class="w-4 h-4 mr-2 text-pink-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"></path>
                    </svg>
                    性别 <span class="text-red-300 ml-1">*</span>
                  </label>
                  <select
                    v-model="form.gender"
                    required
                    class="block w-full px-6 py-4 backdrop-blur-md bg-gradient-to-r from-white to-pink-50 bg-opacity-95 border-2 border-pink-200 hover:border-pink-300 rounded-2xl shadow-lg hover:shadow-xl focus:outline-none focus:ring-4 focus:ring-pink-200 focus:ring-opacity-50 focus:border-pink-400 text-gray-900 text-lg font-medium transition-all duration-300 transform hover:scale-[1.02] cursor-pointer"
                    :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-200': errors.gender }"
                  >
                    <option value="" class="bg-pink-700 text-white font-semibold">请选择性别</option>
                    <option value="M" class="bg-gray-50 text-gray-900 font-medium">👨 男</option>
                    <option value="F" class="bg-gray-50 text-gray-900 font-medium">👩 女</option>
                  </select>
                  <p v-if="errors.gender" class="text-sm text-red-200 drop-shadow flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
                    </svg>
                    {{ errors.gender }}
                  </p>
                </div>

                <!-- 电话 属性d 是从矢量图库中来的 -->
                <div class="space-y-2">
                  <label class="block text-lg font-semibold text-white drop-shadow flex items-center">
                    <svg class="w-4 h-4 mr-2 text-green-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                    </svg>  
                    电话号码 <span class="text-red-300 ml-1">*</span>
                  </label>
                  <input
                    v-model="form.phone"
                    type="tel"
                    required
                    placeholder="请输入手机号码"
                    class="block w-full px-6 py-4 backdrop-blur-md bg-gradient-to-r from-white to-green-50 bg-opacity-95 border-2 border-green-200 hover:border-green-300 rounded-2xl shadow-lg hover:shadow-xl focus:outline-none focus:ring-4 focus:ring-green-200 focus:ring-opacity-50 focus:border-green-400 text-gray-900 placeholder-gray-500 text-lg font-medium transition-all duration-300 transform hover:scale-[1.02]"
                    :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-200': errors.phone }"
                  />
                  <p v-if="errors.phone" class="text-sm text-red-200 drop-shadow flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
                    </svg>
                    {{ errors.phone }}
                  </p>
                </div>

                <!-- 出生日期 -->
                <div class="space-y-2">
                  <label class="block text-lg font-semibold text-white drop-shadow flex items-center">
                    <svg class="w-4 h-4 mr-2 text-yellow-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                    </svg>
                    出生日期 <span class="text-red-300 ml-1">*</span>
                  </label>
                  <div class="relative group">
                    <input
                      v-model="form.birth_date"
                      type="date"
                      required
                      class="block w-full px-6 py-4 backdrop-blur-md bg-gradient-to-r from-white to-yellow-50 bg-opacity-95 border-2 border-yellow-200 hover:border-yellow-300 rounded-2xl shadow-lg hover:shadow-xl focus:outline-none focus:ring-4 focus:ring-yellow-200 focus:ring-opacity-50 focus:border-yellow-400 text-gray-900 text-lg font-medium transition-all duration-300 transform hover:scale-[1.02] group-hover:shadow-yellow-200/50"
                      :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-200': errors.birth_date }"
                    />
                    <div class="absolute inset-0 rounded-2xl bg-gradient-to-r from-yellow-400/10 to-yellow-600/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"></div>
                  </div>
                  <p v-if="errors.birth_date" class="text-sm text-red-200 drop-shadow flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
                    </svg>
                    {{ errors.birth_date }}
                  </p>
                </div>

                <!-- 入职日期 -->
                <div class="space-y-2">
                  <label class="block text-lg font-semibold text-white drop-shadow flex items-center">
                    <svg class="w-4 h-4 mr-2 text-indigo-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                    </svg>
                    入职日期 <span class="text-red-300 ml-1">*</span>
                  </label>
                  <div class="relative group">
                    <input
                      v-model="form.hire_date"
                      type="date"
                      required
                      class="block w-full px-6 py-4 backdrop-blur-md bg-gradient-to-r from-white to-indigo-50 bg-opacity-95 border-2 border-indigo-200 hover:border-indigo-300 rounded-2xl shadow-lg hover:shadow-xl focus:outline-none focus:ring-4 focus:ring-indigo-200 focus:ring-opacity-50 focus:border-indigo-400 text-gray-900 text-lg font-medium transition-all duration-300 transform hover:scale-[1.02] group-hover:shadow-indigo-200/50"
                      :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-200': errors.hire_date }"
                    />
                    <div class="absolute inset-0 rounded-2xl bg-gradient-to-r from-indigo-400/10 to-indigo-600/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"></div>
                  </div>
                  <p v-if="errors.hire_date" class="text-sm text-red-200 drop-shadow flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
                    </svg>
                    {{ errors.hire_date }}
                  </p>
                </div>
              </div>
            </div>

            <!-- 工作信息区域 -->
            <div class="space-y-6">
              <h3 class="text-xl font-bold text-white drop-shadow flex items-center">
                <svg class="w-6 h-6 mr-3 text-purple-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
                </svg>
                工作信息
              </h3>
              
              <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                <!-- 部门 -->
                <div class="space-y-2">
                  <label class="block text-lg font-semibold text-white drop-shadow flex items-center">
                    <svg class="w-4 h-4 mr-2 text-cyan-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
                    </svg>
                    部门 <span class="text-red-300 ml-1">*</span>
                  </label>
                  <select
                    v-model="form.department_ref"
                    required
                    class="block w-full px-6 py-4 backdrop-blur-md bg-gradient-to-r from-white to-cyan-50 bg-opacity-95 border-2 border-cyan-200 hover:border-cyan-300 rounded-2xl shadow-lg hover:shadow-xl focus:outline-none focus:ring-4 focus:ring-cyan-200 focus:ring-opacity-50 focus:border-cyan-400 text-gray-900 text-lg font-medium transition-all duration-300 transform hover:scale-[1.02] cursor-pointer"
                    :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-200': errors.department }"
                  >
                    <option value="" class="bg-cyan-700 text-white font-semibold">请选择部门</option>
                    <option v-for="dept in departments" :key="dept.id" :value="dept.id" class="bg-gray-50 text-gray-900 font-medium">
                      🏢 {{ dept.name }}
                    </option>
                  </select>
                  <p v-if="errors.department" class="text-sm text-red-200 drop-shadow flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
                    </svg>
                    {{ errors.department }}
                  </p>
                </div>

                <!-- 职称 -->
                <div class="space-y-2">
                  <label class="block text-lg font-semibold text-white drop-shadow flex items-center">
                    <svg class="w-4 h-4 mr-2 text-orange-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                    </svg>
                    职称/职务 <span class="text-red-300 ml-1">*</span>
                  </label>
                  <select
                    v-model="form.position"
                    required
                    class="block w-full px-6 py-4 backdrop-blur-md bg-gradient-to-r from-white to-orange-50 bg-opacity-95 border-2 border-orange-200 hover:border-orange-300 rounded-2xl shadow-lg hover:shadow-xl focus:outline-none focus:ring-4 focus:ring-orange-200 focus:ring-opacity-50 focus:border-orange-400 text-gray-900 text-lg font-medium transition-all duration-300 transform hover:scale-[1.02] cursor-pointer"
                    :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-200': errors.position }"
                  >
                    <option value="" class="bg-orange-700 text-white font-semibold">请选择职称</option>
                    <option v-for="pos in positions" :key="pos" :value="pos" class="bg-gray-50 text-gray-900 font-medium">
                      💼 {{ pos }}
                    </option>
                  </select>
                  <p v-if="errors.position" class="text-sm text-red-200 drop-shadow flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
                    </svg>
                    {{ errors.position }}
                  </p>
                </div>

                <!-- 办公地点 -->
                <div class="space-y-2">
                  <label class="block text-lg font-semibold text-white drop-shadow flex items-center">
                    <svg class="w-4 h-4 mr-2 text-rose-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                    </svg>
                    办公地点 <span class="text-red-300 ml-1">*</span>
                  </label>
                  <select
                    v-model="form.location"
                    required
                    class="block w-full px-6 py-4 backdrop-blur-md bg-gradient-to-r from-white to-rose-50 bg-opacity-95 border-2 border-rose-200 hover:border-rose-300 rounded-2xl shadow-lg hover:shadow-xl focus:outline-none focus:ring-4 focus:ring-rose-200 focus:ring-opacity-50 focus:border-rose-400 text-gray-900 text-lg font-medium transition-all duration-300 transform hover:scale-[1.02] cursor-pointer"
                    :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-200': errors.location }"
                  >
                    <option value="" class="bg-rose-700 text-white font-semibold">请选择办公地点</option>
                    <option v-for="loc in locations" :key="loc" :value="loc" class="bg-gray-50 text-gray-900 font-medium">
                      📍 {{ loc }}
                    </option>
                  </select>
                  <p v-if="errors.location" class="text-sm text-red-200 drop-shadow flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
                    </svg>
                    {{ errors.location }}
                  </p>
                </div>
              </div>

              <!-- 基础工资 -->
              <div class="space-y-2">
                <label class="block text-lg font-semibold text-white drop-shadow flex items-center">
                  <svg class="w-4 h-4 mr-2 text-green-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
                  </svg>
                  基础工资 <span class="text-red-300 ml-1">*</span>
                </label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-6 flex items-center pointer-events-none">
                    <span class="text-green-600 text-xl font-bold drop-shadow-sm">¥</span>
                  </div>
                  <input
                    v-model.number="form.base_salary"
                    type="number"
                    step="0.01"
                    min="0"
                    required
                    placeholder="请输入基础工资"
                    class="block w-full pl-12 pr-6 py-4 backdrop-blur-md bg-gradient-to-r from-white to-green-50 bg-opacity-95 border-2 border-green-200 hover:border-green-300 rounded-2xl shadow-lg hover:shadow-xl focus:outline-none focus:ring-4 focus:ring-green-200 focus:ring-opacity-50 focus:border-green-400 text-gray-900 placeholder-gray-500 text-lg font-medium transition-all duration-300 transform hover:scale-[1.02]"
                    :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-200': errors.base_salary }"
                  />
                </div>
                <p v-if="errors.base_salary" class="text-sm text-red-200 drop-shadow flex items-center">
                  <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
                  </svg>
                  {{ errors.base_salary }}
                </p>
                <p class="text-sm text-blue-100 flex items-center drop-shadow-sm opacity-90">
                  <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
                  </svg>
                  基础工资将用于薪资计算
                </p>
              </div>
            </div>

            <!-- 提交按钮 -->
            <div class="pt-8">
              <button 
                type="submit" 
                :disabled="submitting" 
                class="group relative w-full flex justify-center py-5 px-8 border border-transparent text-xl font-bold rounded-2xl text-blue-600 backdrop-blur-lg bg-white bg-opacity-95 hover:bg-opacity-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-white focus:ring-opacity-60 disabled:opacity-60 disabled:cursor-not-allowed transition-all duration-300 transform hover:scale-105 disabled:transform-none shadow-2xl"
              >
                <span v-if="submitting" class="absolute left-0 inset-y-0 flex items-center pl-6">
                  <svg class="animate-spin h-6 w-6 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4l3-3-3-3v4a8 8 0 00-8 8h4z"></path>
                  </svg>
                </span>
                <span class="flex items-center">
                  <svg v-if="!submitting" class="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  {{ submitting ? '正在保存员工信息...' : '保存员工信息' }}
                </span>
              </button>
            </div>
          </div>
        </form>
      </div>

      <!-- 底部说明 -->
      <div class="mt-10 text-center text-white drop-shadow-sm">
        <p class="text-lg font-medium">请确保所有必填信息准确无误</p>
        <p class="mt-2 text-blue-100">员工信息保存后可在员工列表中查看和管理</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'

// --- 页面元数据 ---
// 为页面设置 'default' 布局，这通常意味着它会包含网站的通用页眉、页脚和导航，确保UI一致性。
definePageMeta({
  layout: 'default'
})

// --- API 组合式函数 ---
// 引入封装好的 API 调用逻辑。这种方式（组合式API）使得组件更专注于视图和状态管理，
// 而将数据获取的细节（如端点、头部信息等）抽象出去，提高了代码的可维护性和复用性。
const employeeApi = useEmployeeApi()
const departmentApi = useDepartmentApi()

// --- 响应式状态 ---
const submitting = ref(false) // 控制提交按钮的加载状态和禁用状态，防止重复提交。

// 使用 `reactive` 来创建表单数据对象。对于包含多个字段的复杂对象，`reactive` 比多个 `ref` 更直观和易于管理。
const form = reactive({
  name: '',
  employee_id: '',
  gender: '',
  phone: '',
  birth_date: '',
  hire_date: '',
  department_ref: '', // 存储部门的外键ID
  position: '',
  base_salary: null,
  location: '' // 办公地点
})

// `errors` 对象用于存储验证错误。键是字段名，值是错误信息。
// 这种设计使得在模板中可以轻松地将错误信息与对应的输入框关联起来。
const errors = ref({})

// `departments`、`positions` 和 `locations` 用于存储下拉菜单的选项。
const departments = ref([])
const positions = ref([
  '总经理', '副总经理', '部门经理', '高级工程师', '工程师', '初级工程师',
  '人事经理', '人事专员', '财务经理', '会计师', '市场经理', '市场专员',
  '运营经理', '运营专员', '客服主管', '客服专员', '行政主管', '行政专员'
])
const locations = ref([
  '北京总部', '上海分公司', '深圳分公司', '广州分公司', '杭州分公司', 
  '成都分公司', '武汉分公司', '西安分公司', '南京分公司', '天津分公司',
  '青岛分公司', '大连分公司', '厦门分公司', '苏州分公司', '宁波分公司',
  '远程办公'
])


// --- 数据获取 ---
/**
 * @description 从后端获取部门列表，用于填充表单中的下拉选择框。
 * 包含错误处理和备用数据，以确保即使API请求失败，页面也能以可用状态呈现。
 */
const fetchDepartments = async () => {
  try {
    const response = await departmentApi.getDepartments()
    console.log('Department API response:', response)
    
    // 健壮性设计：处理多种可能的成功响应结构。
    if (response && response.results && Array.isArray(response.results)) {
      departments.value = response.results
    } else if (response && response.success && response.data && Array.isArray(response.data.results)) {
      departments.value = response.data.results
    } else {
      console.error('Invalid department response structure:', response)
      // 降级处理：如果API响应结构不符合预期，提供一组默认数据，保证核心功能可用。
      departments.value = [
        { id: 1, name: "人力资源部" }, { id: 2, name: "客服部" }, { id: 3, name: "技术部" },
        { id: 4, name: "市场部" }, { id: 5, name: "财务部" }, { id: 6, name: "采购部" }
      ]
    }
  } catch (error) {
    console.error('Error fetching departments:', error)
    // 降级处理：在捕获到网络错误或API服务器错误时，也提供默认数据。
    departments.value = [
        { id: 1, name: "人力资源部" }, { id: 2, name: "客服部" }, { id: 3, name: "技术部" },
        { id: 4, name: "市场部" }, { id: 5, name: "财务部" }, { id: 6, name: "采购部" }
    ]
  }
}


// --- 核心逻辑：表单验证与提交 ---

/**
 * @description 验证整个表单的数据。
 * 为什么需要前端验证？
 * 1. 提升用户体验：在数据发送到服务器前，立即向用户反馈错误，无需等待网络请求。
 * 2. 减轻服务器负载：避免将无效或格式错误的数据发送到后端，减少不必要的API调用和数据库操作。
 * @returns {boolean} - 表单是否所有字段都通过验证。
 */
const validateForm = () => {
  errors.value = {} // 在每次验证前清空旧的错误信息。
  
  // 姓名验证
  if (!form.name.trim()) errors.value.name = '请输入员工姓名'
  else if (form.name.trim().length < 2) errors.value.name = '姓名至少需要2个字符'
  
  // 工号验证
  if (!form.employee_id.trim()) errors.value.employee_id = '请输入员工工号'
  else if (!/^[A-Z0-9]+$/.test(form.employee_id.trim())) errors.value.employee_id = '工号只能包含大写字母和数字'
  
  // 性别验证
  if (!form.gender) errors.value.gender = '请选择性别'
  
  // 电话验证
  if (!form.phone.trim()) errors.value.phone = '请输入电话号码'
  else if (!/^1[3-9]\d{9}$/.test(form.phone.trim())) errors.value.phone = '请输入有效的手机号码'
  
  // 出生日期验证 (业务逻辑)
  if (!form.birth_date) {
    errors.value.birth_date = '请选择出生日期'
  } else {
    const birthDate = new Date(form.birth_date)
    const today = new Date()
    const age = today.getFullYear() - birthDate.getFullYear()
    if (age < 16 || age > 70) errors.value.birth_date = '员工年龄应在16-70岁之间'
  }
  
  // 入职日期验证 (业务逻辑)
  if (!form.hire_date) {
    errors.value.hire_date = '请选择入职日期'
  } else {
    const hireDate = new Date(form.hire_date)
    if (hireDate > new Date()) errors.value.hire_date = '入职日期不能晚于今天'
    if (form.birth_date) {
      const birthDate = new Date(form.birth_date)
      const minHireDate = new Date(birthDate.getFullYear() + 16, birthDate.getMonth(), birthDate.getDate())
      if (hireDate < minHireDate) errors.value.hire_date = '入职日期不能早于16岁生日'
    }
  }
  
  // 关联字段验证
  if (!form.department_ref) errors.value.department = '请选择部门'
  if (!form.position) errors.value.position = '请选择职称'
  if (!form.location) errors.value.location = '请选择办公地点'
  
  // 数值范围验证
  if (!form.base_salary || form.base_salary <= 0) errors.value.base_salary = '请输入有效的基础工资'
  else if (form.base_salary < 1000) errors.value.base_salary = '基础工资不能低于1000元'
  else if (form.base_salary > 100000) errors.value.base_salary = '基础工资不能超过100000元'
  
  // 如果 errors 对象为空，说明没有错误，返回 true
  return Object.keys(errors.value).length === 0
}

/**
 * @description 处理表单提交的异步函数。
 */
const submitForm = async () => {
  if (!validateForm()) return // 如果验证失败，则中断提交
  
  submitting.value = true
  
  try {
    // 准备提交的数据负载。这里可以进行最后的数据清理，如 trim()。
    const employeeData = {
      name: form.name.trim(),
      employee_id: form.employee_id.trim(),
      gender: form.gender,
      phone: form.phone.trim(),
      birth_date: form.birth_date,
      hire_date: form.hire_date,
      department_ref: form.department_ref,
      position: form.position,
      base_salary: form.base_salary,
      status: 'active', // 新员工默认为在职状态
      location: form.location // 用户选择的办公地点
    }
    
    // 调用API创建员工
    const response = await employeeApi.createEmployee(employeeData)
    
    if (response.success) {
      // 成功后跳转到员工列表页，给用户明确的操作完成反馈。
      await navigateTo('/employees')
      console.log('员工信息添加成功')
    } else {
      // 处理API返回的业务错误（例如，后端验证失败）
      if (response.errors) {
        // 将后端返回的字段错误信息，填充到前端的 `errors` 对象中，
        // 从而在界面上显示具体的错误，如"该工号已被使用"。
        errors.value = { ...errors.value, ...response.errors }
      } else {
        // 通用错误处理
        console.error('添加员工失败:', response.error)
        // 可以在此处添加一个全局的错误提示，例如使用 Toast 通知。
      }
    }
    
  } catch (error) {
    console.error('添加员工失败（网络或服务器错误）:', error)
  } finally {
    submitting.value = false // 无论成功或失败，最后都恢复提交按钮的状态。
  }
}


// --- 生命周期钩子 ---
/**
 * @description onMounted 是 Vue 的生命周期钩子之一，在组件被挂载到 DOM 后执行。
 * 这里是执行页面初始化操作的理想位置。
 */
onMounted(() => {
  // 为用户提供便利，将入职日期默认为今天。
  const today = new Date()
  form.hire_date = today.toISOString().split('T')[0]
  
  // 确保只在客户端（浏览器）执行，因为 `localStorage` 在服务器端不存在。
  if (process.client) {
    const existingToken = localStorage.getItem('auth_token');
    
    // 开发便利性设计：如果没有token，尝试使用默认凭据自动登录，免去开发时反复登录的麻烦。
    if (!existingToken) {
      $fetch('/api/auth/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: { username: 'admin', password: 'admin123' }
      }).then(loginResponse => {
        if (loginResponse?.success && loginResponse.data?.token) {
          localStorage.setItem('auth_token', loginResponse.data.token);
          localStorage.setItem('user_info', JSON.stringify(loginResponse.data.user));
          console.log('Auto-login successful in add employee page');
          fetchDepartments(); // 登录成功后获取部门数据
        }
      }).catch(err => {
        console.error('Auto-login failed in add employee page:', err);
        fetchDepartments(); // 即使登录失败，也尝试获取，因为某些数据可能是公开的
      });
    } else {
      // 如果已登录，直接获取数据
      fetchDepartments();
    }
  }
})
</script>

 