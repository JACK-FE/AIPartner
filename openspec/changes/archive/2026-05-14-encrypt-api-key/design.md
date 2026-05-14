## Context

`ModelConfig.api_key` is stored as plaintext `CharField` in the database. The REST API already excludes `api_key` from serialization, so the risk is limited to database-level access (SQLite file leak, backup exposure). Django's `SECRET_KEY` provides a convenient and already-managed key source for encryption.

## Goals / Non-Goals

**Goals:**
- Encrypt `api_key` at rest in the database using symmetric encryption
- Transparent encrypt/decrypt — no changes to consumers (`chat/llm.py`, Django Admin)
- Backward-compatible with existing plaintext data (no migration script needed)
- Minimal new dependencies and code

**Non-Goals:**
- Per-user encryption keys
- External key management (Vault, KMS)
- Encrypting any other model fields
- Changing the REST API

## Decisions

**Decision 1: Fernet encryption with key derived from `SECRET_KEY`**

- *Alternative*: Separate `ENCRYPTION_KEY` env var. Adds management burden without meaningful security gain in single-machine deployment.
- *Rationale*: If `SECRET_KEY` is compromised, the Django app is already fully breached. Co-locating the encryption key adds no additional risk.

**Decision 2: SHA-256 key derivation**

- `hashlib.sha256(SECRET_KEY.encode()).digest()` produces exactly 32 bytes, matching Fernet's key requirement after base64 URL-safe encoding.
- *Alternative*: PBKDF2 with salt. Adds complexity without benefit — the input is already a high-entropy key, not a password.

**Decision 3: Transparent property-based API**

- `ModelConfig.api_key` becomes a `@property` that decrypts on read. A `@api_key.setter` stores the raw value, and `save()` handles encryption.
- *Alternative*: Explicit `get_api_key()` / `set_api_key()` methods. Breaks existing consumers (Django Admin form field binding, `llm.py` direct access).
- *Rationale*: Preserves all existing code that reads `model_config.api_key`.

**Decision 4: Auto-detect plaintext for backward compatibility**

- If `decrypt_value()` raises an exception (existing plaintext data), the property returns the raw value.
- On next `save()`, plaintext values are detected and encrypted.
- *Alternative*: Data migration script. Risk of errors, requires downtime coordination.

## Risks / Trade-offs

- **SECRET_KEY rotation breaks decryption**: If `SECRET_KEY` is changed, existing encrypted API keys become unreadable. → Document this; re-enter API keys after rotation.
- **Fernet tokens are base64 strings**: Slightly larger than plaintext (~200 chars for a typical API key). → `max_length=512` is already sufficient.
- **Dual write (admin form saves twice)**: Django Admin auto-saves when editing a ModelConfig. The setter + save() pattern handles this — plaintext is only encrypted once.
