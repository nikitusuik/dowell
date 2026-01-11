<template>
  <div style="display:flex; flex-direction:column; gap:12px;">
    <p v-if="tasks.length === 0">Пока нет задач.</p>

    <TaskItem
      v-for="t in tasks"
      :key="t.id"
      :task="t"
      @edit="$emit('edit', $event)"
      @remove="$emit('remove', $event)"
    />
  </div>
</template>

<script setup>
import TaskItem from './TaskItem.vue'

defineProps({
  tasks: { type: Array, required: true }
})

defineEmits(['edit', 'remove'])
</script>
