<template>
  <section style="border:1px solid #ddd; border-radius:16px; padding:14px;">
    <!-- Именованный слот: заголовок -->
    <header v-if="$slots.header" style="margin-bottom:10px;">
      <slot name="header" />
    </header>

    <!-- Обычный слот: основное содержимое -->
    <div>
      <slot />
    </div>

    <!-- Scoped slot: отдаём наружу полезные данные -->
    <footer v-if="$slots.footer" style="margin-top:12px; opacity:0.85;">
      <slot name="footer" :meta="meta" />
    </footer>
  </section>
</template>

<script setup>
// Это данные, которые мы отдаём в scoped slot
const props = defineProps({
  title: { type: String, default: '' },
  hint: { type: String, default: '' },
})

const meta = {
  title: props.title,
  hint: props.hint,
  createdAt: new Date().toISOString(),
}
</script>
