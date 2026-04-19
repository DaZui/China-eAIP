<template>
  <select class="form-select" multiple v-model="store.selectedAirspaces">
    <optgroup v-for="[prefix, items] in groupedAirspaces" :label="prefix" :key="prefix">
      <option :key="item.uuid" :value="item" class="monospace" v-for="item of items">
        {{ item.aixm_designator }} {{ item.aixm_name }}
      </option>
    </optgroup>
  </select>

  <AirspaceHint
    :airspace="airport"
    :key="idx"
    class="my-1"
    v-for="(airport, idx) in store.selectedAirspaces"
  />
</template>

<script setup lang="ts">
import { useGreatCircleMapStore } from '@/stores/GreatCircleMap'
import type { Airspace } from '@/stores/types'
import { computed, onMounted, ref, type ComputedRef, type Ref } from 'vue'
import AirspaceHint from './AirspaceHint.vue'

const store = useGreatCircleMapStore()

const mapping: Ref<Map<string, string>> = ref(
  new Map([
    [
      'NAS',
      'National Airspace System. [note: The airspace within which a State provides Air Traffic Services is usually composed of:1) the territories over which the State has jurisdiction;2) those portions of the airspace over the high seas or in airspace of undetermined sovereignty where the provision of ATS are provided as determined by regional agreements. It can usually be determined by the UNION of FIRs (including, where appropriate, NO-FIRs) of the UNION of NAS-P. .]',
    ],
    [
      'FIR',
      'Flight information region. Airspace of defined dimensions within which flight information service and alerting service are provided. Description: ICAO Recognized. Might, for example, be used if service provided by more than one unit.',
    ],
    ['FIR_P', 'Part of an FIR.'],
    [
      'UIR',
      'Upper flight information region. An upper airspace of defined dimensions within which flight information service and alerting service are provided. Description: Non-ICAO Recognized. Each state determines its definition for upper airspace.',
    ],
    [
      'UIR_P',
      'Part of a UIR. [note: Might, for example, be used if more than one unites provide service in different parts of a UIR .]',
    ],
    [
      'CTA',
      'Control area. A controlled airspace extending upwards from a specified limit above the earth. Description: ICAO Recognized.',
    ],
    ['CTA_P', 'Part of a CTA.'],
    ['OCA_P', 'Part of an OCA.'],
    [
      'OCA',
      'Oceanic control area. A Control Area extending upwards in the upper airspace. Description: Non-ICAO Recognized.',
    ],
    [
      'UTA',
      'Upper control area. A Control Area extending upwards in the upper airspace. Description: Non-ICAO Recognized.',
    ],
    ['UTA_P', 'Part of a UTA.'],
    [
      'TMA',
      'Terminal control area. Control area normally established at the confluence of ATS routes in the vicinity of one or more major aerodromes. Description: Non-ICAO Recognized. Mainly used in Europe under the Flexible Use of Airspace concept.',
    ],
    ['TMA_P', 'Part of a TMA.'],
    [
      'CTR',
      'Control zone. A controlled airspace extending upwards from the surface of the earth to a specified upper limit. Description: ICAO Recognized.',
    ],
    ['CTR_P', 'Part of a CTR.'],
    ['OTA', 'Oceanic transition area.'],
    [
      'SECTOR',
      'Control sector. A subdivision of a designated control area within which responsibility is assigned to one controller or to a small group of controllers. Description: ICAO Recognized.',
    ],
    ['SECTOR_C', 'Temporary consolidated (collapsed) sector.'],
    [
      'TSA',
      'Temporary segregated area (FUA). Airspace of pre-defined dimensions within which activities require the reservation of airspace for the exclusive use of specific users during a predetermined period of time. Description: (NATO) An area in which there are special restrictive measures employed to prevent or minimize interference between friendly forces. An area under military jurisdiction in which special security measures are employed to prevent unauthorized entry.',
    ],
    [
      'CBA',
      'Cross border area (FUA). Airspace of defined dimensions, above the land areas or territorial waters of more than one state. Description: Non-ICAO Recognized. Mainly used in Europe under the Flexible Use of Airspace concept.',
    ],
    [
      'RCA',
      'Reduced co-ordination area (FUA). Portion of airspace of defined dimensions within which general aviation traffic is permitted "off-route" without requiring general aviation traffic controllers to initiate co-ordination with OAT controllers. Description: Non-ICAO Recognized. Mainly used in Europe under the Flexible Use of Airspace concept.',
    ],
    ['RAS', 'Regulated airspace (not otherwise covered).'],
    [
      'AWY',
      'Airway (corridor). A control area or portion thereof established in the form of a corridor.',
    ],
    [
      'MTR',
      'Military Training Route buffer. A control area or portion thereof, established in the form of a corridor around a military training route in order to protect it from other traffic.',
    ],
    [
      'P',
      'Prohibited area. Airspace of defined dimensions, above the land areas or territorial waters of a State, within which the flight of aircraft is prohibited. Description: ICAO Recognized.',
    ],
    [
      'R',
      'Restricted area. Airspace of defined dimensions, above the land areas or territorial waters of a State, within which the flight of aircraft is restricted in accordance with certain specified conditions. Description: ICAO Recognized.',
    ],
    [
      'D',
      'Danger area. Airspace of defined dimensions within which activities dangerous to the flight of aircraft may exist at specified times. Description: ICAO Recognized.',
    ],
    [
      'ADIZ',
      'Air Defence Identification Zone. Special designated airspace of defined dimensions within which aircraft are required to comply with special identification and/or reporting procedures additional to those related to the provision of air traffic services (ATS). Description: ICAO Recognized.',
    ],
    [
      'NO_FIR',
      'Airspace for which not even an FIR is defined. [note: There are parts in the world for which there is neither an FIR nor any other airspace-type is defined. These airspaces will be marked as NO-FIR .]',
    ],
    ['PART', 'Part of an airspace (used in airspace aggregation).'],
    ['CLASS', 'Airspace having a specified class.'],
    ['POLITICAL', 'Political/administrative area.'],
    ['D_OTHER', 'Activities of dangerous nature (other than a danger area).'],
    [
      'TRA',
      'Temporary reserved area (FUA). Airspace of pre-defined dimensions within which activities require the reservation of airspace during a predetermined period of time. Description: Non-ICAO Recognized. Mainly used in Europe under the Flexible Use of Airspace concept.',
    ],
    [
      'A',
      'Alert area. Airspace which may contain a high volume of pilot training activities or unusual type of aerial activity, neither of which is hazardous to aircraft. Description: Non-ICAO Recognized. Mainly used in contiguous United States and its territories.',
    ],
    [
      'W',
      'Warning area. A non-regulatory airspace of defined dimensions designated over international waters that contains activity which may be hazardous to aircraft not participating in the activity. The purpose of such warning areas is to warn non participating pilots of the potential danger. Description: Non-ICAO Recognized. Mainly used in contiguous United States and its territories.',
    ],
    ['PROTECT', 'Airspace protected from specific air traffic.'],
    [
      'AMA',
      'Minimum altitude area. The lowest altitude to be used under instrument meteorological conditions (IMC) which will provide a minimum vertical clearance of 300 m (1 000 ft) or in designated mountainous terrain 600 m (2 000 ft) above all obstacles located in the area specified. Description: ICAO Recognized. Published by many States as rectangles of 1 x 1 degree on the ENR 6 charts. Note - In the exact calculation 984 feet can be used as an equivalent to 300 metres.',
    ],
    [
      'ASR',
      'Altimeter setting region. Airspace of defined dimensions within which standardized altimeter setting procedures apply. Description: Non-ICAO Recognized. For example, during flight the altimeter shall be set to the current altimeter setting of the nearest station along the route of flight.',
    ],
    [
      'ADV',
      'Advisory Area. An area of defined dimensions within which air traffic advisory service is available. Description: ICAO Recognized. Air traffic control service provides a much more complete service than air traffic advisory service; advisory areas and routes are therefore not established within controlled airspace, but air traffic advisory service may be provided below and above.',
    ],
    [
      'UADV',
      'Upper Advisory Area. An area of defined dimensions in upper airspace within which air traffic advisory service is available. Description: ICAO Recognized. Air traffic control service provides a much more complete service than air traffic advisory service; advisory areas and routes are therefore not established within controlled airspace, but air traffic advisory service may be provided below and above.',
    ],
    [
      'ATZ',
      'Airport Traffic Zone. Airspace of defined dimensions established around an airport for the protection of airport traffic. Description: ICAO Recognized.',
    ],
    ['ATZ_P', 'Part of an airport traffic zone'],
    ['HTZ', 'Helicopter traffic zone'],
    ['NAS_P', 'A part of a national airspace system'],
    ['OTHER', 'Other'],
  ]),
)

const groupedAirspaces: ComputedRef<Map<string, Airspace[]>> = computed(() => {
  const x: Map<string, Airspace[]> = new Map()

  for (const airspace of store.allAirspaces) {
    const key = `${airspace.aixm_type}: ${mapping.value.get(airspace.aixm_type) || 'OTHER'}`

    if (!x.has(key)) x.set(key, [])

    x.get(key)!.push(airspace)
  }

  return x
})

onMounted(async function () {
  store.allAirspaces = []
  const response = await fetch(
    `/api/china-eaip-datasets/${store.selectedChinaEaipDataset}/Airspace/elements`,
  )
  store.allAirspaces = await response.json()
})
</script>
