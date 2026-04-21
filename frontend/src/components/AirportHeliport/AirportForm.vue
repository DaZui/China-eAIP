<template>
  <select class="form-select" multiple v-model="store.selectedAirportsHeliports">
    <optgroup
      v-for="prefix in ['B', 'G', 'H', 'J', 'L', 'P', 'S', 'U', 'W', 'Y']"
      :label="prefix"
      :key="prefix"
    >
      <option
        :key="airport.id"
        :value="airport"
        class="font-monospace"
        v-for="airport of store.allAirportsHeliports.filter(
          (x) => x.properties.ICAO代码.slice(1, 2) === prefix,
        )"
      >
        {{ airport.properties.ICAO代码 }}
        {{ airport.properties.IATA代码 }}
        {{ airport.properties.名称 }}
        ({{ airport.properties.大版本号 }}.{{ airport.properties.小版本号 }},
        {{ airport.properties.有效期自 }} ~ {{ airport.properties.有效期至 }})
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
