<template>
  <footer class="card" style="margin-top:12px; display:flex; justify-content:space-between; align-items:center; gap:12px; color:var(--muted);">
    <small>© {{ year }} Dowell</small>
    <small>Сделал: Никита Ригун</small>
  </footer>
</template>

<script setup>
const year = new Date().getFullYear()
</script>
