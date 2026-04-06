<template>
  <ColSelect
    v-if="!store.国内模式"
    :options="providers"
    :size="labelWidth"
    label="Provider"
    v-model="store.底图提供商"
  />
  <ColSelect
    :options="styles"
    :size="labelWidth"
    :label="store.国内模式 ? '风格' : 'Style'"
    v-model="store.底图风格"
  />
  <ColSelect
    :options="languages"
    :size="labelWidth"
    :label="store.国内模式 ? '语言' : 'Language'"
    v-model="store.底图语言"
  />
  <ColSelect
    v-if="!store.国内模式"
    :options="jurisdictions"
    :size="labelWidth"
    label="Jurisdiction"
    v-model="store.底图边界标准"
  />
</template>

<script setup lang="ts">
import { computed, ref, type ComputedRef, type Ref } from 'vue'
import { useGreatCircleMapStore } from '../../stores/GreatCircleMap'
import ColSelect from './ColumnSelector.vue'

const store = useGreatCircleMapStore()
const labelWidth: Ref<1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | null> = ref(3)

type Options = [string, string][]

const providers: Ref<Options> = ref([
  ['Google', 'Google Maps'],
  ['高德', '高德地图'],
  ['OpenStreetMap', 'OpenStreetMap'],
])

const styles: ComputedRef<Options> = computed(
  (): Options =>
    store.底图提供商 === 'Google'
      ? [
          ['street', 'Maps'],
          ['satellite', 'Satellite'],
          ['hybrid', 'Hybrid (Satellite with Labels)'],
          ['terrain', 'Terrain'],
        ]
      : store.底图提供商 === '高德'
        ? [
            ['street', '地图'],
            ['satellite', '卫星'],
          ]
        : [],
)

const languages: ComputedRef<Options> = computed(
  (): Options =>
    store.底图提供商 === 'Google'
      ? [
          ['en-US', 'English (United States)'],
          ['zh-CN', '中文 (中国大陆)'],
        ]
      : store.底图提供商 === '高德'
        ? [
            ['zh-CN', '简体中文'],
            ['en-US', '英语'],
          ]
        : [],
)

const jurisdictions: ComputedRef<Options> = computed(
  (): Options =>
    store.底图提供商 === 'Google'
      ? [
          ['aq', 'Antarctica'],
          ['cn', 'China'],
          ['jp', 'Japan'],
          ['us', 'United States'],
        ]
      : [],
)
</script>
