<template>
  <div class="card">
    <div class="card-body">
      <h5 class="card-title">{{ airspace.aixm_name }}</h5>
      <h6 class="card-subtitle mb-2 text-body-secondary">
        {{ airspace.aixm_designator }}
        {{ airspace.aixm_type }}
      </h6>
      <h6 class="card-subtitle mb-2 text-body-secondary">
        <!-- {{ airspace.geometry.coordinates[1].toFixed(6) }}°N,
        {{ airspace.geometry.coordinates[0].toFixed(6) }}°E -->
      </h6>
      <p class="card-text"></p>
      <table class="table table-sm spread">
        <tbody>
          <DisplayList v-for="([a, c], idx) in items" :key="idx" :title="a" :items="c" />
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { type Airspace } from '@/stores/types'
import { computed, type ComputedRef } from 'vue'
import DisplayList from '../DisplayList.vue'

const props = defineProps<{ airspace: Airspace }>()

const items: ComputedRef<[string, string[]][]> = computed(() => [
  ['Version', [`${props.airspace.aixm_sequence_number}.${props.airspace.aixm_correction_number}`]],
  [
    'Validity',
    [
      `Since ${props.airspace.information_valid_since}`,
      `Until ${props.airspace.information_valid_until}`,
    ],
  ],
])
</script>

<style scoped>
.spread td {
  text-align: end;
}
</style>
