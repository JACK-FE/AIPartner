## Why

AI 好友的回复目前只有文字，用户在某些场景下（驾驶、做家务、眼睛疲劳）不方便阅读屏幕。添加语音播报能力可以让用户以听觉方式获取回复，提升多场景下的使用体验。

## What Changes

- 新增语音播报功能：AI 好友回复时，文字正常流式展示，同时使用浏览器内置 TTS 引擎朗读回复内容
- 聊天页顶部新增语音开关按钮，用户可随时开启/关闭语音播报
- 开关状态持久化到 localStorage，刷新页面后保持用户偏好
- 发送新消息时自动中断正在播放的语音，避免前后消息语音重叠

## Capabilities

### New Capabilities
- `voice-reply`: AI 好友回复的语音播报能力——句子级朗读、开关控制、状态持久化

### Modified Capabilities
<!-- None -->

## Impact

- **前端改动**：`Chat.vue` 新增开关 UI + 集成语音逻辑；新建 `composables/useVoice.ts` 管理语音状态与播放
- **后端改动**：无
- **新增依赖**：无（使用浏览器内置 `SpeechSynthesis` API）
- **破坏性变更**：无
