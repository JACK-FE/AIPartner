## ADDED Requirements

### Requirement: Replay icon on assistant messages

每条 AI 回复消息气泡 SHALL 在文本末尾显示语音重播图标，图标状态根据音频的获取和播放进度变化。

#### Scenario: Icon hidden for user messages
- **WHEN** 消息 role 为 `user`
- **THEN** 消息气泡不显示语音重播图标

#### Scenario: Icon hidden during initial auto-play
- **WHEN** AI 回复流式完成且语音自动播放中
- **THEN** 消息气泡不显示重播图标

#### Scenario: Icon appears after auto-play ends
- **WHEN** AI 回复的自动播放完成
- **THEN** 消息气泡末尾显示可点击的静态 🔊 图标

#### Scenario: Icon shows loading state
- **WHEN** 用户点击历史消息的重播图标，TTS 请求未完成
- **THEN** 图标显示为旋转加载动画，不可点击

#### Scenario: Icon shows error state
- **WHEN** TTS 请求失败
- **THEN** 图标显示为红色 ❌，用户可点击重试

### Requirement: Lazy TTS for history messages

历史消息的音频 SHALL 在用户首次点击重播时惰性请求，页面加载时不预生成。

#### Scenario: History message has no audio on load
- **WHEN** 用户进入聊天页，历史消息已加载
- **THEN** 历史 AI 回复消息不触发 TTS 请求

#### Scenario: Click triggers TTS request
- **WHEN** 用户点击某条历史 AI 回复的重播图标
- **THEN** 系统调用 `POST /characters/:id/tts/` 获取音频，完成后自动播放

### Requirement: Audio URL caching

成功获取的音频 URL SHALL 按消息 ID 缓存，同一条消息不会重复请求 TTS。

#### Scenario: Second click uses cached URL
- **WHEN** 消息已有缓存的音频 URL
- **THEN** 点击重播图标直接使用缓存 URL 播放，不发起新的 TTS 请求

### Requirement: Single active playback

系统 SHALL 确保全局同时只有一条消息处于播放状态。

#### Scenario: New replay stops current playback
- **WHEN** 用户点击消息 A 的重播图标时，消息 B 正在播放
- **THEN** 消息 B 的播放立即停止，消息 A 开始加载并播放

#### Scenario: Sending new message stops playback
- **WHEN** 用户在语音播放中发送新消息
- **THEN** 当前播放立即停止

### Requirement: Playback completion restores replay icon

音频播放结束后，图标 SHALL 恢复为可重播状态。

#### Scenario: Audio ends naturally
- **WHEN** 重播的音频自然播放到结束
- **THEN** 图标从播放中状态恢复为静态可点击的 🔊 图标

#### Scenario: Audio is interrupted
- **WHEN** 重播的音频被其他消息的中断播放
- **THEN** 被中断的消息图标恢复为静态可点击的 🔊 图标
