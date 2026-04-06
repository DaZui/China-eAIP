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
        :geojson="store.转换Feature(item)"
      >
        <LPopup><AirportHint :airport="item" /></LPopup>
        <LTooltip><AirportHint :airport="item" /></LTooltip>
      </LGeoJson>

      <template v-for="[category, items] in store.项目s" :key="category">
        <LGeoJson v-for="(item, idx) in items" :key="idx" :geojson="store.转换Feature(item.object)">
          <LPopup :content="item.description" />
          <LTooltip :content="item.description" />
        </LGeoJson>
      </template>
    </LMap>
  </div>
</template>
<script setup lang="ts">
import { LGeoJson, LMap, LPopup, LTooltip } from '@vue-leaflet/vue-leaflet'
import 'leaflet/dist/leaflet.css'
import TileLayerBase from '../components/底图/TileLayerBase.vue'
import AirportHint from '../components/AirportHint.vue'
import { useGreatCircleMapStore } from '../stores/GreatCircleMap'
import GreatCircleMapSettings from './GreatCircleMapSettings.vue'
const store = useGreatCircleMapStore()
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
