<template>
  <div>
    <h1>Dowell</h1>
    <p>Winter Arc Checker — контроль дисциплины на месяц.</p>

    <button @click="goToTasks">
      Перейти к задачам
    </button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function goToTasks() {
  router.push({ name: 'tasks' })
}
</script>
