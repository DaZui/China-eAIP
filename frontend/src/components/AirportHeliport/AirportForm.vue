<template>
  <select class="form-select" multiple v-model="store.selectedAirportsHeliports">
    <optgroup v-for="(airports, prefix) in grouped" :label="prefix" :key="prefix">
      <option :key="airport.id" :value="airport" class="font-monospace" v-for="airport of airports">
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
import type { AirportHeliport } from '@/stores/types'
import { computed, onMounted, type ComputedRef } from 'vue'
import AirportHint from './AirportHint.vue'

const store = useGreatCircleMapStore()

const grouped: ComputedRef<Record<'Current' | 'Upcoming' | 'Expired', AirportHeliport[]>> =
  computed(() => {
    const v: Record<'Current' | 'Upcoming' | 'Expired', AirportHeliport[]> = {
      Current: [],
      Upcoming: [],
      Expired: [],
    }

    for (const x of store.allAirportsHeliports) {
      if (x.properties.有效期至 <= store.参考时间输出) v.Expired.push(x)
      else if (x.properties.有效期自 > store.参考时间输出) v.Upcoming.push(x)
      else v.Current.push(x)
    }

    return v
  })
onMounted(async function () {
  store.allAirportsHeliports = []
  const response = await fetch(`/api/china-eaip-datasets/AirportHeliports`)
  store.allAirportsHeliports = await response.json()
})
</script>
