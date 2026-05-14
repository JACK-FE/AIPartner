import client from './client'
import type { User } from '../types'

export const authApi = {
  register(data: { username: string; email: string; password: string }) {
    return client.post('/auth/register/', data)
  },
  login(data: { email: string; password: string }) {
    return client.post('/auth/login/', data)
  },
  refresh(refresh: string) {
    return client.post('/auth/refresh/', { refresh })
  },
  getProfile() {
    return client.get<User>('/auth/me/')
  },
  updateProfile(data: Partial<User>) {
    return client.put<User>('/auth/me/', data)
  },
}
