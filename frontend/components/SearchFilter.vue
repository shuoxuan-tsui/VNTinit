<template>
  <div class="bg-white p-4 rounded-lg shadow-sm border border-gray-200 mb-6">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <!-- 搜索框 -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">搜索</label>
        <div class="relative">
          <input
            v-model="searchQuery"
            type="text"
            :placeholder="searchPlaceholder"
            class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary"
          />
          <Icon name="heroicons:magnifying-glass" class="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
        </div>
      </div>

      <!-- 动态筛选器 -->
      <div v-for="filter in filterOptions" :key="filter.key">
        <label class="block text-sm font-medium text-gray-700 mb-1">{{ filter.label }}</label>
        <select
          v-if="filter.type === 'select'"
          v-model="filters[filter.key]"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary"
        >
          <option value="">全部</option>
          <option v-for="option in filter.options" :key="option.value" :value="option.value">
            {{ option.label }}
          </option>
        </select>
        <input
          v-else-if="filter.type === 'date'"
          v-model="filters[filter.key]"
          type="date"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary"
        />
        <input
          v-else-if="filter.type === 'number'"
          v-model="filters[filter.key]"
          type="number"
          :placeholder="filter.placeholder"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary"
        />
        <input
          v-else
          v-model="filters[filter.key]"
          type="text"
          :placeholder="filter.placeholder"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary"
        />
      </div>
    </div>

    <!-- 操作按钮 -->
    <div class="flex justify-between items-center mt-4">
      <button
        @click="clearFilters"
        class="px-4 py-2 text-sm text-gray-600 hover:text-gray-800 border border-gray-300 rounded-md hover:bg-gray-50"
      >
        清除筛选
      </button>
      <slot name="actions" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, reactive } from 'vue'
import { useDebounceFn } from '@vueuse/core'

interface FilterOption {
  key: string
  label: string
  type: 'text' | 'select' | 'date' | 'number'
  placeholder?: string
  options?: Array<{ value: string; label: string }>
}

const props = defineProps<{
  searchPlaceholder?: string
  filterOptions: FilterOption[]
  modelValue: Record<string, any>
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: Record<string, any>): void
  (e: 'search', query: string): void
  (e: 'filter', filters: Record<string, any>): void
}>()

const searchQuery = ref('')
const filters = reactive<Record<string, any>>({})

// 初始化筛选器
props.filterOptions.forEach(option => {
  filters[option.key] = props.modelValue[option.key] || ''
})

// 防抖搜索
const debouncedSearch = useDebounceFn((query: string) => {
  emit('search', query)
}, 300)

watch(searchQuery, (newQuery) => {
  debouncedSearch(newQuery)
})

watch(filters, (newFilters) => {
  emit('filter', { ...newFilters })
  emit('update:modelValue', { search: searchQuery.value, ...newFilters })
}, { deep: true })

function clearFilters() {
  searchQuery.value = ''
  props.filterOptions.forEach(option => {
    filters[option.key] = ''
  })
}
</script> 