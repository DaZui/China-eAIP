import type {
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
} from './types'

function deg2rad(v: number): number {
  return v * (Math.PI / 180)
}

function rad2deg(v: number): number {
  return v * (180 / Math.PI)
}

function sin(v: number): number {
  return Math.sin(deg2rad(v))
}

function sin组合(主数: number, 系数s: [number, number][]): number {
  return (
    系数s
      .map(([外系数, 内系数]): number => 外系数 * sin(3 * 内系数 * 主数))
      .reduce((a, b): number => a + b) / 3
  )
}

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

class Converter {
  system: 'gcj02' | 'wgs84'
  center: number

  constructor(system: 'gcj02' | 'wgs84', center: number) {
    this.system = system
    this.center = center
  }

  convertPoint(point: Position): Position {
    if (this.system === 'gcj02') point = wgs84_to_gcj02(point)
    return [标准化角(point[0], this.center), point[1], point[2]]
  }

  convertPoints(points: Position[]): Position[] {
    return points.map((x) => this.convertPoint(x))
  }

  convertLineString(inputLineStrings: Position[][]): Position[][] {
    const outputLineStrings: Position[][] = []
    for (const inputLineString of inputLineStrings) {
      const convertedPoints: Position[] = this.convertPoints(inputLineString)

      if (!convertedPoints[0]) continue
      let outputLineString: Position[] = []
      let previousPoint: Position = convertedPoints[0]
      for (const currentPoint of convertedPoints) {
        if (Math.abs(currentPoint[0] - previousPoint[0]) > 180) {
          outputLineStrings.push(outputLineString)
          outputLineString = []
        }
        outputLineString.push(currentPoint)
        previousPoint = currentPoint
      }
      if (outputLineString.length > 1) outputLineStrings.push(outputLineString)
    }
    return outputLineStrings
  }

  convertGeometry(origin: Geometry): Point | MultiPoint | MultiLineString | Polygon | MultiPolygon {
    if (origin.type === 'Point')
      return {
        coordinates: this.convertPoint(origin.coordinates),
        type: 'Point',
      }
    if (origin.type === 'MultiPoint')
      return {
        coordinates: this.convertPoints(origin.coordinates),
        type: 'MultiPoint',
      }
    if (origin.type === 'LineString')
      return {
        coordinates: this.convertLineString([origin.coordinates]),
        type: 'MultiLineString',
      }
    if (origin.type === 'MultiLineString')
      return {
        coordinates: this.convertLineString(origin.coordinates),
        type: 'MultiLineString',
      }
    return origin
  }

  convertGeometryCollection(origin: GeometryCollection): GeometryCollection {
    return {
      geometries: origin.geometries.map((x) => this.convertGeometry(x)),
      type: 'GeometryCollection',
    }
  }

  convertFeature(origin: Feature): Feature {
    return {
      properties: origin.properties,
      id: origin.id,
      type: 'Feature',
      geometry:
        origin.geometry.type === 'GeometryCollection'
          ? this.convertGeometryCollection(origin.geometry)
          : this.convertGeometry(origin.geometry),
    }
  }

  convert(
    origin: Feature | FeatureCollection | Geometry | GeometryCollection,
  ): Feature | FeatureCollection | Geometry | GeometryCollection {
    if (origin.type === 'Feature') return this.convertFeature(origin)
    if (origin.type === 'FeatureCollection')
      return {
        features: origin.features.map((x) => this.convertFeature(x)),
        type: 'FeatureCollection',
      }
    if (origin.type === 'GeometryCollection') return this.convertGeometryCollection(origin)
    return this.convertGeometry(origin)
  }
}

export { Converter }
