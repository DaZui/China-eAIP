<template>
  <select class="form-select" v-model="store.selectedChinaEaipDataset">
    <optgroup :label="store.国内模式 ? b : c" v-for="[a, b, c] of items" :key="a">
      <option
        v-for="(dataset, idx) in store.allChinaEaipDatasets.filter((x) => x.status == a)"
        :key="idx"
        :value="dataset.filename"
      >
        {{ dataset.publication_number }} {{ dataset.version_number }} ({{
          dataset.effective_since
        }})
      </option>
    </optgroup>
  </select>
</template>

<script setup lang="ts">
import { useGreatCircleMapStore } from '@/stores/GreatCircleMap'
import { type Ref, onMounted, ref } from 'vue'

const items: Ref<[string, string, string][]> = ref([
  ['current', '当前有效', 'Current'],
  ['upcoming', '尚未生效', 'Upcoming'],
  ['expired', '已经失效', 'Expired'],
])

const store = useGreatCircleMapStore()
onMounted(store.fetchChinaEaipDatasets)
</script>
