## ADDED Requirements

### Requirement: User can register with email and password
The system SHALL allow users to register with a username, email, and password. No email verification is required. Username and email MUST be unique. Password MUST be at least 6 characters.

#### Scenario: Successful registration
- **WHEN** user submits valid username, email, and password
- **THEN** system creates account and returns JWT tokens

#### Scenario: Duplicate username
- **WHEN** user submits a username that already exists
- **THEN** system returns 400 error with "Username already taken" message

#### Scenario: Duplicate email
- **WHEN** user submits an email that already exists
- **THEN** system returns 400 error with "Email already registered" message

#### Scenario: Short password
- **WHEN** user submits password shorter than 6 characters
- **THEN** system returns 400 error with password requirements

### Requirement: User can login
The system SHALL authenticate users with email and password, returning JWT access and refresh tokens.

#### Scenario: Successful login
- **WHEN** user submits correct email and password
- **THEN** system returns access token and refresh token

#### Scenario: Invalid credentials
- **WHEN** user submits incorrect email or password
- **THEN** system returns 401 error

### Requirement: User can refresh JWT token
The system SHALL allow users to obtain a new access token using a valid refresh token.

#### Scenario: Successful token refresh
- **WHEN** user submits valid refresh token
- **THEN** system returns new access token

#### Scenario: Expired refresh token
- **WHEN** user submits expired refresh token
- **THEN** system returns 401 error

### Requirement: User can view own profile
The system SHALL return the authenticated user's profile information.

#### Scenario: View profile
- **WHEN** authenticated user requests their profile
- **THEN** system returns username, email, avatar, bio, created_at

#### Scenario: Unauthenticated access
- **WHEN** unauthenticated user requests profile
- **THEN** system returns 401 error

### Requirement: User can update own profile
The system SHALL allow authenticated users to update their username, avatar, and bio.

#### Scenario: Update profile
- **WHEN** authenticated user submits valid profile changes
- **THEN** system updates and returns updated profile

#### Scenario: Update to existing username
- **WHEN** user submits a username that another user already has
- **THEN** system returns 400 error
