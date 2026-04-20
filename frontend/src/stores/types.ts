type Position = [number, number, number?]

interface Point {
  coordinates: Position
  type: 'Point'
}

interface MultiPoint {
  coordinates: Position[]
  type: 'MultiPoint'
}

interface LineString {
  coordinates: Position[]
  type: 'LineString'
}

interface MultiLineString {
  coordinates: Position[][]
  type: 'MultiLineString'
}

interface Polygon {
  coordinates: Position[][]
  type: 'Polygon'
}

interface MultiPolygon {
  coordinates: Position[][][]
  type: 'MultiPolygon'
}

type Geometry = Point | MultiPoint | LineString | MultiLineString | Polygon | MultiPolygon

interface GeometryCollection {
  geometries: Geometry[]
  type: 'GeometryCollection'
}

interface Feature {
  geometry: Geometry | GeometryCollection
  id: string
  properties: object
  type: 'Feature'
}

interface FeatureCollection {
  type: 'FeatureCollection'
  features: Feature[]
}
interface Base {
  uuid: string
  有效期自: string
  有效期至: string
  大版本号: number
  小版本号: number
}

interface WithAnnotations {
  aixm_annotations: string
}

interface Runway extends Base, WithAnnotations {
  aixm_designator: string
  长度: [number | null, number | null]
  宽度: [number | null, number | null]
  路肩宽度: [number | null, null]
  aixm_associated_airport_heliport: string
  notes: [[string, number, number, string], [string, number, number, string]][]
}

interface AirportHeliportProperties extends Base, WithAnnotations {
  ICAO代码: string
  IATA代码: string

  海拔: [number | null, number | null]
  温度: number | null

  名称: string
  aixm_magnetic_variation_display: string[]

  runways: Runway[]
  notes: [string, string][]
}

interface AirportHeliport extends Feature {
  geometry: Point
  properties: AirportHeliportProperties
}

interface Airspace extends Base {
  aixm_type: string
  aixm_designator: string
  aixm_name: string
  features: FeatureCollection
}

interface BaselineDataPackage {
  publication_number: string
  version_number: string
  filename: string
  effective_since: string
  status: 'current' | 'expired' | 'upcoming'
}

export type {
  AirportHeliport,
  AirportHeliportProperties,
  Airspace,
  BaselineDataPackage,
  Feature,
  FeatureCollection,
  Geometry,
  GeometryCollection,
  LineString,
  MultiLineString,
  MultiPoint,
  MultiPolygon,
  Point,
  Polygon,
  Position,
}
