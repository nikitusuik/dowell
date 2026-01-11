<template>
  <div>
    <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
      <small>{{ label }}</small>
      <small>{{ percent }}%</small>
    </div>

    <div style="height:12px; border:1px solid #ddd; border-radius:999px; overflow:hidden;">
      <div :style="barStyle"></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  value: { type: Number, required: true }, // выполнено
  max: { type: Number, required: true },   // всего
  label: { type: String, default: 'Прогресс' },
})

const percent = computed(() => {
  if (props.max <= 0) return 0
  const p = Math.floor((props.value / props.max) * 100)
  return Math.max(0, Math.min(100, p))
})

const barStyle = computed(() => ({
  height: '100%',
  width: percent.value + '%',
  background: '#e11d48', // красный (в стиле winter arc), можно поменять позже
}))
</script>
