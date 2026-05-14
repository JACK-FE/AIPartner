## Why

`ModelConfig.api_key` is currently stored as plaintext in the database. If the SQLite database file is leaked (backup exposure, misconfigured static file serving), all LLM API keys are compromised. Encrypting the API key at rest prevents this attack vector.

## What Changes

- Add `cryptography` dependency for Fernet symmetric encryption
- Add `config/crypto.py` module with encrypt/decrypt utilities keyed from Django `SECRET_KEY`
- Modify `ModelConfig.api_key` to auto-encrypt on save and auto-decrypt on read via property
- Existing plaintext API keys remain readable and are encrypted on next save (no migration needed)

## Capabilities

### New Capabilities

- `api-key-encryption`: API keys stored in ModelConfig are encrypted at rest using Fernet symmetric encryption. Encryption is transparent to all consumers (LLM integration, Admin panel). Existing plaintext data is backward-compatible.

### Modified Capabilities

<!-- None -->

## Impact

- **New dependency**: `cryptography` in `requirements.txt`
- **New file**: `backend/config/crypto.py`
- **Modified file**: `backend/apps/characters/models.py` (ModelConfig.save + api_key property)
- **No API changes**: `api_key` is not exposed in any REST endpoint
- **No admin changes**: Django Admin reads/writes through the model transparently
- **No LLM integration changes**: `chat/llm.py` reads `model_config.api_key` which auto-decrypts
