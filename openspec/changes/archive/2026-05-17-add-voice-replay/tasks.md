## 1. useVoice 增加播放结束回调

- [x] 1.1 `playAudio` 增加可选 `onEnded` 回调参数，在 `audio.onended` 时触发

## 2. chatStore 增加音频状态管理

- [x] 2.1 新增 `audioUrls`（`Map<number, string>`）和 `audioState`（`Map<number, string>`）状态
- [x] 2.2 新增 `activePlayingMsgId` 追踪当前播放的消息 ID
- [x] 2.3 实现 `requestAudio(msgId, text, characterId)`：调 TTS API，更新 audioState（loading → ready/error），缓存 URL
- [x] 2.4 实现 `playMessageAudio(msgId)`：先 stopCurrent，再调用 useVoice.playAudio，更新 activePlayingMsgId 和 audioState
- [x] 2.5 实现 `stopCurrent()`：停止当前播放，恢复对应消息的 audioState 为 ready
- [x] 2.6 播放自然结束时通过 onEnded 回调恢复 audioState

## 3. Chat.vue 消息气泡模板增加重播图标

- [x] 3.1 在消息气泡模板中，对 assistant 消息在文本后追加图标区域
- [x] 3.2 图标根据 `audioState` 渲染四种状态：idle（不显示）、loading（n-spin）、ready（🔊 可点击）、playing（跳动动画）、error（❌ 红色可重试）
- [x] 3.3 `sendMessage` 流式完成后自动走 `requestAudio` → `playMessageAudio`，自动播放完后图标变为 ready
- [x] 3.4 历史消息的 assistant 气泡显示为 idle（无图标），用户点击惰性走 `requestAudio`
- [x] 3.5 发新消息时调用 `stopCurrent()` 停止当前重播
