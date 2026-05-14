## Why

AI companion/character chat platforms are growing rapidly, but most either lock users into fixed characters or require complex setup. There's an opportunity to build a lightweight, open platform where users can create, share, and chat with customizable AI characters using a unified backend model configuration. Users want a friendly space to discover AI personalities, follow their favorites, and create their own — all with a clean, modern UI.

## What Changes

- **New Vue 3 + Django project** (AI Partner) from scratch
- **Account system**: email + password registration/login (no email verification)
- **Square page** (home): browse publicly shared AI characters with search and sorting
- **Chat page**: real-time streaming chat with AI characters via SSE
- **Friends page**: shows recently chatted and followed AI characters
- **Create page**: form to create new AI characters with custom name, avatar, description, personality, model selection; also shows user's own creations
- **Profile page**: user info display and editing
- **Backend model config system**: admin-managed list of available LLM models (provider, model name, API key, endpoint)
- **Follow system**: users can follow/unfollow AI characters
- **Avatar system**: preset emoji/icon avatars + Gravatar fallback (no file upload initially)
- **Database**: SQLite (development), designed for easy migration to MySQL

## Capabilities

### New Capabilities
- `user-auth`: User registration, login, session management, profile CRUD
- `character-management`: Create, read, update, delete AI characters with custom attributes
- `character-discovery`: Browse, search, and sort public AI characters on the square page
- `character-follow`: Follow/unfollow characters, view followed and recent characters
- `chat-engine`: Streaming chat with AI characters via SSE, message history
- `model-config`: Admin CRUD for available LLM models (provider, model name, API key)
- `avatar-system`: Preset avatar selection and Gravatar integration

### Modified Capabilities

None (new project, no existing specs).

## Impact

- New Django project with DRF, JWT auth, SSE streaming views
- New Vue 3 project with Naive UI, Pinia, Vue Router
- SQLite database with models for User, AICharacter, Follow, Conversation, Message, ModelConfig
- No external dependencies beyond Django/Vue ecosystem and LLM API calls
- Admin panel for model configuration
