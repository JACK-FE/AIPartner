export interface User {
  id: number
  username: string
  email: string
  avatar: string
  bio: string
  date_joined: string
}

export interface ModelConfig {
  id: number
  provider: string
  model_name: string
  sort_order: number
}

export interface AICharacter {
  id: number
  name: string
  avatar: string
  description: string
  personality?: string
  system_prompt?: string
  is_public: boolean
  follow_count: number
  creator_name: string
  model_name: string
  model_provider?: string
  is_followed: boolean
  created_at: string
  updated_at?: string
}

export interface Follow {
  id: number
  character: AICharacter
  created_at: string
}

export interface Conversation {
  id: number
  character_id: number
  character_name: string
  character_avatar: string
  last_message_at: string
  created_at: string
}

export interface Message {
  id: number
  role: 'user' | 'assistant'
  content: string
  created_at: string
}

export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}
