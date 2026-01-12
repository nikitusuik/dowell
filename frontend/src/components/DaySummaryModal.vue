<template>
  <div v-if="open" class="overlay" @click.self="$emit('close')">
    <div class="modal">
      <h2>Итоги дня</h2>

      <div class="row" style="margin-bottom:12px;">
        <span class="badge">Баллы: {{ score }}/100</span>
        <span
          class="badge"
          :style="{ color: failed ? 'var(--bad)' : 'var(--ok)' }"
        >
          {{ failed ? 'День провален' : 'День выполнен' }}
        </span>
        <span class="badge">
          {{ completedCount }} / {{ totalCount }} задач
        </span>
      </div>

      <div class="list">
        <div
          v-for="r in rows"
          :key="r.id"
          class="row-item"
        >
          <div>
            <strong>{{ r.title }}</strong>
            <div class="muted">
              {{ r.value }} {{ r.unit }} /
              min {{ r.min_value }} · target {{ r.target_value }}
            </div>
          </div>

          <div>
            <span v-if="r.passed" style="color:var(--ok)">✔</span>
            <span v-else style="color:var(--bad)">✘</span>
          </div>
        </div>
      </div>

      <div style="margin-top:14px; text-align:right;">
        <button class="btn-primary" @click="$emit('close')">
          Закрыть
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  open: Boolean,
  score: Number,
  failed: Boolean,
  completedCount: Number,
  totalCount: Number,
  rows: Array,
})

defineEmits(['close'])
</script>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  width: 100%;
  max-width: 620px;
  background: #0b1020 !important;
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 16px;
}


.list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.row-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-radius: 12px;
  background: rgba(255,255,255,0.05);
  border: 1px solid var(--line);
}

.muted {
  font-size: 13px;
  color: var(--muted);
}
</style>
