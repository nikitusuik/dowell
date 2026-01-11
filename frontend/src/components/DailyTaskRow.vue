<template>
  <LayoutCard :title="task.title" :hint="hintText">
    <template #header>
      <div style="display:flex; justify-content:space-between; align-items:center; gap:10px;">
        <strong>{{ task.title }}</strong>
        <span v-if="task.important" title="Важно">⭐</span>
      </div>
    </template>

    <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
      <label>
        Сегодня:
        <input
          ref="inputRef"
          type="number"
          :placeholder="String(task.min_value)"
          v-model.number="localValue"
          min="0"
          step="1"
          style="width:110px;"
        />
      </label>

      <span style="opacity:0.8;">
        {{ task.unit }} • min: {{ task.min_value }} • target: {{ task.target_value }}
      </span>

      <span v-if="passed" style="font-weight:600;">✅ зачёт</span>
      <span v-else style="font-weight:600;">❌ не зачёт</span>
    </div>

    <template #footer="{ meta }">
      <small style="display:block;">
        {{ meta.title }} • {{ meta.hint }}
      </small>
    </template>
  </LayoutCard>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import LayoutCard from './LayoutCard.vue'

const props = defineProps({
  task: { type: Object, required: true },
  modelValue: { type: Number, default: null }, // значение "снаружи"
})

const emit = defineEmits(['update:modelValue'])

const inputRef = ref(null)

// локальная копия, чтобы удобно работать с v-model
const localValue = ref(props.modelValue)

// если родитель поменял modelValue — обновим локально
watch(
  () => props.modelValue,
  (v) => {
    localValue.value = v
  }
)

// когда локальное поменялось — отдаём наверх
watch(localValue, (v) => {
  emit('update:modelValue', v)
})

const passed = computed(() => {
  const v = Number(localValue.value)
  if (!Number.isFinite(v)) return false
  return v >= Number(props.task.min_value)
})

const hintText = computed(() => `Введите результат за сегодня (${props.task.unit})`)
</script>
