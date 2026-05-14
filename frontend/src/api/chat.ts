import client from './client'
import type { Message, Conversation, PaginatedResponse } from '../types'

export const chatApi = {
  messages(characterId: number, params?: { page?: number }) {
    return client.get<PaginatedResponse<Message>>(`/characters/${characterId}/messages/`, { params })
  },
  conversations() {
    return client.get<Conversation[]>('/conversations/')
  },
}
