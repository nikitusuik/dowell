<template>
  <div>
    <h2>Создать задачу</h2>
    <TaskForm submitText="Создать" @submit="submit" />
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import TaskForm from '../components/TaskForm.vue'
import { createTask } from '../api'

const router = useRouter()

async function submit(payload) {
  try {
    await createTask(payload)
    router.push({ name: 'tasks' }) // программная навигация
  } catch (e) {
    alert(e.message || 'Ошибка создания')
  }
}
</script>
