<template>
  <div
    class="card font-monospace"
    :class="{
      'text-bg-danger': 状态 === 'Expired',
      'text-bg-warning': 状态 === 'Upcoming',
    }"
  >
    <div class="card-header">
      {{ 属性.名称 }} <span class="badge text-bg-secondary">{{ 状态 }}: {{ 版本号 }}</span>
    </div>

    <div class="card-body">
      <div class="row">
        <div class="col-5">{{ 属性.ICAO代码 }}</div>
        <div class="col-7 text-end">{{ airport.geometry.coordinates[1].toFixed(5) }}°N</div>
        <div class="col-5">{{ 属性.IATA代码 }}</div>
        <div class="col-7 text-end">{{ airport.geometry.coordinates[0].toFixed(5) }}°E</div>
        <div class="col-6">{{ convertLength(属性.海拔) }}</div>
        <div class="col-6 text-end fst-italic">{{ convertLength(属性.海拔, 1, 'ft') }}</div>
        <div class="col-6">{{ convertTemperature(referenceTemperature) }}</div>
        <div class="col-6 text-end fst-italic">
          {{ convertTemperature(referenceTemperature, 1, '°F') }}
        </div>
      </div>

      <div
        v-show="verbose"
        v-for="([title, value], idx) in [
          ['Magnetic Variation', 属性.aixm_magnetic_variation_display.join(' ')],
        ].concat(属性.notes)"
        :key="idx"
      >
        <div class="fst-italic">{{ title }}:</div>
        <div class="text-end">{{ value }}</div>
      </div>
    </div>

    <ul
      class="list-group list-group-flush"
      :class="{
        'list-group-item-danger': 状态 === 'Expired',
        'list-group-item-warning': 状态 === 'Upcoming',
      }"
    >
      <li class="list-group-item" v-for="(runway, idx) in 属性.runways" :key="idx">
        <div>
          RWY {{ runway.aixm_designator }}
          <span class="badge text-bg-secondary">v{{ runway.大版本号 }}.{{ runway.小版本号 }}</span>
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
          <div class="text-end">Since {{ runway.有效期自.slice(2, 16) }}Z</div>
          <div class="text-end">Until {{ runway.有效期至.slice(2, 16) }}Z</div>
        </div>
      </li>
    </ul>
    <div class="card-footer text-end" v-if="verbose">
      <div>Since {{ 属性.有效期自.slice(2, 16) }}Z</div>
      <div>Until {{ 属性.有效期至.slice(2, 16) }}Z</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useGreatCircleMapStore } from '@/stores/GreatCircleMap'
import { type AirportHeliport, type AirportHeliportProperties } from '@/stores/types'
import { convertLength, convertTemperature } from '@/stores/units'
import { computed, type ComputedRef } from 'vue'

const store = useGreatCircleMapStore()
const props = defineProps<{ airport: AirportHeliport; verbose?: boolean }>()
const 属性: ComputedRef<AirportHeliportProperties> = computed(() => props.airport.properties)
const 状态: ComputedRef<'Upcoming' | 'Expired' | 'Current'> = computed(() =>
  store.判断时间范围(属性.value.有效期自, 属性.value.有效期至),
)
const 版本号: ComputedRef<string> = computed(() => `v${属性.value.大版本号}.${属性.value.小版本号}`)
const referenceTemperature: ComputedRef<number | null> = computed(() => 属性.value.温度)
</script>

<style scoped>
.spread td {
  text-align: end;
}
</style>
