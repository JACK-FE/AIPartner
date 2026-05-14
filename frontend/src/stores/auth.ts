import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authApi } from '../api/auth'
import type { User } from '../types'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const isAuthenticated = ref(!!localStorage.getItem('access_token'))

  async function login(email: string, password: string) {
    const { data } = await authApi.login({ email, password })
    localStorage.setItem('access_token', data.access)
    localStorage.setItem('refresh_token', data.refresh)
    isAuthenticated.value = true
    await fetchProfile()
  }

  async function register(username: string, email: string, password: string) {
    await authApi.register({ username, email, password })
    await login(email, password)
  }

  async function fetchProfile() {
    try {
      const { data } = await authApi.getProfile()
      user.value = data
    } catch {
      logout()
    }
  }

  async function updateProfile(data: Partial<User>) {
    const { data: updated } = await authApi.updateProfile(data)
    user.value = updated
  }

  function logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    user.value = null
    isAuthenticated.value = false
  }

  return { user, isAuthenticated, login, register, fetchProfile, updateProfile, logout }
})
