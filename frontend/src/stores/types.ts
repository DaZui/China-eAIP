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

interface AirportHeliport extends Feature {
  geometry: Point
  properties: {
    uuid: string
    information_valid_since: string
    information_valid_until: string
    aixm_sequence_number: number
    aixm_correction_number: number
    aixm_location_indicator_icao: string
    aixm_designator_iata: string
    aixm_annotations: string

    aixm_field_elevation: [number | null, number | null]
    aixm_reference_temperature_in_celcius: number | null

    aixm_name_display: string
    aixm_magnetic_variation_display: string[]
  }
}

interface AirspaceFeature extends Feature {
  geometry: LineString
  properties: {
    uuid: string
    information_valid_since: string
    information_valid_until: string
    aixm_sequence_number: number
    aixm_correction_number: number
  }
}

interface Airspace {
  uuid: string
  information_valid_since: string
  information_valid_until: string
  aixm_sequence_number: number
  aixm_correction_number: number
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
