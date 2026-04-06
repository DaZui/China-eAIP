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
  id?: string
  properties: object
  type: 'Feature'
}

interface FeatureCollection {
  type: 'FeatureCollection'
  features: Feature[]
}

interface 机场 extends Feature {
  geometry: Point
  properties: {
    designator: string
    name: string
    locationIndicatorICAO: string
    designatorIATA: string
    type: string
    certifiedICAO: string
    controlType: string
    fieldElevationInMeter: number
    magneticVariation: string
    dateMagneticVariation: string
    referenceTemperatureInCelcius: number
    certificationDate: string
    certificationExpirationDate: string
    annotations: string
    servedCity: string
    availability: string
  }
  id: string
}

interface BaselineDataPackage {
  publication_number: string
  version_number: string
  filename: string
  effective_since: string
  status: 'current' | 'expired' | 'upcoming'
}

export type {
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
  机场,
}
