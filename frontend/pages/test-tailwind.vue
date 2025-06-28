<template>
  <!--
    设计思路:
    - 这是一个用于视觉验证的开发工具页面，旨在提供一个清晰的看板，来检查 TailwindCSS 的各项配置是否按预期工作。
    - 页面被划分为多个 <section>，每个部分专注于测试一个特定的 TailwindCSS 功能，如颜色、响应式、自定义工具类和动画。
    - 这种结构化的展示使得开发者可以一目了然地确认样式系统的健康状况。
  -->
  <div class="min-h-screen bg-gray-50 p-8">
    <div class="max-w-7xl mx-auto">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">TailwindCSS v4 测试页面</h1>
      
      <!-- 
        颜色系统测试:
        - 用于验证 `tailwind.config.js` 中定义的自定义主题颜色（如 primary, accent）是否可以成功应用。
        - 如果这些卡片显示了正确的颜色，说明主题配置无误。
      -->
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
      
      <!-- 
        响应式布局测试:
        - 这个网格布局使用了 Tailwind 的响应式前缀（sm:, md:, lg:）。
        - 通过调整浏览器窗口的大小，可以测试在不同断点下，网格的列数是否按预期变化（手机1列，平板2列，桌面3列，大桌面4列）。
        - 这能确保响应式设计在各种设备上都能正常工作。
      -->
      <section class="mb-8">
        <h2 class="text-xl font-semibold mb-4">响应式布局测试</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          <div class="bg-blue-500 text-white p-4 rounded">Item 1</div>
          <div class="bg-green-500 text-white p-4 rounded">Item 2</div>
          <div class="bg-yellow-500 text-white p-4 rounded">Item 3</div>
          <div class="bg-red-500 text-white p-4 rounded">Item 4</div>
        </div>
      </section>
      
      <!-- 
        自定义工具类测试:
        - 用于测试通过插件添加的或在 `tailwind.config.js` 中自定义的工具类。
        - `scrollbar-thin` 可能是一个自定义插件（如 `tailwind-scrollbar`）提供的类，用于美化滚动条。
        - 如果滚动条样式与默认不同，说明插件配置成功。
      -->
      <section class="mb-8">
        <h2 class="text-xl font-semibold mb-4">自定义工具类测试</h2>
        <div class="scrollbar-thin h-32 overflow-y-auto bg-white p-4 rounded shadow">
          <p v-for="i in 10" :key="i" class="mb-2">
            滚动条测试内容 {{ i }}
          </p>
        </div>
      </section>
      
      <!-- 
        过渡和动画测试:
        - 结合了 Vue 的 `<transition>` 组件和 TailwindCSS 的过渡工具类。
        - 点击按钮时，`show` 的值会改变，触发元素的进入和离开动画。
        - `enter-active-class`, `enter-from-class` 等属性指定了动画不同阶段应用的 CSS 类。
        - 这可以验证项目中 Vue 过渡效果与 TailwindCSS 的集成是否顺畅。
      -->
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
/**
 * TailwindCSS 测试页面脚本
 *
 * 设计思路:
 * - 此页面的主要逻辑在模板中，用于视觉展示。
 * - 脚本部分非常简单，只包含触发动画所必需的最少逻辑。
 */
import { ref } from 'vue'

// 一个响应式变量，用于控制"过渡和动画测试"部分中元素的显示与隐藏。
const show = ref(false)
</script>