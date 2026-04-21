<template>
  <div class="card">
    <div class="card-header">{{ airport.名称 }}</div>

    <div class="card-body">
      <div class="row font-monospace">
        <div class="col-5">{{ airport.aixm_location_indicator_icao }}</div>
        <div class="col-7 text-end">{{ airport.坐标点.coordinates[1].toFixed(5) }}°N</div>
        <div class="col-5">{{ airport.aixm_designator_iata }}</div>
        <div class="col-7 text-end">{{ airport.坐标点.coordinates[0].toFixed(5) }}°E</div>
        <div class="col-6">{{ convertLength([airport.aixm_field_elevation, null]) }}</div>
        <div class="col-6 text-end fst-italic">
          {{ convertLength([airport.aixm_field_elevation, null], 1, 'ft') }}
        </div>
        <div class="col-6">{{ convertTemperature(airport.aixm_reference_temperature) }}</div>
        <div class="col-6 text-end fst-italic">
          {{ convertTemperature(airport.aixm_reference_temperature, 1, '°F') }}
        </div>
      </div>

      <div v-if="verbose && airport.aixm_magnetic_variation">
        <div class="fst-italic">Magnetic Variation:</div>
        <div class="text-end">{{ airport.aixm_magnetic_variation.toFixed(2) }}°</div>
        <div class="text-end" v-if="airport.aixm_date_magnetic_variation">
          Updated in {{ airport.aixm_date_magnetic_variation }}
        </div>
      </div>

      <div v-for="(items, key) in verbose ? airport.注解s : []" :key="key">
        <div class="fst-italic">{{ key }}:</div>
        <div class="text-end" v-for="(item, idx) in items" :key="idx">{{ item }}</div>
      </div>

      <div v-if="verbose && airport.用途s.length > 0">
        <div class="fst-italic">Availability:</div>

        <table class="table table-sm">
          <thead>
            <th>Military</th>
            <th>Purpose</th>
            <th>Rule</th>
            <th>Type</th>
          </thead>
          <tbody>
            <tr v-for="(item, idx) in airport.用途s" :key="idx">
              <td v-for="(value, idx2) in item" :key="idx2">{{ value }}</td>
            </tr>
          </tbody>
        </table>
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
