import type { LatLngLiteral } from 'leaflet'
import { defineStore } from 'pinia'
import { computed, ref, type ComputedRef, type Ref } from 'vue'
import type {
  BaselineDataPackage,
  Feature,
  FeatureCollection,
  Geometry,
  GeometryCollection,
  MultiLineString,
  MultiPoint,
  MultiPolygon,
  Point,
  Polygon,
  Position,
  机场,
} from './types'

interface Item {
  object: Geometry | GeometryCollection | Feature | FeatureCollection
  description: string
  category: string
}

const deg2rad: (v: number) => number = (v: number): number => (Math.PI / 180) * v
const rad2deg: (v: number) => number = (v: number): number => (180 / Math.PI) * v
const sin: (v: number) => number = (v: number): number => Math.sin(deg2rad(v))

const sin组合: (主数: number, 系数s: [number, number][]) => number = (
  主数: number,
  系数s: [number, number][],
): number =>
  系数s
    .map(([外系数, 内系数]): number => 外系数 * sin(3 * 内系数 * 主数))
    .reduce((a, b): number => a + b) / 3

function wgs84_to_gcj02(point: Position): Position {
  const A = 6378245 // SK - 42 reference system 半长轴
  const _F: number = 1 / 298.3 // SK - 42 reference system 反扁率
  const EE: number = 2 * _F - _F ** 2

  const y: number = point[1] - 35
  const x: number = point[0] - 105

  const 共同分子: number =
    sin组合(x, [
      [40, 120],
      [40, 360],
    ]) +
    (0.1 * x * y + x + 2 * y + 0.1 * Math.abs(x) ** 0.5 + -100)
  const 经度分子: number =
    sin组合(x, [
      [600, 2],
      [300, 5],
      [80, 20],
      [40, 60],
    ]) +
    (0.1 * x ** 2 + 400 + 共同分子)
  const 纬度分子: number =
    sin组合(y, [
      [640, 2],
      [320, 5],
      [80, 20],
      [40, 60],
    ]) +
    (0.2 * y ** 2 + x + y + 0.1 * Math.abs(x) ** 0.5 + 共同分子)

  const common: number = 1 - EE * sin(point[1]) ** 2
  const 经度分母: number = (A * Math.cos(deg2rad(point[1]))) / common ** 0.5
  const 纬度分母: number = (A * (1 - EE)) / common ** 1.5
  const 新经度: number = point[0] + rad2deg(经度分子 / 经度分母)
  const 新纬度: number = point[1] + rad2deg(纬度分子 / 纬度分母)
  return point[2] ? [新经度, 新纬度, point[2]] : [新经度, 新纬度]
}

function 标准化角(角度: number, 中心角度: number): number {
  while (角度 < 中心角度 - 180) 角度 += 360
  while (角度 >= 中心角度 + 180) 角度 -= 360
  return 角度
}

type DistanceUnits = 'M' | 'FT' | 'FL' | 'SM' | 'CM' | 'KM' | 'MI' | 'NM'

export const useGreatCircleMapStore = defineStore('great-circle-map', () => {
  const 国内模式: ComputedRef<boolean> = computed(() =>
    window.location.hostname.endsWith('lihanming.cn'),
  )

  const 高度单位: Ref<DistanceUnits> = ref('M')
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

  function 距离转换(value: number | null, from: DistanceUnits, to: DistanceUnits): number | null {
    if (value === null) return null
    const 转换表: Map<DistanceUnits, number> = new Map([
      ['M', 1],
      ['CM', 0.01],
      ['FL', 30.48],
      ['FT', 0.3048],
      ['KM', 1000],
      ['MI', 1609.344],
      ['NM', 1852],
      ['SM', 10],
    ])
    return (value * 转换表.get(from)!) / 转换表.get(to)!
  }

  function 转换高度(values: [number | null, number | null]) {
    const elevation = 距离转换(values[0], 'M', 高度单位.value)
    const accuracy = 距离转换(values[1], 'M', 高度单位.value)

    if (elevation === null) return 'Not Available'

    if (高度单位.value === 'FL')
      return `FL${elevation.toFixed()}` + (accuracy ? ` ± ${accuracy.toFixed()}` : '')

    return (
      elevation.toFixed(1) +
      (accuracy ? ` ± ${accuracy.toFixed(1)} ` : ` `) +
      高度单位.value.toLocaleLowerCase()
    )
  }

  function 转换Position(raw: Position): Position {
    const position: Position = 使用中国坐标.value == 'gcj02' ? wgs84_to_gcj02(raw) : raw
    return [标准化角(position[0], 底图中心.value.lng), position[1], position[2]]
  }

  function 转换Positions(线段s: Position[][]): Position[][] {
    const output线段s: Position[][] = []
    for (const 线段 of 线段s) {
      const 点s: Position[] = 线段.map(转换Position)
      if (!点s[0]) continue
      let 当前线段: Position[] = []
      let 上一点: Position = 点s[0]
      for (const 当前点 of 点s) {
        if (Math.abs(当前点[0] - 上一点[0]) > 180) {
          output线段s.push(当前线段)
          当前线段 = []
        }
        当前线段.push(当前点)
        上一点 = 当前点
      }
      if (当前线段.length > 1) output线段s.push(当前线段)
    }
    return output线段s
  }

  function 转换单一Geometry(
    origin: Geometry,
  ): Point | MultiPoint | MultiLineString | Polygon | MultiPolygon {
    if (origin.type === 'Point')
      return { coordinates: 转换Position(origin.coordinates), type: 'Point' }
    if (origin.type === 'MultiPoint')
      return { coordinates: origin.coordinates.map(转换Position), type: 'MultiPoint' }
    if (origin.type === 'LineString')
      return { coordinates: 转换Positions([origin.coordinates]), type: 'MultiLineString' }
    if (origin.type === 'MultiLineString')
      return { coordinates: 转换Positions(origin.coordinates), type: 'MultiLineString' }
    return origin
  }

  function 转换GeometryCollection(origin: GeometryCollection): GeometryCollection {
    return {
      geometries: origin.geometries.map(转换单一Geometry),
      type: 'GeometryCollection',
    }
  }

  function 转换一个Feature(origin: Feature): Feature {
    return {
      properties: origin.properties,
      id: origin.id,
      type: 'Feature',
      geometry:
        origin.geometry.type === 'GeometryCollection'
          ? 转换GeometryCollection(origin.geometry)
          : 转换单一Geometry(origin.geometry),
    }
  }

  function 转换Feature(
    origin: Feature | FeatureCollection | Geometry | GeometryCollection,
  ): Feature | FeatureCollection | Geometry | GeometryCollection {
    if (origin.type === 'Feature') return 转换一个Feature(origin)
    if (origin.type === 'FeatureCollection')
      return { features: origin.features.map(转换一个Feature), type: 'FeatureCollection' }
    if (origin.type === 'GeometryCollection') return 转换GeometryCollection(origin)
    return 转换单一Geometry(origin)
  }

  const 项目s: Ref<Map<string, Item[]>> = ref(new Map())

  function 添加项目(objectText: string, description: string, category: string): void {
    if (!项目s.value.has(category)) 项目s.value.set(category, [])
    项目s.value.get(category)?.push({
      object: JSON.parse(objectText),
      description,
      category,
    })
  }

  function 删除项目(category: string, idx: number): void {
    项目s.value.get(category)?.splice(idx, 1)
    if (项目s.value.get(category)?.length === 0) 项目s.value.delete(category)
  }

  const allChinaEaipDatasets: Ref<BaselineDataPackage[]> = ref([])
  const selectedChinaEaipDataset: Ref<string> = ref('')

  async function fetchChinaEaipDatasets() {
    const response = await fetch(`/api/china-eaip-datasets`)
    allChinaEaipDatasets.value = await response.json()
  }

  const allAirportsHeliports: Ref<机场[]> = ref([])
  const selectedAirportsHeliports: Ref<机场[]> = ref([])

  return {
    allAirportsHeliports,
    selectedAirportsHeliports,
    国内模式,
    底图边界标准,
    底图风格,
    底图缩放,
    底图提供商,
    底图语言,
    底图中心,
    删除项目,
    使用中国坐标,
    allChinaEaipDatasets,
    fetchChinaEaipDatasets,
    selectedChinaEaipDataset,
    添加项目,
    显示设置界面,
    项目s,
    转换Feature,
    高度单位,
    转换高度,
  }
})
