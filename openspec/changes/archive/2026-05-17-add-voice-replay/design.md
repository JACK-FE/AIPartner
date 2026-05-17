## Context

当前语音实现：AI 回复流式结束后，前端调用 `POST /characters/:id/tts/` 获取音频 URL，通过 `HTMLAudioElement` 自动播放一次。URL 未与消息关联存储，播放后无法重播。

后端 TTS 使用 Edge TTS，音频文件以 `{timestamp}_{text_hash}.mp3` 存储于 `media/tts/`，24h 后清理。同一文本 + 同一 preset 会覆盖写入同名文件。

本设计在前端层增加语音重播能力，不改动后端。

## Goals / Non-Goals

**Goals:**
- 每条 AI 回复消息可重播语音
- 图标状态覆盖：加载中、可播放、播放中、错误
- 自动播放完成后才显示重播图标
- 全局单实例播放，新播放自动停止旧播放
- 历史消息惰性请求 TTS（点击才生成）

**Non-Goals:**
- 不修改 Message 模型或后端 API
- 不预加载历史消息的语音
- 不改变现有自动播放逻辑的行为

## Decisions

### 1. 纯前端方案，零后端改动

**选择**：在 `chatStore` 中维护 `Map<messageId, audioUrl>` 和 `Map<messageId, state>`，不修改 Message 模型。

**理由**：
- TTS 文件名基于 `md5(preset:text)` 确定性生成，重复请求不会重复合成，只返回已有 URL
- 24h 文件生命周期对聊天重播场景足够
- 当前架构就是前端驱动 TTS，保持职责一致

**备选**：在 Message 表加 `audio_url` 字段，流式完成后由后端生成并存储。放弃理由：改动面大（模型迁移 + 视图改造），当前阶段性价比低。

### 2. 每条消息独立状态机

```
IDLE → LOADING → READY → PLAYING → READY
                  ↘ ERROR ↗
```

- IDLE：无音频，无图标
- LOADING：正在请求 TTS，显示旋转图标
- READY：音频就绪，显示静态 🔊 图标，可点击
- PLAYING：正在播放，显示跳动动画图标，不可点击
- ERROR：TTS 请求失败，显示红色 ❌，点击重试

**理由**：状态驱动渲染，避免条件分支散落。图标视觉在所有状态下都可预测。

### 3. useVoice 增加 onEnded 回调

```ts
function playAudio(url: string, onEnded?: () => void)
```

`onEnded` 在音频自然结束时触发，用于将消息状态从 PLAYING 切回 READY。

**理由**：最小改动。`useVoice` 不感知消息状态，只暴露播放生命周期回调。状态管理留在 `chatStore`。

### 4. 全局播放在 chatStore 中互斥

`activePlayingMsgId: number | null` 追踪当前播放的消息 ID。`playAudio(msgId)` 内部先调用 `stopCurrent()`，确保同时只有一条消息出声。

**理由**：多个 `Audio` 实例同时播放会造成噪音混乱。在 store 层做互斥，视图层无感知。

### 5. 历史消息惰性 TTS

页面加载时，历史消息不预生成音频。用户点击某条消息的 🔊 图标时，才调用 TTS API。

**理由**：避免页面加载时的 N 次 TTS 请求，减少服务端压力和用户等待。

## Risks / Trade-offs

- [刷新页面后音频 URL 缓存丢失] → 用户点击重播时重新请求 TTS。由于文件名确定性（同一 text+preset 返回同一文件），后端不会重复合成，只是走一次 HTTP round trip。
- [24h 后文件被清理，URL 失效] → 点击重播会重新触发 TTS 生成新文件。对用户透明。
- [TTS API 错误处理] → ERROR 状态保留在消息上，用户可点击重试。
