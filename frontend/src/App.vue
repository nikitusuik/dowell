<template>
  <div class="container">
    <AppHeader />

    <div style="height:12px;"></div>

    <RouterView />

    <AppFooter />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'
</script>
