<template>
  <div>
    <div v-if="loading" class="p-4 text-center">
      <div class="inline-flex items-center">
        <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-primary mr-3"></div>
        <span class="text-gray-600">加载中...</span>
      </div>
    </div>
    <table v-else class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th v-for="col in columns" :key="col.key" @click="col.sortable && onSort(col.key)"
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100">
            <div class="flex items-center space-x-1">
              <span>{{ col.label }}</span>
              <Icon v-if="col.sortable" :name="getSortIcon(col.key)" class="h-4 w-4 text-gray-400" />
            </div>
          </th>
          <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        <tr v-for="row in data" :key="row.id" class="hover:bg-gray-50 transition-colors">
          <td v-for="col in columns" :key="col.key" class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
            {{ row[col.key] }}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-right">
            <slot name="actions" :row="row" />
          </td>
        </tr>
      </tbody>
    </table>
    <div v-if="pagination.totalPages > 1" class="bg-white px-4 py-3 border-t border-gray-200 sm:px-6">
      <div class="flex items-center justify-between">
        <button @click="onPageChange(pagination.currentPage - 1)" :disabled="pagination.currentPage <= 1"
                class="px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50">
          上一页
        </button>
        <span class="text-sm text-gray-700">第 {{ pagination.currentPage }} / {{ pagination.totalPages }} 页</span>
        <button @click="onPageChange(pagination.currentPage + 1)" :disabled="pagination.currentPage >= pagination.totalPages"
                class="px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50">
          下一页
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

defineProps<{
  columns: Array<{ key: string; label: string; sortable?: boolean }>,
  data: any[],
  loading: boolean,
  pagination: { currentPage: number; totalPages: number }
}>()
const emit = defineEmits<{
  (e: 'sort', key: string): void
  (e: 'page-change', page: number): void
}>()

function onSort(key: string) {
  emit('sort', key)
}
function onPageChange(page: number) {
  emit('page-change', page)
}

const getSortIcon = (key: string) => {
  // placeholder: user can customize based on sort state
  return 'heroicons:arrow-down-tray'
}
</script> 