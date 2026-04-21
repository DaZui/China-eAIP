<template>
  <select class="form-select" multiple v-model="store.selectedAirportsHeliports">
    <optgroup
      v-for="prefix in ['B', 'G', 'H', 'J', 'L', 'P', 'S', 'U', 'W', 'Y']"
      :label="prefix"
      :key="prefix"
    >
      <option
        :key="airport.uuid"
        :value="airport"
        class="font-monospace"
        v-for="airport of store.allAirportsHeliports.filter(
          (x) => x.aixm_location_indicator_icao.slice(1, 2) === prefix,
        )"
      >
        {{ airport.aixm_location_indicator_icao }}
        {{ airport.aixm_designator_iata }}
        {{ airport.名称 }}
        ({{ airport.大版本号 }}.{{ airport.小版本号 }}, {{ airport.有效期自 }} ~
        {{ airport.有效期至 }})
      </option>
    </optgroup>
  </select>
  <div class="row row-cols-1 row-cols-md-2 g-4 my-1">
    <div class="col" :key="idx" v-for="(airport, idx) in store.selectedAirportsHeliports">
      <AirportHint class="h-100" verbose :airport="airport" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useGreatCircleMapStore } from '@/stores/GreatCircleMap'
import { onMounted } from 'vue'
import AirportHint from './AirportHint.vue'

const store = useGreatCircleMapStore()

onMounted(async function () {
  store.allAirportsHeliports = []
  const response = await fetch(
    `/api/china-eaip-datasets/AirportHeliports?timestamp=${store.参考时间输出}`,
  )
  store.allAirportsHeliports = await response.json()
})
</script>
