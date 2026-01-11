<template>
  <div v-if="open" style="position:fixed; inset:0; background:rgba(0,0,0,0.35); display:flex; align-items:center; justify-content:center; padding:16px;">
    <div style="background:#fff; border-radius:16px; padding:16px; max-width:720px; width:100%;">
      <div style="display:flex; justify-content:space-between; align-items:center; gap:12px;">
        <h3 style="margin:0;">Итоги дня</h3>
        <button @click="$emit('close')">✖</button>
      </div>

      <p style="margin-top:10px;">
        <strong>Баллы:</strong> {{ score }}/100
        <span v-if="failed" style="color:crimson; font-weight:600;">(день провален)</span>
      </p>

      <p><strong>Выполнено:</strong> {{ completedCount }} / {{ totalCount }} ({{ progressPercent }}%)</p>

      <div style="display:flex; flex-direction:column; gap:8px; margin-top:12px;">
        <div v-for="row in rows" :key="row.id" style="padding:10px; border:1px solid #eee; border-radius:12px;">
          <div style="display:flex; justify-content:space-between; gap:10px;">
            <strong>{{ row.title }}</strong>
            <span v-if="row.passed">✅</span>
            <span v-else>❌</span>
          </div>
          <div style="opacity:0.85;">
            value: {{ row.value ?? '—' }} {{ row.unit }} • min {{ row.min_value }} • target {{ row.target_value }} • quality {{ row.quality.toFixed(2) }}
          </div>
        </div>
      </div>

      <div style="display:flex; justify-content:flex-end; margin-top:14px;">
        <button @click="$emit('close')">Закрыть</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  open: { type: Boolean, default: false },
  score: { type: Number, default: 0 },
  failed: { type: Boolean, default: false },
  completedCount: { type: Number, default: 0 },
  totalCount: { type: Number, default: 0 },
  rows: { type: Array, default: () => [] },
})

defineEmits(['close'])

const progressPercent = computed(() => {
  if (props.totalCount <= 0) return 0
  return Math.floor((props.completedCount / props.totalCount) * 100)
})
</script>
