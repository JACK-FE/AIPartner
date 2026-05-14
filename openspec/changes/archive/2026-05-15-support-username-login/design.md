## Context

当前系统登录流程仅支持邮箱 + 密码认证。`EmailBackend` 通过 `User.objects.get(email=email)` 查找用户。前端登录页输入框标签和占位符均为"邮箱"。

用户名已存在于系统中——注册时必填，个人资料可编辑——但登录时完全忽略。前端 `Login.vue` 表单字段名为 `email`，发送 `POST /api/auth/login/` 时携带 `{"email": "...", "password": "..."}`。

本次变更方案 A（统一字段）：单一输入框接受用户名或邮箱，后端自动识别。变更量最小，前端仅改标签文案，后端仅扩展现有认证后端。

## Goals / Non-Goals

**Goals:**
- 用户可在登录输入框中输入用户名或邮箱，后端自动匹配
- 保持 API 请求格式不变，零破坏性变更
- 变更集中在 3 个文件内，最小化改动面

**Non-Goals:**
- 不添加手机号登录、OAuth 等第三方登录方式
- 不改变注册流程
- 不调整密码策略或 Token 机制
- 不添加"忘记用户名"等找回功能

## Decisions

**1. API 字段名保持 `email`**

不改为 `credential` 等新名称，因为：
- 对现有 API 客户端零影响
- 后端将 `email` 参数视为"凭证标识符"，先按邮箱匹配，失败则回退按用户名匹配
- 与 Django simplejwt 的 `TokenObtainSerializer.username_field` 机制兼容

备选方案（未采用）：将字段改名为 `credential` — 语义更准确但会产生破坏性变更。

**2. 后端认证优先级：邮箱 > 用户名**

`EmailBackend.authenticate()` 中先尝试 `User.objects.get(email=email)`，捕获 `DoesNotExist` 后再尝试 `User.objects.get(username=email)`。

原因是邮箱地址包含 `@` 符号有天然识别特征，先按邮箱查询更高效。且当用户邮箱与另一用户用户名相同时，应优先匹配邮箱（用户本意更可能是用邮箱登录）。

**3. 前端仅修改标签和文案**

不修改表单字段名（保持 `email`）、不修改 `authApi.login()` 签名、不修改 `authStore.login()` 参数。变更仅限于 `Login.vue` 的三个字符串（label、placeholder、rule message）。

## Risks / Trade-offs

| 风险 | 缓解措施 |
|------|----------|
| 用户 A 的邮箱与用户 B 的用户名相同，用户 B 无法用自己的用户名登录 | 邮箱优先匹配策略确保此场景下邮箱用户不受影响；用户名与邮箱冲突的场景在实际中极少出现 |
| 错误消息"用户名或密码错误"对纯邮箱用户略显不自然 | 比"邮箱或密码错误"更通用，覆盖两者场景 |
| 用户名登录时前端字段名仍为 `email`，浏览器自动填充可能不理想 | 浏览器主要根据 `type` 和 `name` 属性来决定自动填充，`name="email"` 对密码管理器的填充行为已经是最好的通用选择 |
