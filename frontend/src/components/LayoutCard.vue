<template>
  <section class="card">
    <header v-if="$slots.header" style="margin-bottom:10px;">
      <slot name="header" />
    </header>

    <div>
      <slot />
    </div>

    <footer v-if="$slots.footer" style="margin-top:12px; color:var(--muted);">
      <slot name="footer" :meta="meta" />
    </footer>
  </section>
</template>

<script setup>
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
