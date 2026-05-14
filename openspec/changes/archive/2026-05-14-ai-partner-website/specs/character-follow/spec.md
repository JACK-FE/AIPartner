## ADDED Requirements

### Requirement: User can follow a character
The system SHALL allow authenticated users to follow a public AI character. Following SHALL increment the character's follow_count.

#### Scenario: Follow a character
- **WHEN** authenticated user follows a character they don't already follow
- **THEN** system creates follow relationship and increments follow_count

#### Scenario: Follow own character
- **WHEN** user follows a character they created
- **THEN** system allows it (creators can follow their own characters)

#### Scenario: Follow non-existent character
- **WHEN** user tries to follow a non-existent character
- **THEN** system returns 404 error

#### Scenario: Unauthenticated follow
- **WHEN** unauthenticated user tries to follow
- **THEN** system returns 401 error

### Requirement: User can unfollow a character
The system SHALL allow authenticated users to unfollow a character they previously followed. Unfollowing SHALL decrement the follow_count.

#### Scenario: Unfollow a character
- **WHEN** authenticated user unfollows a character they follow
- **THEN** system removes follow relationship and decrements follow_count

#### Scenario: Unfollow not-followed character
- **WHEN** user unfollows a character they don't follow
- **THEN** system returns 404 error

### Requirement: User can view their followed characters
The system SHALL return the list of characters the authenticated user follows, ordered by follow time descending.

#### Scenario: View followed list
- **WHEN** authenticated user requests their follows
- **THEN** system returns list of followed characters

#### Scenario: No follows yet
- **WHEN** authenticated user has no follows
- **THEN** system returns empty list

### Requirement: User can see if they follow a character
The system SHALL indicate whether the current user follows a character in the character detail and list responses.

#### Scenario: Check follow status in detail
- **WHEN** authenticated user views a character they follow
- **THEN** response includes is_followed=true

#### Scenario: Check follow status in list
- **WHEN** authenticated user views character list
- **THEN** each character includes is_followed field
