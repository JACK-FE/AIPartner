<template>
  <div style="max-width: 1200px; margin: 0 auto; padding: 24px;">
    <div style="display: flex; gap: 16px; margin-bottom: 24px; align-items: center; flex-wrap: wrap;">
      <n-input v-model:value="search" placeholder="搜索AI好友..." clearable style="max-width: 300px;" @keyup.enter="doSearch" />
      <n-select v-model:value="sort" :options="sortOptions" style="width: 120px;" @update:value="fetchData" />
      <n-select v-model:value="modelFilter" :options="modelOptions" placeholder="模型筛选" clearable style="width: 160px;" @update:value="fetchData" />
    </div>

    <div v-if="store.loading && !store.characters.length" style="text-align: center; padding: 48px;">
      <n-spin size="large" />
    </div>

    <n-grid v-else :cols="4" :x-gap="16" :y-gap="16" responsive="screen" :col-span="{ xs: 1, s: 2, m: 3, l: 4 }">
      <n-grid-item v-for="c in store.characters" :key="c.id">
        <CharacterCard :character="c" @follow-toggled="fetchData" />
      </n-grid-item>
    </n-grid>

    <div v-if="!store.characters.length && !store.loading" style="text-align: center; padding: 48px; color: #999;">
      暂无公开的AI好友
    </div>

    <div v-if="store.total > store.characters.length" style="text-align: center; padding: 24px;">
      <n-button @click="loadMore" :loading="store.loading">加载更多</n-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useCharacterStore } from '../stores/character'
import CharacterCard from '../components/CharacterCard.vue'
import { NInput, NSelect, NGrid, NGridItem, NButton, NSpin, useMessage } from 'naive-ui'

const store = useCharacterStore()
const message = useMessage()
const page = ref(1)
const search = ref('')
const sort = ref('new')
const modelFilter = ref<number | null>(null)

const sortOptions = [
  { label: '最新', value: 'new' },
  { label: '最热', value: 'hot' },
]

const modelOptions = computed(() => [
  ...store.models.map(m => ({ label: `${m.provider} / ${m.model_name}`, value: m.id })),
])

async function fetchData() {
  page.value = 1
  try {
    await store.fetchList({ page: 1, search: search.value, sort: sort.value, model_id: modelFilter.value?.toString() })
  } catch {
    message.error('加载失败')
  }
}

async function loadMore() {
  page.value += 1
  try {
    await store.fetchList({ page: page.value, search: search.value, sort: sort.value, model_id: modelFilter.value?.toString() })
  } catch {
    message.error('加载失败')
  }
}

function doSearch() {
  fetchData()
}

onMounted(() => {
  store.fetchModels()
  fetchData()
})
</script>
