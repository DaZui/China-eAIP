<template>
  <tr v-if="items.length > 0">
    <th>{{ title }}</th>
    <td style="text-align: end">
      <div v-for="(value, index) in items" :key="index">{{ value }}</div>
    </td>
  </tr>
</template>

<script setup lang="ts">
defineProps<{ title: string; items: string[] }>()
</script>
