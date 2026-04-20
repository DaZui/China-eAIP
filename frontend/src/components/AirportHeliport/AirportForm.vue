<template>
  <select class="form-select" multiple v-model="store.selectedAirportsHeliports">
    <optgroup v-for="prefix in groups" :label="prefix" :key="prefix">
      <option
        :key="airport.id"
        :value="airport"
        class="monospace"
        v-for="airport of store.allAirportsHeliports.filter((x) =>
          x.properties.aixm_location_indicator_icao.startsWith(prefix),
        )"
      >
        {{ airport.properties.aixm_location_indicator_icao }}
        {{ airport.properties.aixm_designator_iata }} {{ airport.properties.aixm_name_display }}
      </option>
    </optgroup>
  </select>

  <AirportHint
    verbose
    :airport="airport"
    :key="idx"
    v-for="(airport, idx) in store.selectedAirportsHeliports"
  />
</template>

<script setup lang="ts">
import { useGreatCircleMapStore } from '@/stores/GreatCircleMap'
import { onMounted, ref, type Ref } from 'vue'
import AirportHint from './AirportHint.vue'

const store = useGreatCircleMapStore()
const groups: Ref<string[]> = ref(['ZB', 'ZG', 'ZH', 'ZJ', 'ZL', 'ZP', 'ZS', 'ZU', 'ZW', 'ZY'])

onMounted(async function () {
  store.allAirportsHeliports = []
  const response = await fetch(
    `/api/china-eaip-datasets/${store.selectedChinaEaipDataset}/AirportHeliport/elements`,
  )
  store.allAirportsHeliports = await response.json()
})
</script>
