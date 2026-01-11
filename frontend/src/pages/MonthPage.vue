<template>
  <div>
    <h1>Месяц</h1>

    <p v-if="loading">Загрузка...</p>
    <p v-else-if="error" style="color:crimson;">{{ error }}</p>

    <table v-else style="width:100%; border-collapse:collapse;">
      <thead>
        <tr>
          <th style="text-align:left; border-bottom:1px solid #ddd; padding:8px;">Дата</th>
          <th style="text-align:left; border-bottom:1px solid #ddd; padding:8px;">Баллы</th>
          <th style="text-align:left; border-bottom:1px solid #ddd; padding:8px;">Выполнено</th>
          <th style="text-align:left; border-bottom:1px solid #ddd; padding:8px;">Статус</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="d in days" :key="d.day">
          <td style="padding:8px; border-bottom:1px solid #eee;">{{ d.day }}</td>
          <td style="padding:8px; border-bottom:1px solid #eee;">{{ d.score }}/100</td>
          <td style="padding:8px; border-bottom:1px solid #eee;">{{ d.completed_count }}/{{ d.total_count }}</td>
          <td style="padding:8px; border-bottom:1px solid #eee;">
            <span v-if="d.failed" style="color:crimson; font-weight:600;">провал</span>
            <span v-else style="font-weight:600;">ок</span>
          </td>
        </tr>

        <tr v-if="days.length === 0">
          <td colspan="4" style="padding:10px; opacity:0.7;">Пока нет сохранённых дней.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { fetchMonthLogs } from '../api'

const loading = ref(false)
const error = ref('')
const days = ref([])

async function load() {
  loading.value = true
  error.value = ''
  try {
    days.value = await fetchMonthLogs()
  } catch (e) {
    error.value = e.message || 'Ошибка'
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>
