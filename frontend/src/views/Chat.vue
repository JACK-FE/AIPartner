<template>
  <div style="max-width: 800px; margin: 0 auto; padding: 24px; display: flex; flex-direction: column; height: calc(100vh - 112px);">
    <div v-if="character" style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px; padding-bottom: 16px; border-bottom: 1px solid #eee;">
      <n-avatar :src="character.avatar" :size="48" />
      <div style="flex: 1;">
        <div style="font-weight: 600;">{{ character.name }}</div>
        <n-text depth="3" style="font-size: 12px;">{{ character.model_name }}</n-text>
      </div>
      <n-button v-if="voice.supported.value" size="small" @click="voice.toggle()">
        {{ voice.enabled.value ? '🔊' : '🔇' }}
      </n-button>
      <n-button size="small" :type="character.is_followed ? 'primary' : 'default'" @click="toggleFollow">
        {{ character.is_followed ? '已关注' : '关注' }}
      </n-button>
    </div>

    <div ref="msgContainer" style="flex: 1; overflow-y: auto; padding: 16px 0; display: flex; flex-direction: column; gap: 12px;">
      <div v-for="msg in chatStore.messages" :key="msg.id || msg.created_at" :style="{ display: 'flex', justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start' }">
        <div :style="{ maxWidth: '70%', padding: '10px 16px', borderRadius: msg.role === 'user' ? '18px 18px 4px 18px' : '18px 18px 18px 4px', background: msg.role === 'user' ? '#18a058' : '#e8e8e8', color: msg.role === 'user' ? '#fff' : '#333' }">
          {{ msg.content }}
          <div v-if="msg.id === 0" style="display: inline-block; margin-left: 4px;">
            <n-spin size="small" />
          </div>
        </div>
      </div>
    </div>

    <div style="display: flex; gap: 8px; padding-top: 16px; border-top: 1px solid #eee;">
      <n-input v-model:value="inputText" type="textarea" :rows="2" placeholder="输入消息..." @keyup.ctrl.enter="sendMessage" />
      <n-button type="primary" @click="sendMessage" :disabled="!inputText.trim() || chatStore.streaming" style="align-self: flex-end;">发送</n-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { useChatStore } from '../stores/chat'
import { charactersApi } from '../api/characters'
import { useVoice } from '../composables/useVoice'
import type { AICharacter } from '../types'

import { NAvatar, NButton, NInput, NSpin, NText, useMessage } from 'naive-ui'

const route = useRoute()
const chatStore = useChatStore()
const message = useMessage()
const character = ref<AICharacter | null>(null)
const inputText = ref('')
const msgContainer = ref<HTMLElement | null>(null)
const characterId = Number(route.params.id)
const voice = useVoice()

async function toggleFollow() {
  if (!character.value) return
  try {
    if (character.value.is_followed) {
      await charactersApi.unfollow(character.value.id)
      character.value.is_followed = false
      character.value.follow_count = Math.max(0, character.value.follow_count - 1)
    } else {
      await charactersApi.follow(character.value.id)
      character.value.is_followed = true
      character.value.follow_count += 1
    }
  } catch {
    message.error('操作失败')
  }
}

async function sendMessage() {
  const content = inputText.value.trim()
  if (!content || chatStore.streaming) return
  inputText.value = ''
  voice.stop()

  chatStore.addMessage({ id: Date.now(), role: 'user', content, created_at: new Date().toISOString() })
  chatStore.streaming = true
  chatStore.startNewAssistantMessage()

  try {
    const token = localStorage.getItem('access_token')
    const resp = await fetch(`http://localhost:8000/api/characters/${characterId}/chat/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ content }),
    })

    const reader = resp.body?.getReader()
    if (!reader) return

    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n')
      buffer = lines.pop() || ''

      for (const line of lines) {
        if (line.startsWith('event: token')) continue
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6))
            if (data.token) {
              chatStore.appendToLastMessage(data.token)
              voice.feedToken(data.token)
            }
            if (data.message_id) {
              chatStore.updateLastMessageId(data.message_id)
            }
          } catch { }
        }
      }
      await nextTick()
      scrollToBottom()
    }
  } catch (err) {
    message.error('发送失败')
  } finally {
    chatStore.streaming = false
    voice.flush()
    scrollToBottom()
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (msgContainer.value) {
      msgContainer.value.scrollTop = msgContainer.value.scrollHeight
    }
  })
}

onMounted(async () => {
  try {
    const { data } = await charactersApi.get(characterId)
    character.value = data
  } catch {
    message.error('加载角色失败')
  }
  await chatStore.fetchMessages(characterId)
  scrollToBottom()
})

onUnmounted(() => {
  voice.stop()
})
</script>
