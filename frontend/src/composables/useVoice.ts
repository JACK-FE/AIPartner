import { ref, watch } from 'vue'

const STORAGE_KEY = 'voice_enabled'

export function useVoice() {
  const supported = ref(true)
  const enabled = ref(localStorage.getItem(STORAGE_KEY) === 'true')
  let currentAudio: HTMLAudioElement | null = null

  watch(enabled, (val) => {
    localStorage.setItem(STORAGE_KEY, String(val))
  })

  function toggle() {
    enabled.value = !enabled.value
    if (!enabled.value) {
      stop()
    }
  }

  function playAudio(url: string) {
    if (!enabled.value) return
    stop()
    const audio = new Audio(url)
    audio.play().catch(() => {})
    currentAudio = audio
  }

  function stop() {
    if (currentAudio) {
      currentAudio.pause()
      currentAudio.currentTime = 0
      currentAudio = null
    }
  }

  return { supported, enabled, toggle, playAudio, stop }
}
