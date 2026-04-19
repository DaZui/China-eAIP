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
import { useGreatCircleMapStore } from '@/stores/GreatCircleMap'
import { type Airspace } from '@/stores/types'
import { computed, type ComputedRef } from 'vue'
import DisplayList from '../DisplayList.vue'

const store = useGreatCircleMapStore()
const props = defineProps<{ airspace: Airspace }>()

const items: ComputedRef<[string, string[]][]> = computed(() => [
  // ['Field Elevation', [store.转换高度(props.airspace.properties.aixm_field_elevation)]],
  // [
  //   'Reference Temperature',
  //   [store.转换温度(props.airspace.properties.aixm_reference_temperature_in_celcius)],
  // ],
  // ['Magnetic Variation', props.airspace.properties.aixm_magnetic_variation_display],
  // ['Annotations', props.airspace.properties.aixm_annotations.split(/[:,]/).map((x) => x.trim())],
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
