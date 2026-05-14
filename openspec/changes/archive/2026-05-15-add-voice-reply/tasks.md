## 1. Voice Composable

- [x] 1.1 新建 `frontend/src/composables/useVoice.ts`，封装 Web Speech API
- [x] 1.2 实现 `enabled` 状态管理（初始化读取 localStorage，变更时写回）
- [x] 1.3 实现 `speechSynthesis` 可用性检测（`supported`）
- [x] 1.4 实现 `feedToken(token)` —— 累积 token 到缓冲区，遇句子分隔符时调用 `speak()`
- [x] 1.5 实现 `speak(sentence)` —— 创建 SpeechSynthesisUtterance 并朗读
- [x] 1.6 实现 `stop()` —— 取消当前语音并清空缓冲区
- [x] 1.7 实现 `flush()` —— SSE 流结束后朗读缓冲区剩余文本

## 2. Chat Page Integration

- [x] 2.1 在 Chat.vue 头部（头像与关注按钮之间）添加语音开关按钮（`n-button`，图标区分开关状态）
- [x] 2.2 当 `supported` 为 false 时隐藏语音开关
- [x] 2.3 在 `sendMessage()` 开头调用 `voice.stop()` 停止上一段语音
- [x] 2.4 在 SSE token 循环中调用 `voice.feedToken(data.token)`
- [x] 2.5 在 finally 块中（done 事件后）调用 `voice.flush()`
- [x] 2.6 在 `onUnmounted` 中调用 `voice.stop()`
