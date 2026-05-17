## Why

当前 AI 好友的语音回复只能听一次——流式回复结束后自动播放，播完即弃，用户无法再次收听。对于想回味某句对话、或第一次没听清的用户，缺少重播入口。需要在每条 AI 回复消息上提供一个可重播语音的图标按钮。

## What Changes

- 每条 AI 回复消息气泡末尾增加语音重播图标，支持播放中动画、加载态、错误态三种视觉反馈
- 自动播放完成后图标才显示为可重播状态（避免与初始自动播放冲突）
- 全局同时只有一条消息处于播放状态，点击新消息的重播会自动停止当前播放
- 历史消息的音频在用户点击时惰性请求 TTS 生成，不预加载
- 音频 URL 在前端按消息 ID 缓存，同一条消息不会重复请求 TTS

## Capabilities

### New Capabilities
- `voice-replay`: AI 回复消息的语音重播功能，包括图标交互、状态管理、与现有自动播放的协调

### Modified Capabilities
<!-- 不修改现有 spec 级别的需求 -->

## Impact

- `frontend/src/views/Chat.vue` — 消息气泡模板增加图标，流式完成后触发音频缓存
- `frontend/src/stores/chat.ts` — 新增音频状态管理（URL 缓存、播放状态、互斥控制）
- `frontend/src/composables/useVoice.ts` — `playAudio` 增加播放结束回调
- 后端：无改动
