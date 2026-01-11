<template>
  <div>
    <h2>Редактировать задачу</h2>

    <p v-if="loading">Загрузка...</p>
    <p v-else-if="error" style="color:crimson;">{{ error }}</p>

    <TaskForm
      v-else
      :initial="task"
      submitText="Сохранить изменения"
      @submit="submit"
    />
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import TaskForm from '../components/TaskForm.vue'
import { fetchTask, updateTask } from '../api'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const error = ref('')
const task = ref(null)

async function load() {
  loading.value = true
  error.value = ''
  try {
    task.value = await fetchTask(route.params.id)
  } catch (e) {
    error.value = e?.message || 'Ошибка загрузки'
  } finally {
    loading.value = false
  }
}

async function submit(payload) {
  try {
    await updateTask(route.params.id, payload)
    router.push({ name: 'tasks' })
  } catch (e) {
    alert(e?.message || 'Ошибка сохранения')
  }
}

onMounted(load)
</script>
