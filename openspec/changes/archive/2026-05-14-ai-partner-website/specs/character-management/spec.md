## ADDED Requirements

### Requirement: User can create an AI character
The system SHALL allow authenticated users to create AI characters with name, avatar, description, personality, model selection, and public/private toggle. The system SHALL auto-generate a system prompt from the personality and name fields.

#### Scenario: Create character with all fields
- **WHEN** authenticated user submits name, avatar, description, personality, model_id, and is_public=true
- **THEN** system creates character, auto-generates system_prompt, and returns the character

#### Scenario: Create character with minimum fields
- **WHEN** authenticated user submits only name and model_id
- **THEN** system creates character with defaults for other fields

#### Scenario: Unauthenticated creation
- **WHEN** unauthenticated user tries to create a character
- **THEN** system returns 401 error

### Requirement: User can view their own characters
The system SHALL return all characters created by the authenticated user.

#### Scenario: List my characters
- **WHEN** authenticated user requests their characters
- **THEN** system returns list of characters they created

#### Scenario: No characters yet
- **WHEN** authenticated user has no characters
- **THEN** system returns empty list

### Requirement: User can update their own character
The system SHALL allow the creator of a character to update its fields. Updating personality SHALL regenerate the system_prompt.

#### Scenario: Update character fields
- **WHEN** creator updates character name, description, or personality
- **THEN** system updates character and regenerates system_prompt if personality changed

#### Scenario: Non-creator tries to update
- **WHEN** a user who is not the creator tries to update a character
- **THEN** system returns 403 error

### Requirement: User can delete their own character
The system SHALL allow the creator of a character to delete it. Deletion SHALL cascade to related follows, conversations, and messages.

#### Scenario: Delete own character
- **WHEN** creator deletes a character
- **THEN** system deletes character and all related data

#### Scenario: Non-creator tries to delete
- **WHEN** a user who is not the creator tries to delete
- **THEN** system returns 403 error

### Requirement: System auto-generates system prompt
The system SHALL generate a system prompt from the character's name and personality description using a predefined template.

#### Scenario: Generate prompt from personality
- **WHEN** character is created with personality "friendly and helpful"
- **THEN** system_prompt contains the personality description woven into a prompt template
