<template>
  <div class="card my-3">
    <div class="card-body">
      <h5 class="card-title">{{ airport.properties.aixm_name_display }}</h5>
      <h6 class="card-subtitle mb-2 text-body-secondary">
        {{ airport.properties.aixm_location_indicator_icao }} /
        {{ airport.properties.aixm_designator_iata }}
      </h6>
      <h6 class="card-subtitle mb-2 text-body-secondary">
        {{ airport.geometry.coordinates[1].toFixed(6) }}°N,
        {{ airport.geometry.coordinates[0].toFixed(6) }}°E
      </h6>

      <table class="table table-sm spread">
        <tbody>
          <tr>
            <th>Field Elevation</th>
            <td colspan="2">
              {{ convertLength(airport.properties.aixm_field_elevation) }} /
              {{ convertLength(airport.properties.aixm_field_elevation, 1, 'ft') }}
            </td>
          </tr>
          <tr>
            <th>Reference Temperature</th>
            <td colspan="2">
              {{ convertTemperature(referenceTemperature) }} /
              {{ convertTemperature(referenceTemperature, 1, '°F') }}
            </td>
          </tr>
          <tr>
            <th>Magnetic Variation</th>
            <td colspan="2">{{ airport.properties.aixm_magnetic_variation_display.join(' ') }}</td>
          </tr>
          <tr>
            <th>Annotations</th>
            <td colspan="2">{{ airport.properties.aixm_annotations }}</td>
          </tr>
          <tr>
            <th>Version</th>
            <td colspan="2">
              v{{ airport.properties.aixm_sequence_number }}.{{
                airport.properties.aixm_correction_number
              }}
              ({{ airport.properties.information_valid_since }} ~
              {{ airport.properties.information_valid_until }})
            </td>
          </tr>
          <template v-for="(runway, idx) in airport.properties.runways" :key="idx">
            <tr>
              <th :rowspan="3">RWY {{ runway.aixm_designator }}</th>
              <th>Size</th>
              <td>
                <div v-for="unit in ['m', 'ft'] as const" :key="unit">
                  {{ convertLength(runway.长度, 0, unit) }} x
                  {{ convertLength(runway.宽度, 0, unit) }}

                  <span v-if="runway.路肩宽度[0]">
                    ({{ convertLength(runway.路肩宽度, 0, unit) }})
                  </span>
                </div>
              </td>
            </tr>
            <tr>
              <th>Annotations</th>
              <td>{{ runway.aixm_annotations }}</td>
            </tr>
            <tr>
              <th>Version</th>
              <td>
                v{{ runway.aixm_sequence_number }}.{{ runway.aixm_correction_number }} ({{
                  runway.information_valid_since
                }}
                ~ {{ runway.information_valid_until }})
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { type AirportHeliport } from '@/stores/types'
import { convertLength, convertTemperature } from '@/stores/units'
import { computed, type ComputedRef } from 'vue'

const props = defineProps<{ airport: AirportHeliport; verbose?: boolean }>()

const referenceTemperature: ComputedRef<number | null> = computed(
  () => props.airport.properties.aixm_reference_temperature_in_celcius,
)
</script>

<style scoped>
.spread td {
  text-align: end;
}
</style>
