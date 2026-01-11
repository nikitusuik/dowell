<template>
  <form @submit.prevent="onSubmit" style="display:flex; flex-direction:column; gap:12px;">
    <div>
      <label>Заголовок *</label><br />
      <input v-model.trim="form.title" placeholder="Напр. Отжимания на кулаках" />
      <div v-if="errors.title" style="color:crimson;">{{ errors.title }}</div>
    </div>

    <div>
      <label>Описание</label><br />
      <textarea v-model.trim="form.description" rows="3" placeholder="Пояснение / техника / заметки"></textarea>
    </div>

    <div>
      <label>Единица измерения *</label><br />
      <select v-model="form.unit">
        <option value="reps">reps</option>
        <option value="pages">pages</option>
        <option value="glasses">glasses</option>
        <option value="minutes">minutes</option>
        <option value="km">km</option>
        <option value="custom">custom</option>
      </select>
    </div>

    <div style="display:flex; gap:12px; flex-wrap:wrap;">
      <div>
        <label>Минимум (порог) *</label><br />
        <input type="number" v-model.number="form.min_value" min="1" step="1" />
        <div v-if="errors.min_value" style="color:crimson;">{{ errors.min_value }}</div>
      </div>

      <div>
        <label>Цель (верхняя шкала) *</label><br />
        <input type="number" v-model.number="form.target_value" min="1" step="1" />
        <div v-if="errors.target_value" style="color:crimson;">{{ errors.target_value }}</div>
      </div>

      <div>
        <label>Вес (коэф.) *</label><br />
        <input type="number" v-model.number="form.weight" min="0.1" step="0.1" />
        <div v-if="errors.weight" style="color:crimson;">{{ errors.weight }}</div>
      </div>
    </div>

    <div>
      <label>Категория</label><br />
      <label><input type="radio" value="strength" v-model="form.category" /> strength</label>
      <label style="margin-left:10px;"><input type="radio" value="health" v-model="form.category" /> health</label>
      <label style="margin-left:10px;"><input type="radio" value="study" v-model="form.category" /> study</label>
      <label style="margin-left:10px;"><input type="radio" value="custom" v-model="form.category" /> custom</label>
    </div>

    <div>
      <label><input type="checkbox" v-model="form.important" /> Важно</label>
      <label style="margin-left:12px;"><input type="checkbox" v-model="form.active" /> В челлендже</label>
    </div>

    <button type="submit">{{ submitText }}</button>

    <div v-if="errors.form" style="color:crimson;">{{ errors.form }}</div>
  </form>
</template>

<script setup>
import { reactive } from 'vue'

const props = defineProps({
  submitText: { type: String, default: 'Сохранить' },
  initial: { type: Object, default: null },
})

const emit = defineEmits(['submit'])

const form = reactive({
  title: props.initial?.title ?? '',
  description: props.initial?.description ?? '',
  unit: props.initial?.unit ?? 'reps',
  min_value: props.initial?.min_value ?? 1,
  target_value: props.initial?.target_value ?? 1,
  weight: props.initial?.weight ?? 1.0,
  category: props.initial?.category ?? 'custom',
  important: props.initial?.important ?? false,
  active: props.initial?.active ?? true,
})

const errors = reactive({
  title: '',
  min_value: '',
  target_value: '',
  weight: '',
  form: '',
})

function validate() {
  errors.title = ''
  errors.min_value = ''
  errors.target_value = ''
  errors.weight = ''
  errors.form = ''

  if (!form.title.trim()) errors.title = 'Заголовок обязателен'
  if (!(form.min_value > 0)) errors.min_value = 'Минимум должен быть > 0'
  if (!(form.target_value > 0)) errors.target_value = 'Цель должна быть > 0'
  if (form.target_value < form.min_value) errors.target_value = 'Цель должна быть >= минимуму'
  if (!(form.weight > 0)) errors.weight = 'Вес должен быть > 0'

  return !(errors.title || errors.min_value || errors.target_value || errors.weight)
}

function onSubmit() {
  if (!validate()) return
  emit('submit', { ...form })
}
</script>
