import client from './client'
import type { AICharacter, ModelConfig, Follow, PaginatedResponse } from '../types'

export const charactersApi = {
  list(params?: { page?: number; search?: string; sort?: string; model_id?: string }) {
    return client.get<PaginatedResponse<AICharacter>>('/characters/', { params })
  },
  mine() {
    return client.get<AICharacter[]>('/characters/mine/')
  },
  get(id: number) {
    return client.get<AICharacter>(`/characters/${id}/`)
  },
  create(data: { name: string; avatar?: string; description?: string; personality?: string; model: number; is_public?: boolean }) {
    return client.post<AICharacter>('/characters/', data)
  },
  update(id: number, data: Partial<AICharacter>) {
    return client.put<AICharacter>(`/characters/${id}/`, data)
  },
  delete(id: number) {
    return client.delete(`/characters/${id}/`)
  },
  follow(id: number) {
    return client.post(`/characters/${id}/follow/`)
  },
  unfollow(id: number) {
    return client.delete(`/characters/${id}/unfollow/`)
  },
  follows() {
    return client.get<Follow[]>('/follows/')
  },
  models() {
    return client.get<ModelConfig[]>('/models/')
  },
}
