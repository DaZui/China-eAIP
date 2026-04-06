<template>
  <LTileLayer v-bind="params" detect-retina v-if="store.底图提供商 === '高德'" />
  <LTileLayer v-bind="params" detect-retina v-else-if="store.底图提供商 === 'Google'" />
  <LTileLayer v-bind="params" detect-retina v-else />
</template>

<script setup lang="ts">
import { useGreatCircleMapStore } from '@/stores/GreatCircleMap'
import { LTileLayer } from '@vue-leaflet/vue-leaflet'
import { computed, type ComputedRef } from 'vue'

const store = useGreatCircleMapStore()

interface Property {
  'layer-type': 'base'
  subdomains: string
  url: string
}

const url: ComputedRef<string> = computed((): string => {
  const params = new URLSearchParams({ x: '{x}', y: '{y}', z: '{z}' })
  if (store.底图提供商 === '高德') {
    params.set('style', store.底图风格 === 'satellite' ? '6' : '7')
    params.set('lang', store.底图语言 === 'zh-CN' ? 'zh_CN' : 'en')
    return `https://wprd0{s}.is.autonavi.com/appmaptile?${decodeURIComponent(`${params}`)}`
  } else if (store.底图提供商 === 'Google') {
    params.set('hl', store.底图语言)
    params.set('gl', store.底图边界标准)
    params.set('lyrs', { satellite: 's', hybrid: 'y', terrain: 'p', street: 'm' }[store.底图风格])
    return `https://mts{s}.google.com/vt?${decodeURIComponent(`${params}`)}`
  } else return `https://{s}.tile.${store.底图提供商}.org/{z}/{x}/{y}.png`
})

const subdomains: ComputedRef<string> = computed((): string =>
  store.底图提供商 === '高德' ? '1234' : store.底图提供商 === 'Google' ? '0123' : 'abc',
)

const params: ComputedRef<Property> = computed(
  (): Property => ({ 'layer-type': 'base', subdomains: subdomains.value, url: url.value }),
)
</script>
