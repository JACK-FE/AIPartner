## 1. Dependencies

- [x] 1.1 Add `cryptography` to `backend/requirements.txt`

## 2. Encryption Module

- [x] 2.1 Create `backend/config/crypto.py` with `encrypt_value()` and `decrypt_value()` functions using Fernet with SECRET_KEY-derived key

## 3. Model Modification

- [x] 3.1 Add `@property api_key` getter on `ModelConfig` that decrypts on read, with fallback to plaintext for existing data
- [x] 3.2 Add `@api_key.setter` on `ModelConfig` that stores raw value
- [x] 3.3 Override `ModelConfig.save()` to encrypt `api_key` before writing if it is plaintext

## 4. Verification

- [x] 4.1 Verify existing code consumers (`chat/llm.py`, Django Admin) work without modification
- [x] 4.2 Verify REST API does not expose `api_key`
