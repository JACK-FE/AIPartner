<template>
  <div style="max-width: 1200px; margin: 0 auto; padding: 24px;">
    <n-h2>最近聊天</n-h2>
    <div v-if="chatStore.conversations.length" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px; margin-bottom: 32px;">
      <n-card v-for="conv in chatStore.conversations" :key="conv.id" hoverable @click="router.push(`/chat/${conv.character_id}`)" style="cursor: pointer;">
        <template #cover>
          <div style="display: flex; justify-content: center; padding: 12px;">
            <n-avatar :src="conv.character_avatar" :size="64" />
          </div>
        </template>
        <div style="text-align: center; font-weight: 500;">{{ conv.character_name }}</div>
      </n-card>
    </div>
    <n-empty v-else description="暂无聊天记录" style="margin-bottom: 32px;" />

    <n-h2>我的关注</n-h2>
    <div v-if="follows.length" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px;">
      <n-card v-for="f in follows" :key="f.id" hoverable @click="router.push(`/chat/${f.character.id}`)" style="cursor: pointer;">
        <template #cover>
          <div style="display: flex; justify-content: center; padding: 12px;">
            <n-avatar :src="f.character.avatar" :size="64" />
          </div>
        </template>
        <div style="text-align: center; font-weight: 500;">{{ f.character.name }}</div>
      </n-card>
    </div>
    <n-empty v-else description="暂无关注" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useChatStore } from '../stores/chat'
import { charactersApi } from '../api/characters'
import type { Follow } from '../types'
import { NCard, NH2, NAvatar, NEmpty } from 'naive-ui'

const router = useRouter()
const chatStore = useChatStore()
const follows = ref<Follow[]>([])

onMounted(async () => {
  await Promise.all([
    chatStore.fetchConversations(),
    charactersApi.follows().then(({ data }) => { follows.value = data }),
  ])
})
</script>
