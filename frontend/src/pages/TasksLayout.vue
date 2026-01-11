<template>
  <div>
    <h1>Задачи</h1>

    <div style="display:flex; gap: 10px; margin: 12px 0;">
      <RouterLink to="/tasks">Список</RouterLink>
      <RouterLink to="/tasks/new">Создать</RouterLink>
    </div>

    <div style="padding: 12px; border: 1px dashed #ccc; border-radius: 12px;">
      <!-- Вот это ключ: тут рендерится дочерняя "страница" -->
      <RouterView />
    </div>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>
