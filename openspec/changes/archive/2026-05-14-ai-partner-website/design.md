## Context

A new web application for creating, sharing, and chatting with customizable AI characters. Users can browse public AI characters on the square page, follow favorites, chat via streaming responses, and create their own characters. The backend centrally manages available LLM models (OpenAI, Claude, DeepSeek, etc.) so users just pick from a list.

Tech stack: Vue 3 (Naive UI) + Django (DRF) + SQLite (dev, migratable to MySQL). No file uploads initially — avatars use preset emoji/icons and Gravatar.

## Goals / Non-Goals

**Goals:**
- Full account system (register, login, profile)
- Square page: browse public AI characters with search, sort (hot/new), pagination
- Chat page: SSE streaming chat with message history
- Friends page: recently chatted + followed characters
- Create page: build new AI characters with custom name, avatar, description, personality, model selection
- Profile page: user info display and editing
- Admin-managed model configuration (provider, model name, API key)
- Follow/unfollow system with counter
- Clean, modern UI with Naive UI components

**Non-Goals:**
- No email verification on registration
- No file uploads (avatars use presets + Gravatar)
- No WebSocket (SSE is sufficient for streaming)
- No mobile apps (responsive web only)
- No multi-tenant or team features
- No real-time multiplayer or concurrent editing

## Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Frontend framework** | Vue 3 + Naive UI | Naive UI is the most "fresh and clean" Vue 3 component library; tree-shakeable, TypeScript native |
| **Backend framework** | Django + DRF | Mature, batteries-included; DRF for REST API; admin panel built-in for model config |
| **Auth** | SimpleJWT (access + refresh tokens) | Stateless, standard for SPA + DRF; no session overhead |
| **Streaming** | SSE via StreamingHttpResponse | Simpler than WebSocket/Channels; no Redis needed; unidirectional server→client is sufficient for chat |
| **Database** | SQLite (dev) → MySQL (prod) | SQLite for zero-setup development; Django ORM abstracts the difference; migration path is just changing settings |
| **Avatar** | Preset emoji/icons + Gravatar | No file storage needed; Gravatar uses email hash for consistent avatars |
| **System prompt** | Auto-generated from personality + name | Template-based generation reduces user friction; can be customized later |
| **State management** | Pinia | Official Vue 3 state management; simple, TypeScript-friendly |
| **API style** | REST (not GraphQL) | Simpler for this scope; DRF native; pagination and filtering built-in |

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                       Frontend (Vue 3)                        │
│  ┌─────────┐ ┌──────────┐ ┌────────┐ ┌────────┐ ┌────────┐  │
│  │  Square │ │   Chat   │ │ Friends│ │ Create │ │ Profile│  │
│  └────┬────┘ └────┬─────┘ └───┬────┘ └───┬────┘ └───┬────┘  │
│       │           │           │          │           │       │
│  ┌────┴───────────┴───────────┴──────────┴───────────┴────┐  │
│  │              API Layer (axios + interceptors)           │  │
│  └───────────────────────────┬────────────────────────────┘  │
│                              │ JWT Token                     │
└──────────────────────────────┼───────────────────────────────┘
                               │ HTTP / SSE
┌──────────────────────────────┼───────────────────────────────┐
│                       Backend (Django)                       │
│  ┌───────────────────────────┴────────────────────────────┐  │
│  │                   DRF ViewSet Layer                      │  │
│  └──────┬──────────┬──────────┬──────────┬────────────────┘  │
│         │          │          │          │                    │
│  ┌──────┴──┐ ┌─────┴─────┐ ┌─┴────────┐ ┌┴──────────────┐   │
│  │ accounts│ │ characters│ │   chat   │ │ model_config  │   │
│  │ (auth)  │ │  (CRUD)   │ │ (SSE)    │ │ (admin only)  │   │
│  └────┬────┘ └─────┬─────┘ └────┬─────┘ └───────┬───────┘   │
│       │            │            │                │           │
│  ┌────┴────────────┴────────────┴────────────────┴───────┐  │
│  │                    Models (ORM)                        │  │
│  │  User | AICharacter | Follow | Conversation | Message  │  │
│  │  ModelConfig                                            │  │
│  └──────────────────────────┬─────────────────────────────┘  │
│                             │ SQLite/MySQL                   │
└─────────────────────────────┼────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │  LLM API (OpenAI,  │
                    │  Claude, DeepSeek) │
                    └───────────────────┘
```

## Data Model

```
accounts_User
  id, username, email, password_hash, avatar, bio
  created_at, updated_at

characters_AICharacter
  id, creator (FK→User), name, avatar, description
  personality, system_prompt, model (FK→ModelConfig)
  is_public (bool), follow_count (int, denormalized)
  created_at, updated_at

characters_Follow
  id, user (FK→User), character (FK→AICharacter)
  created_at
  unique_together: (user, character)

chat_Conversation
  id, user (FK→User), character (FK→AICharacter)
  last_message_at (datetime, nullable)
  created_at
  unique_together: (user, character)

chat_Message
  id, conversation (FK→Conversation), role (user/assistant)
  content (text), created_at
  index: (conversation, created_at)

characters_ModelConfig
  id, provider, model_name, api_key (encrypted)
  api_base_url, is_active, sort_order
  created_at, updated_at
```

## API Routes

```
POST   /api/auth/register              Register
POST   /api/auth/login                 Login
POST   /api/auth/refresh               Refresh token
GET    /api/auth/me                    Current user
PUT    /api/auth/me                    Update profile

GET    /api/characters                 Square list (paginated, search, sort)
GET    /api/characters/mine            My created characters
GET    /api/characters/:id             Character detail
POST   /api/characters                 Create character
PUT    /api/characters/:id             Update character
DELETE /api/characters/:id             Delete character

POST   /api/characters/:id/follow      Follow
DELETE /api/characters/:id/follow      Unfollow
GET    /api/follows                    My followed characters

GET    /api/conversations              Recent conversations
GET    /api/characters/:id/messages    Message history
POST   /api/characters/:id/messages    Send message (SSE response)

GET    /api/models                     Available models
```

## SSE Chat Flow

```
Client                              Server
  │                                    │
  │  POST /api/characters/:id/messages │
  │  { content: "Hello!" }            │
  │──────────────────────────────────▶│
  │                                    │  Save user message
  │                                    │  Build message array (system prompt + history)
  │                                    │  Call LLM API streaming
  │  ◀──── SSE stream ────────────────│
  │  event: token                     │
  │  data: {"token": "Hi"}           │
  │  event: token                     │
  │  data: {"token": " there"}        │
  │  event: token                     │
  │  data: {"token": "!"}             │
  │  event: done                      │  Save full response
  │  data: {"message_id": 42}         │
  │                                    │
```

## Frontend Route Design

```
/                    Square (home)
/chat/:characterId   Chat with AI character
/friends             Friends page
/create              Create new AI character
/profile             Profile page
/login               Login
/register            Registration
```

## Component Tree

```
App.vue
├── NavBar.vue (logo, nav links, search bar, user menu)
├── RouterView
│   ├── Square.vue
│   │   ├── CategoryTabs (model-based filters)
│   │   ├── SortSelect (hot / new)
│   │   └── CharacterGrid.vue
│   │       └── CharacterCard.vue (avatar, name, desc, follow btn)
│   ├── Chat.vue
│   │   ├── ChatHeader (character info + follow btn)
│   │   ├── MessageList.vue
│   │   │   └── MessageBubble.vue
│   │   └── ChatInput.vue
│   ├── Friends.vue
│   │   ├── SectionBlock ("Recent Chats")
│   │   └── SectionBlock ("Followed")
│   ├── Create.vue
│   │   ├── CreateForm.vue (avatar picker, name, desc, personality, model select, public toggle)
│   │   └── MyCharacters.vue (list of own creations)
│   ├── Profile.vue
│   ├── Login.vue
│   └── Register.vue
```

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| **LLM API latency** — streaming may be slow | SSE handles this naturally; show typing indicator in UI |
| **API key security** — keys stored in DB | Encrypt at rest using Django's `Fernet` or similar; restrict admin access |
| **SQLite concurrency** — write contention under load | SQLite is fine for dev/single-user; migrate to MySQL for production |
| **No email verification** — spam accounts | Add CAPTCHA if needed; rate-limit registration endpoints |
| **SSE connection limits** — browser limits concurrent connections | Only one SSE connection per chat session; close on navigation |
| **Prompt injection** — users could craft malicious inputs | Rate limiting; content length limits; optional moderation layer |
