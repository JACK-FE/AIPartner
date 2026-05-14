## 1. Backend Project Setup

- [x] 1.1 Create Django project `config` and apps: `accounts`, `characters`, `chat`
- [x] 1.2 Configure SQLite database, CORS headers, DRF, SimpleJWT in settings
- [x] 1.3 Set up URL routing (project-level + app-level urls.py)
- [x] 1.4 Install and configure Django admin for all models
- [x] 1.5 Create `requirements.txt` with all dependencies

## 2. Database Models

- [x] 2.1 Create `User` model (accounts app) with username, email, password, avatar, bio
- [x] 2.2 Create `ModelConfig` model (characters app) with provider, model_name, api_key (encrypted), api_base_url, is_active, sort_order
- [x] 2.3 Create `AICharacter` model (characters app) with creator FK, name, avatar, description, personality, system_prompt, model FK, is_public, follow_count
- [x] 2.4 Create `Follow` model (characters app) with user FK, character FK, unique_together constraint
- [x] 2.5 Create `Conversation` model (chat app) with user FK, character FK, last_message_at, unique_together constraint
- [x] 2.6 Create `Message` model (chat app) with conversation FK, role, content, created_at, index
- [x] 2.7 Run migrations

## 3. Authentication API (accounts app)

- [x] 3.1 Implement register endpoint (POST /api/auth/register)
- [x] 3.2 Implement login endpoint (POST /api/auth/login) with JWT tokens
- [x] 3.3 Implement token refresh endpoint (POST /api/auth/refresh)
- [x] 3.4 Implement profile view/update endpoints (GET/PUT /api/auth/me)
- [x] 3.5 Add Gravatar default avatar logic on user creation

## 4. Character Management API (characters app)

- [x] 4.1 Implement character creation endpoint (POST /api/characters) with auto-generated system_prompt
- [x] 4.2 Implement list own characters endpoint (GET /api/characters/mine)
- [x] 4.3 Implement character detail endpoint (GET /api/characters/:id)
- [x] 4.4 Implement character update endpoint (PUT /api/characters/:id) with system_prompt regeneration
- [x] 4.5 Implement character delete endpoint (DELETE /api/characters/:id) with cascade
- [x] 4.6 Implement model list endpoint (GET /api/models) for available models

## 5. Character Discovery API (square page)

- [x] 5.1 Implement public character list endpoint (GET /api/characters) with pagination
- [x] 5.2 Add search by name (case-insensitive partial match) to character list
- [x] 5.3 Add sort options (hot by follow_count, new by created_at) to character list
- [x] 5.4 Add model filter to character list
- [x] 5.5 Add is_followed field to character responses for authenticated users

## 6. Follow System API (characters app)

- [x] 6.1 Implement follow endpoint (POST /api/characters/:id/follow) with follow_count increment
- [x] 6.2 Implement unfollow endpoint (DELETE /api/characters/:id/follow) with follow_count decrement
- [x] 6.3 Implement followed list endpoint (GET /api/follows)

## 7. Chat Engine API (chat app)

- [x] 7.1 Implement message history endpoint (GET /api/characters/:id/messages) with pagination
- [x] 7.2 Implement recent conversations endpoint (GET /api/conversations)
- [x] 7.3 Implement SSE streaming chat endpoint (POST /api/characters/:id/messages)
- [x] 7.4 Implement LLM API integration with streaming support (OpenAI-compatible interface)
- [x] 7.5 Implement conversation auto-creation and context building (system prompt + last 20 messages)
- [x] 7.6 Implement message persistence (save user message before stream, save assistant response after)

## 8. Frontend Project Setup

- [x] 8.1 Create Vue 3 project with Vite, TypeScript, Naive UI, Pinia, Vue Router
- [x] 8.2 Configure project structure (api/, components/, views/, router/, stores/)
- [x] 8.3 Set up API client (axios) with JWT interceptor
- [x] 8.4 Set up Vue Router with route definitions (/, /chat/:id, /friends, /create, /profile, /login, /register)
- [x] 8.5 Set up Pinia stores (auth store, character store, chat store)
- [x] 8.6 Implement NavBar component with navigation links, search bar, user menu

## 9. Frontend Auth Pages

- [x] 9.1 Implement Login page with email/password form
- [x] 9.2 Implement Register page with username/email/password form
- [x] 9.3 Implement auth store with login, register, logout, token refresh logic
- [x] 9.4 Add route guards (redirect to login if unauthenticated for protected routes)

## 10. Frontend Square Page

- [x] 10.1 Implement Square page with public character list (paginated)
- [x] 10.2 Implement CharacterCard component (avatar, name, description, follow button)
- [x] 10.3 Implement search bar functionality
- [x] 10.4 Implement sort selector (hot/new)
- [x] 10.5 Implement model filter tabs
- [x] 10.6 Implement CharacterGrid component for responsive card layout

## 11. Frontend Chat Page

- [x] 11.1 Implement Chat page with header (character info + follow button)
- [x] 11.2 Implement MessageList component with message bubbles
- [x] 11.3 Implement ChatInput component with send button
- [x] 11.4 Implement SSE streaming (EventSource or fetch + ReadableStream) for receiving AI responses
- [x] 11.5 Implement typing indicator during streaming
- [x] 11.6 Implement follow/unfollow button in chat header

## 12. Frontend Friends Page

- [x] 12.1 Implement Friends page with "Recent Chats" section (from conversations API)
- [x] 12.2 Implement "Followed" section (from follows API)
- [x] 12.3 Implement navigation to chat on character click

## 13. Frontend Create Page

- [x] 13.1 Implement CreateForm component (avatar picker, name, description, personality, model select, public toggle)
- [x] 13.2 Implement avatar preset picker (emoji/icon selection)
- [x] 13.3 Implement model selection dropdown (from /api/models)
- [x] 13.4 Implement MyCharacters section showing user's created characters
- [x] 13.5 Add edit/delete functionality for own characters

## 14. Frontend Profile Page

- [x] 14.1 Implement Profile page with user avatar, username, bio, stats (creation count, follow count)
- [x] 14.2 Implement profile edit modal/form

## 15. Admin & Configuration

- [x] 15.1 Register all models in Django admin
- [x] 15.2 Configure admin for ModelConfig CRUD with encrypted API key display
- [x] 15.3 Create initial preset avatar list (emoji/icon URLs)
- [x] 15.4 Create system prompt generation template
