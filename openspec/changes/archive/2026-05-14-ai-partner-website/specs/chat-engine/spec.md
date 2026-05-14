## ADDED Requirements

### Requirement: User can view message history
The system SHALL return paginated message history for a conversation between the authenticated user and a character, ordered by creation time ascending.

#### Scenario: View conversation history
- **WHEN** authenticated user requests messages for a character they have chatted with
- **THEN** system returns paginated messages ordered by time

#### Scenario: First time chatting
- **WHEN** authenticated user requests messages for a character they haven't chatted with
- **THEN** system returns empty list

#### Scenario: Unauthenticated access
- **WHEN** unauthenticated user requests messages
- **THEN** system returns 401 error

### Requirement: User can send a message and receive streaming response
The system SHALL accept a user message, save it, construct the conversation context (system prompt + recent history), call the configured LLM API with streaming, and return the response via SSE.

#### Scenario: Send message and receive streaming reply
- **WHEN** authenticated user sends a message to a character
- **THEN** system returns SSE stream with token events and a final done event

#### Scenario: SSE stream format
- **WHEN** user receives streaming response
- **THEN** each chunk is formatted as `event: token\ndata: {"token": "..."}\n\n` and final event as `event: done\ndata: {"message_id": N}\n\n`

### Requirement: System saves both user and assistant messages
The system SHALL save the user's message before streaming begins, and save the complete assistant response after streaming completes.

#### Scenario: Messages saved after streaming
- **WHEN** streaming completes
- **THEN** both user message and assistant message are persisted in the database

### Requirement: Conversation is auto-created on first message
The system SHALL automatically create a Conversation record when a user sends the first message to a character.

#### Scenario: Auto-create conversation
- **WHEN** user sends first message to a character
- **THEN** system creates a new Conversation and associates the message with it

#### Scenario: Reuse existing conversation
- **WHEN** user sends another message to the same character
- **THEN** system reuses the existing Conversation

### Requirement: Recent conversations are tracked
The system SHALL update last_message_at on the Conversation whenever a new message is sent or received, and return recent conversations ordered by this field.

#### Scenario: Recent conversations list
- **WHEN** authenticated user requests recent conversations
- **THEN** system returns conversations ordered by last_message_at descending, with character info

### Requirement: Conversation context includes recent history
The system SHALL include the last N messages (configurable, default 20) from the conversation history when calling the LLM API, plus the system prompt.

#### Scenario: Context includes history
- **WHEN** user sends a message in an existing conversation
- **THEN** LLM API call includes system prompt and last 20 messages as context
