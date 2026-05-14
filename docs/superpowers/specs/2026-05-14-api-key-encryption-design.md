# API Key Encryption Design

## Context

`ModelConfig.api_key` is currently stored as plaintext in the database (SQLite). If the database file is leaked (backup exposure, misconfigured static file serving), all LLM API keys are compromised. The REST API does not expose `api_key` — the risk is limited to database-level access.

## Decision

Encrypt `api_key` at rest using **Fernet symmetric encryption** with a key derived from Django's `SECRET_KEY`.

- **Why SECRET_KEY:** Single-machine deployment. If `SECRET_KEY` is compromised, the Django app is already fully breached — no additional risk from co-locating the encryption key.
- **Why Fernet:** Built into the `cryptography` library, audited, simple API, includes authentication (tamper detection).

## Implementation

### New module: `backend/config/crypto.py`

```
encrypt_value(plain: str) -> str
decrypt_value(cipher: str) -> str
```

Implementation details:

- Derive a 32-byte key from `SECRET_KEY` via SHA-256
- Encode it as URL-safe base64 for Fernet
- `encrypt_value` returns a Fernet token string
- `decrypt_value` returns the original plaintext

### Model: `apps/characters/models.py` — `ModelConfig`

- `api_key` field unchanged (`CharField(max_length=512)`)
- Override `save()`: if `api_key` is plaintext (not a valid Fernet token), encrypt it before saving
- Add `@property api_key` getter: decrypt the stored ciphertext and return plaintext
- Add `@api_key.setter`: store the value as-is (raw input from admin/user), encryption happens in `save()`

### Compatibility with existing data

- If decryption fails on read (existing plaintext in DB), return the raw value unchanged
- On next `save()`, the plaintext value will be encrypted

### Dependency

Add `cryptography` to `backend/requirements.txt`.

## Impact

| Component | Change |
|-----------|--------|
| `config/crypto.py` | New file |
| `characters/models.py` | Property + save override on `ModelConfig` |
| `requirements.txt` | Add `cryptography` |
| `chat/llm.py` | None (reads `model_config.api_key`) |
| `characters/admin.py` | None |
| `characters/serializers.py` | None (api_key not exposed) |
| `characters/views.py` | None |
