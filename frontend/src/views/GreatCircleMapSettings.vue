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
          <AipForm v-else-if="currentOption === 1" />
          <AirportForm v-else-if="currentOption === 2" />

          <template v-for="[category, items] in store.项目s" :key="category">
            <div class="card mb-3" v-for="(item, idx) in items" :key="idx">
              <div class="card-header">
                <div class="row">
                  <div class="col">{{ category }} #{{ idx + 1 }}</div>
                  <div class="col text-end">
                    <button
                      type="button"
                      class="btn-close btn-small"
                      @click="store.删除项目(category, idx)"
                    ></button>
                  </div>
                </div>
              </div>
              <div class="card-body" v-html="item.description"></div>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, type ComputedRef, type Ref } from 'vue'
import AipForm from '../components/AipForm.vue'
import AirportForm from '../components/AirportForm.vue'
import TileLayerSelector from '../components/底图/TileLayerSelector.vue'
import { useGreatCircleMapStore } from '../stores/GreatCircleMap'

const store = useGreatCircleMapStore()
const currentOption: Ref<number> = ref(0)
const options: ComputedRef<string[]> = computed(() =>
  store.selectedChinaEaipDataset === ''
    ? store.国内模式
      ? ['地图设置', 'AIP']
      : ['Base Map', 'AIP']
    : store.国内模式
      ? ['地图设置', 'AIP', '机场']
      : ['Base Map', 'AIP', 'Airport / Heliport'],
)
</script>

<style lang="css" scoped>
.nowrap {
  white-space: pre-line;
}
</style>
