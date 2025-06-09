<template>
  <form @submit.prevent="onSubmit" class="space-y-4">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700">姓名</label>
        <input v-model="form.name" type="text" required class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary" />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700">工号</label>
        <input v-model="form.employee_id" type="text" required class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary" />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700">部门</label>
        <input v-model="form.department" type="text" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary" />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700">职称</label>
        <input v-model="form.position" type="text" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary" />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700">入职日期</label>
        <input v-model="form.hire_date" type="date" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary" />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700">电话</label>
        <input v-model="form.phone" type="tel" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary" />
      </div>
    </div>
    <div class="flex justify-end space-x-2">
      <button type="button" @click="onCancel" class="px-4 py-2 border rounded-md text-gray-700 hover:bg-gray-100">取消</button>
      <button type="submit" class="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary-dark">{{ submitLabel }}</button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { reactive, watch, toRefs } from 'vue'

const props = defineProps({
  modelValue: { type: Object as () => Record<string, any>, default: () => ({}) },
  submitLabel: { type: String, default: '保存' }
})
const emit = defineEmits<{
  (e: 'update:modelValue', value: Record<string, any>): void
  (e: 'submit', value: Record<string, any>): void
  (e: 'cancel'): void
}>()

const form = reactive({
  name: '', employee_id: '', department: '', position: '', hire_date: '', phone: '',
  ...props.modelValue
})

watch(() => props.modelValue, (v) => Object.assign(form, v))

function onSubmit() {
  emit('update:modelValue', { ...form })
  emit('submit', { ...form })
}
function onCancel() {
  emit('cancel')
}
</script> 