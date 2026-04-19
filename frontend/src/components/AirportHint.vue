<template>
  <div class="card">
    <div class="card-body">
      <h5 class="card-title">{{ airport.properties.aixm_name_display }}</h5>
      <h6 class="card-subtitle mb-2 text-body-secondary">
        {{ airport.properties.aixm_designator_iata }} /
        {{ airport.properties.aixm_location_indicator_icao }}
      </h6>
      <h6 class="card-subtitle mb-2 text-body-secondary">
        {{ airport.geometry.coordinates[1].toFixed(6) }}°N,
        {{ airport.geometry.coordinates[0].toFixed(6) }}°E
      </h6>
      <p class="card-text"></p>
      <table class="table table-sm spread">
        <tbody>
          <tr>
            <th>Field Elevation</th>
            <td>{{ store.转换高度(airport.properties.aixm_field_elevation) }}</td>
          </tr>
          <tr>
            <th>Reference Temperature</th>
            <td>{{ store.转换温度(airport.properties.aixm_reference_temperature_in_celcius) }}</td>
          </tr>
          <DisplayList
            v-for="([a, b, c], idx) in items"
            :key="idx"
            :title="a"
            :horizontal="b"
            :items="c"
          />
        </tbody>
      </table>
    </div>
  </div>
</template>
<script setup lang="ts">
import { useGreatCircleMapStore } from '@/stores/GreatCircleMap'
import type { 机场 } from '@/stores/types'
import { computed, type ComputedRef } from 'vue'
import DisplayList from './DisplayList.vue'

const store = useGreatCircleMapStore()
const props = defineProps<{ airport: 机场 }>()

const items: ComputedRef<[string, boolean, string[]][]> = computed(() => [
  ['Magnetic Variation', false, props.airport.properties.aixm_magnetic_variation_display],
  [
    'Annotations',
    false,
    props.airport.properties.aixm_annotations.split(/[:,]/).map((x) => x.trim()),
  ],
  [
    'Version',
    false,
    [
      `Version ${props.airport.properties.aixm_sequence_number}.${props.airport.properties.aixm_correction_number}`,
    ],
  ],
  [
    'Validity',
    false,
    [
      `Since ${props.airport.properties.information_valid_since}`,
      `Until ${props.airport.properties.information_valid_until}`,
    ],
  ],
])
</script>
<style scoped>
.spread td {
  text-align: end;
}
</style>
