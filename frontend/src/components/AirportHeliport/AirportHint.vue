<template>
  <div class="card font-monospace">
    <div class="card-header">{{ airport.名称 }}</div>

    <div class="card-body">
      <div class="row">
        <div class="col-5">{{ airport.aixm_location_indicator_icao }}</div>
        <div class="col-7 text-end">{{ airport.geometry.coordinates[1].toFixed(5) }}°N</div>
        <div class="col-5">{{ airport.aixm_designator_iata }}</div>
        <div class="col-7 text-end">{{ airport.geometry.coordinates[0].toFixed(5) }}°E</div>
        <div class="col-6">{{ convertLength(airport.海拔) }}</div>
        <div class="col-6 text-end fst-italic">{{ convertLength(airport.海拔, 1, 'ft') }}</div>
        <div class="col-6">{{ convertTemperature(airport.aixm_reference_temperature) }}</div>
        <div class="col-6 text-end fst-italic">
          {{ convertTemperature(airport.aixm_reference_temperature, 1, '°F') }}
        </div>
      </div>

      <div
        v-show="verbose"
        v-for="([title, value], idx) in [['Magnetic Variation', `${airport.地磁偏角}`]].concat(
          airport.notes,
        )"
        :key="idx"
      >
        <div class="fst-italic">{{ title }}:</div>
        <div class="text-end">{{ value }}</div>
      </div>
    </div>

    <ul class="list-group list-group-flush" v-if="airport.跑道s.length > 0">
      <li class="list-group-item" v-for="(runway, idx) in airport.跑道s" :key="idx">
        <div>RWY{{ runway.aixm_designator }}</div>

        <div class="text-center">
          {{ runway.方向s.map((val) => `${val.aixm_true_bearing?.toFixed(2)}°`).join(' / ') }}
        </div>

        <div class="row">
          <div class="col-6">{{ convertLength(runway.长度, 0) }}</div>
          <div class="col-6 text-end fst-italic">{{ convertLength(runway.长度, 0, 'ft') }}</div>
          <div class="col">{{ convertLength(runway.宽度, 0) }}</div>
          <div class="col text-end fst-italic">{{ convertLength(runway.宽度, 0, 'ft') }}</div>
        </div>

        <div class="row" v-if="verbose && runway.路肩宽度[0]">
          <div class="col-6">{{ convertLength(runway.路肩宽度, 1) }}</div>
          <div class="col-6 text-end fst-italic">{{ convertLength(runway.路肩宽度, 1, 'ft') }}</div>
        </div>

        <div v-if="verbose">
          <div class="fst-italic">Surface from {{ runway.notes[0]![0][0] }}:</div>
          <div class="row" v-for="(x, idx) in runway.notes" :key="idx">
            <div class="col">
              <div>
                {{ convertLength([x[0][1], null], 0) }} - {{ convertLength([x[0][2], null], 0) }}
              </div>
              <div class="fst-italic">
                {{ convertLength([x[0][1], null], 0, 'ft') }} -
                {{ convertLength([x[0][2], null], 0, 'ft') }}
              </div>
            </div>
            <div class="col text-end">{{ x[0][3] }}</div>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { type AirportHeliport } from '@/stores/types'
import { convertLength, convertTemperature } from '@/stores/units'

defineProps<{ airport: AirportHeliport; verbose?: boolean }>()
</script>
