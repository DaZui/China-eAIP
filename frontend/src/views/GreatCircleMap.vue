<template>
  <button
    class="btn btn-primary btn-lg"
    id="floating-button"
    type="button"
    @click="store.显示设置界面 = true"
  >
    ⚙
  </button>

  <GreatCircleMapSettings v-if="store.显示设置界面" />

  <div id="map">
    <LMap
      :options="{ attributionControl: false }"
      :use-global-leaflet="false"
      v-model:center="store.底图中心"
      v-model:zoom="store.底图缩放"
    >
      <TileLayerBase />

      <LGeoJson
        v-for="(item, idx) in store.selectedAirportsHeliports"
        :key="idx"
        :geojson="converter.convert(item.geometry)"
      >
        <LPopup><AirportHint :airport="item" /></LPopup>
        <LTooltip><AirportHint :airport="item" /></LTooltip>
      </LGeoJson>
    </LMap>
  </div>
</template>

<script setup lang="ts">
import AirportHint from '@/components/AirportHeliport/AirportHint.vue'
import TileLayerBase from '@/components/底图/TileLayerBase.vue'
import { useGreatCircleMapStore } from '@/stores/GreatCircleMap'
import { Converter } from '@/stores/wgsgcj'
import GreatCircleMapSettings from '@/views/GreatCircleMapSettings.vue'
import { LGeoJson, LMap, LPopup, LTooltip } from '@vue-leaflet/vue-leaflet'
import 'leaflet/dist/leaflet.css'
import { computed, type ComputedRef } from 'vue'

const store = useGreatCircleMapStore()

const converter: ComputedRef<Converter> = computed(
  () => new Converter(store.使用中国坐标, store.底图中心.lng),
)
</script>

<style scoped>
#floating-button {
  position: absolute;
  right: 5px;
  top: 5px;
  z-index: 1;
}

#map {
  height: 100%;
  left: 0%;
  overflow: hidden;
  position: absolute;
  top: 0%;
  width: 100%;
  z-index: 0;
}
</style>
