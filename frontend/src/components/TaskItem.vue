<template>
  <div style="display:flex; justify-content:space-between; gap:12px; padding:12px; border:1px solid #eee; border-radius:12px;">
    <div>
      <div style="display:flex; gap:8px; align-items:center;">
        <strong>{{ task.title }}</strong>
        <span v-if="task.important" title="Важно">⭐</span>
        <span v-if="!task.active" style="opacity:0.6;">(не в челлендже)</span>
      </div>

      <div style="opacity:0.8;">
        {{ task.unit }} • min: {{ task.min_value }} • target: {{ task.target_value }} • weight: {{ task.weight }}
      </div>

      <div v-if="task.description" style="margin-top:6px; opacity:0.9;">
        {{ task.description }}
      </div>
    </div>

    <div style="display:flex; flex-direction:column; gap:8px; min-width:180px;">
      <button @click="$emit('edit', task.id)">Редактировать</button>

      <button @click="$emit('toggle-active', task.id)">
        {{ task.active ? 'Убрать из челленджа' : 'Вернуть в челлендж' }}
      </button>

      <button @click="$emit('remove', task.id)">Удалить</button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  task: { type: Object, required: true }
})

defineEmits(['edit', 'remove', 'toggle-active'])
</script>
