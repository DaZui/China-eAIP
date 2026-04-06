<template>
  <div class="card">
    <div class="card-body">
      <h5 class="card-title" v-if="airport.properties.servedCity === airport.properties.name">
        {{ airport.properties.servedCity }}
      </h5>
      <h5 class="card-title" v-else>
        {{ airport.properties.servedCity }} / {{ airport.properties.name }}
      </h5>
      <h6 class="card-subtitle mb-2 text-body-secondary">
        {{ airport.properties.designatorIATA }} / {{ airport.properties.locationIndicatorICAO }}
      </h6>
      <h6 class="card-subtitle mb-2 text-body-secondary">
        {{ airport.geometry.coordinates[1].toFixed(6) }}°N,
        {{ airport.geometry.coordinates[0].toFixed(6) }}°E
      </h6>
      <p class="card-text"></p>
      <table class="table spread">
        <tbody>
          <tr>
            <th>Designator</th>
            <td>{{ airport.properties.designator }}</td>
          </tr>
          <tr>
            <th>Type</th>
            <td>{{ airport.properties.type }}</td>
          </tr>
          <tr>
            <th>ICAO Certified</th>
            <td>{{ airport.properties.certifiedICAO }}</td>
          </tr>
          <tr>
            <th>Control Type</th>
            <td>{{ airport.properties.controlType }}</td>
          </tr>
          <tr>
            <th>Field Elevation</th>
            <td>
              {{ airport.properties.fieldElevationInMeter.toFixed(1) }} m<br />
              ({{ (airport.properties.fieldElevationInMeter / 0.3048).toFixed(1) }} ft)
            </td>
          </tr>
          <tr>
            <th>Reference Temperature</th>
            <td>
              {{ airport.properties.referenceTemperatureInCelcius.toFixed(1) }} ℃<br />
              ({{ (airport.properties.referenceTemperatureInCelcius * 1.8 + 32).toFixed(1) }} ℉)
            </td>
          </tr>
          <tr>
            <th>Magnetic Variation</th>
            <td>
              <div>{{ airport.properties.magneticVariation }}°</div>
              <div v-if="airport.properties.dateMagneticVariation">
                (Updated in {{ airport.properties.dateMagneticVariation }})
              </div>
            </td>
          </tr>
          <tr>
            <th>Certification Date</th>
            <td>{{ airport.properties.certificationDate }}</td>
          </tr>
          <tr>
            <th>Certification Expiration Date</th>
            <td>{{ airport.properties.certificationExpirationDate }}</td>
          </tr>
          <tr>
            <th>Annotations</th>
            <td>{{ airport.properties.annotations }}</td>
          </tr>
          <tr>
            <th>Availability</th>
            <td>{{ airport.properties.availability }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
<script setup lang="ts">
import type { 机场 } from '@/stores/types'
defineProps<{ airport: 机场 }>()
</script>
<style scoped>
.spread td {
  text-align: end;
}
</style>
