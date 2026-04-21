type Position = [number, number, number?]

interface Point {
  coordinates: Position
  type: 'Point'
}

interface LineString {
  coordinates: Position[]
  type: 'LineString'
}

interface MultiLineString {
  coordinates: Position[][]
  type: 'MultiLineString'
}

interface Base {
  uuid: string
  有效期自: string
  有效期至: string
  大版本号: number
  小版本号: number
}

interface CentrelinePoint extends Base {
  aixm_on_runway: string
  aixm_role: string
  aixm_annotations: {
    '@gml:id': string
    'aixm:propertyName': { $: string }
    'aixm:purpose': { $: string }
    'aixm:translatedNote': {
      'aixm:LinguisticNote': { '@gml:id': string; 'aixm:note': { '@lang': 'eng'; $: string } }
    }[]
  }[]
}

interface Direction extends Base {
  aixm_designator: string
  aixm_true_bearing: number | null
  aixm_true_bearing_accuracy: number | null
  aixm_used_runway: string
  航向角: [number | null, number | null]
  中线点s: CentrelinePoint[]
}

interface Runway extends Base {
  aixm_designator: string
  长度: [number | null, number | null]
  宽度: [number | null, number | null]
  路肩宽度: [number | null, null]
  aixm_associated_airport_heliport: string
  notes: [[string, number, number, string], [string, number, number, string]][]
  方向s: Direction[]
}

interface AirportHeliport extends Base {
  aixm_designator: string
  aixm_name: string
  aixm_location_indicator_icao: string
  aixm_designator_iata: string
  aixm_type: string
  aixm_certified_icao: boolean | null
  aixm_control_type: string
  aixm_field_elevation: number | null
  aixm_field_elevation_accuracy: number | null
  aixm_magnetic_variation: number | null
  aixm_magnetic_variation_accuracy: number | null
  aixm_date_magnetic_variation: number | null
  aixm_magnetic_variation_change: number | null
  aixm_reference_temperature: number | null
  aixm_certification_date: string | null
  aixm_certification_expiration_date: string | null
  aixm_served_city: string
  aixm_latitude: number
  aixm_longitude: number
  aixm_horizontal_accuracy: number | null
  aixm_annotations: string
  aixm_availability: string

  跑道s: Runway[]
  geometry: Point
  notes: [string, string][]
  名称: string
  海拔: [number | null, number | null]
  地磁偏角: [number | null, number | null, number | null, number | null]
}

export type { AirportHeliport, LineString, MultiLineString, Point, Position }
