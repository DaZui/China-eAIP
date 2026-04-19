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
          <DisplayList v-for="([a, c], idx) in items" :key="idx" :title="a" :items="c" />
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useGreatCircleMapStore } from '@/stores/GreatCircleMap'
import { type AirportHeliport } from '@/stores/types'
import { computed, type ComputedRef } from 'vue'
import DisplayList from '../DisplayList.vue'

const store = useGreatCircleMapStore()
const props = defineProps<{ airport: AirportHeliport }>()

const items: ComputedRef<[string, string[]][]> = computed(() => [
  ['Field Elevation', [store.转换高度(props.airport.properties.aixm_field_elevation)]],
  [
    'Reference Temperature',
    [store.转换温度(props.airport.properties.aixm_reference_temperature_in_celcius)],
  ],
  ['Magnetic Variation', props.airport.properties.aixm_magnetic_variation_display],
  ['Annotations', props.airport.properties.aixm_annotations.split(/[:,]/).map((x) => x.trim())],
  [
    'Version',
    [
      `${props.airport.properties.aixm_sequence_number}.${props.airport.properties.aixm_correction_number}`,
    ],
  ],
  [
    'Validity',
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
