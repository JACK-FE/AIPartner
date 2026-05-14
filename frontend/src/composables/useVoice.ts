import { ref, watch } from 'vue'

const STORAGE_KEY = 'voice_enabled'
const SENTENCE_END = /[。！？\n!?;]/

export function useVoice() {
  const supported = ref(typeof window !== 'undefined' && 'speechSynthesis' in window)
  const enabled = ref(localStorage.getItem(STORAGE_KEY) === 'true')
  const buffer = ref('')

  watch(enabled, (val) => {
    localStorage.setItem(STORAGE_KEY, String(val))
  })

  function toggle() {
    enabled.value = !enabled.value
    if (!enabled.value) {
      stop()
    }
  }

  function speak(sentence: string) {
    if (!supported.value || !sentence.trim()) return
    const utterance = new SpeechSynthesisUtterance(sentence)
    utterance.lang = 'zh-CN'
    window.speechSynthesis.speak(utterance)
  }

  function feedToken(token: string) {
    if (!enabled.value) return
    buffer.value += token
    let match: RegExpExecArray | null
    while ((match = SENTENCE_END.exec(buffer.value)) !== null) {
      const sentence = buffer.value.substring(0, match.index + 1)
      buffer.value = buffer.value.substring(match.index + 1)
      speak(sentence)
    }
  }

  function flush() {
    if (!enabled.value || !buffer.value.trim()) return
    speak(buffer.value)
    buffer.value = ''
  }

  function stop() {
    if (supported.value) {
      window.speechSynthesis.cancel()
    }
    buffer.value = ''
  }

  return { supported, enabled, toggle, feedToken, flush, stop }
}
