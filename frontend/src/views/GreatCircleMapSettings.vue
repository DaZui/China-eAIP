<template>
  <div class="modal" style="display: block">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h4 class="modal-title">{{ store.国内模式 ? '设置' : 'Settings' }}</h4>
          <button type="button" class="btn-close" @click="store.显示设置界面 = false"></button>
        </div>

        <div class="modal-body">
          <ul class="nav nav-tabs my-3">
            <li class="nav-item" v-for="(option, idx) in options" :key="idx">
              <button
                :class="{ active: currentOption === idx }"
                @click="currentOption = idx"
                class="nav-link"
              >
                {{ option }}
              </button>
            </li>
          </ul>
          <TileLayerSelector v-if="currentOption === 0" />
          <AirportForm v-else-if="currentOption === 1" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, type ComputedRef, type Ref } from 'vue'
import AirportForm from '../components/AirportHeliport/AirportForm.vue'
import TileLayerSelector from '../components/底图/TileLayerSelector.vue'
import { useGreatCircleMapStore } from '../stores/GreatCircleMap'

const store = useGreatCircleMapStore()
const currentOption: Ref<number> = ref(0)
const options: ComputedRef<string[]> = computed(() =>
  store.国内模式 ? ['地图设置', '机场 Airport / Heliport'] : ['Base Map', 'Airport / Heliport'],
)
</script>

<style lang="css" scoped>
.nowrap {
  white-space: pre-line;
}
</style>
