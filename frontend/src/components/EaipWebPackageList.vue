<template>
  <p class="my-2 text-body-secondary">
    {{
      store.国内模式
        ? '以下为 raw/ 中各期 AIP 网页压缩包解压后的离线 eAIP 站点，点击即可在本站点内浏览。'
        : 'Offline eAIP sites extracted from the AIP web packages. Click to browse within this site.'
    }}
  </p>
  <div class="list-group">
    <a
      class="list-group-item list-group-item-action d-flex align-items-center justify-content-between font-monospace"
      :href="pkg.url"
      :key="pkg.name"
      v-for="pkg in store.eaipWebPackages"
    >
      {{ pkg.name }}
      <span class="badge text-bg-secondary fw-normal">
        {{ pkg.version }} · {{ dayjs(pkg.modified).format('YYYY-MM-DD HH:mm') }}
      </span>
    </a>
  </div>
  <p class="my-2 text-body-secondary" v-if="store.eaipWebPackages.length === 0">
    {{ store.国内模式 ? '暂无已解压的 AIP 网页包。' : 'No extracted eAIP packages yet.' }}
  </p>
</template>

<script setup lang="ts">
import { useGreatCircleMapStore } from '@/stores/GreatCircleMap'
import dayjs from 'dayjs'
import { onMounted } from 'vue'

const store = useGreatCircleMapStore()

onMounted(async function () {
  store.eaipWebPackages = []
  const response = await fetch('/api/china-eaip-datasets/EaipWebPackages')
  store.eaipWebPackages = await response.json()
})
</script>
