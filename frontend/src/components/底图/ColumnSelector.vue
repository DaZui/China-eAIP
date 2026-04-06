<template>
  <div class="row mb-3" v-if="options.length > 0">
    <label class="col-form-label text-end" :class="[labelWidth]">{{ label }}</label>
    <div :class="[inputWidth]">
      <select class="form-select" v-model="model">
        <option v-for="[a, b] in options" :key="a" :value="a">{{ b }}</option>
      </select>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, type ComputedRef } from 'vue'

const model = defineModel()
const props = defineProps<{
  size: 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | null
  label: string
  options: [string, string][]
}>()

const labelWidth: ComputedRef<string> = computed((): string =>
  props.size ? `col-${props.size}` : 'col',
)

const inputWidth: ComputedRef<string> = computed((): string =>
  props.size ? `col-${12 - props.size}` : 'col',
)
</script>
