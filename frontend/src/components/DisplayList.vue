<template>
  <tr v-if="items.length > 0">
    <th>{{ title }}</th>
    <td style="text-align: end" v-if="horizontal">
      <div class="row">
        <div class="col" v-for="(value, index) in items" :key="index">{{ value }}</div>
      </div>
    </td>
    <td style="text-align: end" v-else>
      <div v-for="(value, index) in items" :key="index">{{ value }}</div>
    </td>
  </tr>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  items: string[]
  horizontal?: boolean
}>()
</script>
