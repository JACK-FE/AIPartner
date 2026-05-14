<template>
  <n-card :title="character.name" hoverable @click="router.push(`/chat/${character.id}`)" style="cursor: pointer;">
    <template #cover>
      <div style="display: flex; justify-content: center; padding: 16px;">
        <n-avatar :src="character.avatar" :size="80" fallback-src="https://api.dicebear.com/9.x/bottts/svg?seed=default" />
      </div>
    </template>
    <n-ellipsis :line-clamp="2">
      {{ character.description || '暂无简介' }}
    </n-ellipsis>
    <template #footer>
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <n-tag size="small">{{ character.model_name }}</n-tag>
        <div style="display: flex; align-items: center; gap: 8px;">
          <n-button
            v-if="auth.isAuthenticated"
            size="tiny"
            :type="character.is_followed ? 'primary' : 'default'"
            @click.stop="toggleFollow"
          >
            {{ character.is_followed ? '已关注' : '关注' }}
          </n-button>
          <n-text depth="3" style="font-size: 12px;">{{ character.follow_count }} 关注</n-text>
        </div>
      </div>
    </template>
  </n-card>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { charactersApi } from '../api/characters'
import type { AICharacter } from '../types'
import { NCard, NAvatar, NButton, NTag, NText, NEllipsis, useMessage } from 'naive-ui'

const props = defineProps<{ character: AICharacter }>()
const emit = defineEmits<{ (e: 'follow-toggled'): void }>()
const router = useRouter()
const auth = useAuthStore()
const message = useMessage()

async function toggleFollow() {
  try {
    if (props.character.is_followed) {
      await charactersApi.unfollow(props.character.id)
      props.character.is_followed = false
      props.character.follow_count = Math.max(0, props.character.follow_count - 1)
    } else {
      await charactersApi.follow(props.character.id)
      props.character.is_followed = true
      props.character.follow_count += 1
    }
    emit('follow-toggled')
  } catch {
    message.error('操作失败')
  }
}
</script>
