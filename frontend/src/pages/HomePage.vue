<template>
  <div>
    <h1>Dowell — сегодня</h1>
    <p style="opacity:0.8;">Дата: {{ today }}</p>

    <LayoutCard title="Прогресс дня" hint="Считается по количеству выполненных задач">
      <template #header>
        <strong>Прогресс</strong>
      </template>

      <ProgressBar :value="completedCount" :max="activeTasks.length" label="Выполнено задач" />

      <div style="margin-top:10px;">
        <button :disabled="activeTasks.length === 0 || submitting" @click="submitDay">
          {{ submitting ? 'Сохраняю...' : 'Сохранить день' }}
        </button>
      </div>

      <template #footer="{ meta }">
        <small>{{ meta.hint }}</small>
      </template>
    </LayoutCard>

    <div style="height:12px;"></div>

    <p v-if="loading">Загрузка задач...</p>
    <p v-else-if="error" style="color:crimson;">{{ error }}</p>

    <div v-else style="display:flex; flex-direction:column; gap:12px;">
      <p v-if="activeTasks.length === 0">
        Нет активных задач. Перейди в «Задачи» и включи хотя бы одну (active).
      </p>

      <DailyTaskRow
        v-for="t in activeTasks"
        :key="t.id"
        :task="t"
        v-model="results[t.id]"
      />
    </div>

    <DaySummaryModal
      :open="modalOpen"
      :score="summary.score"
      :failed="summary.failed"
      :completed-count="summary.completedCount"
      :total-count="summary.totalCount"
      :rows="summary.rows"
      @close="modalOpen = false"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import LayoutCard from '../components/LayoutCard.vue'
import ProgressBar from '../components/ProgressBar.vue'
import DailyTaskRow from '../components/DailyTaskRow.vue'
import DaySummaryModal from '../components/DaySummaryModal.vue'
import { fetchTasks, submitToday } from '../api'

const today = new Date().toLocaleDateString()

const loading = ref(false)
const submitting = ref(false)
const error = ref('')

const tasks = ref([])

// results: объект вида { [taskId]: number | null }
const results = reactive({})

const modalOpen = ref(false)
const summary = reactive({
  score: 0,
  failed: false,
  completedCount: 0,
  totalCount: 0,
  rows: [],
})

const activeTasks = computed(() => tasks.value.filter((t) => t.active))

const completedCount = computed(() => {
  return activeTasks.value.filter((t) => {
    const v = Number(results[t.id])
    return Number.isFinite(v) && v >= Number(t.min_value)
  }).length
})

async function load() {
  loading.value = true
  error.value = ''
  try {
    tasks.value = await fetchTasks()

    // подготовим results
    for (const t of tasks.value) {
      if (results[t.id] === undefined) results[t.id] = null
    }
  } catch (e) {
    error.value = e?.message || 'Ошибка загрузки'
  } finally {
    loading.value = false
  }
}

async function submitDay() {
  if (submitting.value) return
  submitting.value = true

  try {
    // 1) собираем payload
    const items = activeTasks.value.map((t) => ({
      task_id: t.id,
      value: results[t.id] ?? null,
    }))

    // 2) сохраняем на сервер
    const saved = await submitToday(items)

    // 3) строим данные для модалки
    const taskById = Object.fromEntries(activeTasks.value.map((t) => [t.id, t]))

    summary.score = saved.score
    summary.failed = saved.failed
    summary.completedCount = saved.completed_count
    summary.totalCount = saved.total_count

    summary.rows = saved.items.map((i) => {
      const t = taskById[i.task_id]
      return {
        id: i.task_id,
        title: t?.title ?? `Task ${i.task_id}`,
        unit: t?.unit ?? '',
        min_value: t?.min_value ?? 0,
        target_value: t?.target_value ?? 0,
        weight: t?.weight ?? 1,
        value: i.value,
        passed: i.passed,
        quality: i.quality,
      }
    })

    modalOpen.value = true
  } catch (e) {
    alert(e?.message || 'Ошибка сохранения дня')
  } finally {
    submitting.value = false
  }
}

onMounted(load)
</script>
