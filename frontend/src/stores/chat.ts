import { defineStore } from 'pinia'
import { ref, shallowRef } from 'vue'
import { chatApi } from '../api/chat'
import { ttsApi } from '../api/characters'
import { useVoice } from '../composables/useVoice'
import type { Message, Conversation } from '../types'

export const useChatStore = defineStore('chat', () => {
  const messages = ref<Message[]>([])
  const conversations = ref<Conversation[]>([])
  const streaming = ref(false)

  // 语音重播状态
  const audioUrls = shallowRef(new Map<number, string>())
  const audioState = shallowRef(new Map<number, string>())
  const activePlayingMsgId = ref<number | null>(null)

  let voiceInstance: ReturnType<typeof useVoice> | null = null

  function setVoice(v: ReturnType<typeof useVoice>) {
    voiceInstance = v
  }

  async function fetchMessages(characterId: number) {
    const { data } = await chatApi.messages(characterId)
    messages.value = data.results
  }

  async function fetchConversations() {
    const { data } = await chatApi.conversations()
    conversations.value = data
  }

  function addMessage(msg: Message) {
    messages.value.push(msg)
  }

  function appendToLastMessage(token: string) {
    const last = messages.value[messages.value.length - 1]
    if (last && last.role === 'assistant') {
      last.content += token
    }
  }

  function startNewAssistantMessage() {
    messages.value.push({ id: 0, role: 'assistant', content: '', created_at: new Date().toISOString() })
  }

  function updateLastMessageId(id: number) {
    const last = messages.value[messages.value.length - 1]
    if (last) last.id = id
  }

  // ---- 语音重播 ----

  async function requestAudio(msgId: number, text: string, characterId: number) {
    const state = new Map(audioState.value)
    state.set(msgId, 'loading')
    audioState.value = state

    try {
      const { data } = await ttsApi.synthesize(characterId, text)
      const urls = new Map(audioUrls.value)
      urls.set(msgId, data.audio_url)
      audioUrls.value = urls

      const nextState = new Map(audioState.value)
      nextState.set(msgId, 'ready')
      audioState.value = nextState
    } catch {
      const nextState = new Map(audioState.value)
      nextState.set(msgId, 'error')
      audioState.value = nextState
    }
  }

  function playMessageAudio(msgId: number) {
    if (!voiceInstance) return
    const url = audioUrls.value.get(msgId)
    if (!url) return

    stopCurrent()

    const nextState = new Map(audioState.value)
    nextState.set(msgId, 'playing')
    audioState.value = nextState
    activePlayingMsgId.value = msgId

    voiceInstance.playAudio(url, () => {
      const s = new Map(audioState.value)
      s.set(msgId, 'ready')
      audioState.value = s
      activePlayingMsgId.value = null
    })
  }

  function stopCurrent() {
    if (voiceInstance) {
      voiceInstance.stop()
    }
    const currentId = activePlayingMsgId.value
    if (currentId !== null) {
      const s = new Map(audioState.value)
      s.set(currentId, 'ready')
      audioState.value = s
      activePlayingMsgId.value = null
    }
  }

  return {
    messages, conversations, streaming,
    audioUrls, audioState, activePlayingMsgId,
    setVoice,
    fetchMessages, fetchConversations,
    addMessage, appendToLastMessage, startNewAssistantMessage, updateLastMessageId,
    requestAudio, playMessageAudio, stopCurrent,
  }
})
