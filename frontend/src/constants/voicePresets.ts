import type { VoicePreset } from '../types'

/**
 * 音色预设列表。
 * 与后端 voice_presets.py 保持同步。
 */
export const VOICE_PRESETS: VoicePreset[] = [
  { key: 'shaonv', label: '少女音', gender: 'female', description: '年轻温柔，自然亲和' },
  { key: 'huopo', label: '活泼少女', gender: 'female', description: '明快活泼，元气满满' },
  { key: 'dongbei', label: '东北女声', gender: 'female', description: '东北方言，爽朗亲切' },
  { key: 'shaanxi', label: '陕西女声', gender: 'female', description: '陕西方言，质朴温暖' },
  { key: 'shaonian', label: '少年音', gender: 'male', description: '清爽阳光，青春洋溢' },
  { key: 'dashu', label: '大叔音', gender: 'male', description: '低沉厚重，稳重成熟' },
  { key: 'zhengtai', label: '正太音', gender: 'male', description: '童稚可爱，纯真男孩' },
  { key: 'xinwen', label: '新闻男声', gender: 'male', description: '专业播音，字正腔圆' },
]

export const DEFAULT_VOICE_PRESET = 'shaonv'
