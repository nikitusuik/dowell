<template>
  <header class="card" style="display:flex; justify-content:space-between; align-items:center; gap:12px;">
    <div style="display:flex; flex-direction:column;">
      <strong style="font-size:18px;">Dowell</strong>
      <small style="color:var(--muted);">Winter Arc • дисциплина на месяц</small>
    </div>

    <nav style="display:flex; gap:12px; flex-wrap:wrap; justify-content:flex-end;">
      <RouterLink to="/" class="badge">Сегодня</RouterLink>
      <RouterLink to="/tasks" class="badge">Задачи</RouterLink>
      <RouterLink to="/tasks/new" class="badge">Создать</RouterLink>
      <RouterLink to="/month" class="badge">Месяц</RouterLink>
    </nav>
  </header>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>
