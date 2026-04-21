type GeoJSONPosition = [number, number, number?]

interface GeoJSONPoint {
  coordinates: GeoJSONPosition
  type: 'Point'
}

interface GeoJSONLineString {
  coordinates: GeoJSONPosition[]
  type: 'LineString'
}

interface GeoJSONMultiLineString {
  coordinates: GeoJSONPosition[][]
  type: 'MultiLineString'
}

interface Base {
  uuid: string
  有效期自: string
  有效期至: string
  大版本号: number
  小版本号: number
}

interface Nil {
  '@nilReason': 'unknown'
  '@xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance'
  '@xsi:nil': 'true'
}

// eslint-disable-next-line @typescript-eslint/no-empty-object-type
interface WithAnnotation {
  // aixm_annotation: {
  //   '@gml:id': string
  //   'aixm:propertyName': { $: string }
  //   'aixm:purpose': { $: string }
  //   'aixm:translatedNote': {
  //     'aixm:LinguisticNote': { '@gml:id': string; 'aixm:note': { $: string; '@lang': string } }
  //   }[]
  // }[]
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
  aixm_associated_declared_distances: {
    '@gml:id': string
    'aixm:type': { $: string }
    'aixm:declaredValue': {
      'aixm:RunwayDeclaredDistanceValue': {
        '@gml:id': string
        'aixm:distance': { $: string; '@uom': 'M' }
        'aixm:distanceAccuracy': Nil
      }
    }[]
  }[]
}

interface Direction extends Base {
  aixm_designator: string
  aixm_true_bearing: number
  aixm_used_runway: string
  中线点s: CentrelinePoint[]
}

interface Runway extends Base {
  aixm_designator: string
  aixm_nominal_length: number
  aixm_nominal_width: number
  aixm_width_shoulder: number | null
  aixm_associated_airport_heliport: string

  方向s: Direction[]

  notes: [[string, number, number, string], [string, number, number, string]][]
}

// interface Point {
//   latitude: number
//   longitude: number
//   geometry: GeoJSONPoint | null
// }

// interface ElevatedPoint extends Point {
//   aixm_elevation: number | null
//   aixm_special_elevation: '' | 'UNL' | 'GND' | 'FLOOR' | 'CEILING'
// }

interface AirportHeliport extends Base, WithAnnotation {
  // aixm_designator: string
  // aixm_name: string
  aixm_location_indicator_icao: string
  aixm_designator_iata: string
  // aixm_type: string
  // aixm_certified_icao: boolean | null
  // aixm_control_type: string
  aixm_field_elevation: number | null
  aixm_magnetic_variation: number | null
  aixm_date_magnetic_variation: number | null
  aixm_reference_temperature: number | null
  // aixm_certification_date: string | null
  // aixm_certification_expiration_date: string | null
  // aixm_arp: ElevatedPoint
  // aixm_served_city: string
  // aixm_availability: {
  //   '@gml:id': string
  //   'aixm:usage': {
  //     'aixm:AirportHeliportUsage': {
  //       '@gml:id': string
  //       'aixm:selection': {
  //         'aixm:ConditionCombination': {
  //           '@gml:id': string
  //           'aixm:flight': {
  //             'aixm:FlightCharacteristic': {
  //               '@gml:id': string
  //               'aixm:type': { $: string } | Nil
  //               'aixm:rule': { $: string } | Nil
  //               'aixm:military': { $: string } | Nil
  //               'aixm:purpose': { $: string } | Nil
  //             }
  //           }[]
  //         }
  //       }
  //     }
  //   }[]
  // }[]

  跑道s: Runway[]
  坐标点: GeoJSONPoint
  注解s: { [key: string]: string[] }
  名称: string
  用途s: [string, string, string, string][]
}

export type {
  AirportHeliport,
  GeoJSONLineString as LineString,
  GeoJSONMultiLineString as MultiLineString,
  GeoJSONPoint as Point,
  GeoJSONPosition as Position,
}
