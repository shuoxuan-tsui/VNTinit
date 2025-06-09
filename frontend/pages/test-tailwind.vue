<template>
  <div class="min-h-screen bg-gray-50 p-8">
    <div class="max-w-7xl mx-auto">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">TailwindCSS v4 测试页面</h1>
      
      <!-- 颜色测试 -->
      <section class="mb-8">
        <h2 class="text-xl font-semibold mb-4">颜色系统测试</h2>
        <div class="grid grid-cols-5 gap-4">
          <div class="bg-primary text-white p-4 rounded">Primary</div>
          <div class="bg-accent text-white p-4 rounded">Accent</div>
          <div class="bg-success text-white p-4 rounded">Success</div>
          <div class="bg-warning text-white p-4 rounded">Warning</div>
          <div class="bg-danger text-white p-4 rounded">Danger</div>
        </div>
      </section>
      
      <!-- 响应式测试 -->
      <section class="mb-8">
        <h2 class="text-xl font-semibold mb-4">响应式布局测试</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          <div class="bg-blue-500 text-white p-4 rounded">Item 1</div>
          <div class="bg-green-500 text-white p-4 rounded">Item 2</div>
          <div class="bg-yellow-500 text-white p-4 rounded">Item 3</div>
          <div class="bg-red-500 text-white p-4 rounded">Item 4</div>
        </div>
      </section>
      
      <!-- 工具类测试 -->
      <section class="mb-8">
        <h2 class="text-xl font-semibold mb-4">自定义工具类测试</h2>
        <div class="scrollbar-thin h-32 overflow-y-auto bg-white p-4 rounded shadow">
          <p v-for="i in 10" :key="i" class="mb-2">
            滚动条测试内容 {{ i }}
          </p>
        </div>
      </section>
      
      <!-- 动画测试 -->
      <section class="mb-8">
        <h2 class="text-xl font-semibold mb-4">过渡和动画测试</h2>
        <button 
          @click="show = !show"
          class="px-4 py-2 bg-primary text-white rounded hover:bg-primary-dark transition-colors duration-200"
        >
          切换显示
        </button>
        <transition
          enter-active-class="transition ease-out duration-300"
          enter-from-class="transform opacity-0 scale-95"
          enter-to-class="transform opacity-100 scale-100"
          leave-active-class="transition ease-in duration-200"
          leave-from-class="transform opacity-100 scale-100"
          leave-to-class="transform opacity-0 scale-95"
        >
          <div v-if="show" class="mt-4 p-4 bg-white rounded shadow">
            过渡动画内容
          </div>
        </transition>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const show = ref(false)
</script>