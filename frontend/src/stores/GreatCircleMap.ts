import type { LatLngLiteral } from 'leaflet'
import { defineStore } from 'pinia'
import { computed, ref, type ComputedRef, type Ref } from 'vue'
import type { AirportHeliport, Airspace, BaselineDataPackage } from './types'
import type { TemperatureUnits } from './units'
import { convertTemperature } from './units'

export const useGreatCircleMapStore = defineStore('great-circle-map', () => {
  const 国内模式: ComputedRef<boolean> = computed(() =>
    window.location.hostname.endsWith('lihanming.cn'),
  )

  const 温度单位: Ref<TemperatureUnits> = ref('°C')
  const 底图语言: Ref<'zh-CN' | 'en-US' | string> = ref('zh-CN')
  const 底图风格: Ref<'street' | 'satellite' | 'hybrid' | 'terrain'> = ref('street')
  const 底图边界标准: Ref<'cn' | 'us' | 'aq' | 'jp'> = ref('cn')
  const 底图提供商: Ref<'高德' | 'Google' | 'OpenStreetMap'> = ref(
    国内模式.value ? '高德' : 'Google',
  )
  const 底图缩放: Ref<number> = ref(2)
  const 底图中心: Ref<LatLngLiteral> = ref({ lat: 23, lng: 113 })
  const 显示设置界面: Ref<boolean> = ref(true)
  const 使用中国坐标: Ref<'wgs84' | 'gcj02'> = ref(国内模式.value ? 'gcj02' : 'wgs84')

  function 转换温度(value: number | null): string {
    const elevation = convertTemperature(value, 温度单位.value)
    return elevation ? `${elevation.toFixed(1)} ${温度单位.value}` : 'Not Available'
  }

  const allChinaEaipDatasets: Ref<BaselineDataPackage[]> = ref([])
  const selectedChinaEaipDataset: Ref<string> = ref('')

  async function fetchChinaEaipDatasets() {
    const response = await fetch(`/api/china-eaip-datasets`)
    allChinaEaipDatasets.value = await response.json()
  }

  const allAirportsHeliports: Ref<AirportHeliport[]> = ref([])
  const selectedAirportsHeliports: Ref<AirportHeliport[]> = ref([])

  const allAirspaces: Ref<Airspace[]> = ref([])
  const selectedAirspaces: Ref<Airspace[]> = ref([])

  return {
    底图边界标准,
    底图风格,
    底图缩放,
    底图提供商,
    底图语言,
    底图中心,
    国内模式,
    使用中国坐标,
    温度单位,
    显示设置界面,
    转换温度,
    allAirportsHeliports,
    allAirspaces,
    allChinaEaipDatasets,
    fetchChinaEaipDatasets,
    selectedAirportsHeliports,
    selectedAirspaces,
    selectedChinaEaipDataset,
  }
})
