import { defineStore } from 'pinia'
import { ref } from 'vue'
import { charactersApi } from '../api/characters'
import type { AICharacter, ModelConfig } from '../types'

export const useCharacterStore = defineStore('character', () => {
  const characters = ref<AICharacter[]>([])
  const myCharacters = ref<AICharacter[]>([])
  const models = ref<ModelConfig[]>([])
  const total = ref(0)
  const loading = ref(false)

  async function fetchList(params?: { page?: number; search?: string; sort?: string; model_id?: string }) {
    loading.value = true
    try {
      const { data } = await charactersApi.list(params)
      if (params?.page && params.page > 1) {
        characters.value.push(...data.results)
      } else {
        characters.value = data.results
      }
      total.value = data.count
    } finally {
      loading.value = false
    }
  }

  async function fetchMine() {
    const { data } = await charactersApi.mine()
    myCharacters.value = data
  }

  async function fetchModels() {
    const { data } = await charactersApi.models()
    models.value = data
  }

  return { characters, myCharacters, models, total, loading, fetchList, fetchMine, fetchModels }
})
