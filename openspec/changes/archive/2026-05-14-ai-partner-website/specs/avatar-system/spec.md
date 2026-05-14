## ADDED Requirements

### Requirement: User avatars use Gravatar by default
The system SHALL automatically set a user's avatar to their Gravatar URL (based on email hash) when no custom avatar is set.

#### Scenario: Default avatar on registration
- **WHEN** user registers without specifying an avatar
- **THEN** system sets avatar to Gravatar URL based on their email

#### Scenario: Gravatar URL format
- **WHEN** user has no custom avatar
- **THEN** avatar field contains `https://www.gravatar.com/avatar/{md5(email)}?d=identicon&s=200`

### Requirement: Character avatars use preset emoji/icons
The system SHALL provide a set of preset emoji/icon avatar URLs for AI characters. Users select from these when creating a character.

#### Scenario: Select preset avatar
- **WHEN** user creates a character and selects a preset avatar
- **THEN** system saves the preset avatar URL

#### Scenario: Default preset
- **WHEN** user creates a character without selecting an avatar
- **THEN** system assigns a random preset avatar

### Requirement: User can update their avatar
The system SHALL allow users to update their avatar URL (for custom Gravatar or other image URLs).

#### Scenario: Update avatar
- **WHEN** authenticated user updates their avatar field
- **THEN** system saves the new avatar URL

#### Scenario: Reset to default
- **WHEN** user sets avatar to empty
- **THEN** system resets to Gravatar URL
