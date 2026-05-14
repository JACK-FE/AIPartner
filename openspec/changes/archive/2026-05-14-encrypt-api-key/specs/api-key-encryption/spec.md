## ADDED Requirements

### Requirement: API key is encrypted at rest
The system SHALL encrypt `ModelConfig.api_key` before storing it in the database and decrypt it when read, using Fernet symmetric encryption with a key derived from Django's `SECRET_KEY`.

#### Scenario: New API key is saved encrypted
- **WHEN** a new ModelConfig is created with an `api_key` value
- **THEN** the stored database value is an encrypted Fernet token, not the original plaintext

#### Scenario: API key is transparently decrypted on read
- **WHEN** code reads `model_config.api_key`
- **THEN** the returned value is the original plaintext API key

#### Scenario: Existing plaintext data is readable
- **WHEN** a pre-existing ModelConfig has a plaintext `api_key` in the database
- **THEN** reading `model_config.api_key` returns the plaintext value without error

#### Scenario: Plaintext data is encrypted on next save
- **WHEN** a pre-existing ModelConfig with a plaintext `api_key` is saved again
- **THEN** the database value is updated to an encrypted Fernet token

#### Scenario: API key is NOT exposed via REST API
- **WHEN** any REST API endpoint returns ModelConfig data (e.g., `/api/models/`)
- **THEN** the response SHALL NOT include the `api_key` field
