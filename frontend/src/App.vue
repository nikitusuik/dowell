<template>
  <div style="max-width: 900px; margin: 0 auto; padding: 16px;">
    <header style="display:flex; gap: 12px; align-items:center; margin-bottom: 16px;">
      <strong>Dowell</strong>

      <nav style="display:flex; gap: 10px;">
        <RouterLink to="/">Главная</RouterLink>
        <RouterLink to="/tasks">Задачи</RouterLink>
        <RouterLink to="/tasks/new">Создать</RouterLink>
        <RouterLink to="/month">Месяц</RouterLink>
      </nav>
    </header>

    <main style="padding: 12px; border: 1px solid #ddd; border-radius: 12px;">
      <RouterView />
    </main>

    <footer style="margin-top: 16px; opacity: 0.7;">
      <small>Dowell • SPA на Vue 3</small>
    </footer>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>
