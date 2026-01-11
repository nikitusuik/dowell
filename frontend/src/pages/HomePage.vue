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
        <button :disabled="activeTasks.length === 0" @click="submitDay">
          Сохранить день
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
import { fetchTasks } from '../api'

const today = new Date().toLocaleDateString()

const loading = ref(false)
const error = ref('')

const tasks = ref([])

// results: объект вида { [taskId]: number }
const results = reactive({})

const modalOpen = ref(false)
const summary = reactive({
  score: 0,
  failed: false,
  completedCount: 0,
  totalCount: 0,
  rows: [],
})

const activeTasks = computed(() => tasks.value.filter(t => t.active))

const completedCount = computed(() => {
  return activeTasks.value.filter(t => {
    const v = Number(results[t.id])
    return Number.isFinite(v) && v >= Number(t.min_value)
  }).length
})

async function load() {
  loading.value = true
  error.value = ''
  try {
    tasks.value = await fetchTasks()

    // Подготовим results для активных задач (если ещё нет)
    for (const t of tasks.value) {
      if (results[t.id] === undefined) results[t.id] = null
    }
  } catch (e) {
    error.value = e.message || 'Ошибка загрузки'
  } finally {
    loading.value = false
  }
}

function submitDay() {
  const rows = activeTasks.value.map(t => {
    const value = Number(results[t.id])
    const safeValue = Number.isFinite(value) ? value : 0

    const passed = safeValue >= Number(t.min_value)
    const quality = Math.min(safeValue / Number(t.target_value), 1)

    return {
      id: t.id,
      title: t.title,
      unit: t.unit,
      min_value: t.min_value,
      target_value: t.target_value,
      weight: t.weight,
      value: Number.isFinite(value) ? value : null,
      passed,
      quality,
    }
  })

  const totalCount = rows.length
  const completedCountLocal = rows.filter(r => r.passed).length

  // день провален, если провалено больше 1 задачи
  const failedCount = rows.filter(r => !r.passed).length
  const failed = failedCount > 1

  // балл по весам (твой вариант: качество = min(value/target, 1))
  const sumWeight = rows.reduce((acc, r) => acc + Number(r.weight || 1), 0) || 1
  const weightedQuality = rows.reduce((acc, r) => acc + Number(r.weight || 1) * r.quality, 0)

  let score = Math.floor((weightedQuality / sumWeight) * 100)
  if (failed) score = 0

  summary.score = score
  summary.failed = failed
  summary.completedCount = completedCountLocal
  summary.totalCount = totalCount
  summary.rows = rows

  modalOpen.value = true
}

onMounted(load)
</script>
