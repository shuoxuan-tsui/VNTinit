<template>
  <Modal
    :show="show"
    :title="title"
    :icon="icon"
    :type="type"
    size="sm"
    @close="onCancel"
  >
    <div class="text-sm text-gray-500">
      {{ message }}
    </div>

    <template #footer>
      <button
        @click="onCancel"
        class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
      >
        {{ cancelText }}
      </button>
      <button
        @click="onConfirm"
        :class="confirmButtonClasses"
        class="px-4 py-2 text-sm font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2"
      >
        {{ confirmText }}
      </button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  show: boolean
  title?: string
  message: string
  type?: 'default' | 'success' | 'warning' | 'danger'
  confirmText?: string
  cancelText?: string
  icon?: string
}

const props = withDefaults(defineProps<Props>(), {
  title: '确认操作',
  type: 'default',
  confirmText: '确认',
  cancelText: '取消'
})

const emit = defineEmits<{
  (e: 'confirm'): void
  (e: 'cancel'): void
  (e: 'update:show', value: boolean): void
}>()

const confirmButtonClasses = computed(() => {
  const classes = {
    default: 'text-white bg-primary hover:bg-primary-dark focus:ring-primary',
    success: 'text-white bg-green-600 hover:bg-green-700 focus:ring-green-500',
    warning: 'text-white bg-yellow-600 hover:bg-yellow-700 focus:ring-yellow-500',
    danger: 'text-white bg-red-600 hover:bg-red-700 focus:ring-red-500'
  }
  return classes[props.type]
})

function onConfirm() {
  emit('confirm')
  emit('update:show', false)
}

function onCancel() {
  emit('cancel')
  emit('update:show', false)
}
</script> 