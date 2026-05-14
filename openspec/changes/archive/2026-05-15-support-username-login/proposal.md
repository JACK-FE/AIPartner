## Why

当前系统注册时必须填写用户名，但登录却只能用邮箱——用户在注册时提供用户名，登录时却无法使用，体验不一致且不直观。应支持用户名登录，使用户可以用同一凭证（用户名或邮箱）登录。

## What Changes

- 后端认证后端扩展为同时支持邮箱和用户名查找用户
- 登录接口的输入字段保持为 `email`，但后端逻辑会自动先按邮箱匹配，失败则回退按用户名匹配
- 前端登录页面输入框标签从"邮箱"改为"用户名/邮箱"，提示文案相应更新
- 错误提示从英文 "Invalid email or password" 改为中文"用户名或密码错误"

## Capabilities

### New Capabilities

- `username-login`: 允许用户使用用户名作为替代邮箱的登录凭证，后端认证时自动识别输入是邮箱还是用户名

### Modified Capabilities

<!-- 无现有 capability 受影响 -->

## Impact

- 后端：`apps/accounts/auth_backend.py`（认证逻辑）、`apps/accounts/serializers.py`（错误消息）
- 前端：`src/views/Login.vue`（表单标签与提示文案）
- API 请求格式不变，无破坏性变更
- 不涉及数据库变更或新增依赖
