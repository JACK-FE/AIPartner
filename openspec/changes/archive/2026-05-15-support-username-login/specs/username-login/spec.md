## ADDED Requirements

### Requirement: Login with username or email

The system SHALL allow users to authenticate using either their username or email address along with their password through a single credential field.

#### Scenario: Login with email succeeds

- **WHEN** user submits `{"email": "user@example.com", "password": "correct_password"}`
- **AND** a user with email `user@example.com` exists
- **THEN** the system authenticates the user and returns access and refresh JWT tokens

#### Scenario: Login with username succeeds

- **WHEN** user submits `{"email": "myusername", "password": "correct_password"}`
- **AND** no user with email `myusername` exists
- **AND** a user with username `myusername` exists
- **THEN** the system authenticates the user and returns access and refresh JWT tokens

#### Scenario: Login with invalid credentials fails

- **WHEN** user submits `{"email": "unknown", "password": "any_password"}`
- **AND** no user has email `unknown` and no user has username `unknown`
- **THEN** the system returns a 401 error with message "用户名或密码错误"

#### Scenario: Email takes priority over username

- **WHEN** user submits `{"email": "conflict", "password": "correct_password"}`
- **AND** user A has email `conflict` and user B has username `conflict`
- **THEN** the system authenticates as user A (email match takes priority)

### Requirement: Login UI accepts username or email

The login page SHALL display a unified input field labeled "用户名/邮箱" that accepts either a username or email address.

#### Scenario: Login form displays unified label

- **WHEN** user navigates to the login page
- **THEN** the credential input field displays label "用户名/邮箱"
- **AND** the placeholder text displays "请输入用户名或邮箱"
