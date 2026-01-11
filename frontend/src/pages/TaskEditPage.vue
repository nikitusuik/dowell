<template>
  <div>
    <h1>Редактировать задачу</h1>
    <p>Тут будет форма редактирования для id = {{ id }}</p>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()
const id = route.params.id
</script>
