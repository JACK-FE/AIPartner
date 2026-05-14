## ADDED Requirements

### Requirement: Admin can manage model configurations
The system SHALL provide an admin interface (Django admin) for CRUD operations on model configurations.

#### Scenario: Admin creates model config
- **WHEN** admin user creates a model config with provider, model_name, api_key, api_base_url
- **THEN** system saves the config with encrypted api_key

#### Scenario: Admin updates model config
- **WHEN** admin user updates a model config
- **THEN** system updates the config

#### Scenario: Admin deletes model config
- **WHEN** admin user deletes a model config
- **THEN** system deletes it (characters using this model must be reassigned first or prevented)

#### Scenario: Admin disables model
- **WHEN** admin sets is_active=false on a model config
- **THEN** existing characters using this model continue to work but new characters cannot select it

### Requirement: API key is stored encrypted
The system SHALL encrypt API keys at rest in the database using a secure encryption method.

#### Scenario: Key encrypted at rest
- **WHEN** admin saves a model config with api_key
- **THEN** the api_key is encrypted before storage

#### Scenario: Key decrypted for use
- **WHEN** system needs to call the LLM API
- **THEN** system decrypts the api_key in memory for the API call

### Requirement: Available models are exposed via API
The system SHALL expose a read-only API endpoint listing all active model configurations for use in the character creation form.

#### Scenario: List active models
- **WHEN** any user (authenticated or not) requests the model list
- **THEN** system returns active models ordered by sort_order, excluding api_key

#### Scenario: No active models
- **WHEN** no models are active
- **THEN** system returns empty list
