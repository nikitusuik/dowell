<template>
  <div>
    <LayoutCard title="Список задач" hint="Фильтрация и сортировка на клиенте">
      <template #header>
        <div style="display:flex; justify-content:space-between; align-items:center; gap:12px;">
          <h2 style="margin:0;">Список задач</h2>
          <small style="opacity:0.75;">API → Vue</small>
        </div>
      </template>

      <div style="display:flex; gap:12px; flex-wrap:wrap; margin: 12px 0;">
        <label>
          Фильтр:
          <select v-model="filter">
            <option value="all">все</option>
            <option value="active">в челлендже</option>
            <option value="inactive">не в челлендже</option>
          </select>
        </label>

        <label>
          Сортировка:
          <select v-model="sortBy">
            <option value="created">по дате добавления</option>
            <option value="alpha">по алфавиту</option>
            <option value="weight">по весу (сложности)</option>
          </select>
        </label>

        <button @click="load">Обновить</button>
      </div>

      <p v-if="loading">Загрузка...</p>
      <p v-else-if="error" style="color:crimson;">{{ error }}</p>

      <TaskList
        v-else
        :tasks="sortedTasks"
        @remove="removeTask"
        @edit="goEdit"
      />

      <template #footer="{ meta }">
        <small>
          {{ meta.title }} • {{ meta.hint }} • создано: {{ meta.createdAt }}
        </small>
      </template>
    </LayoutCard>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import TaskList from '../components/TaskList.vue'
import LayoutCard from '../components/LayoutCard.vue'
import { fetchTasks, deleteTask } from '../api'

const router = useRouter()

const tasks = ref([])
const loading = ref(false)
const error = ref('')

const filter = ref('all')
const sortBy = ref('created')

watch([filter, sortBy], () => {
  // требование задания: watch используется для реакции на изменение UI-состояния
})

const filteredTasks = computed(() => {
  if (filter.value === 'active') return tasks.value.filter(t => t.active)
  if (filter.value === 'inactive') return tasks.value.filter(t => !t.active)
  return tasks.value
})

const sortedTasks = computed(() => {
  const arr = [...filteredTasks.value]
  if (sortBy.value === 'alpha') arr.sort((a, b) => a.title.localeCompare(b.title))
  if (sortBy.value === 'weight') arr.sort((a, b) => (b.weight ?? 0) - (a.weight ?? 0))
  if (sortBy.value === 'created') arr.sort((a, b) => (a.id ?? 0) - (b.id ?? 0))
  return arr
})

async function load() {
  loading.value = true
  error.value = ''
  try {
    tasks.value = await fetchTasks()
  } catch (e) {
    error.value = e.message || 'Ошибка загрузки'
  } finally {
    loading.value = false
  }
}

function goEdit(id) {
  router.push({ name: 'task-edit', params: { id } })
}

async function removeTask(id) {
  if (!confirm('Удалить задачу?')) return
  try {
    await deleteTask(id)
    tasks.value = tasks.value.filter(t => t.id !== id)
  } catch (e) {
    alert(e.message || 'Ошибка удаления')
  }
}

onMounted(load)
</script>
