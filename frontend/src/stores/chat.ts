import { defineStore } from 'pinia'
import { ref } from 'vue'
import { chatApi } from '../api/chat'
import type { Message, Conversation } from '../types'

export const useChatStore = defineStore('chat', () => {
  const messages = ref<Message[]>([])
  const conversations = ref<Conversation[]>([])
  const streaming = ref(false)

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

  return { messages, conversations, streaming, fetchMessages, fetchConversations, addMessage, appendToLastMessage, startNewAssistantMessage, updateLastMessageId }
})
